package com.example.botdetector.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface BlockedCallDao {

    @Insert
    suspend fun insertBlockedCall(call: BlockedCall): Long

    @Query("SELECT * FROM blocked_calls ORDER BY timestampMillis DESC")
    fun getAllBlockedCalls(): Flow<List<BlockedCall>>

    @Query("SELECT * FROM blocked_calls WHERE id = :callId")
    suspend fun getBlockedCallById(callId: Long): BlockedCall?

    @Query("DELETE FROM blocked_calls")
    suspend fun clearAllBlockedCalls()
}
