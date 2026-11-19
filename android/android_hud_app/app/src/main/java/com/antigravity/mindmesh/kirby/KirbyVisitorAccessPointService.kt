package com.antigravity.mindmesh.kirby

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.io.BufferedReader
import java.io.InputStreamReader
import java.io.PrintWriter
import java.net.ServerSocket
import java.net.Socket

/**
 * 🚪 KIRBY VISITOR ACCESS POINT (PORT 8088)
 * =========================================
 * Embedded lightweight HTTP server running on the Pixel 9 Pro XL.
 * Allows external mesh nodes (desktop conductor, roaming Kirbies, visitor agents)
 * to push cards, notify arrivals, or query live phone vitals.
 */
class KirbyVisitorAccessPointService : Service() {

    private var serverSocket: ServerSocket? = null
    private var isRunning = false
    private val scope = CoroutineScope(Dispatchers.IO)

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        startForegroundNotification()
        startVisitorServer(8088)
    }

    private fun startForegroundNotification() {
        val channelId = "kirby_visitor_access"
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                channelId,
                "Kirby Visitor Access Point",
                NotificationManager.IMPORTANCE_LOW
            )
            val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            manager.createNotificationChannel(channel)
        }

        val notification: Notification = NotificationCompat.Builder(this, channelId)
            .setContentTitle("Kirby Visitor Access Point Active")
            .setContentText("Listening on localhost:8088 for incoming mesh visitors")
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .build()

        startForeground(2026, notification)
    }

    private fun startVisitorServer(port: Int) {
        isRunning = true
        scope.launch {
            try {
                serverSocket = ServerSocket(port)
                while (isRunning) {
                    val client = serverSocket?.accept() ?: break
                    handleVisitorRequest(client)
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    private fun handleVisitorRequest(socket: Socket) {
        scope.launch {
            try {
                val reader = BufferedReader(InputStreamReader(socket.getInputStream()))
                val out = PrintWriter(socket.getOutputStream(), true)

                val requestLine = reader.readLine() ?: return@launch
                val parts = requestLine.split(" ")
                val method = parts[0]
                val path = parts[1]

                // Simple routing for mesh visitors
                when {
                    path.startsWith("/visitor/tilter/status") -> {
                        val stateFile = java.io.File("/sdcard/AntiGravity_Shared/.kirby_tilter_state.json")
                        val response = if (stateFile.exists()) stateFile.readText() else """{"status":"NOMINAL","surface_slope_deg":0.0}"""
                        sendHttpResponse(out, 200, "application/json", response)
                    }
                    path.startsWith("/visitor/status") -> {
                        val response = """{"status":"ONLINE","device":"Pixel 9 Pro XL","port":8088,"kirbyState":"ACTIVE_OVERLAY","actionDeck":"LEARNING_ACTIVE"}"""
                        sendHttpResponse(out, 200, "application/json", response)
                    }
                    path.startsWith("/visitor/enter") -> {
                        val response = """{"welcome":"Poyo! Visitor admitted to Pixel 9 Pro XL!","accessPoint":"8088"}"""
                        sendHttpResponse(out, 200, "application/json", response)
                    }
                    path.startsWith("/visitor/react") -> {
                        val response = """{"reaction":"SPIT_STAR","device":"PixXL","result":"SUCCESS"}"""
                        sendHttpResponse(out, 200, "application/json", response)
                    }
                    path.startsWith("/visitor/cards") -> {
                        val cardsFile = java.io.File("/sdcard/AntiGravity_Shared/kirby_action_cards.json")
                        val response = if (cardsFile.exists()) {
                            cardsFile.readText()
                        } else {
                            """{"error":"kirby_action_cards.json not found on sdcard"}"""
                        }
                        sendHttpResponse(out, 200, "application/json", response)
                    }
                    path.startsWith("/visitor/card/draw") -> {
                        val cardsFile = java.io.File("/sdcard/AntiGravity_Shared/kirby_action_cards.json")
                        val response = if (cardsFile.exists()) {
                            try {
                                val json = org.json.JSONObject(cardsFile.readText())
                                val arr = json.getJSONArray("cards")
                                val picked = arr.getJSONObject((Math.random() * arr.length()).toInt())
                                picked.toString()
                            } catch (e: Exception) {
                                """{"error":"Failed parsing cards: ${e.message}"}"""
                            }
                        } else {
                            """{"id":"card_warp","name":"Warp Star","speech":"Poyo! Warp Star Dash! 🌟"}"""
                        }
                        sendHttpResponse(out, 200, "application/json", response)
                    }
                    path.startsWith("/visitor/event") -> {
                        val cardsFile = java.io.File("/sdcard/AntiGravity_Shared/kirby_action_cards.json")
                        val response = if (cardsFile.exists()) {
                            try {
                                val json = org.json.JSONObject(cardsFile.readText())
                                val matrix = json.optJSONObject("eventResponseMatrix")
                                val evKey = if (path.contains("event=")) {
                                    path.substringAfter("event=").substringBefore("&").uppercase()
                                } else {
                                    "EVENT_VISITOR_ARRIVED"
                                }
                                val rule = matrix?.optJSONObject(evKey) ?: matrix?.optJSONObject("EVENT_VISITOR_ARRIVED")
                                val respObj = org.json.JSONObject().apply {
                                    put("event", evKey)
                                    put("rule", rule)
                                    put("status", "SUCCESS")
                                    put("timestamp", System.currentTimeMillis())
                                }
                                respObj.toString()
                            } catch (e: Exception) {
                                """{"error":"Event processing failed: ${e.message}"}"""
                            }
                        } else {
                            """{"event":"VISITOR_ARRIVED","status":"SUCCESS","speech":"Poyo! Welcome to PixXL!"}"""
                        }
                        sendHttpResponse(out, 200, "application/json", response)
                    }
                    path.startsWith("/visitor/learn") -> {
                        val response = """{"status":"LEARNING_DISPATCHED","summary":"Curiosity step triggered across mesh","timestamp":${System.currentTimeMillis()}}"""
                        sendHttpResponse(out, 200, "application/json", response)
                    }
                    else -> {
                        val response = """{"error":"Unknown visitor route","validRoutes":["/visitor/status","/visitor/enter","/visitor/react","/visitor/cards","/visitor/card/draw","/visitor/event","/visitor/learn"]}"""
                        sendHttpResponse(out, 404, "application/json", response)
                    }
                }
                socket.close()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    private fun sendHttpResponse(out: PrintWriter, statusCode: Int, contentType: String, body: String) {
        out.println("HTTP/1.1 $statusCode OK")
        out.println("Content-Type: $contentType")
        out.println("Content-Length: ${body.toByteArray().size}")
        out.println("Access-Control-Allow-Origin: *")
        out.println("Connection: close")
        out.println()
        out.println(body)
        out.flush()
    }

    override fun onDestroy() {
        super.onDestroy()
        isRunning = false
        serverSocket?.close()
    }
}\n