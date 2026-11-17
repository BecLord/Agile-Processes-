package com.example.botdetector.detection

class MockScamDetectionEngine : ScamDetectionEngine {

    override fun analyseCall(
        phoneNumber: String,
        callAudioPath: String?
    ): ScamDetectionResult {

        val isSuspicious = phoneNumber.startsWith("+1800")

        val confidence = if (isSuspicious) 0.92f else 0.12f

        return ScamDetectionResult(
            isScam = isSuspicious,
            isAiGenerated = isSuspicious,
            confidence = confidence,
            classification = if (isSuspicious) "SCAM" else "SAFE"
        )
    }
}
