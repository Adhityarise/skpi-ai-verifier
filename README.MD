# 🎓 SKPI AI Verifier & Audit System

An AI-powered document verification system designed to automate and validate **Surat Keterangan Pendamping Ijazah (SKPI)** certificates for Indonesian higher education institutions. Built using a **Human-in-the-Loop (HITL)** architecture powered by Vision LLMs and structured JSON extraction.

---

## 📌 Executive Summary

Manual verification of student achievement certificates is a major administrative bottleneck in universities. **SKPI AI Verifier** solves this by introducing a dual-stage auditing pipeline:

1. **Automated Vision Extraction (80% Workload):** Validates document authenticity, recipient matching, issuing entities, signatures, and compulsory criteria (e.g., required internship hours or exam scores).
2. **Human-in-the-Loop Safeguard (20% Workload):** Flags low-confidence extractions, missing mandatory fields, or degraded document quality for review within the app. Routing flagged items to an actual admin queue is on the roadmap (see below).

---

## 🚀 Key Features

* **Multimodal Document Parsing:** Processes student certificates directly from image files (`.jpg`, `.jpeg`, `.png`) using Gemini Vision AI.
* **Structured XML Prompting:** Enforces strict compliance with institutional guidelines using structured XML prompt wrappers.
* **Guaranteed JSON Schema:** Forces LLM responses into strict JSON for seamless API integration and database persistence.
* **Smart Exception Handling: Automatically detects anomalies, missing mandatory attributes (e.g., missing internship duration), or blurry images and surfaces them as MANUAL_REVIEW in the app.
* **Environment Isolation:** Zero hardcoded API credentials; utilizes `.env` management and `.gitignore` protocols.

---

## 🏗 System Architecture

```text
[ Mahasiswa ] ───> Upload certificate (JPG/PNG)
                          │
                          ▼
                 [ Streamlit Engine ]
                          │
         (Structured Prompt + Image Base64)
                          │
                          ▼
               [ Vision LLM Engine ]
                          │
              ┌───────────┴───────────┐
              │ Output: JSON Schema   │
              └───────────┬───────────┘
                          │
       ┌──────────────────┴──────────────────┐
       │                                     │
       ▼                                     ▼
[ Status: AUTO_APPROVE ]           [ Status: MANUAL_REVIEW ]
• Name Matched                     • Low Confidence Score
• Required Fields Valid            • Missing Duration/Signatures
• High Confidence Score (>90%)     • Image Blur / Anomaly
       │                                     │
       ▼                                     ▼
(Included in SKPI)                 (Flagged for Review — admin routing: planned)
```

## 🛠 Tech Stack

Frontend & Dashboard: Streamlit

Backend Runtime: Python 3.10+

AI Engine: Google Gemini Vision API (gemini-3.5-flash-lite)

Environment & Config: python-dotenv, Pillow

## 📦 Installation & Setup

1. Prerequisites

Ensure you have Python 3.10 or higher installed on your local machine.

2. Clone Repository


git clone [https://github.com/Adhityarise/skpi-ai-verifier.git](https://github.com/your-username/skpi-ai-verifier.git)

cd skpi-ai-verifier

3. Setup Virtual Environment (Optional but Recommended)

python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

4. Install Dependencies

pip install -r requirements.txt


5. Environment Configuration
Create a .env file in the project root directory and insert your Gemini API Key:

Code:
GEMINI_API_KEY="your_API_key"

1. Run Application

streamlit run app.py

## 📊 Sample Extraction Payload (JSON)
``` JSON
{
  "is_name_matched": true,
  "confidence_score": 0.98,
  "category": "achievements",
  "extracted_data": {
    "recipient_name": "Budi",
    "activity_title": "JUARA 2 Business plan competition",
    "issuing_institution": "HIMA",
    "issue_date": "2020-12-24",
    "rank_or_role": "Lead Team",
    "duration_hours": null,
    "score_or_grade": null
  },
  "status": "AUTO_APPROVE",
  "flag_reason": null
}
```
## 🛣 Future Roadmap
[ ] Anthropic Claude 3.5 Sonnet Integration for multi-page PDF analysis.

[ ] Database integration (PostgreSQL / Supabase) for student audit trails.

[ ] Admin verification dashboard for MANUAL_REVIEW queue management.

## 📄 License
This project is open-source and available under the MIT License.

## 🧑‍🦰 About

Version app : 1.0
By Adhityarise
