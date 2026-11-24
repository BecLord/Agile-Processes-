package com.example.botdetector

import android.content.Context
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.botdetector.data.AdminMessage
import com.example.botdetector.data.AppDatabase
import com.example.botdetector.data.BlockedCall
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@Composable
fun ContactAdminScreen(
    context: android.content.Context,
    modifier: Modifier = Modifier
) {
    val database = AppDatabase.getDatabase(context)
    val scope = rememberCoroutineScope()

    var message by remember { mutableStateOf("") }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var confirmationMessage by remember { mutableStateOf<String?>(null) }

    val maxMessageLength = 500

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(
            text = "Contact Admin",
            style = MaterialTheme.typography.headlineMedium
        )

        Spacer(modifier = Modifier.height(16.dp))

        OutlinedTextField(
            value = message,
            onValueChange = { newMessage ->
                if (newMessage.length <= maxMessageLength) {
                    message = newMessage
                    errorMessage = null
                } else {
                    errorMessage =
                        "Message cannot exceed $maxMessageLength characters."
                }
            },
            label = {
                Text("Your message")
            },
            supportingText = {
                Text("${message.length}/$maxMessageLength characters")
            },
            isError = errorMessage != null,
            modifier = Modifier.fillMaxWidth()
        )

        errorMessage?.let { error ->
            Text(
                text = error,
                color = MaterialTheme.colorScheme.error,
                style = MaterialTheme.typography.bodySmall
            )
        }

        Spacer(modifier = Modifier.height(16.dp))

        Button(
            onClick = {
                val validationError = validateMessage(message)

                if (validationError != null) {
                    errorMessage = validationError
                    confirmationMessage = null
                } else {
                    scope.launch {
                        database.adminMessageDao().insertMessage(
                            AdminMessage(
                                userId = "guest_user",
                                message = message.trim(),
                                timestampMillis = System.currentTimeMillis(),
                                status = "SENT"
                            )
                        )

                        message = ""
                        confirmationMessage = "Your message has been sent"
                    }
                }
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Submit")
        }

        confirmationMessage?.let { confirmation ->
            Spacer(modifier = Modifier.height(16.dp))

            Text(
                text = confirmation,
                color = MaterialTheme.colorScheme.primary
            )
        }
    }
}

fun validateMessage(message: String): String? {
    return when {
        message.isBlank() -> "Message cannot be empty."
        message.length > 500 ->
            "Message cannot exceed 500 characters."

        containsInappropriateContent(message) ->
            "Message contains inappropriate content."

        else -> null
    }
}

fun containsInappropriateContent(message: String): Boolean {
    val blockedWords = listOf(
        "spam",
        "abuse",
        "offensive"
    )

    return blockedWords.any {
        message.lowercase().contains(it)
    }
}

@Composable
fun ScamCallLogScreen(
    context: Context,
    modifier: Modifier = Modifier
) {
    val database = AppDatabase.getDatabase(context)
    val blockedCalls by database
        .blockedCallDao()
        .getAllBlockedCalls()
        .collectAsStateWithLifecycle(initialValue = emptyList())

    var selectedCall by remember { mutableStateOf<BlockedCall?>(null) }

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(
            text = "Scam Call Log",
            style = MaterialTheme.typography.headlineMedium
        )

        Spacer(modifier = Modifier.height(16.dp))

        if (blockedCalls.isEmpty()) {
            Text("No blocked scam calls yet.")
        } else {
            LazyColumn {
                items(blockedCalls) { call ->
                    BlockedCallItem(
                        call = call,
                        onViewDetails = {
                            selectedCall = call
                        }
                    )

                    HorizontalDivider()
                }
            }
        }
    }

    selectedCall?.let { call ->
        CallDetailsDialog(
            call = call,
            onDismiss = {
                selectedCall = null
            }
        )
    }
}

@Composable
fun BlockedCallItem(
    call: BlockedCall,
    onViewDetails: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp)
    ) {
        Text(
            text = formatPhoneNumber(call.phoneNumber),
            style = MaterialTheme.typography.titleMedium
        )

        Text(
            text = formatDateTime(call.timestampMillis),
            style = MaterialTheme.typography.bodyMedium
        )

        Text(
            text = "${call.classification} • Confidence: " +
                    "${(call.classificationConfidence * 100).toInt()}%",
            style = MaterialTheme.typography.bodySmall
        )

        TextButton(onClick = onViewDetails) {
            Text("View details")
        }
    }
}

@Composable
fun CallDetailsDialog(
    call: BlockedCall,
    onDismiss: () -> Unit
) {
    AlertDialog(
        onDismissRequest = onDismiss,
        title = {
            Text("Call Details")
        },
        text = {
            Column {
                Text("Phone number: ${formatPhoneNumber(call.phoneNumber)}")
                Text("Date and time: ${formatDateTime(call.timestampMillis)}")
                Text("Classification: ${call.classification}")
                Text(
                    "Confidence: " +
                            "${(call.classificationConfidence * 100).toInt()}%"
                )
                Text("Duration: ${call.durationSeconds} seconds")
            }
        },
        confirmButton = {
            TextButton(onClick = onDismiss) {
                Text("Close")
            }
        }
    )
}

fun formatPhoneNumber(phoneNumber: String): String {
    return phoneNumber
}

fun formatDateTime(timestampMillis: Long): String {
    val formatter = SimpleDateFormat(
        "dd MMM yyyy, HH:mm",
        Locale.getDefault()
    )

    return formatter.format(Date(timestampMillis))
}