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

class MainActivity : AppCompatActivity() {

    private lateinit var latitudeInput: EditText
    private lateinit var longitudeInput: EditText
    private lateinit var radiusInput: EditText
    private lateinit var resultText: TextView
    private lateinit var analyzeButton: Button
    private lateinit var languageButton: Button

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

        languageButton = Button(this).apply {
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
            text = "أدخل الإحداثيات واضغط «بدء التحليل»."
            textSize = 16f
            setTextColor(Color.DKGRAY)
            setPadding(10, 30, 10, 30)
        }

        root.addView(resultText)

        scrollView.addView(root)

        setContentView(scrollView)
    }

    private fun createInput(
        label: String,
        value: String
    ): EditText {

        return EditText(this).apply {

            hint = label
            setText(value)
            textSize = 
            16f

            setPadding(
                20,
                15,
                20,
                15
            )

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

            languageButton.text =
                "English / العربية"

            analyzeButton.text =
                "بدء التحليل / Analyze"

            resultText.text =
                "أدخل الإحداثيات واضغط «بدء التحليل»."

        } else {

            languageButton.text =
                "العربية / English"

            analyzeButton.text =
                "Analyze / بدء التحليل"

            resultText.text =
                "Enter the coordinates and press Analyze."
        }

}
    private fun startAnalysis() {

        val latitude =
            latitudeInput.text.toString().trim()

        val longitude =
            longitudeInput.text.toString().trim()

        val radius =
            radiusInput.text.toString().trim()

        if (latitude.isEmpty() ||
            longitude.isEmpty()
        ) {

            if (arabic) {
                resultText.text =
                    "⚠️ يرجى إدخال خط العرض وخط الطول."
            } else {
                resultText.text =
                    "⚠️ Please enter latitude and longitude."
            }

            return
        }

        val latValue =
            latitude.toDoubleOrNull()

        val lonValue =
            longitude.toDoubleOrNull()

        val radiusValue =
            radius.toDoubleOrNull()

        if (latValue == null ||
            lonValue == null
        ) {

            if (arabic) {
                resultText.text =
                    "⚠️ الإحداثيات غير صحيحة."
            } else {
                resultText.text =
                    "⚠️ Invalid coordinates."
            }

            return
        }

        val lat = latValue
        val lon = lonValue
        val rad = radiusValue ?: 500.0

        if (lat < -90.0 ||
            lat > 90.0 ||
            lon < -180.0 ||
            lon > 180.0
        ) {

            if (arabic) {
                resultText.text =
                    "⚠️ خط العرض أو خط الطول خارج النطاق الصحيح."
            } else {
                resultText.text =
                    "⚠️ Latitude or longitude is outside the valid range."
            }

            return
        }

        if (rad <= 0.0) {

            if (arabic) {
                resultText.text =
                    "⚠️ نصف القطر يجب أن يكون أكبر من صفر."
            } else {
                resultText.text =
                    "⚠️ Radius must be greater than zero."
            }

            return
        
         }
             analyzeButton.isEnabled = false

        if (arabic) {
            resultText.text =
                "⏳ جارٍ الاتصال بخادم التحليل...\n\n" +
                        "قد يستغرق تحليل صور الأقمار الصناعية بعض الوقت."
        } else {
            resultText.text =
                "⏳ Connecting to the analysis server...\n\n" +
                        "Satellite analysis may take some time."
        }

        Thread {

            var connection: HttpURLConnection? = null

            try {

                val jsonRequest = JSONObject()

                jsonRequest.put(
                    "latitude",
                    lat
                )

                jsonRequest.put(
                    "longitude",
                    lon
                )

                jsonRequest.put(
                    "radius_m",
                    rad
                )

                val url =
                    URL(apiUrl)

                connection =
                    url.openConnection() as HttpURLConnection

                connection.requestMethod =
                    "POST"

                connection.connectTimeout =
                    30000

                connection.readTimeout =
                    180000

                connection.doOutput =
                    true

                connection.setRequestProperty(
                    "Content-Type",
                    "application/json; charset=UTF-8"
                )

                connection.setRequestProperty(
                    "Accept",
                    "application/json"
                )

                connection.outputStream.use { output ->

                    output.write(
                        jsonRequest
                            .toString()
                            .toByteArray(Charsets.UTF_8)
                    )
                }

                val responseCode =
                    connection.responseCode

                val responseText: String

                if (responseCode in 200..299) {

                    responseText =
                        connection.inputStream
                            .bufferedReader()
                            .use {
                                it.readText()
                            }

                } else {

                    responseText =
                        connection.errorStream
                            ?.bufferedReader()
                            ?.use {
                                it.readText()
                            }
                            ?: "Unknown server error"
                } 
                                runOnUiThread {

                    analyzeButton.isEnabled = true

                    if (responseCode in 200..299) {

                        resultText.text =
                            formatAnalysisResult(responseText)

                    } else {

                        if (arabic) {

                            resultText.text =
                                "❌ فشل التحليل.\n\n" +
                                        "رمز الخادم: $responseCode\n\n" +
                                        responseText

                        } else {

                            resultText.text =
                                "❌ Analysis failed.\n\n" +
                                        "Server code: $responseCode\n\n" +
                                        responseText
                        }
                    }
                }

            } catch (e: Exception) {

                runOnUiThread {

                    analyzeButton.isEnabled = true

                    if (arabic) {

                        resultText.text =
                            "❌ تعذر الاتصال بخادم التحليل.\n\n" +
                                    "الخطأ:\n" +
                                    (e.message ?: "خطأ غير معروف")

                    } else {

                        resultText.text =
                            "❌ Unable to connect to the analysis server.\n\n" +
                                    "Error:\n" +
                                    (e.message ?: "Unknown error")
                    }
                }

            } finally {

                connection?.disconnect()
            }

        }.start()
    }

    private fun formatAnalysisResult(
        responseText: String
    ): String {

        return try {

            val json = JSONObject(responseText)
            val builder = StringBuilder()

            builder.append(
                if (arabic) {
                    "✅ اكتمل التحليل\n\n"
                } else {
                    "✅ Analysis completed\n\n"
                }
            )

            appendValue(
                builder,
                json,
                "latitude",
                if (arabic) "خط العرض" else "Latitude"
            )

            appendValue(
                builder,
                json,
                "longitude",
                if (arabic) "خط الطول" else "Longitude"
            )

            appendValue(
                builder,
                json,
                "radius_m",
                if (arabic) "نصف القطر" else "Radius"
            )

            if (json.has("scores")) {

                val scores =
                    json.getJSONObject("scores")

                builder.append(
                    if (arabic) {
                        "📊 النتائج\n\n"
                    } else {
                        "📊 Results\n\n"
                    }
                )

                appendValue(
                    builder,
                    scores,
                    "final",
                    if (arabic) "النتيجة النهائية" else "Final score"
                )

                appendValue(
                    builder,
                    scores,
                    "spectral",
                    if (arabic) "النتيجة الطيفية" else "Spectral score"
                )

                appendValue(
                    builder,
                    scores,
                    "temporal",
                    if (arabic) "النتيجة الزمنية" else "Temporal score"
                )

                appendValue(
                    builder,
                    scores,
                    "geometry",
                    if (arabic) "النتيجة المكانية" else "Spatial score"
                )
            }

            appendValue(
                builder,
                json,
                "classification",
                if (arabic) "التصنيف" else "Classification"
            )

            appendValue(
                builder,
                json,
                "description",
                if (arabic) "الوصف" else "Description"
            )

            if (json.has("spatial")) {

                val spatial =
                    json.getJSONObject("spatial")

                builder.append(
                    if (arabic) {
                        "📍 التحليل المكاني\n\n"
                    } else {
                        "📍 Spatial analysis\n\n"
                    }
                )

                appendValue(
                    builder,
                    spatial,
                    "score",
                    if (arabic) "النتيجة" else "Score"
                )

                appendValue(
                    builder,
                    spatial,
                    "anomaly_ratio",
                    if (arabic) "نسبة الشذوذ" else "Anomaly ratio"
                )
            }

            if (json.has("temporal")) {

                val temporal =
                    json.getJSONObject("temporal")

                builder.append(
                    if (arabic) {
                        "🕒 التحليل الزمني\n\n"
                    } else {
                        "🕒 Temporal analysis\n\n"
                    }
                )

                appendValue(
                    builder,
                    temporal,
                    "score",
                    if (arabic) "النتيجة" else "Score"
                )

                appendValue(
                    builder,
                    temporal,
                    "mean_change",
                    if (arabic) "متوسط التغير" else "Mean change"
                )

                appendValue(
                    builder,
                    temporal,
                    "change_ratio",
                    if (arabic) "نسبة التغير" else "Change ratio"
                )
            }

            builder.toString().trim()

        } catch (e: Exception) {

            responseText
        }
    }

    private fun appendValue(
        builder: StringBuilder,
        json: JSONObject,
        key: String,
        label: String
    ) {

        if (!json.has(key) ||
            json.isNull(key)
        ) {
            return
        }

        builder.append(label)
            .append(": ")
            .append(json.get(key).toString())
            .append("\n\n")
    }
}
