package com.antigravity.mindmesh.kirby

import android.content.Context
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.os.Handler
import android.os.Looper
import org.json.JSONObject
import java.io.File
import kotlin.math.acos
import kotlin.math.cos
import kotlin.math.max
import kotlin.math.min
import kotlin.math.sin

/**
 * 🧭 PIXXL TILT & WATTY COMPASS SENSOR ACCLIMATOR 🧭
 * =====================================================================
 * Monitors physical orientation, tilt angle, surface slope, and compass
 * heading on the Pixel 9 Pro XL Actua display.
 *
 * Coordinates with the Adaptive Circumstance Response Coordination
 * Synergy Orchestration Handlers (ACR-CSOH) to acclimate the floating
 * Kirby HUD companion and dual flying bubbles for maximum visibility!
 * =====================================================================
 */
class PixXLTiltCompassAcclimator(
    private val context: Context,
    private val callback: TilterAcclimationCallback
) : SensorEventListener {

    interface TilterAcclimationCallback {
        fun onTilterStateChanged(
            pitchDeg: Float,
            rollDeg: Float,
            headingDeg: Float,
            surfaceSlopeDeg: Float,
            offKilterSeverity: Float,
            counterLeanDeg: Float,
            keystoneStretchY: Float,
            cardinalHeading: String
        )
    }

    private val sensorManager = context.getSystemService(Context.SENSOR_SERVICE) as SensorManager
    private val rotationSensor: Sensor? = sensorManager.getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR)
    private val accelSensor: Sensor? = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
    private val magSensor: Sensor? = sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD)

    // Filtered attitude
    private var pitch = 0f
    private var roll = 0f
    private var azimuth = 0f
    private var surfaceSlope = 0f

    // Smoothing factor (Low-pass exponential filter)
    private val alpha = 0.22f

    // Matrices for sensor calculation
    private val rotationMatrix = FloatArray(9)
    private val orientationVals = FloatArray(3)
    private val lastAccel = FloatArray(3)
    private val lastMag = FloatArray(3)
    private var hasAccel = false
    private var hasMag = false

    private val mainHandler = Handler(Looper.getMainLooper())
    private var lastPersistTime = 0L

    companion object {
        private val CARDINALS = arrayOf(
            "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
        )

        fun headingToCardinal(headingDeg: Float): String {
            val norm = (headingDeg % 360f + 360f) % 360f
            val idx = (((norm + 11.25f) / 22.5f).toInt()) % 16
            return CARDINALS[idx]
        }
    }

    fun start() {
        if (rotationSensor != null) {
            sensorManager.registerListener(this, rotationSensor, SensorManager.SENSOR_DELAY_UI)
        } else {
            accelSensor?.let { sensorManager.registerListener(this, it, SensorManager.SENSOR_DELAY_UI) }
            magSensor?.let { sensorManager.registerListener(this, it, SensorManager.SENSOR_DELAY_UI) }
        }
    }

    fun stop() {
        sensorManager.unregisterListener(this)
    }

    override fun onSensorChanged(event: SensorEvent?) {
        if (event == null) return

        when (event.sensor.type) {
            Sensor.TYPE_ROTATION_VECTOR -> {
                SensorManager.getRotationMatrixFromVector(rotationMatrix, event.values)
                SensorManager.getOrientation(rotationMatrix, orientationVals)
                updateAttitude(
                    newAzimuth = Math.toDegrees(orientationVals[0].toDouble()).toFloat(),
                    newPitch = Math.toDegrees(orientationVals[1].toDouble()).toFloat(),
                    newRoll = Math.toDegrees(orientationVals[2].toDouble()).toFloat()
                )
            }

            Sensor.TYPE_ACCELEROMETER -> {
                System.arraycopy(event.values, 0, lastAccel, 0, 3)
                hasAccel = true
                if (hasMag) computeFromAccelAndMag()
            }

            Sensor.TYPE_MAGNETIC_FIELD -> {
                System.arraycopy(event.values, 0, lastMag, 0, 3)
                hasMag = true
                if (hasAccel) computeFromAccelAndMag()
            }
        }
    }

    private fun computeFromAccelAndMag() {
        if (SensorManager.getRotationMatrix(rotationMatrix, null, lastAccel, lastMag)) {
            SensorManager.getOrientation(rotationMatrix, orientationVals)
            updateAttitude(
                newAzimuth = Math.toDegrees(orientationVals[0].toDouble()).toFloat(),
                newPitch = Math.toDegrees(orientationVals[1].toDouble()).toFloat(),
                newRoll = Math.toDegrees(orientationVals[2].toDouble()).toFloat()
            )
        }
    }

    private fun updateAttitude(newAzimuth: Float, newPitch: Float, newRoll: Float) {
        // Low-pass exponential smoothing
        val normAzimuth = (newAzimuth + 360f) % 360f
        azimuth += alpha * (normAzimuth - azimuth)
        pitch += alpha * (newPitch - pitch)
        roll += alpha * (newRoll - roll)

        // Spherical trigonometry for total slope angle from floor
        val pRad = Math.toRadians(pitch.toDouble())
        val rRad = Math.toRadians(roll.toDouble())
        val cosSlope = max(-1.0, min(1.0, cos(pRad) * cos(rRad)))
        surfaceSlope = Math.toDegrees(acos(cosSlope)).toFloat()

        // Severity: Device slope (55%) + off-kilter viewing assumption (45%)
        val normSlope = min(1.0f, surfaceSlope / 75.0f)
        val offKilterSeverity = min(1.0f, normSlope * 0.85f + 0.15f)

        // Counter-lean opposes roll
        val counterLeanDeg = -roll * 0.82f

        // Keystone inverse stretch
        val effTiltRad = Math.toRadians(min(78.0, max(0.0, surfaceSlope.toDouble())))
        val keystoneStretchY = (1.0 / max(0.20, cos(effTiltRad))).toFloat()

        val cardinal = headingToCardinal(azimuth)

        callback.onTilterStateChanged(
            pitchDeg = pitch,
            rollDeg = roll,
            headingDeg = azimuth,
            surfaceSlopeDeg = surfaceSlope,
            offKilterSeverity = offKilterSeverity,
            counterLeanDeg = counterLeanDeg,
            keystoneStretchY = keystoneStretchY,
            cardinalHeading = cardinal
        )

        val now = System.currentTimeMillis()
        if (now - lastPersistTime > 2000L) {
            lastPersistTime = now
            persistStateToFile(offKilterSeverity, counterLeanDeg, keystoneStretchY, cardinal)
        }
    }

    private fun persistStateToFile(
        severity: Float,
        counterLean: Float,
        keystoneStretch: Float,
        cardinal: String
    ) {
        try {
            val stateFile = File("/sdcard/AntiGravity_Shared/.kirby_tilter_state.json")
            val obj = JSONObject().apply {
                put("timestamp", System.currentTimeMillis() / 1000.0)
                put("device", "Pixel 9 Pro XL")
                put("attitude", JSONObject().apply {
                    put("pitch_deg", pitch.toDouble())
                    put("roll_deg", roll.toDouble())
                    put("heading_deg", azimuth.toDouble())
                    put("cardinal_heading", cardinal)
                    put("surface_slope_deg", surfaceSlope.toDouble())
                })
                put("synergy_metrics", JSONObject().apply {
                    put("severity_score", severity.toDouble())
                    put("category", if (severity > 0.6) "EXTREME_OFF_KILTER" else if (severity > 0.3) "WATTY_TILTER_MODERATE" else "NOMINAL_ON_AXIS")
                })
                put("keystone_compensation", JSONObject().apply {
                    put("stretch_y", keystoneStretch.toDouble())
                })
                put("kirby_posture", JSONObject().apply {
                    put("counter_lean_deg", counterLean.toDouble())
                    put("compass_cardinal", cardinal)
                })
            }
            stateFile.writeText(obj.toString(2))
        } catch (e: Exception) {
            // Non-critical persistence
        }
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {}
}
