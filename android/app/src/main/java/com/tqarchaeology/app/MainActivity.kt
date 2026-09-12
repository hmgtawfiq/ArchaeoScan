package com.tqarchaeology.app

import android.os.Bundle
import android.view.Gravity
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private var arabic = false

    private lateinit var title: TextView
    private lateinit var subtitle: TextView
    private lateinit var analyzeButton: Button
    private lateinit var languageButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            setPadding(48, 48, 48, 48)
        }

        title = TextView(this).apply {
            text = "TQ Archaeology"
            textSize = 30f
            gravity = Gravity.CENTER
        }

        subtitle = TextView(this).apply {
            text = "Archaeological Analysis"
            textSize = 18f
            gravity = Gravity.CENTER
            setPadding(0, 16, 0, 48)
        }

        analyzeButton = Button(this).apply {
            text = "Start Analysis"
            textSize = 16f

            setOnClickListener {
                if (arabic) {
                    subtitle.text =
                        "أدخل الإحداثيات لبدء التحليل الأثري."
                } else {
                    subtitle.text =
                        "Enter coordinates to begin archaeological analysis."
                }
            }
        }

        languageButton = Button(this).apply {
            text = "العربية"
            textSize = 15f

            setOnClickListener {
                arabic = !arabic
                updateLanguage()
            }
        }

        root.addView(
            title,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            )
        )

        root.addView(
            subtitle,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            )
        )

        root.addView(
            analyzeButton,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            )
        )

        root.addView(
            languageButton,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            )
        )

        setContentView(root)
    }

    private fun updateLanguage() {
        if (arabic) {
            title.text = "TQ Archaeology"
            subtitle.text = "التحليل الأثري"
            analyzeButton.text = "بدء التحليل"
            languageButton.text = "English"
        } else {
            title.text = "TQ Archaeology"
            subtitle.text = "Archaeological Analysis"
            analyzeButton.text = "Start Analysis"
            languageButton.text = "العربية"
        }
    }
}
