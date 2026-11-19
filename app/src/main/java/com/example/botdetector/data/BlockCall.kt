package com.example.botdetector.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "blocked_calls")
data class BlockedCall(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,

    val phoneNumber: String,

    val timestampMillis: Long,

    val classificationConfidence: Float,

    val classification: String,

    val durationSeconds: Int = 0
)
