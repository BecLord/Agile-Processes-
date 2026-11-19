package com.example.botdetector

import androidx.compose.runtime.mutableStateListOf
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

data class ScamCallItem(
    val phoneNumber: String,
    val timestamp: String,
    val reason: String
)

object CallLogManager {
    val scamCalls = mutableStateListOf<ScamCallItem>()

    init {
        //a sample log entry for initial testing/previewing
        scamCalls.add(
            ScamCallItem(
                phoneNumber = "+1 (800) 555-0199",
                timestamp = SimpleDateFormat("dd-MM-yyyy ss:mm:HH", Locale.getDefault()).format(Date()),
                reason = "Detected Bot / Scam Pattern"
            )
        )
    }

    fun logCall(phoneNumber: String, reason: String) {
        val currentTime = SimpleDateFormat("dd-MM-yyyy ss:mm:HH", Locale.getDefault()).format(Date())
        scamCalls.add(0, ScamCallItem(phoneNumber, currentTime, reason))
    }
}
