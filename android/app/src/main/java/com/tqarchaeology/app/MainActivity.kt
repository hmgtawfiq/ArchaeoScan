package com.tqarchaeology.app

import android.os.Bundle
import android.view.Gravity
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private var arabic = true

    private lateinit var title: TextView
    private lateinit var subtitle: TextView
    private lateinit var latitudeInput: EditText
    private lateinit var longitudeInput: EditText
    private lateinit var radiusInput: EditText
    private lateinit var analyzeButton: Button
    private lateinit var languageButton: Button
    private lateinit var resultText: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            setPadding(40, 40, 40, 40)
        }

        title = TextView(this).apply {
            text = "TQ Archaeology"
            textSize = 30f
            gravity = Gravity.CENTER
        }

        subtitle = TextView(this).apply {
            text = "التحليل الأثري"
            textSize = 18f
            gravity = Gravity.CENTER
            setPadding(0, 12, 0, 30)
        }

        latitudeInput = EditText(this).apply {
            hint = "خط العرض Latitude"
            inputType = 8194
        }

        longitudeInput = EditText(this).apply {
            hint = "خط الطول Longitude"
            inputType = 8194
        }

        radiusInput = EditText(this).apply {
            hint = "نصف قطر التحليل بالمتر"
            inputType = 2
            setText("500")
        }

        analyzeButton = Button(this).apply {
            text = "بدء التحليل"
            textSize = 16f

            setOnClickListener {
                showInputStatus()
            }
        }

        languageButton = Button(this).apply {
            text = "English"
            textSize = 15f

            setOnClickListener {
                arabic = !arabic
                updateLanguage()
            }
        }

        resultText = TextView(this).apply {
            text = ""
            textSize = 16f
            gravity = Gravity.CENTER
            setPadding(0, 25, 0, 0)
        }

        root.addView(title)
        root.addView(subtitle)

        root.addView(
            latitudeInput,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            )
        )

        root.addView(
            longitudeInput,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            )
        )

        root.addView(
            radiusInput,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            )
        )

        root.addView(analyzeButton)
        root.addView(languageButton)
        root.addView(resultText)

        setContentView(root)
    }

    private fun showInputStatus() {

        val latitude = latitudeInput.text.toString().trim()
        val longitude = longitudeInput.text.toString().trim()
        val radius = radiusInput.text.toString().trim()

        if (latitude.isEmpty() || longitude.isEmpty()) {
            resultText.text =
                if (arabic) {
                    "يرجى إدخال خط العرض وخط الطول."
                } else {
                    "Please enter latitude and longitude."
                }
            return
        }

        resultText.text =
            if (arabic) {
                "تم تجهيز نقطة التحليل:\n\nخط العرض: $latitude\nخط الطول: $longitude\nنصف القطر: $radius م\n\nجاهز لربط التحليل بالأقمار الصناعية."
            } else {
                "Analysis point ready:\n\nLatitude: $latitude\nLongitude: $longitude\nRadius: $radius m\n\nReady to connect satellite analysis."
            }
    }

    private fun updateLanguage() {

        if (arabic) {
            title.text = "TQ Archaeology"
            subtitle.text = "التحليل الأثري"
            latitudeInput.hint = "خط العرض Latitude"
            longitudeInput.hint = "خط الطول Longitude"
            radiusInput.hint = "نصف قطر التحليل بالمتر"
            analyzeButton.text = "بدء التحليل"
            languageButton.text = "English"
        } else {
            title.text = "TQ Archaeology"
            subtitle.text = "Archaeological Analysis"
            latitudeInput.hint = "Latitude"
            longitudeInput.hint = "Longitude"
            radiusInput.hint = "Analysis radius in meters"
            analyzeButton.text = "Start Analysis"
            languageButton.text = "العربية"
        }

        resultText.text = ""
    }
}
