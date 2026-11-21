package com.example.botdetector.detection

data class ScamDetectionResult(
    val isScam: Boolean,
    val isAiGenerated: Boolean,
    val confidence: Float,
    val classification: String
)

interface ScamDetectionEngine {
    fun analyseCall(
        phoneNumber: String,
        callAudioPath: String?
    ): ScamDetectionResult
}

interface ScamDetection : ScamDetectionEngine
