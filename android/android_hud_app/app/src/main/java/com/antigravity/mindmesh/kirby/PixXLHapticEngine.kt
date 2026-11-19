package com.antigravity.mindmesh.kirby

import android.content.Context
import android.os.Build
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import android.view.HapticFeedbackConstants
import android.view.View

/**
 * 📳 PixXL Native Haptic Engine
 * ==============================
 * Tuned specifically for the Google Pixel 9 Pro XL Linear Resonant Actuator (LRA).
 * Provides rich multi-touch tactile sensations:
 *   - Detent ticks for pinch-scale milestones (every 0.25x)
 *   - Rotary ratchet clicks for multi-finger twisting (every 30°)
 *   - Boundary collision thuds for overscroll/edge docking
 *   - Dual-pulse confirmations for multi-touch tap gestures
 */
class PixXLHapticEngine(private val context: Context) {

    private val vibrator: Vibrator? = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
        val vibratorManager = context.getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as? VibratorManager
        vibratorManager?.defaultVibrator
    } else {
        @Suppress("DEPRECATION")
        context.getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator
    }

    private var lastTickTime: Long = 0

    /**
     * Crisp ultra-short detent tick (ideal for pinch milestone detents).
     */
    fun detentTick() {
        val now = System.currentTimeMillis()
        if (now - lastTickTime < 18) return // Anti-saturation throttle
        lastTickTime = now

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R && vibrator?.areAllPrimitivesSupported(VibrationEffect.Composition.PRIMITIVE_TICK) == true) {
            val composition = VibrationEffect.startComposition()
                .addPrimitive(VibrationEffect.Composition.PRIMITIVE_TICK, 0.7f)
                .compose()
            vibrator.vibrate(composition)
        } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            vibrator?.vibrate(VibrationEffect.createPredefined(VibrationEffect.EFFECT_TICK))
        } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            vibrator?.vibrate(VibrationEffect.createOneShot(10, 80))
        } else {
            @Suppress("DEPRECATION")
            vibrator?.vibrate(10)
        }
    }

    /**
     * Solid click confirmation (button taps, single pointer selection).
     */
    fun affirmClick() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R && vibrator?.areAllPrimitivesSupported(VibrationEffect.Composition.PRIMITIVE_CLICK) == true) {
            val composition = VibrationEffect.startComposition()
                .addPrimitive(VibrationEffect.Composition.PRIMITIVE_CLICK, 1.0f)
                .compose()
            vibrator.vibrate(composition)
        } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            vibrator?.vibrate(VibrationEffect.createPredefined(VibrationEffect.EFFECT_CLICK))
        } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            vibrator?.vibrate(VibrationEffect.createOneShot(22, 180))
        } else {
            @Suppress("DEPRECATION")
            vibrator?.vibrate(22)
        }
    }

    /**
     * Heavy thud feedback (screen edge docking, boundary limits, 3-finger events).
     */
    fun heavyThud() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R && vibrator?.areAllPrimitivesSupported(VibrationEffect.Composition.PRIMITIVE_THUD) == true) {
            val composition = VibrationEffect.startComposition()
                .addPrimitive(VibrationEffect.Composition.PRIMITIVE_THUD, 1.0f)
                .compose()
            vibrator.vibrate(composition)
        } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            vibrator?.vibrate(VibrationEffect.createPredefined(VibrationEffect.EFFECT_HEAVY_CLICK))
        } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            vibrator?.vibrate(VibrationEffect.createOneShot(45, 255))
        } else {
            @Suppress("DEPRECATION")
            vibrator?.vibrate(45)
        }
    }

    /**
     * Dual-pulse haptic for two-finger double-tap or gesture resets.
     */
    fun doubleClick() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R && vibrator?.areAllPrimitivesSupported(VibrationEffect.Composition.PRIMITIVE_CLICK) == true) {
            val composition = VibrationEffect.startComposition()
                .addPrimitive(VibrationEffect.Composition.PRIMITIVE_CLICK, 0.7f)
                .addPrimitive(VibrationEffect.Composition.PRIMITIVE_CLICK, 1.0f, 40)
                .compose()
            vibrator.vibrate(composition)
        } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val timings = longArrayOf(0, 15, 35, 22)
            val amplitudes = intArrayOf(0, 140, 0, 220)
            vibrator?.vibrate(VibrationEffect.createWaveform(timings, amplitudes, -1))
        } else {
            @Suppress("DEPRECATION")
            vibrator?.vibrate(longArrayOf(0, 15, 35, 22), -1)
        }
    }

    /**
     * Dynamic drag pickup ramp.
     */
    fun dragPickup() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R && vibrator?.areAllPrimitivesSupported(VibrationEffect.Composition.PRIMITIVE_QUICK_RISE) == true) {
            val composition = VibrationEffect.startComposition()
                .addPrimitive(VibrationEffect.Composition.PRIMITIVE_QUICK_RISE, 0.8f)
                .compose()
            vibrator.vibrate(composition)
        } else {
            affirmClick()
        }
    }

    /**
     * Edge docking snap pulse.
     */
    fun dockSnap() {
        heavyThud()
    }

    /**
     * Perform view-based tactile feedback fallback.
     */
    fun performViewHaptic(view: View, constant: Int = HapticFeedbackConstants.VIRTUAL_KEY) {
        view.performHapticFeedback(constant, HapticFeedbackConstants.FLAG_IGNORE_GLOBAL_SETTING)
    }
}
