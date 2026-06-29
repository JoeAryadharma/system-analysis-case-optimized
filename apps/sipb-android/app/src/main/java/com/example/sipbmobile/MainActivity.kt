package com.example.sipbmobile

import android.os.Bundle
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.ComponentActivity

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val webView = WebView(this)
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.settings.allowFileAccess = true
        webView.settings.databaseEnabled = true
        
        // Ensure links open inside the app instead of default browser
        webView.webViewClient = WebViewClient()
        
        // Load the local HTML prototype from assets
        webView.loadUrl("file:///android_asset/index.html")
        
        setContentView(webView)
    }
}
