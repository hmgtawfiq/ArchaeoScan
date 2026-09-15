package com.tqarchaeology.app

import android.graphics.Color
import android.os.Bundle
import android.text.InputType
import android.view.Gravity
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast

import androidx.appcompat.app.AppCompatActivity

import org.json.JSONObject
import org.osmdroid.config.Configuration
import org.osmdroid.tileprovider.tilesource.TileSourceFactory
import org.osmdroid.util.GeoPoint
import org.osmdroid.views.MapView
import org.osmdroid.views.overlay.Marker

import java.net.HttpURLConnection
import java.net.URL

class MainActivity : AppCompatActivity() {

    private lateinit var mapView: MapView
    private lateinit var latitudeText: TextView
    private lateinit var longitudeText: TextView
    private lateinit var radiusInput: EditText
    private lateinit var analyzeButton: Button

    private var selectedPoint =
        GeoPoint(33.7204130, 36.5563628)

    private var selectedMarker: Marker? = null

    private val apiUrl =
        "https://tq-archaeology-api.onrender.com/api/analyze"

    override fun onCreate(
        savedInstanceState: Bundle?
    ) {
        super.onCreate(savedInstanceState)

        Configuration.getInstance()
            .userAgentValue = packageName

        createInterface()
    }

    private fun createInterface() {

        val root = LinearLayout(this).apply {
            orientation =
                LinearLayout.VERTICAL

            setBackgroundColor(
                Color.WHITE
            )
        }

        val title = TextView(this).apply {

            text =
                "TQ Archaeology"

            textSize = 28f

            gravity =
                Gravity.CENTER

            setTextColor(
                Color.rgb(30, 30, 30)
            )

            setPadding(
                10,
                20,
                10,
                5
            )
        }

        root.addView(title)

        val subtitle = TextView(this).apply {

            text =
                "اختيار موقع الدراسة وتحليل المؤشرات"

            textSize = 15f

            gravity =
                Gravity.CENTER

            setTextColor(
                Color.DKGRAY
            )

            setPadding(
                10,
                0,
                10,
                15
            )
        }

        root.addView(subtitle)

        mapView = MapView(this).apply {

            setTileSource(
                TileSourceFactory.MAPNIK
            )

            setMultiTouchControls(
                true
            )

            controller.setZoom(
                12.0
            )

            controller.setCenter(
                selectedPoint
            )

            layoutParams =
                LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    0,
                    1f
                )
        }

        root.addView(mapView)

        val infoLayout =
            LinearLayout(this).apply {

                orientation =
                    LinearLayout.VERTICAL

                setPadding(
                    20,
                    10,
                    20,
                    10
                )
            }

        latitudeText =
            TextView(this).apply {

                text =
                    "خط العرض: ${selectedPoint.latitude}"

                textSize = 15f
            }

        longitudeText =
            TextView(this).apply {

                text =
                    "خط الطول: ${selectedPoint.longitude}"

                textSize = 15f
            }

        infoLayout.addView(
            latitudeText
        )

        infoLayout.addView(
            longitudeText
        )

        radiusInput =
            EditText(this).apply {

                hint =
                    "نصف قطر الدراسة بالمتر"

                setText("500")

                textSize = 16f

                inputType =
                    InputType.TYPE_CLASS_NUMBER
            }

        infoLayout.addView(
            radiusInput
        )

        analyzeButton =
            Button(this).apply {

                text =
                    "🔬 تحليل الموقع"

                textSize = 17f

                setOnClickListener {

                    startAnalysis()
                }
            }

        infoLayout.addView(
            analyzeButton
        )

        root.addView(
            infoLayout
        )

        setContentView(root)

        addMarker(
            selectedPoint
        )

        mapView.setOnTouchListener { _, _ ->

            val center =
                mapView.mapCenter as GeoPoint

            selectedPoint =
                GeoPoint(
                    center.latitude,
                    center.longitude
                )

            latitudeText.text =
                "خط العرض: ${selectedPoint.latitude}"

            longitudeText.text =
                "خط الطول: ${selectedPoint.longitude}"

            addMarker(
                selectedPoint
            )

            false
        }
    }

    private fun addMarker(
        point: GeoPoint
    ) {

        selectedMarker?.let {

            mapView.overlays.remove(it)
        }

        val marker =
            Marker(mapView)

        marker.position =
            point

        marker.title =
            "موقع الدراسة"

        marker.setAnchor(
            Marker.ANCHOR_CENTER,
            Marker.ANCHOR_BOTTOM
        )

        mapView.overlays.add(
            marker
        )

        selectedMarker =
            marker

        mapView.invalidate()
    }
        private fun startAnalysis() {

        val radius =
            radiusInput.text
                .toString()
                .trim()
                .toDoubleOrNull()
                ?: 500.0

        if (radius <= 0.0) {

            radiusInput.error =
                "يجب أن يكون نصف القطر أكبر من صفر"

            return
        }

        analyzeButton.isEnabled =
            false

        analyzeButton.text =
            "⏳ جارٍ التحليل..."

        val latitude =
            selectedPoint.latitude

        val longitude =
            selectedPoint.longitude

        Thread {

            var connection:
                    HttpURLConnection? = null

            try {

                val jsonRequest =
                    JSONObject()

                jsonRequest.put(
                    "latitude",
                    latitude
                )

                jsonRequest.put(
                    "longitude",
                    longitude
                )

                jsonRequest.put(
                    "radius_m",
                    radius
                )

                val url =
                    URL(apiUrl)

                connection =
                    url.openConnection()
                            as HttpURLConnection

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
                            .toByteArray(
                                Charsets.UTF_8
                            )
                    )
                }

                val responseCode =
                    connection.responseCode

                val responseText: String

                if (
                    responseCode in 200..299
                ) {

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
                            ?: "خطأ غير معروف من الخادم"
                }

                runOnUiThread {

                    analyzeButton.isEnabled =
                        true

                    analyzeButton.text =
                        "🔬 تحليل الموقع"

                    if (
                        responseCode in 200..299
                    ) {

                        showAnalysisResult(
                            responseText
                        )

                    } else {

                        Toast.makeText(
                            this,
                            "فشل التحليل: HTTP $responseCode",
                            Toast.LENGTH_LONG
                        ).show()
                    }
                }

            } catch (e: Exception) {

                runOnUiThread {

                    analyzeButton.isEnabled =
                        true

                    analyzeButton.text =
                        "🔬 تحليل الموقع"

                    Toast.makeText(
                        this,
                        "تعذر الاتصال بالخادم:\n${e.message}",
                        Toast.LENGTH_LONG
                    ).show()
                }

            } finally {

                connection?.disconnect()
            }

        }.start()
    }
           private fun showAnalysisResult(
        responseText: String
    ) {

        try {

            val json =
                JSONObject(responseText)

            val scores =
                json.optJSONObject("scores")

            val finalScore =
                scores?.optDouble(
                    "final",
                    0.0
                ) ?: 0.0

            val spectralScore =
                scores?.optDouble(
                    "spectral",
                    0.0
                ) ?: 0.0

            val temporalScore =
                scores?.optDouble(
                    "temporal",
                    0.0
                ) ?: 0.0

            val geometryScore =
                scores?.optDouble(
                    "geometry",
                    0.0
                ) ?: 0.0

            val classification =
                json.optString(
                    "classification",
                    "غير محدد"
                )

            val description =
                json.optString(
                    "description",
                    ""
                )

            val result =
                """
                
                ✅ اكتمل تحليل الموقع
                
                📍 موقع الدراسة
                
                خط العرض:
                ${selectedPoint.latitude}
                
                خط الطول:
                ${selectedPoint.longitude}
                
                📊 نتائج التحليل
                
                النتيجة النهائية:
                ${"%.2f".format(finalScore)}
                
                النتيجة الطيفية:
                ${"%.2f".format(spectralScore)}
                
                النتيجة الزمنية:
                ${"%.2f".format(temporalScore)}
                
                النتيجة المكانية:
                ${"%.2f".format(geometryScore)}
                
                🎯 التصنيف:
                $classification
                
                📝 التفسير:
                $description
                
                ⚠️ ملاحظة مهمة:
                
                هذه النتائج تمثل مؤشرات
                وشذوذات تستحق الدراسة،
                ولا تعني إثبات وجود أثر
                أو دفين.
                
                """.trimIndent()

            android.app.AlertDialog.Builder(
                this
            )
                .setTitle(
                    "TQ Archaeology"
                )
                .setMessage(
                    result
                )
                .setPositiveButton(
                    "موافق",
                    null
                )
                .show()

        } catch (e: Exception) {

            android.app.AlertDialog.Builder(
                this
            )
                .setTitle(
                    "نتيجة التحليل"
                )
                .setMessage(
                    responseText
                )
                .setPositiveButton(
                    "موافق",
                    null
                )
                .show()
        }
    } 
              override fun onResume() {
        super.onResume()
        mapView.onResume()
    }

    override fun onPause() {
        super.onPause()
        mapView.onPause()
    }
} 
    
