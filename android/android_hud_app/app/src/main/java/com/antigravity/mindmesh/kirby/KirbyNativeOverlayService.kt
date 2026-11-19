package com.antigravity.mindmesh.kirby

import android.animation.Animator
import android.animation.AnimatorListenerAdapter
import android.animation.ValueAnimator
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.app.usage.UsageEvents
import android.app.usage.UsageStatsManager
import android.content.Context
import android.content.Intent
import android.content.pm.ApplicationInfo
import android.graphics.Color
import android.graphics.PixelFormat
import android.graphics.drawable.GradientDrawable
import android.hardware.display.DisplayManager
import android.os.Build
import android.os.Handler
import android.os.IBinder
import android.os.Looper
import android.view.Display
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.WindowManager
import android.view.animation.LinearInterpolator
import android.widget.LinearLayout
import android.widget.TextView
import java.util.concurrent.CopyOnWriteArrayList
import kotlin.math.abs
import kotlin.math.atan2
import kotlin.math.hypot
import kotlin.math.roundToInt
import kotlin.math.sin
import kotlin.random.Random

/**
 * 🌸 KIRBY NATIVE AUTONOMOUS OVERLAY SERVICE (DUAL-BUBBLE & CURVED FLIGHT ENGINE)
 * ===================================================================================
 * Pixel 9 Pro XL Floating Companion featuring:
 *   1. Dual Chat Bubble Engine:
 *      - Attached Trailing Bubble (direct speech & interactive haptic feedback)
 *      - Detached Flying Curved Bubbles (spawned entities that float diagonally in a
 *        graceful arc, curve downwards with gravity, and pop/fade away!)
 *   2. Aspect-Ratio & Camera Punch-Hole Calibration (Pixel 9 Pro XL safe margins)
 *   3. Exterior Lap Patrol: high-speed perimeter laps along the 4 edges of the screen
 *   4. Autonomous Random Roaming: gentle sinusoidal levitation & waypoint wandering
 *   5. Multi-Touch Haptics: 1-finger drag, 2-finger scale/twist, double-tap moods
 */
class KirbyNativeOverlayService : Service() {

    companion object {
        const val ACTION_TOGGLE_SCARCE_MODE = "com.antigravity.mindmesh.kirby.ACTION_TOGGLE_SCARCE_MODE"
        const val ACTION_SET_SCARCE_MODE = "com.antigravity.mindmesh.kirby.ACTION_SET_SCARCE_MODE"
        const val EXTRA_SCARCE_ENABLED = "scarce_enabled"
        private const val NOTIFICATION_ID = 2025
        private const val CHANNEL_ID = "kirby_native_overlay"

        @Volatile
        var isScarceModeActive: Boolean = false
            private set
    }

    private lateinit var windowManager: WindowManager
    private lateinit var overlayView: LinearLayout
    private lateinit var trailingSpeechBubble: TextView
    private lateinit var kirbySprite: TextView
    private lateinit var layoutParams: WindowManager.LayoutParams
    private lateinit var haptics: PixXLHapticEngine

    // Active detached flying bubbles list for lifecycle cleanup
    private val activeFlyingBubbles = CopyOnWriteArrayList<View>()

    // Screen boundaries (Calibrated for Pixel 9 Pro XL punch-hole & nav bar)
    private var screenWidth = 1080
    private var screenHeight = 2400
    private val topMargin = 145f   // Safe clearance beneath camera punch-hole cutout & status bar
    private val bottomMargin = 220f // Clearance above gesture navigation pill
    private val sideMargin = 30f

    // Motion & Physics State
    private var posX = 100f
    private var posY = 400f
    private var targetX = 100f
    private var targetY = 400f
    private var velX = 0f
    private var velY = 0f
    private var currentScale = 1.0f
    private var isFacingRight = true

    // 🧭 Adaptive Tilter & Watty Compass Acclimator
    private var tiltAcclimator: PixXLTiltCompassAcclimator? = null
    private var currentCounterLean = 0f
    private var currentKeystoneStretch = 1.0f
    private var currentSlope = 0f
    private var currentCompassHeading = "N"

    // State Machine
    enum class BehaviorState {
        EXTERIOR_LAPS,
        RANDOM_ROAM,
        PLAYFUL_HOP,
        WARP_DASH,
        CORNER_SNOOZE
    }

    private var currentState = BehaviorState.EXTERIOR_LAPS
    private var stateTicks = 0
    private var maxStateTicks = 380
    private var isUserInteracting = false
    private var resumeAutonomousTime = 0L

    // Exterior Lap Navigation
    private var lapLeg = 0 // 0: Top L->R, 1: Right T->B, 2: Bottom R->L, 3: Left B->T
    private var lapsCompleted = 0

    // Sinusoidal Float & Hop Physics
    private var floatPhase = 0f
    private var hopProgress = 0f

    // Timing for flying bubble spawns
    private var ticksSinceLastFlyingBubble = 0

    // Sprite Moods & Faces
    private val roamFaces = listOf("*(^o^)*", "(>‿<)", "(★ω★)", "(•̀ᴗ•́)و", "(੭ˊᵕˋ)੭")
    private val sprintFaces = listOf("ε=ε=┌( >‿<)┘", "ε=ε=┌(★ω★)┘", "ε=ε=┌( ^o^)┘", "└(•̀ᴗ•́)┐ =3=3")
    private val snoozeFace = "(u.uz) *zZz*"

    // Attached Dialogue Lines (Dynamically augmented from kirby_action_cards.json)
    private var trailingQuotes = listOf(
        "Poyo! MindMesh active! 🌸",
        "Autonomous Agent on Duty! 🫡",
        "Tensor TPU running cozy! ☕",
        "3 Dev Envs Synced & Locked! ✨",
        "Overclocking Tensor G4! ⭐",
        "Pixel 9 Pro XL Companion! 💕"
    )

    // Flying Detached Bubble Droplets (Short, buoyant, colorful chirps!)
    private var flyingBubbleChirps = listOf(
        "Poyo! ✨",
        "⭐ Star Shard!",
        "Wheee! 💨",
        "Boing! 💫",
        "Tensor G4 ☕",
        "Zoom zoom! 🚀",
        "Poyo poyo! 🌸",
        "Pop! 🫧",
        "Catch me! 💕",
        "Lap +1 🏁",
        "Hehe! 🌈",
        "✨⭐✨",
        "Zzzz... 🌙",
        "Speedy Poyo! ⚡",
        "(੭ˊᵕˋ)੭ 💖"
    )

    private val bubbleBorderColors = intArrayOf(
        0xFFFF79C6.toInt(), // Neon Pink
        0xFF8BE9FD.toInt(), // Cyan
        0xFFF1FA8C.toInt(), // Yellow
        0xFF50FA7B.toInt(), // Green
        0xFFBD93F9.toInt(), // Purple
        0xFFFFB86C.toInt()  // Orange
    )

    // Trailing Bubble Timer
    private var trailingBubbleTicksRemaining = 0
    private val mainHandler = Handler(Looper.getMainLooper())
    private var isLoopRunning = false

    // Hide / Scarce Mode & Gaming Auto-Hide State
    private var isManualScarceMode = false
    private var isGamingAutoHidden = false
    private var lastGameCheckTime = 0L
    private var ticksSinceLastScarceChime = 0
    private var scarceChimeView: View? = null
    private var scarceChimeWindowManager: WindowManager? = null
    private val calmChimeLines = listOf(
        "(u.u) poyo...",
        "(*_*) standing by",
        "(._.) quiet mode"
    )

    private val isScarceMode: Boolean
        get() = isManualScarceMode || isGamingAutoHidden

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_TOGGLE_SCARCE_MODE -> {
                isManualScarceMode = !isManualScarceMode
                applyScarceModeState()
            }
            ACTION_SET_SCARCE_MODE -> {
                isManualScarceMode = intent.getBooleanExtra(EXTRA_SCARCE_ENABLED, false)
                applyScarceModeState()
            }
        }
        return START_STICKY
    }

    override fun onCreate() {
        super.onCreate()
        haptics = PixXLHapticEngine(this)
        startForegroundNotification()
        loadDynamicActionDeck()
        setupFloatingView()
        setupTilterAcclimator()
        startAutonomousEngine()
    }

    private fun loadDynamicActionDeck() {
        try {
            val cardsFile = java.io.File("/sdcard/AntiGravity_Shared/kirby_action_cards.json")
            if (cardsFile.exists()) {
                val root = org.json.JSONObject(cardsFile.readText())
                val arr = root.optJSONArray("cards")
                if (arr != null && arr.length() > 0) {
                    val dynamicQuotes = mutableListOf<String>()
                    val dynamicChirps = mutableListOf<String>()
                    for (i in 0 until arr.length()) {
                        val card = arr.getJSONObject(i)
                        val speech = card.optString("speech", "")
                        val icon = card.optString("icon", "🌸")
                        val name = card.optString("name", "")
                        if (speech.isNotEmpty()) dynamicQuotes.add(speech)
                        dynamicChirps.add("$icon $name!")
                    }
                    if (dynamicQuotes.isNotEmpty()) trailingQuotes = dynamicQuotes
                    if (dynamicChirps.isNotEmpty()) flyingBubbleChirps = dynamicChirps
                }
            }
        } catch (e: Exception) {
            // Graceful fallback to default in-memory lists
        }
    }

    private fun startForegroundNotification() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "Kirby Native Overlay",
                NotificationManager.IMPORTANCE_LOW
            )
            val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            manager.createNotificationChannel(channel)
        }
        startForeground(NOTIFICATION_ID, buildForegroundNotification())
    }

    private fun buildForegroundNotification(): Notification {
        val toggleIntent = Intent(this, KirbyNativeOverlayService::class.java).apply {
            action = ACTION_TOGGLE_SCARCE_MODE
        }
        val togglePendingIntent = PendingIntent.getService(
            this,
            1001,
            toggleIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val title = if (isScarceMode) {
            if (isGamingAutoHidden) "Kirby Scarce Mode (Gaming Auto-Hide)" else "Kirby Scarce Mode (Hidden)"
        } else {
            "Kirby Autonomous Companion Active"
        }
        val body = if (isScarceMode) {
            "Idle animations suppressed • Touch-passthrough chime-ins only"
        } else {
            "Roaming, doing laps & flying chat bubbles on Pixel 9 Pro XL"
        }
        val actionLabel = if (isScarceMode) "Show Kirby" else "Hide (Scarce)"

        val builder = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            Notification.Builder(this, CHANNEL_ID)
        } else {
            @Suppress("DEPRECATION")
            Notification.Builder(this)
        }

        val toggleAction = Notification.Action.Builder(
            android.R.drawable.ic_menu_view,
            actionLabel,
            togglePendingIntent
        ).build()

        return builder
            .setContentTitle(title)
            .setContentText(body)
            .setSmallIcon(android.R.drawable.star_on)
            .setOngoing(true)
            .addAction(toggleAction)
            .build()
    }

    private fun updateForegroundNotification() {
        try {
            val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            manager.notify(NOTIFICATION_ID, buildForegroundNotification())
        } catch (e: Exception) {}
    }

    private fun updateScreenMetrics() {
        val dm = resources.displayMetrics
        screenWidth = dm.widthPixels
        screenHeight = dm.heightPixels
    }

    private fun setupFloatingView() {
        windowManager = getSystemService(Context.WINDOW_SERVICE) as WindowManager
        updateScreenMetrics()

        val layoutType = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        } else {
            @Suppress("DEPRECATION")
            WindowManager.LayoutParams.TYPE_PHONE
        }

        layoutParams = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            layoutType,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = posX.toInt()
            y = posY.toInt()
        }

        overlayView = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(10, 10, 10, 10)
        }

        // Mode A: Attached Trailing Speech Bubble (for user interaction and direct speech)
        trailingSpeechBubble = TextView(this).apply {
            text = "Poyo! Autonomous Roaming Active! 🌸"
            setTextColor(Color.WHITE)
            textSize = 12f
            setPadding(22, 10, 22, 10)
            val bg = GradientDrawable().apply {
                setColor(0xEE161B22.toInt())
                cornerRadius = 24f
                setStroke(3, 0xFFFF79C6.toInt())
            }
            background = bg
            visibility = View.VISIBLE
            alpha = 1.0f
        }
        overlayView.addView(trailingSpeechBubble)

        // Native Kirby Sprite with strict 1:1 aspect ratio preservation
        kirbySprite = TextView(this).apply {
            text = "*(^o^)*"
            textSize = 34f
            setTextColor(0xFFFF79C6.toInt())
            setPadding(12, 12, 12, 12)
        }
        overlayView.addView(kirbySprite)

        setupTouchInteraction()
        windowManager.addView(overlayView, layoutParams)
    }

    private fun setupTouchInteraction() {
        var initialX = 0
        var initialY = 0
        var initialTouchX = 0f
        var initialTouchY = 0f

        var initialDistance = 0f
        var initialAngle = 0f
        var baseScale = 1.0f
        var baseRotation = 0f
        var lastMilestone = 1.0f
        var lastRatchetDeg = 0
        var lastSingleTapTime = 0L
        var lastTwoFingerTapTime = 0L

        overlayView.setOnTouchListener { _, event ->
            val pointerCount = event.pointerCount

            when (event.actionMasked) {
                MotionEvent.ACTION_DOWN -> {
                    val now = System.currentTimeMillis()
                    if (pointerCount == 1 && now - lastSingleTapTime < 320L) {
                        // 1-finger double-tap quick-hide into Scarce Mode
                        lastSingleTapTime = 0L
                        isUserInteracting = false
                        isManualScarceMode = true
                        applyScarceModeState()
                        return@setOnTouchListener true
                    }
                    lastSingleTapTime = now
                    isUserInteracting = true
                    initialX = layoutParams.x
                    initialY = layoutParams.y
                    initialTouchX = event.rawX
                    initialTouchY = event.rawY
                    haptics.dragPickup()
                    popTrailingBubble("Picked up! Wheee! 💕", 0xFF8BE9FD.toInt())
                    true
                }

                MotionEvent.ACTION_POINTER_DOWN -> {
                    if (pointerCount == 2) {
                        val dx = event.getX(1) - event.getX(0)
                        val dy = event.getY(1) - event.getY(0)
                        initialDistance = hypot(dx, dy)
                        initialAngle = (atan2(dy.toDouble(), dx.toDouble()) * (180.0 / Math.PI)).toFloat()
                        baseScale = currentScale
                        baseRotation = kirbySprite.rotation
                        lastMilestone = (currentScale * 4).roundToInt() / 4f
                        lastRatchetDeg = (initialAngle / 30).roundToInt() * 30

                        haptics.affirmClick()
                        popTrailingBubble("Pinch to scale • Twist to spin ✨", 0xFFF1FA8C.toInt())

                        val now = System.currentTimeMillis()
                        if (now - lastTwoFingerTapTime < 350) {
                            kirbySprite.text = roamFaces[Random.nextInt(roamFaces.size)]
                            popTrailingBubble("Mood changed! Poyo! 💖", 0xFFFF79C6.toInt())
                            currentScale = 1.0f
                            applySpriteTransform()
                            kirbySprite.rotation = 0f
                            haptics.doubleClick()
                            lastTwoFingerTapTime = 0
                        } else {
                            lastTwoFingerTapTime = now
                        }
                    } else if (pointerCount == 3) {
                        haptics.heavyThud()
                        popTrailingBubble("🔋 PixXL Vitals: Nominal • Lap: #$lapsCompleted", 0xFF50FA7B.toInt())
                    }
                    true
                }

                MotionEvent.ACTION_MOVE -> {
                    if (pointerCount == 1) {
                        layoutParams.x = initialX + (event.rawX - initialTouchX).toInt()
                        layoutParams.y = initialY + (event.rawY - initialTouchY).toInt()
                        posX = layoutParams.x.toFloat()
                        posY = layoutParams.y.toFloat()
                        windowManager.updateViewLayout(overlayView, layoutParams)
                    } else if (pointerCount == 2) {
                        val dx = event.getX(1) - event.getX(0)
                        val dy = event.getY(1) - event.getY(0)
                        val newDist = hypot(dx, dy)
                        val newAngle = (atan2(dy.toDouble(), dx.toDouble()) * (180.0 / Math.PI)).toFloat()

                        if (initialDistance > 10f) {
                            val pinchRatio = newDist / initialDistance
                            val targetScale = (baseScale * pinchRatio).coerceIn(0.65f, 2.5f)

                            val nearestMilestone = (targetScale * 4).roundToInt() / 4f
                            if (abs(targetScale - nearestMilestone) < 0.04f && nearestMilestone != lastMilestone) {
                                lastMilestone = nearestMilestone
                                haptics.detentTick()
                                popTrailingBubble("Scale: ${String.format("%.2f", nearestMilestone)}x", 0xFFBD93F9.toInt())
                            }

                            currentScale = targetScale
                            applySpriteTransform()
                        }

                        val deltaAngle = newAngle - initialAngle
                        val targetRotation = baseRotation + deltaAngle
                        val nearestRatchet = (targetRotation / 30).roundToInt() * 30
                        if (abs(targetRotation - nearestRatchet) < 4f && nearestRatchet != lastRatchetDeg) {
                            lastRatchetDeg = nearestRatchet
                            haptics.detentTick()
                        }
                        kirbySprite.rotation = targetRotation
                    }
                    true
                }

                MotionEvent.ACTION_UP, MotionEvent.ACTION_CANCEL -> {
                    posX = layoutParams.x.toFloat()
                    posY = layoutParams.y.toFloat()
                    haptics.dockSnap()
                    popTrailingBubble("Landing! Resuming roaming soon... ✨", 0xFFFFB86C.toInt())

                    // Spawn a playful farewell flying bubble on landing!
                    spawnFlyingCurvedBubble("Poyo landing! 🌸", posX, posY, if (isFacingRight) 1f else -1f)

                    resumeAutonomousTime = System.currentTimeMillis() + 2200L
                    isUserInteracting = false
                    true
                }

                else -> false
            }
        }
    }

    /**
     * Preserves strict 1:1 aspect ratio with horizontal direction flip and adaptive keystone stretch.
     */
    private fun applySpriteTransform(stretchY: Float = currentKeystoneStretch) {
        kirbySprite.scaleX = (if (isFacingRight) 1.0f else -1.0f) * currentScale
        kirbySprite.scaleY = currentScale * stretchY
    }

    private fun setupTilterAcclimator() {
        tiltAcclimator = PixXLTiltCompassAcclimator(this, object : PixXLTiltCompassAcclimator.TilterAcclimationCallback {
            override fun onTilterStateChanged(
                pitchDeg: Float,
                rollDeg: Float,
                headingDeg: Float,
                surfaceSlopeDeg: Float,
                offKilterSeverity: Float,
                counterLeanDeg: Float,
                keystoneStretchY: Float,
                cardinalHeading: String
            ) {
                currentCounterLean = counterLeanDeg
                currentKeystoneStretch = keystoneStretchY
                currentSlope = surfaceSlopeDeg
                currentCompassHeading = cardinalHeading

                if (!isUserInteracting) {
                    kirbySprite.rotation = counterLeanDeg
                    applySpriteTransform(keystoneStretchY)

                    // Adaptive contrast & font scaling for acute viewing
                    if (offKilterSeverity > 0.55f) {
                        trailingSpeechBubble.textSize = 13.5f
                    } else {
                        trailingSpeechBubble.textSize = 12.0f
                    }
                }
            }
        })
        tiltAcclimator?.start()
    }

    /**
     * Mode A: Trailing / Direct speech bubble attached directly above Kirby.
     */
    fun popTrailingBubble(text: String, borderColor: Int = 0xFFFF79C6.toInt()) {
        trailingSpeechBubble.text = text
        val bg = GradientDrawable().apply {
            setColor(0xEE161B22.toInt())
            cornerRadius = 24f
            setStroke(3, borderColor)
        }
        trailingSpeechBubble.background = bg
        trailingSpeechBubble.visibility = View.VISIBLE
        trailingSpeechBubble.alpha = 1.0f
        trailingSpeechBubble.scaleX = 1.15f
        trailingSpeechBubble.scaleY = 1.15f
        trailingSpeechBubble.translationY = 0f

        trailingSpeechBubble.animate()
            .scaleX(1.0f)
            .scaleY(1.0f)
            .setDuration(200)
            .start()

        trailingBubbleTicksRemaining = 100 // ~3 seconds at 30ms/tick
    }

    /**
     * Mode B: Independent Flying Curved Chat Bubble
     * Spawns a separate window entity that launches off Kirby, floats diagonally
     * in a graceful parabolic arc, curves down, and fades away!
     */
    fun spawnFlyingCurvedBubble(
        text: String,
        startX: Float,
        startY: Float,
        dirX: Float = 1.0f,
        borderColor: Int = bubbleBorderColors[Random.nextInt(bubbleBorderColors.size)]
    ) {
        // Enforce max concurrent flying bubbles to prevent window clutter
        if (activeFlyingBubbles.size >= 4) {
            val oldest = activeFlyingBubbles.firstOrNull()
            if (oldest != null) {
                activeFlyingBubbles.remove(oldest)
                try {
                    windowManager.removeView(oldest)
                } catch (e: Exception) {}
            }
        }

        val bubbleView = TextView(this).apply {
            this.text = text
            setTextColor(Color.WHITE)
            textSize = 11.5f
            setPadding(22, 10, 22, 10)
            val bg = GradientDrawable().apply {
                setColor(0xF0181A20.toInt())
                cornerRadius = 22f
                setStroke(2, borderColor)
            }
            background = bg
            elevation = 10f
        }

        val layoutType = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        } else {
            @Suppress("DEPRECATION")
            WindowManager.LayoutParams.TYPE_PHONE
        }

        val bParams = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            layoutType,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
            WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE or
            WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = startX.toInt()
            y = startY.toInt()
        }

        try {
            windowManager.addView(bubbleView, bParams)
            activeFlyingBubbles.add(bubbleView)
        } catch (e: Exception) {
            return
        }

        // Flight parameters for graceful diagonal climb and downward curve
        val flightDuration = (2200L + Random.nextInt(600)) // 2.2 - 2.8 seconds
        val horizontalTravel = (Random.nextFloat() * 160f + 140f) * dirX
        val apexRise = Random.nextFloat() * 120f + 90f // floats upward initially by 90-210px
        val gravityDrop = Random.nextFloat() * 180f + 130f // curves down by 130-310px

        val animator = ValueAnimator.ofFloat(0f, 1f).apply {
            duration = flightDuration
            interpolator = LinearInterpolator()
        }

        animator.addUpdateListener { anim ->
            val t = anim.animatedFraction // 0.0 -> 1.0

            // Horizontal diagonal flight
            val curX = startX + horizontalTravel * t

            // Vertical: Parabolic arc with initial upward climb and gravity fall curve:
            // -apexRise * sin(pi * 0.9 * t) produces the upward balloon lift
            // gravityDrop * (t * t) curves the bubble downward as it loses upward momentum
            val lift = -apexRise * sin(t * Math.PI.toFloat() * 0.9f)
            val fall = gravityDrop * (t * t)
            val curY = startY + lift + fall

            bParams.x = curX.roundToInt().coerceIn(sideMargin.toInt(), (screenWidth - 180))
            bParams.y = curY.roundToInt().coerceIn(topMargin.toInt() - 60, (screenHeight - bottomMargin.toInt()))

            // Dynamic Scale & Alpha envelope:
            // 0.0 -> 0.15: Pop in (scale 0.4 -> 1.0, alpha 0 -> 1)
            // 0.15 -> 0.70: Glide gracefully at full size
            // 0.70 -> 1.00: Shrink softly and fade out away (alpha 1 -> 0, scale 1 -> 0.6)
            val alpha = when {
                t < 0.15f -> t / 0.15f
                t > 0.65f -> (1.0f - t) / 0.35f
                else -> 1.0f
            }

            val scale = when {
                t < 0.15f -> 0.5f + (t / 0.15f) * 0.5f
                t > 0.70f -> 1.0f - ((t - 0.70f) / 0.30f) * 0.4f
                else -> 1.0f
            }

            bubbleView.alpha = alpha
            bubbleView.scaleX = scale
            bubbleView.scaleY = scale

            try {
                windowManager.updateViewLayout(bubbleView, bParams)
            } catch (e: Exception) {
                anim.cancel()
            }
        }

        animator.addListener(object : AnimatorListenerAdapter() {
            override fun onAnimationEnd(animation: Animator) {
                activeFlyingBubbles.remove(bubbleView)
                try {
                    windowManager.removeView(bubbleView)
                } catch (e: Exception) {}
            }
        })

        animator.start()
    }

    /**
     * Main Autonomous Roaming & Exterior Laps Engine Loop
     */
    private fun startAutonomousEngine() {
        isLoopRunning = true
        pickNextBehaviorState()

        val runnable = object : Runnable {
            override fun run() {
                if (!isLoopRunning) return

                val now = System.currentTimeMillis()
                if (now - lastGameCheckTime >= 2500L) {
                    lastGameCheckTime = now
                    checkForegroundGamingApp()
                }

                if (isScarceMode) {
                    maybeSpawnScarceChimeIn()
                } else {
                    if (!isUserInteracting && now >= resumeAutonomousTime) {
                        updateAutonomousMotion()
                        checkFlyingBubbleSpawns()
                    }
                    updateTrailingBubbleFloating()
                }

                mainHandler.postDelayed(this, 30L) // ~33 FPS smooth motion
            }
        }
        mainHandler.post(runnable)
    }

    /**
     * Applies Hide / Scarce Mode state:
     * - Hides the main interactive overlay & suppresses over-energetic idle animations/haptics.
     * - Clears any active flying bubbles immediately.
     * - Updates the persistent notification & Quick Settings tile state.
     */
    private fun applyScarceModeState() {
        val scarce = isScarceMode
        isScarceModeActive = scarce
        updateForegroundNotification()

        if (!::overlayView.isInitialized) return

        if (scarce) {
            overlayView.visibility = View.GONE
            trailingSpeechBubble.visibility = View.INVISIBLE
            trailingBubbleTicksRemaining = 0
            ticksSinceLastScarceChime = 0
            clearActiveFlyingBubbles()
        } else {
            clearScarceChimeView()
            overlayView.visibility = View.VISIBLE
            popTrailingBubble("Poyo! Back from Scarce Mode ✨", 0xFF8BE9FD.toInt())
        }
    }

    private fun clearActiveFlyingBubbles() {
        for (bubble in activeFlyingBubbles) {
            try {
                windowManager.removeView(bubble)
            } catch (e: Exception) {}
        }
        activeFlyingBubbles.clear()
    }

    /**
     * Gaming auto-hide: detects foreground game-category apps via UsageStatsManager
     * and automatically enters Scarce Mode while playing video games.
     */
    private fun checkForegroundGamingApp() {
        val detectedGame = isForegroundAppAGame()
        if (detectedGame != isGamingAutoHidden) {
            isGamingAutoHidden = detectedGame
            applyScarceModeState()
        }
    }

    private fun isForegroundAppAGame(): Boolean {
        try {
            val usm = getSystemService(Context.USAGE_STATS_SERVICE) as? UsageStatsManager ?: return false
            val end = System.currentTimeMillis()
            val begin = end - 10_000L
            val events = usm.queryEvents(begin, end) ?: return false
            val event = UsageEvents.Event()
            var foregroundPkg: String? = null
            while (events.hasNextEvent()) {
                events.getNextEvent(event)
                if (event.eventType == UsageEvents.Event.ACTIVITY_RESUMED ||
                    event.eventType == UsageEvents.Event.MOVE_TO_FOREGROUND
                ) {
                    foregroundPkg = event.packageName
                }
            }
            val pkg = foregroundPkg ?: return false
            if (pkg == packageName) return false

            val appInfo = packageManager.getApplicationInfo(pkg, 0)
            val isCategoryGame = Build.VERSION.SDK_INT >= Build.VERSION_CODES.O &&
                appInfo.category == ApplicationInfo.CATEGORY_GAME
            @Suppress("DEPRECATION")
            val isLegacyGame = (appInfo.flags and ApplicationInfo.FLAG_IS_GAME) != 0
            return isCategoryGame || isLegacyGame
        } catch (e: Exception) {
            return false
        }
    }

    /**
     * Inactive-area chime-in: while in Scarce Mode, only allow brief, low-opacity,
     * touch-passthrough (FLAG_NOT_TOUCHABLE | FLAG_NOT_FOCUSABLE) chime-ins when an
     * inactive screen margin or secondary display area is available.
     */
    private fun maybeSpawnScarceChimeIn() {
        ticksSinceLastScarceChime++
        // Brief chime-in roughly every ~45 seconds (1500 ticks @ 30ms)
        if (ticksSinceLastScarceChime < 1500) return
        ticksSinceLastScarceChime = 0
        spawnScarceChimeIn(calmChimeLines[Random.nextInt(calmChimeLines.size)])
    }

    private fun spawnScarceChimeIn(text: String) {
        clearScarceChimeView()

        val displayManager = getSystemService(Context.DISPLAY_SERVICE) as? DisplayManager
        val secondaryDisplay: Display? = displayManager
            ?.getDisplays(DisplayManager.DISPLAY_CATEGORY_PRESENTATION)
            ?.firstOrNull()

        val targetContext = if (secondaryDisplay != null) {
            createDisplayContext(secondaryDisplay)
        } else {
            this
        }
        val targetWm = targetContext.getSystemService(Context.WINDOW_SERVICE) as WindowManager

        val chimeView = TextView(targetContext).apply {
            this.text = text
            setTextColor(Color.WHITE)
            textSize = 11f
            alpha = 0.35f
            setPadding(18, 6, 18, 6)
            background = GradientDrawable().apply {
                setColor(0x99161B22.toInt())
                cornerRadius = 18f
                setStroke(1, 0x88FF79C6.toInt())
            }
        }

        val layoutType = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        } else {
            @Suppress("DEPRECATION")
            WindowManager.LayoutParams.TYPE_PHONE
        }

        val params = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            layoutType,
            WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE or
                WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
                WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN,
            PixelFormat.TRANSLUCENT
        ).apply {
            // Place in inactive top-end corner margin (or secondary display corner)
            gravity = Gravity.TOP or Gravity.END
            x = sideMargin.toInt()
            y = 18
        }

        try {
            targetWm.addView(chimeView, params)
            scarceChimeView = chimeView
            scarceChimeWindowManager = targetWm
            mainHandler.postDelayed({ clearScarceChimeView() }, 2400L)
        } catch (e: Exception) {
            scarceChimeView = null
            scarceChimeWindowManager = null
        }
    }

    private fun clearScarceChimeView() {
        val view = scarceChimeView ?: return
        val wm = scarceChimeWindowManager ?: windowManager
        try {
            wm.removeView(view)
        } catch (e: Exception) {}
        scarceChimeView = null
        scarceChimeWindowManager = null
    }

    /**
     * Periodically spawns independent flying bubbles while roaming or sprinting
     */
    private fun checkFlyingBubbleSpawns() {
        ticksSinceLastFlyingBubble++

        // Spawn a flying curved bubble every 3.5 - 5 seconds, or on special actions
        val spawnThreshold = when (currentState) {
            BehaviorState.EXTERIOR_LAPS -> 85 // Faster bubble trail during laps (~2.5s)
            BehaviorState.WARP_DASH -> 25     // Rapid burst during warp sprint
            BehaviorState.PLAYFUL_HOP -> 70   // On hops
            else -> 120                       // ~3.6s during gentle roam
        }

        if (ticksSinceLastFlyingBubble >= spawnThreshold) {
            ticksSinceLastFlyingBubble = 0

            // Choose launch direction opposite or diagonal to movement
            val launchDir = if (isFacingRight) {
                if (Random.nextBoolean()) -0.8f else 1.2f
            } else {
                if (Random.nextBoolean()) 0.8f else -1.2f
            }

            val bubbleText = when (currentState) {
                BehaviorState.EXTERIOR_LAPS -> {
                    if (Random.nextFloat() < 0.4f) "Lap #$lapsCompleted 🏁" else flyingBubbleChirps[Random.nextInt(flyingBubbleChirps.size)]
                }
                BehaviorState.CORNER_SNOOZE -> "Zzz... 🌙"
                else -> flyingBubbleChirps[Random.nextInt(flyingBubbleChirps.size)]
            }

            // Launch from slightly above Kirby's head
            spawnFlyingCurvedBubble(bubbleText, posX + 20f, posY - 20f, launchDir)
        }
    }

    private fun updateTrailingBubbleFloating() {
        if (trailingBubbleTicksRemaining > 0) {
            trailingBubbleTicksRemaining--
            trailingSpeechBubble.translationY -= 0.15f

            if (trailingBubbleTicksRemaining < 25) {
                trailingSpeechBubble.alpha = trailingBubbleTicksRemaining / 25f
            }
        } else {
            trailingSpeechBubble.visibility = View.INVISIBLE
        }
    }

    private fun pickNextBehaviorState() {
        stateTicks = 0
        updateScreenMetrics()

        val roll = Random.nextFloat()
        currentState = when {
            roll < 0.40f -> {
                // 40% chance: Exterior Lap Patrol!
                maxStateTicks = 480
                lapLeg = Random.nextInt(4)
                kirbySprite.text = sprintFaces[Random.nextInt(sprintFaces.size)]
                applySpriteTransform()
                popTrailingBubble("Exterior Lap Patrol Active! 🏃💨", 0xFFFF79C6.toInt())
                BehaviorState.EXTERIOR_LAPS
            }
            roll < 0.72f -> {
                // 32% chance: Random Waypoint Roam
                maxStateTicks = 260
                pickNewRoamWaypoint()
                kirbySprite.text = roamFaces[Random.nextInt(roamFaces.size)]
                applySpriteTransform()
                if (Random.nextFloat() < 0.5f) {
                    popTrailingBubble(trailingQuotes[Random.nextInt(trailingQuotes.size)], 0xFF8BE9FD.toInt())
                }
                BehaviorState.RANDOM_ROAM
            }
            roll < 0.86f -> {
                // 14% chance: Playful Parabolic Hop
                maxStateTicks = 180
                hopProgress = 0f
                pickNewRoamWaypoint()
                kirbySprite.text = "(>‿<)ノ"
                applySpriteTransform()
                BehaviorState.PLAYFUL_HOP
            }
            roll < 0.93f -> {
                // 7% chance: Warp Sprint Dash
                maxStateTicks = 90
                pickWarpDashTarget()
                kirbySprite.text = "🌟(★ω★)🌟"
                applySpriteTransform()
                BehaviorState.WARP_DASH
            }
            else -> {
                // 7% chance: Corner Snooze Catnap
                maxStateTicks = 160
                kirbySprite.text = snoozeFace
                applySpriteTransform()
                spawnFlyingCurvedBubble("Zzz... 🌙", posX, posY, 0.5f, 0xFFBD93F9.toInt())
                BehaviorState.CORNER_SNOOZE
            }
        }
    }

    private fun pickNewRoamWaypoint() {
        updateScreenMetrics()
        val viewW = if (overlayView.width > 0) overlayView.width.toFloat() else 180f
        val viewH = if (overlayView.height > 0) overlayView.height.toFloat() else 180f

        val minX = sideMargin
        val maxX = (screenWidth - viewW - sideMargin).coerceAtLeast(minX + 10)
        val minY = topMargin
        val maxY = (screenHeight - viewH - bottomMargin).coerceAtLeast(minY + 10)

        targetX = minX + Random.nextFloat() * (maxX - minX)
        targetY = minY + Random.nextFloat() * (maxY - minY)
    }

    private fun pickWarpDashTarget() {
        updateScreenMetrics()
        val viewW = if (overlayView.width > 0) overlayView.width.toFloat() else 180f
        targetX = if (posX < screenWidth / 2f) screenWidth - viewW - sideMargin else sideMargin
        targetY = (topMargin + Random.nextFloat() * (screenHeight - topMargin - bottomMargin))
    }

    private fun updateAutonomousMotion() {
        stateTicks++
        floatPhase += 0.08f

        val viewW = if (overlayView.width > 0) overlayView.width.toFloat() else 180f
        val viewH = if (overlayView.height > 0) overlayView.height.toFloat() else 180f
        val minX = sideMargin
        val maxX = (screenWidth - viewW - sideMargin).coerceAtLeast(minX + 10)
        val minY = topMargin
        val maxY = (screenHeight - viewH - bottomMargin).coerceAtLeast(minY + 10)

        when (currentState) {
            BehaviorState.EXTERIOR_LAPS -> {
                // High-speed perimeter patrol around the screen edges
                val speed = 14.5f

                when (lapLeg) {
                    0 -> {
                        // Leg 0: Top edge (Left -> Right) - safe beneath camera punch hole
                        targetX = maxX
                        targetY = minY
                        isFacingRight = true
                    }
                    1 -> {
                        // Leg 1: Right edge (Top -> Bottom)
                        targetX = maxX
                        targetY = maxY
                    }
                    2 -> {
                        // Leg 2: Bottom edge (Right -> Left)
                        targetX = minX
                        targetY = maxY
                        isFacingRight = false
                    }
                    3 -> {
                        // Leg 3: Left edge (Bottom -> Top)
                        targetX = minX
                        targetY = minY
                    }
                }

                applySpriteTransform()

                val dx = targetX - posX
                val dy = targetY - posY
                val dist = hypot(dx, dy)

                if (dist < speed * 1.5f) {
                    posX = targetX
                    posY = targetY
                    lapLeg = (lapLeg + 1) % 4
                    if (lapLeg == 0) {
                        lapsCompleted++
                        popTrailingBubble("Lap #$lapsCompleted complete! 🏁", 0xFF50FA7B.toInt())
                        spawnFlyingCurvedBubble("Lap #$lapsCompleted! Wheee! 🌟", posX, posY, if (isFacingRight) 1f else -1f)
                        haptics.detentTick()
                    }
                } else {
                    posX += (dx / dist) * speed
                    posY += (dy / dist) * speed
                }

                // Gentle vertical sprint bobbing
                val sprintBob = sin(floatPhase * 2.2f) * 2.5f
                layoutParams.x = posX.roundToInt()
                layoutParams.y = (posY + sprintBob).roundToInt()
            }

            BehaviorState.RANDOM_ROAM -> {
                // Gentle floating drift towards target waypoint with sinusoidal levitation
                val speed = 4.5f
                val dx = targetX - posX
                val dy = targetY - posY
                val dist = hypot(dx, dy)

                if (dist < speed * 2f || stateTicks % 90 == 0 && dist < 80f) {
                    pickNewRoamWaypoint()
                } else {
                    velX = (dx / dist) * speed
                    velY = (dy / dist) * speed
                    posX += velX
                    posY += velY

                    isFacingRight = velX >= 0
                    applySpriteTransform()
                }

                // Sinusoidal vertical hover
                val hoverLevitation = sin(floatPhase) * 6.0f
                layoutParams.x = posX.roundToInt().coerceIn(minX.toInt(), maxX.toInt())
                layoutParams.y = (posY + hoverLevitation).roundToInt().coerceIn(minY.toInt(), maxY.toInt())
            }

            BehaviorState.PLAYFUL_HOP -> {
                // Bouncy gravity hops with proportional squish & stretch
                hopProgress += 0.05f
                val speedX = 6.0f
                val dx = targetX - posX

                posX += (if (dx >= 0) 1f else -1f) * speedX
                isFacingRight = dx >= 0

                val bounceHeight = 35f
                val arc = sin(hopProgress * Math.PI.toFloat()) * bounceHeight
                val stretch = 1.0f + sin(hopProgress * Math.PI.toFloat()) * 0.15f
                applySpriteTransform(stretch)

                if (hopProgress >= 1.0f) {
                    hopProgress = 0f
                    haptics.detentTick()
                    // Spawn a playful hop bubble!
                    if (Random.nextFloat() < 0.6f) {
                        spawnFlyingCurvedBubble("Boing! 💫", posX, posY, if (isFacingRight) 1f else -1f)
                    }
                }

                layoutParams.x = posX.roundToInt().coerceIn(minX.toInt(), maxX.toInt())
                layoutParams.y = (targetY - arc).roundToInt().coerceIn(minY.toInt(), maxY.toInt())
            }

            BehaviorState.WARP_DASH -> {
                val dashSpeed = 24f
                val dx = targetX - posX
                val dy = targetY - posY
                val dist = hypot(dx, dy)

                if (dist < dashSpeed * 1.5f) {
                    posX = targetX
                    posY = targetY
                    haptics.heavyThud()
                    popTrailingBubble("Warp complete! Safe landing! ⭐", 0xFFFF79C6.toInt())
                    spawnFlyingCurvedBubble("🌟 Star Sprint!", posX, posY, if (isFacingRight) 1f else -1f)
                    pickNextBehaviorState()
                    return
                } else {
                    posX += (dx / dist) * dashSpeed
                    posY += (dy / dist) * dashSpeed
                    isFacingRight = dx >= 0
                    applySpriteTransform()
                }

                layoutParams.x = posX.roundToInt().coerceIn(minX.toInt(), maxX.toInt())
                layoutParams.y = posY.roundToInt().coerceIn(minY.toInt(), maxY.toInt())
            }

            BehaviorState.CORNER_SNOOZE -> {
                // Peaceful catnap with subtle breathing scale
                val breath = 1.0f + sin(floatPhase * 0.5f) * 0.05f
                kirbySprite.scaleX = (if (isFacingRight) 1f else -1f) * currentScale * breath
                kirbySprite.scaleY = currentScale * breath
            }
        }

        try {
            windowManager.updateViewLayout(overlayView, layoutParams)
        } catch (e: Exception) {}

        if (stateTicks >= maxStateTicks) {
            pickNextBehaviorState()
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        tiltAcclimator?.stop()
        isLoopRunning = false
        mainHandler.removeCallbacksAndMessages(null)

        // Clean up any active detached flying bubbles & scarce chime-in
        clearActiveFlyingBubbles()
        clearScarceChimeView()
        isScarceModeActive = false

        if (::overlayView.isInitialized) {
            try {
                windowManager.removeView(overlayView)
            } catch (e: Exception) {}
        }
    }
}