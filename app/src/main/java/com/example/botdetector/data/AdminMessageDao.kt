package com.example.botdetector.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface AdminMessageDao {

    @Insert
    suspend fun insertMessage(message: AdminMessage): Long

    @Query("SELECT * FROM admin_messages ORDER BY timestampMillis DESC")
    fun getAllMessages(): Flow<List<AdminMessage>>

    @Query("DELETE FROM admin_messages")
    suspend fun clearAllMessages()
}
