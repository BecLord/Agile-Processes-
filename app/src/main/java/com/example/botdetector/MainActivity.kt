package com.example.botdetector

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import com.example.botdetector.ui.theme.BotDetectorTheme
import com.example.botdetector.ScamCallLogScreen

enum class AppScreen {
    LANDING,
    REGISTER,
    LOGIN,
    DASHBOARD,
    VIEW_SCAM_CALL,
    SCAM_CALL_LOG,
    CONTACT_ADMIN,
    RESET_PASSWORD
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            BotDetectorTheme {
                var currentScreen by remember { mutableStateOf(AppScreen.LANDING) }

                Scaffold(
                    modifier = Modifier.fillMaxSize(),
                    bottomBar = {
                        if (currentScreen == AppScreen.DASHBOARD || currentScreen == AppScreen.SCAM_CALL_LOG || currentScreen == AppScreen.CONTACT_ADMIN) {
                            NavigationBar {
                                NavigationBarItem(
                                    selected = currentScreen == AppScreen.DASHBOARD,
                                    onClick = { currentScreen = AppScreen.DASHBOARD },
                                    label = { Text("Dashboard") },
                                    icon = { Text("🏠") }
                                )
                                NavigationBarItem(
                                    selected = currentScreen == AppScreen.SCAM_CALL_LOG,
                                    onClick = { currentScreen = AppScreen.SCAM_CALL_LOG },
                                    label = { Text("Call Log") },
                                    icon = { Text("") }
                                )
                                NavigationBarItem(
                                    selected = currentScreen == AppScreen.CONTACT_ADMIN,
                                    onClick = { currentScreen = AppScreen.CONTACT_ADMIN },
                                    label = { Text("Contact") },
                                    icon = { Text("✉") }
                                )
                            }
                        }
                    }
                ) { innerPadding ->
                    when (currentScreen) {
                        AppScreen.LANDING -> LandingScreen(
                            onNavigateToRegister = { currentScreen = AppScreen.REGISTER },
                            onNavigateToLogin = { currentScreen = AppScreen.LOGIN },
                            modifier = Modifier.padding(innerPadding)
                        )
                        AppScreen.REGISTER -> RegisterScreen(
                            onNavigateToLogin = { currentScreen = AppScreen.LOGIN },
                            onNavigateToLanding = { currentScreen = AppScreen.LANDING },
                            modifier = Modifier.padding(innerPadding)
                        )
                        AppScreen.LOGIN -> LoginScreen(
                            onNavigateToRegister = { currentScreen = AppScreen.REGISTER },
                            onNavigateToSignIn = { currentScreen = AppScreen.DASHBOARD },
                            onNavigateToForgotPassword = { currentScreen = AppScreen.RESET_PASSWORD },
                            modifier = Modifier.padding(innerPadding)
                        )
                        AppScreen.DASHBOARD -> DashboardScreen(
                            onNavigateToViewScamCall = { currentScreen = AppScreen.VIEW_SCAM_CALL },
                            onLogout = { currentScreen = AppScreen.LANDING },
                            modifier = Modifier.padding(innerPadding)
                        )
                        AppScreen.VIEW_SCAM_CALL -> ViewScamCallScreen(
                            onNavigateBack = { currentScreen = AppScreen.DASHBOARD },
                            modifier = Modifier.padding(innerPadding)
                        )
                        AppScreen.SCAM_CALL_LOG -> ScamCallLogScreen(
                            context = this@MainActivity,
                            modifier = Modifier.padding(innerPadding)
                        )
                        AppScreen.CONTACT_ADMIN -> ContactAdminScreen(
                            context = this@MainActivity,
                            modifier = Modifier.padding(innerPadding)
                        )
                        AppScreen.RESET_PASSWORD -> ResetPasswordScreen(
                            onNavigateToLogin = { currentScreen = AppScreen.LOGIN },
                            modifier = Modifier.padding(innerPadding)
                        )
                    }
                }
            }
        }
    }
}
