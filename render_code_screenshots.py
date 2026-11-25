import asyncio
from playwright.async_api import async_playwright
import os

out_dir = r"c:\Users\HP\OneDrive\Desktop\Gen AI\docs\screenshots"
os.makedirs(out_dir, exist_ok=True)

html_templates = {
    "vscode_env.png": """
    <div style="background:#1e1e1e; color:#d4d4d4; font-family:Consolas, monospace; font-size:14px; padding:15px; border-radius:6px; width:750px;">
        <div style="background:#2d2d2d; padding:6px 12px; margin:-15px -15px 15px -15px; border-top-left-radius:6px; border-top-right-radius:6px; color:#cccccc; font-size:12px; display:flex; align-items:center;">
            <span style="height:10px; width:10px; background:#ff5f56; border-radius:50%; display:inline-block; margin-right:6px;"></span>
            <span style="height:10px; width:10px; background:#ffbd2e; border-radius:50%; display:inline-block; margin-right:6px;"></span>
            <span style="height:10px; width:10px; background:#27c93f; border-radius:50%; display:inline-block; margin-right:12px;"></span>
            <span>.env — ClauseAugment AI</span>
        </div>
        <div style="color:#6a9955;"># ClauseAugment AI - Environment Configuration</div>
        <div>HOST=0.0.0.0</div>
        <div>PORT=8000</div>
        <div>DATABASE_URL=sqlite:///backend/clause_augment.db</div>
        <div>LOG_LEVEL=INFO</div>
        <br>
        <div style="color:#6a9955;"># Google Gemini API Configuration (Optional)</div>
        <div><span style="color:#9cdcfe;">GEMINI_API_KEY</span>=<span style="color:#ce9178;">AIzaSyB3X9k...your_gemini_api_key_here</span></div>
        <div><span style="color:#9cdcfe;">GEMINI_MODEL_NAME</span>=<span style="color:#ce9178;">gemini-2.5-flash</span></div>
    </div>
    """,

    "terminal_setup.png": """
    <div style="background:#0c0c0c; color:#cccccc; font-family:Consolas, monospace; font-size:13px; padding:15px; border-radius:6px; width:750px;">
        <div style="background:#1f1f1f; padding:6px 12px; margin:-15px -15px 15px -15px; border-top-left-radius:6px; border-top-right-radius:6px; color:#ffffff; font-size:12px;">
            TERMINAL — PowerShell
        </div>
        <div><span style="color:#3b8eea;">PS C:\\Users\\HP\\OneDrive\\Desktop\\Gen AI&gt;</span> python -m venv venv</div>
        <div><span style="color:#3b8eea;">PS C:\\Users\\HP\\OneDrive\\Desktop\\Gen AI&gt;</span> .\\venv\\Scripts\\activate</div>
        <div><span style="color:#569cd6;">(venv)</span> <span style="color:#3b8eea;">PS C:\\Users\\HP\\OneDrive\\Desktop\\Gen AI&gt;</span> pip install -r backend/requirements.txt</div>
        <div style="color:#6a9955;">Successfully installed fastapi-0.115.0 uvicorn-0.31.0 scikit-learn-1.5.2 nltk-3.9.1 google-genai-0.1.1</div>
        <div><span style="color:#569cd6;">(venv)</span> <span style="color:#3b8eea;">PS C:\\Users\\HP\\OneDrive\\Desktop\\Gen AI&gt;</span> cd frontend; npm install</div>
        <div style="color:#6a9955;">added 142 packages, and audited 143 packages in 3s</div>
    </div>
    """,

    "vscode_app_py.png": """
    <div style="background:#1e1e1e; color:#d4d4d4; font-family:Consolas, monospace; font-size:13px; padding:15px; border-radius:6px; width:750px;">
        <div style="background:#2d2d2d; padding:6px 12px; margin:-15px -15px 15px -15px; border-top-left-radius:6px; border-top-right-radius:6px; color:#cccccc; font-size:12px; display:flex; align-items:center;">
            <span style="height:10px; width:10px; background:#ff5f56; border-radius:50%; display:inline-block; margin-right:6px;"></span>
            <span style="height:10px; width:10px; background:#ffbd2e; border-radius:50%; display:inline-block; margin-right:6px;"></span>
            <span style="height:10px; width:10px; background:#27c93f; border-radius:50%; display:inline-block; margin-right:12px;"></span>
            <span>backend/app/main.py</span>
        </div>
        <div><span style="color:#c586c0;">from</span> <span style="color:#4ec9b0;">fastapi</span> <span style="color:#c586c0;">import</span> FastAPI</div>
        <div><span style="color:#c586c0;">from</span> <span style="color:#4ec9b0;">fastapi.middleware.cors</span> <span style="color:#c586c0;">import</span> CORSMiddleware</div>
        <div><span style="color:#c586c0;">from</span> <span style="color:#4ec9b0;">app.api.routes</span> <span style="color:#c586c0;">import</span> dataset, augmentation, validation, training, evaluation</div>
        <br>
        <div>app = <span style="color:#4ec9b0;">FastAPI</span>(title=<span style="color:#ce9178;">"ClauseAugment AI"</span>, version=<span style="color:#ce9178;">"1.0.0"</span>)</div>
        <br>
        <div>app.include_router(dataset.router, prefix=<span style="color:#ce9178;">"/api"</span>)</div>
        <div>app.include_router(augmentation.router, prefix=<span style="color:#ce9178;">"/api"</span>)</div>
        <div>app.include_router(validation.router, prefix=<span style="color:#ce9178;">"/api"</span>)</div>
        <div>app.include_router(training.router, prefix=<span style="color:#ce9178;">"/api"</span>)</div>
        <div>app.include_router(evaluation.router, prefix=<span style="color:#ce9178;">"/api"</span>)</div>
    </div>
    """,

    "terminal_deploy.png": """
    <div style="background:#0c0c0c; color:#cccccc; font-family:Consolas, monospace; font-size:13px; padding:15px; border-radius:6px; width:750px;">
        <div style="background:#1f1f1f; padding:6px 12px; margin:-15px -15px 15px -15px; border-top-left-radius:6px; border-top-right-radius:6px; color:#ffffff; font-size:12px;">
            TERMINAL — Uvicorn & Ngrok
        </div>
        <div><span style="color:#3b8eea;">PS C:\\Users\\HP\\OneDrive\\Desktop\\Gen AI&gt;</span> python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload</div>
        <div style="color:#6a9955;">INFO:     Started server process [18828]</div>
        <div style="color:#6a9955;">INFO:     Waiting for application startup.</div>
        <div style="color:#6a9955;">INFO:     [ClauseAugment]: Loaded benchmark dataset 'Contract Clause Benchmark Dataset' (200 clauses).</div>
        <div style="color:#6a9955;">INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)</div>
        <br>
        <div><span style="color:#3b8eea;">PS C:\\Users\\HP\\OneDrive\\Desktop\\Gen AI&gt;</span> ngrok http 5173</div>
        <div style="color:#4ec9b0;">Session Status                online</div>
        <div style="color:#4ec9b0;">Account                       BANAVATHU RAMKUMAR (Plan: Free)</div>
        <div style="color:#4ec9b0;">Forwarding                    https://moodiness-escalate-wobbling.ngrok-free.dev -&gt; http://localhost:5173</div>
    </div>
    """
}

async def generate_images():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        for filename, html in html_templates.items():
            await page.set_content(f'<body style="margin:0; background:transparent; display:inline-block;">{html}</body>')
            elem = await page.query_selector("div")
            out_path = os.path.join(out_dir, filename)
            await elem.screenshot(path=out_path)
            print(f"Rendered: {out_path}")
        await browser.close()

asyncio.run(generate_images())
