package com.example.botdetector

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import com.example.botdetector.ui.theme.BotDetectorTheme

enum class AppScreen {
    LANDING,
    REGISTER,
    LOGIN,
    HOME
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            BotDetectorTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    var currentScreen by remember { mutableStateOf(AppScreen.LANDING) }

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
                            onNavigateToSignIn = {
                                currentScreen = AppScreen.HOME
                            },
                            modifier = Modifier.padding(innerPadding)
                        )
                        AppScreen.HOME -> HomeScreen(
                            onLogout = { currentScreen = AppScreen.LANDING },
                            modifier = Modifier.padding(innerPadding)
                        )
                    }
                }
            }
        }
    }
}
