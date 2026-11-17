package com.example.botdetector.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "admin_messages")
data class AdminMessage(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,

    val userId: String,

    val message: String,

    val timestampMillis: Long,

    val status: String
)
