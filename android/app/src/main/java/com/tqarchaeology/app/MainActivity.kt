package com.tqarchaeology.app

import android.graphics.Color
import android.os.Bundle
import android.view.Gravity
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.util.Locale

class MainActivity : AppCompatActivity() {

    private lateinit var latitudeInput: EditText
    private lateinit var longitudeInput: EditText
    private lateinit var radiusInput: EditText
    private lateinit var resultText: TextView
    private lateinit var analyzeButton: Button

    private var arabic = true

    private val apiUrl =
        "https://tq-archaeology-api.onrender.com/api/analyze"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        createInterface()
    }

    private fun createInterface() {

        val scrollView = ScrollView(this)

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(32, 32, 32, 32)
            setBackgroundColor(Color.WHITE)
        }

        val title = TextView(this).apply {
            text = "TQ Archaeology"
            textSize = 30f
            setTextColor(Color.rgb(30, 30, 30))
            gravity = Gravity.CENTER
            setPadding(0, 10, 0, 4)
        }

        root.addView(title)

        val subtitle = TextView(this).apply {
            text = "التحليل الأثري\nArchaeological Analysis"
            textSize = 16f
            gravity = Gravity.CENTER
            setTextColor(Color.DKGRAY)
            setPadding(0, 0, 0, 30)
        }

        root.addView(subtitle)

        val languageButton = Button(this).apply {
            text = "English / العربية"
            setOnClickListener {
                arabic = !arabic
                updateLanguage()
            }
        }

        root.addView(languageButton)

        latitudeInput = createInput(
            "خط العرض Latitude",
            "33.7204130"
        )

        longitudeInput = createInput(
            "خط الطول Longitude",
            "36.5563628"
        )

        radiusInput = createInput(
            "نصف القطر بالمتر Radius (m)",
            "500"
        )

        root.addView(latitudeInput)
        root.addView(longitudeInput)
        root.addView(radiusInput)

        analyzeButton = Button(this).apply {
            text = "بدء التحليل / Analyze"
            textSize = 17f
            setOnClickListener {
                startAnalysis()
            }
        }

        root.addView(analyzeButton)

        resultText = TextView(this).apply {
            text = if (arabic) {
                "أدخل الإحداثيات واضغط «بدء التحليل»."
            } else {
                "Enter the coordinates and press Analyze."
            }

            textSize = 16f
            setTextColor(Color.DKGRAY)
            setPadding(10, 30, 10, 30)
        }

        root.addView(resultText)

        scrollView.addView(root)

        setContentView(scrollView)
    }

    private fun createInput(label: String, value: String): EditText {

        return EditText(this).apply {
            hint = label
            setText(value)
            textSize = 16f
            setPadding(20, 15, 20, 15)

            layoutParams = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ).apply {
                setMargins(0, 12, 0, 12)
            }
        }
    }

    private fun updateLanguage() {

        if (arabic) {
            analyzeButton.text = "بدء التحليل / Analyze"
            resultText.text = "أدخل الإحداثيات واضغط «بدء التحليل»."
        } else {
            analyzeButton.text = "Analyze / بدء التحليل"
            resultText.text = "Enter the coordinates and press Analyze."
        }
    }

    private fun startAnalysis() {

        val latitude = latitudeInput.text.toString().trim()
        val longitude = longitudeInput.text.toString().trim()
        val radius = radiusInput.text.toString().trim()

        if (latitude.isEmpty() || longitude.isEmpty()) {

            resultText.text = if (arabic) {
                "⚠️ يرجى إدخال خط العرض وخط الطول."
            } else {
                "⚠️ Please enter latitude and longitude."
            }

            return
        }

        val lat = latitude.toDoubleOrNull()
        val lon = longitude.toDoubleOrNull()
        val rad = radius.toDoubleOrNull() ?: 500.0

        if (lat == null || lon == null) {

            resultText.text = if (arabic) {
                "⚠️ الإحداثيات غير صحيحة."
            } else {
                "⚠️ Invalid coordinates."
            }

            return
        }

        if (lat !in -90.0..90.0 || lon !in -180.0..180.0) {

            resultText.text = if (arabic) {
                "⚠️ خط العرض أو خط الطول خارج النطاق الصحيح."
            } else {
                "⚠️ Latitude or longitude is outside the valid range."
            }

            return
        }

        if (rad <= 0) {

            resultText.text = if (arabic) {
                "⚠️ نصف القطر يجب أن يكون أكبر من صفر."
            } else {
                "⚠️ Radius must be greater than zero."
            }

            return
        }

        analyzeButton.isEnabled = false

        resultText.text = if (arabic) {
            "⏳ جارٍ الاتصال بخادم التحليل...\n\nقد يستغرق تحليل صور الأقمار الصناعية بعض الوقت."
        } else {
            "⏳ Connecting to the analysis server...\n\nSatellite analysis may take some time."
        }

        Thread {

            try {

                val jsonRequest = JSONObject().apply {
                    put("latitude", lat)
                    put("longitude", lon)
                    put("radius_m", rad)
                }

                val url = URL(apiUrl)

                val connection =
                    url.openConnection() as HttpURLConnection

                connection.requestMethod = "POST"
                connection.connectTimeout = 30000
                connection.readTimeout = 180000

                connection.doOutput = true

                connection.setRequestProperty(
                    "Content-Type",
                    "application/json"
                )

                connection.setRequestProperty(
                    "Accept",
                    "application/json"
                )

                connection.outputStream.use { output ->

                    output.write(
                        jsonRequest.toString().toByteArray(
                            Charsets.UTF_8
                        )
                    )
                }

                val responseCode = connection.responseCode

                val responseText =
                    if (responseCode in 200..299) {

                        connection.inputStream
                            .bufferedReader()
                            .use { it.readText() }

                    } else {

                        connection.errorStream
                            ?.bufferedReader()
                            ?.use { it.readText() }
                           
