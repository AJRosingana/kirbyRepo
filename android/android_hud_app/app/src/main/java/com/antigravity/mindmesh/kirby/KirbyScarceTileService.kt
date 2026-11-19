package com.antigravity.mindmesh.kirby

import android.content.Intent
import android.os.Build
import android.service.quicksettings.Tile
import android.service.quicksettings.TileService

/**
 * Quick Settings Tile for toggling Kirby Hide / Scarce Mode from the notification shade.
 */
class KirbyScarceTileService : TileService() {

    override fun onStartListening() {
        super.onStartListening()
        syncTileState()
    }

    override fun onClick() {
        super.onClick()
        val intent = Intent(this, KirbyNativeOverlayService::class.java).apply {
            action = KirbyNativeOverlayService.ACTION_TOGGLE_SCARCE_MODE
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(intent)
        } else {
            startService(intent)
        }
        syncTileState(!KirbyNativeOverlayService.isScarceModeActive)
    }

    private fun syncTileState(active: Boolean = KirbyNativeOverlayService.isScarceModeActive) {
        qsTile?.let { tile ->
            tile.state = if (active) Tile.STATE_ACTIVE else Tile.STATE_INACTIVE
            tile.label = if (active) "Kirby: Scarce" else "Kirby: Active"
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                tile.subtitle = if (active) "Hidden (Tap to wake)" else "Tap to hide"
            }
            tile.updateTile()
        }
    }
}
