package com.example.botdetector.ui.theme

import android.app.Activity
import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext

private val LightColorScheme = lightColorScheme(
    primary = PinkyRed,
    secondary = PinkyRedDark,
    tertiary = PinkyRedLight,
    background = White,
    surface = White,
    onPrimary = White,
    onSecondary = White,
    onTertiary = White,
    onBackground = Charcoal,
    onSurface = Charcoal
)

private val DarkColorScheme = darkColorScheme(
    primary = PinkyRedLight,
    secondary = PinkyRed,
    tertiary = PinkyRedDark,
    background = Charcoal,
    surface = Charcoal,
    onPrimary = Charcoal,
    onSecondary = White,
    onTertiary = White,
    onBackground = White,
    onSurface = White
)

@Composable
fun BotDetectorTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    // Set dynamicColor to false by default so custom pinky-red & white theme is guaranteed
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }

        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
