package com.antigravity.mindmesh.kirby

import org.json.JSONArray
import org.json.JSONObject

data class VisitorPayload(
    val visitorName: String,
    val originNode: String,
    val message: String,
    val mood: String = "HAPPY_DANCE"
) {
    fun toJson(): String {
        return JSONObject().apply {
            put("visitorName", visitorName)
            put("originNode", originNode)
            put("message", message)
            put("mood", mood)
            put("timestamp", System.currentTimeMillis())
        }.toString()
    }

    companion object {
        fun fromJson(jsonStr: String): VisitorPayload {
            val obj = JSONObject(jsonStr)
            return VisitorPayload(
                visitorName = obj.optString("visitorName", "Anonymous Visitor"),
                originNode = obj.optString("originNode", "desktop_node"),
                message = obj.optString("message", "Poyo! Welcome to PixXL!"),
                mood = obj.optString("mood", "HAPPY_DANCE")
            )
        }
    }
}

data class PhoneVitals(
    val batteryPercent: Int,
    val tempCelsius: Float,
    val isCharging: Boolean,
    val overlayActive: Boolean
)

data class ActionCard(
    val id: String,
    val name: String,
    val icon: String,
    val abilityCategory: String,
    val costAP: Int,
    val cooldown: Double,
    val description: String,
    val speech: String,
    val auraColor: String = "#38bdf8",
    val hapticProfile: String = "detentTick",
    val soundFx: String = "poyo",
    val masteryLevel: Int = 1,
    val eventTriggers: List<String> = emptyList()
) {
    fun toJson(): JSONObject {
        return JSONObject().apply {
            put("id", id)
            put("name", name)
            put("icon", icon)
            put("abilityCategory", abilityCategory)
            put("costAP", costAP)
            put("cooldown", cooldown)
            put("description", description)
            put("speech", speech)
            put("auraColor", auraColor)
            put("hapticProfile", hapticProfile)
            put("soundFx", soundFx)
            put("masteryLevel", masteryLevel)
            put("eventTriggers", JSONArray(eventTriggers))
        }
    }

    companion object {
        fun fromJson(obj: JSONObject): ActionCard {
            val triggersList = mutableListOf<String>()
            val triggersArr = obj.optJSONArray("eventTriggers")
            if (triggersArr != null) {
                for (i in 0 until triggersArr.length()) {
                    triggersList.add(triggersArr.getString(i))
                }
            }
            return ActionCard(
                id = obj.optString("id", "card_unknown"),
                name = obj.optString("name", "Unknown Card"),
                icon = obj.optString("icon", "⭐"),
                abilityCategory = obj.optString("abilityCategory", "BASE"),
                costAP = obj.optInt("costAP", 1),
                cooldown = obj.optDouble("cooldown", 1.5),
                description = obj.optString("description", ""),
                speech = obj.optString("speech", "Poyo! ✨"),
                auraColor = obj.optString("auraColor", "#38bdf8"),
                hapticProfile = obj.optString("hapticProfile", "detentTick"),
                soundFx = obj.optString("soundFx", "poyo"),
                masteryLevel = obj.optInt("masteryLevel", 1),
                eventTriggers = triggersList
            )
        }
    }
}

data class EventResponse(
    val eventName: String,
    val primaryCardId: String,
    val speech: String,
    val haptic: String,
    val sound: String
)