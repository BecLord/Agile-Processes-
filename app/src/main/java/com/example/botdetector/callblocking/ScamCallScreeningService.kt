package com.example.botdetector.callblocking

import android.telecom.Call
import android.telecom.CallScreeningService
import com.example.botdetector.data.AppDatabase
import com.example.botdetector.data.BlockedCall
import com.example.botdetector.detection.MockScamDetectionEngine
import com.example.botdetector.detection.ScamDetectionEngine
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class ScamCallScreeningService : CallScreeningService() {

    private val detectionEngine: ScamDetectionEngine =
        MockScamDetectionEngine()

    private val serviceScope = CoroutineScope(Dispatchers.IO)

    override fun onScreenCall(callDetails: Call.Details) {
        val isIncomingCall =
            callDetails.callDirection == Call.Details.DIRECTION_INCOMING

        if (!isIncomingCall) {
            return
        }

        val phoneNumber = callDetails.handle?.schemeSpecificPart ?: "Unknown"
        val callAudioPath: String? = null

        val result = detectionEngine.analyseCall(
            phoneNumber = phoneNumber,
            callAudioPath = callAudioPath
        )

        val shouldBlock =
            result.isScam || result.isAiGenerated

        val response = CallResponse.Builder()
            .setDisallowCall(shouldBlock)
            .setRejectCall(shouldBlock)
            .setSkipCallLog(shouldBlock)
            .setSkipNotification(shouldBlock)
            .build()

        respondToCall(callDetails, response)

        if (shouldBlock) {
            serviceScope.launch {
                try {
                    val database = AppDatabase.getDatabase(applicationContext)
                    database.blockedCallDao().insertBlockedCall(
                        BlockedCall(
                            phoneNumber = phoneNumber,
                            timestampMillis = System.currentTimeMillis(),
                            classificationConfidence = result.confidence,
                            classification = result.classification,
                            durationSeconds = 0
                        )
                    )
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
        }
    }
}
