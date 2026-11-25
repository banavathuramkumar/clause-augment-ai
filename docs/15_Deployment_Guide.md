# Milestone 15: Deployment Guide & Ngrok Tunneling

## 1. Local Production Deployment

### 1.1 Backend Service
```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Launch production server via uvicorn
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --workers 2
```

### 1.2 Frontend Production Build
```bash
cd frontend
npm install
npm run build
# Serve the compiled static assets
npx serve -s dist -l 3000
```

---

## 2. Public Tunneling via Ngrok
To share the running application publicly:

```bash
# 1. Install Ngrok CLI (or use chocolatey / brew)
# 2. Expose the frontend port (3000 or 5173)
ngrok http 3000

# 3. If accessing backend API independently
ngrok http 8000
```
Forwarding URL (e.g., `https://xyz.ngrok-free.app`) provides immediate public access for live demonstrations and remote portfolio reviews.
