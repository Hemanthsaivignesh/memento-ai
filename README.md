# 🧠 Memento AI — Offline Personal Memory Engine

> **Build AI that runs anywhere.**
>
> A CPU-first, offline AI system that transforms unstructured human data into structured, searchable knowledge using local AI models.

---

## 🚀 Overview

Most modern AI assistants depend on cloud servers, expensive GPUs, and continuous internet connectivity.

This creates problems:

* Privacy risks for sensitive documents
* Dependency on cloud infrastructure
* No access during network failures
* Expensive AI computation

**Memento AI** solves this by bringing AI directly to the user's device.

It is an **offline-first personal intelligence engine** that converts:

* 📄 Documents
* 🖼 Images
* 🎙 Audio
* 📝 Text

into structured memories that can be searched and queried locally.

The entire AI pipeline runs on the user's machine using CPU-optimized models.

---

# 🎯 Problem Statement

Human knowledge is scattered across:

* Resumes
* Notes
* Reports
* Meeting records
* Personal documents
* Voice recordings

Traditional file storage only stores information.

Memento AI creates an intelligent memory layer that understands, organizes, and retrieves this information privately.

---

# 💡 Solution

Memento AI provides:

✅ Offline AI assistant
✅ Local document understanding
✅ Structured memory extraction
✅ Private knowledge storage
✅ Natural language querying
✅ CPU-first inference

The system converts unstructured input into structured data.

Example:

### Input

```
resume.pdf
```

### AI Processing

```
Document
    |
Text Extraction
    |
Entity Understanding
    |
Memory Creation
```

### Structured Output

```json
{
  "type": "experience",
  "title": "Machine Learning Internship",
  "organization": "ABC Technologies",
  "skills": [
    "Python",
    "Machine Learning"
  ],
  "year": "2025",
  "source": "resume.pdf"
}
```

---

# 🏗️ Architecture

```
                 User

                  |
                  v

          Web Application

                  |
                  v

              FastAPI

                  |
        --------------------

        |                  |

 Document Processing   AI Engine


        |                  |

 PDF/Image/Audio     llama.cpp


        |                  |

        -----------


          Memory Engine

                |

                v

            SQLite Database

                |

                v

          Local AI Retrieval

```

---

# ⚙️ Technology Stack

## Frontend

* React
* Vite
* Tailwind CSS

## Backend

* FastAPI
* Python
* SQLAlchemy

## AI Runtime

### Language Model

```
llama.cpp
```

Model:

```
GGUF Quantized Local LLM
```

Example:

```
Qwen2.5-3B-Instruct-GGUF
```

## Document Processing

| Input  | Technology        |
| ------ | ----------------- |
| PDF    | PyMuPDF           |
| Images | Tesseract OCR     |
| Audio  | Whisper.cpp       |
| Text   | Native processing |

## Storage

```
SQLite
```

All data remains on the local device.

---

# 🔒 Offline-First Design

Memento AI works without internet.

During operation:

```
Internet:
OFF

Cloud API Calls:
0

External Requests:
0

AI Inference:
Local

Storage:
Local SQLite
```

No dependency on:

❌ OpenAI API
❌ Anthropic API
❌ Cloud databases
❌ External AI services

---

# ⚡ CPU-First AI

Memento AI is designed for normal laptops.

Supported runtime:

```
llama.cpp
```

Advantages:

* GGUF quantized models
* Low memory usage
* CPU optimized inference
* No CUDA dependency

Target hardware:

```
Intel / AMD CPU laptops
8GB+ RAM
```

---

# 🧠 Core Features

## 1. Multi-Modal Data Ingestion

Supported:

* PDF documents
* Images
* Text files
* Audio recordings

---

## 2. Structured Memory Extraction

Transforms raw information into meaningful objects:

Examples:

* People
* Organizations
* Projects
* Skills
* Experiences
* Events

---

## 3. Local AI Chat

Users can ask:

```
What projects did I build?
```

Memento AI retrieves relevant memories and generates answers locally.

---

## 4. Source Attribution

Every response can reference the original data source.

Example:

```
You worked as an AI Intern at ABC Technologies.

Sources:
- resume.pdf
- internship_report.pdf
```

---

## 5. Private Knowledge Storage

All memories are stored locally.

Database:

```
SQLite
```

No user data leaves the machine.

---

# 📂 Project Structure

```
memento-ai/

├── backend/
│   ├── app/
│   ├── services/
│   ├── models/
│   └── database/

├── frontend/
│   ├── src/
│   └── components/

├── models/
│
├── docs/
│
├── tests/
│
├── README.md
├── LICENSE
└── .gitlab-ci.yml

```

---

# 🛠️ Installation

## Requirements

* Python 3.10+
* Node.js 18+
* CPU-based laptop (8GB+ RAM recommended)
* Tesseract OCR (for image text extraction)

---

## Quick Start

### 1. Clone Repository

```bash
git clone <repository-url>
cd memento-ai
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and update SECRET_KEY (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
```

### 4. Download AI Models

```bash
# Run from project root
python setup_models.py

# This will download:
# - Qwen2.5-3B-Instruct-GGUF (~1.9GB) for LLM inference
# - Whisper Base English (~140MB) for audio transcription
```

Alternatively, download manually:
- LLM: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF
- Whisper: https://huggingface.co/ggerganov/whisper.cpp

### 5. Install Tesseract OCR (Required for images)

**Windows:**
```bash
# Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
# Install and add to PATH
```

**Mac:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
```

### 6. Start Backend

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 8. Access Application

Open browser to: http://localhost:5173

---

## Troubleshooting

### Model Not Found Error

If you see "Model file not found", ensure:
1. You ran `python setup_models.py`
2. The `.env` file has correct `MODEL_PATH`
3. The model file exists in the `models/` directory

### Tesseract Not Found

If OCR fails, ensure Tesseract is installed and in your system PATH:
```bash
# Test installation
tesseract --version
```

### Port Already in Use

If port 8000 or 5173 is in use:
```bash
# Backend - use different port
uvicorn main:app --reload --port 8001

# Frontend - use different port
npm run dev -- --port 5174
```

---

# 🧪 Offline Demo

1. Disable Wi-Fi

2. Start Memento AI

3. Upload:

```
resume.pdf
project_report.pdf
notes.txt
```

4. AI processes locally:

```
Extracting text
       |
Understanding content
       |
Creating memories
       |
Saving locally
```

5. Ask:

```
What skills do I have?
```

Receive locally generated answer.

---

# 📊 Performance Goals

The system is optimized for:

| Metric        | Target        |
| ------------- | ------------- |
| Inference     | CPU only      |
| Memory        | Low footprint |
| Storage       | Local         |
| Network usage | 0 bytes       |
| AI Runtime    | llama.cpp     |

---

# 🌍 Multilingual Support

Planned support:

* English
* Telugu
* Hindi

All language processing will remain offline.

---

# 🔐 Privacy

Memento AI follows a local-first philosophy.

Your:

* Documents
* Memories
* Conversations

remain on your machine.

---

# 🤝 Contribution

Contributions are welcome.

Please read:

```
CONTRIBUTING.md
```

before submitting changes.

---

# 📜 License

This project is licensed under:

```
GNU Affero General Public License v3.0
```

A strong copyleft open-source license.

---

# 🏆 Hackathon Alignment

Memento AI satisfies:

✅ CPU-first inference
✅ Offline-first operation
✅ Local AI models
✅ Structured data extraction
✅ Multi-modal processing
✅ Open-source licensing

---

# 👨‍💻 Team

Built for:

**The CPU-First Hackathon**

Theme:

> Build AI that runs anywhere.
