package com.antigravity.mindmesh.kirby

import android.annotation.SuppressLint
import android.app.Activity
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.webkit.JavascriptInterface
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Button
import android.widget.HorizontalScrollView
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import org.json.JSONObject

/**
 * 📺 MINDMESH DISPLAY OUTPUT & KIRBY CONTROLLER ACTIVITY
 * ========================================================
 * Full-screen MindMesh portal & Kirby companion controller for Pixel 9 Pro XL.
 *
 * Core Features:
 *   1. Auto-Launch on startup: Kirby immediately roams your screen on open!
 *   2. Auto-Resume on permission grant: returns from Settings and launches.
 *   3. Prominent, un-clippable spare button: "🌸 Launch Kirby (Spare / Toggle)"
 *      styled in high-contrast Kirby Neon Pink inside a horizontal scroll container.
 *   4. JavaScript-to-Hardware Haptic Bridge (`window.PixXLNativeHaptics` and `window.AndroidBridge`).
 *   5. Full-screen responsive WebView with fallback to offline MindMesh HUD.
 */
class MainActivity : Activity() {

    private lateinit var webView: WebView
    private lateinit var haptics: PixXLHapticEngine
    private lateinit var btnOverlay: Button
    private lateinit var statusText: TextView
    private val OVERLAY_PERMISSION_REQ_CODE = 1234
    private var isOverlayRunning = false

    /**
     * JS Interface exposing Pixel 9 Pro XL hardware haptics directly to web apps.
     */
    inner class PixXLNativeHapticBridge {
        @JavascriptInterface
        fun tick() {
            runOnUiThread { haptics.detentTick() }
        }

        @JavascriptInterface
        fun click() {
            runOnUiThread { haptics.affirmClick() }
        }

        @JavascriptInterface
        fun thud() {
            runOnUiThread { haptics.heavyThud() }
        }

        @JavascriptInterface
        fun doubleClick() {
            runOnUiThread { haptics.doubleClick() }
        }
    }

    /**
     * Legacy & Unified AndroidBridge interface expected by embedded HTML apps.
     */
    inner class AndroidNativeBridge(private val context: Context) {
        @JavascriptInterface
        fun toggleFloatingOverlay() {
            runOnUiThread {
                haptics.affirmClick()
                toggleOverlay(isManual = true)
            }
        }

        @JavascriptInterface
        fun triggerHaptic(type: String) {
            runOnUiThread {
                when (type) {
                    "light", "tick" -> haptics.detentTick()
                    "medium", "click" -> haptics.affirmClick()
                    "heavy", "thud" -> haptics.heavyThud()
                    "double" -> haptics.doubleClick()
                    else -> haptics.detentTick()
                }
            }
        }

        @JavascriptInterface
        fun getDeviceVitals(): String {
            return JSONObject().apply {
                put("device", "Pixel 9 Pro XL")
                put("runtime", "Android 16 / AVF Linux")
                put("overlayActive", isOverlayRunning)
                put("timestamp", System.currentTimeMillis())
            }.toString()
        }
    }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        haptics = PixXLHapticEngine(this)

        val rootLayout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(0xFF090C10.toInt())
            layoutParams = ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT
            )
        }

        // Top Control Bar in a HorizontalScrollView so buttons NEVER get pushed off-screen or clipped
        val scrollBar = HorizontalScrollView(this).apply {
            isHorizontalScrollBarEnabled = false
            overScrollMode = View.OVER_SCROLL_IF_CONTENT_SCROLLS
            setBackgroundColor(0xFF10141D.toInt())
            setPadding(8, 8, 8, 8)
        }

        val controlBar = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
        }

        // 1. PRIMARY SPARE / MANUAL TOGGLE BUTTON (Un-clippable, high-contrast Kirby Pink)
        btnOverlay = Button(this).apply {
            text = "🌸 Launch Kirby"
            setTextColor(Color.WHITE)
            textSize = 13.5f
            typeface = Typeface.DEFAULT_BOLD
            val bg = GradientDrawable().apply {
                setColor(0xFFFF79C6.toInt()) // Kirby Pink
                cornerRadius = 28f
                setStroke(3, 0xFFFFFFFF.toInt())
            }
            background = bg
            setPadding(36, 16, 36, 16)
            val params = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ).apply {
                setMargins(8, 4, 8, 4)
            }
            layoutParams = params
            setOnClickListener {
                haptics.affirmClick()
                toggleOverlay(isManual = true)
            }
        }

        // 2. VISITOR POINT BUTTON
        val btnVisitor = Button(this).apply {
            text = "🚪 Visitor Point (:8088)"
            setTextColor(0xFF8BE9FD.toInt()) // Cyan
            textSize = 12f
            val bg = GradientDrawable().apply {
                setColor(0xFF1B2230.toInt())
                cornerRadius = 22f
                setStroke(2, 0xFF8BE9FD.toInt())
            }
            background = bg
            setPadding(24, 14, 24, 14)
            val params = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ).apply {
                setMargins(6, 4, 6, 4)
            }
            layoutParams = params
            setOnClickListener {
                haptics.affirmClick()
                startVisitorAccessPoint()
            }
        }

        // 3. HAPTICS LAB BUTTON
        val btnLab = Button(this).apply {
            text = "📳 Haptics Lab"
            setTextColor(0xFFF1FA8C.toInt()) // Yellow
            textSize = 12f
            val bg = GradientDrawable().apply {
                setColor(0xFF1B2230.toInt())
                cornerRadius = 22f
                setStroke(2, 0xFFF1FA8C.toInt())
            }
            background = bg
            setPadding(24, 14, 24, 14)
            val params = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ).apply {
                setMargins(6, 4, 6, 4)
            }
            layoutParams = params
            setOnClickListener {
                haptics.doubleClick()
                webView.loadUrl("http://localhost:8088/haptics")
            }
        }

        // 4. PORTAL / HUD SWITCHER BUTTON
        val btnPortal = Button(this).apply {
            text = "🌐 Dev Portal (:8088)"
            setTextColor(0xFF50FA7B.toInt()) // Green
            textSize = 12f
            val bg = GradientDrawable().apply {
                setColor(0xFF1B2230.toInt())
                cornerRadius = 22f
                setStroke(2, 0xFF50FA7B.toInt())
            }
            background = bg
            setPadding(24, 14, 24, 14)
            val params = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ).apply {
                setMargins(6, 4, 6, 4)
            }
            layoutParams = params
            setOnClickListener {
                haptics.affirmClick()
                webView.loadUrl("http://localhost:8088")
            }
        }

        // 5. OFFLINE APOTHECARY HUD BUTTON
        val btnHud = Button(this).apply {
            text = "🛡️ MindMesh HUD"
            setTextColor(0xFFBD93F9.toInt()) // Purple
            textSize = 12f
            val bg = GradientDrawable().apply {
                setColor(0xFF1B2230.toInt())
                cornerRadius = 22f
                setStroke(2, 0xFFBD93F9.toInt())
            }
            background = bg
            setPadding(24, 14, 24, 14)
            val params = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ).apply {
                setMargins(6, 4, 6, 4)
            }
            layoutParams = params
            setOnClickListener {
                haptics.affirmClick()
                webView.loadUrl("file:///android_asset/index.html")
            }
        }

        controlBar.addView(btnOverlay)
        controlBar.addView(btnVisitor)
        controlBar.addView(btnLab)
        controlBar.addView(btnPortal)
        controlBar.addView(btnHud)
        scrollBar.addView(controlBar)
        rootLayout.addView(scrollBar)

        // Web Display Output Portal with Multi-Touch & Native Haptics Bridge
        webView = WebView(this).apply {
            layoutParams = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.MATCH_PARENT
            )
            settings.javaScriptEnabled = true
            settings.domStorageEnabled = true
            settings.cacheMode = WebSettings.LOAD_NO_CACHE
            settings.setSupportZoom(true)
            settings.builtInZoomControls = true
            settings.displayZoomControls = false
            settings.allowFileAccess = true
            settings.allowContentAccess = true

            // Inject Native Bridges
            addJavascriptInterface(PixXLNativeHapticBridge(), "PixXLNativeHaptics")
            addJavascriptInterface(AndroidNativeBridge(this@MainActivity), "AndroidBridge")

            webViewClient = object : WebViewClient() {
                override fun onReceivedError(
                    view: WebView?,
                    errorCode: Int,
                    description: String?,
                    failingUrl: String?
                ) {
                    // Seamless fallback to embedded asset HUD if remote port 8088 is not running
                    if (failingUrl?.contains("localhost:8088") == true) {
                        view?.loadUrl("file:///android_asset/index.html")
                    }
                }
            }

            // Start by loading local portal, falling back automatically to embedded index.html
            loadUrl("http://localhost:8088")
        }
        rootLayout.addView(webView)

        setContentView(rootLayout)

        // Auto-start Visitor Access Point on port 8088
        startVisitorAccessPoint()

        // 🌸 AUTOMATIC AUTO-LAUNCH: Launch roaming Kirby companion on app open!
        launchKirbyOverlay(isManual = false)
    }

    override fun onResume() {
        super.onResume()
        // If returning after granting overlay permission in Settings, auto-launch Kirby!
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && Settings.canDrawOverlays(this)) {
            if (!isOverlayRunning) {
                launchKirbyOverlay(isManual = false)
            }
        }
    }

    /**
     * Toggles or restarts the roaming Kirby overlay.
     */
    private fun toggleOverlay(isManual: Boolean) {
        if (isOverlayRunning) {
            // Stop overlay
            val serviceIntent = Intent().setClassName(this, "com.antigravity.mindmesh.kirby.KirbyNativeOverlayService")
            stopService(serviceIntent)
            isOverlayRunning = false
            btnOverlay.text = "🌸 Launch Kirby"
            btnOverlay.background = GradientDrawable().apply {
                setColor(0xFFFF79C6.toInt())
                cornerRadius = 28f
                setStroke(3, 0xFFFFFFFF.toInt())
            }
            Toast.makeText(this, "Kirby dismissed to Dream Land ✨", Toast.LENGTH_SHORT).show()
        } else {
            launchKirbyOverlay(isManual)
        }
    }

    /**
     * Verifies overlay permission and launches KirbyNativeOverlayService.
     */
    private fun launchKirbyOverlay(isManual: Boolean) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && !Settings.canDrawOverlays(this)) {
            val intent = Intent(
                Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                Uri.parse("package:$packageName")
            )
            val msg = if (isManual) {
                "Please enable 'Display over other apps' to allow Kirby to roam screen!"
            } else {
                "Grant 'Display over other apps' permission to allow Kirby to roam!"
            }
            Toast.makeText(this, msg, Toast.LENGTH_LONG).show()
            startActivityForResult(intent, OVERLAY_PERMISSION_REQ_CODE)
        } else {
            val serviceIntent = Intent().setClassName(this, "com.antigravity.mindmesh.kirby.KirbyNativeOverlayService")
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                startForegroundService(serviceIntent)
            } else {
                startService(serviceIntent)
            }
            isOverlayRunning = true
            btnOverlay.text = "🌸 Kirby Active (Tap to Stop)"
            btnOverlay.background = GradientDrawable().apply {
                setColor(0xFF50FA7B.toInt()) // Neon Green
                cornerRadius = 28f
                setStroke(3, 0xFF090C10.toInt())
            }
            Toast.makeText(this, "🌸 Kirby Multi-Touch Overlay Active & Roaming!", Toast.LENGTH_SHORT).show()
        }
    }

    private fun startVisitorAccessPoint() {
        val serviceIntent = Intent().setClassName(this, "com.antigravity.mindmesh.kirby.KirbyVisitorAccessPointService")
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(serviceIntent)
        } else {
            startService(serviceIntent)
        }
    }
}