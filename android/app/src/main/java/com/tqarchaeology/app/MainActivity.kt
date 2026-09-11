package com.tqarchaeology.app

import android.os.Bundle
import android.view.Gravity
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            setPadding(48, 48, 48, 48)
        }

        val title = TextView(this).apply {
            text = "TQ Archaeology"
            textSize = 30f
            gravity = Gravity.CENTER
        }

        val subtitle = TextView(this).apply {
            text = "Archaeological Analysis"
            textSize = 18f
            gravity = Gravity.CENTER
            setPadding(0, 16, 0, 48)
        }

        val analyzeButton = Button(this).apply {
            text = "Start Analysis"
            textSize = 16f
            setOnClickListener {
                subtitle.text =
                    "Enter coordinates to begin archaeological analysis."
            }
        }

        val languageButton = Button(this).apply {
            text = "العربية"
            textSize = 15f
            setOnClickListener {
                title.text = "TQ Archaeology"
                subtitle.text = "التحليل الأثري"
                analyzeButton.text = "بدء التحليل"
                languageButton.text = "English"
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
}
