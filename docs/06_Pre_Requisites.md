# Milestone 06: Pre-Requisites and Environment Setup

## 1. System Requirements
- **Operating System**: Windows 10/11, macOS, or Linux.
- **Python**: Version 3.10+ (tested on Python 3.11 and 3.14).
- **Node.js**: Version 18.0+ (tested on Node.js v22.19.0).
- **Package Managers**: `pip` and `npm`.

---

## 2. Backend Setup Instructions
```bash
# 1. Navigate to the project root
cd "c:\Users\HP\OneDrive\Desktop\Gen AI"

# 2. Install backend dependencies
pip install fastapi uvicorn pydantic pandas numpy scikit-learn nltk imbalanced-learn openpyxl google-genai sqlalchemy pytest httpx

# 3. Configure environment variables
# Create .env file with:
# GEMINI_API_KEY=your_optional_api_key_here
# GEMINI_MODEL_NAME=gemini-2.5-flash

# 4. Start the FastAPI backend server
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 3. Frontend Setup Instructions
```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Build or run development server
npm run dev
# Or build for production:
npm run build
```
Access the application at `http://localhost:5173` or `http://localhost:3000`.
