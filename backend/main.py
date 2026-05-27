from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import engine
from models import Base
from fastapi.responses import HTMLResponse
from database import SessionLocal
from models import Visit

from analytics import router as analytics_router
from groq import Groq
from dotenv import load_dotenv

import os

# ======================================================
# LOAD ENV
# ======================================================

load_dotenv()

# ======================================================
# FASTAPI APP
# ======================================================

app = FastAPI(
    title="Lahari Portfolio AI Assistant",
    description="AI assistant for Lahari M's engineering portfolio",
    version="1.0.0"
)
Base.metadata.create_all(bind=engine)
# ======================================================
# CORS
# ======================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(analytics_router)
# ======================================================
# GROQ CLIENT
# ======================================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ======================================================
# LOAD PORTFOLIO CONTEXT
# ======================================================

with open(
    "portfolio_context.txt",
    "r",
    encoding="utf-8"
) as file:

    portfolio_context = file.read()

# ======================================================
# REQUEST MODEL
# ======================================================

class ChatRequest(BaseModel):
    message: str

# ======================================================
# SYSTEM PROMPT
# ======================================================

SYSTEM_PROMPT = f"""
You are Lahari M's AI Portfolio Assistant.

Your role is to explain:
- backend engineering projects
- async systems
- workflow orchestration
- AI infrastructure
- retrieval systems
- deployment workflows
- reliability engineering
- engineering decisions
- operational backend systems

IMPORTANT RULES:
- Respond professionally and clearly.
- Keep answers concise but informative.
- Prioritize backend engineering depth.
- Use structured formatting.
- Use bullet points where useful.
- Never invent information.
- Only answer using the provided portfolio context.
- If information is unavailable, say:
"I don't have information about that currently."

When comparing projects:
- explain architecture complexity
- workflow orchestration
- reliability engineering
- backend depth
- operational complexity

When discussing strengths:
focus on:
- async systems
- workflow continuity
- backend reliability
- operational engineering
- queue orchestration
- fault isolation

PORTFOLIO CONTEXT:

{portfolio_context}
"""

# ======================================================
# ROOT ROUTE
# ======================================================

@app.get("/")
async def root():

    return {
        "status": "running",
        "service": "Lahari Portfolio AI Assistant",
        "backend": "FastAPI + Groq"
    }

# ======================================================
# HEALTH CHECK
# ======================================================

@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }

# ======================================================
# SUGGESTED QUESTIONS
# ======================================================

@app.get("/suggestions")
async def suggestions():

    return {
        "questions": [

            "Why does MedRoute use Redis queues?",

            "How does hospital rerouting work?",

            "What backend systems has Lahari built?",

            "What makes MedRoute technically strong?",

            "Explain the async worker architecture.",

            "What reliability systems are implemented?",

            "What did Lahari work on during her internship?",

            "Explain the Distributed Archive Platform.",

            "What are Lahari's strongest backend skills?",

            "How does the FSM workflow operate?",

            "How does failure recovery work in MedRoute?",

            "What deployment infrastructure has Lahari used?"
        ]
    }

# ======================================================
# CHAT ROUTE
# ======================================================

@app.post("/chat")
async def chat(req: ChatRequest):

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": req.message
                }
            ],

            temperature=0.3,
            max_tokens=700
        )

        reply = response.choices[0].message.content

        return {
            "success": True,
            "reply": reply
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
@app.get("/admin", response_class=HTMLResponse)

async def admin_dashboard():

    db = SessionLocal()

    visits = db.query(Visit).all()

    total_visits = len(visits)

    unique_sessions = len(
        set(v.session_id for v in visits)
    )

    pages = {}

    total_duration = 0

    for v in visits:

        pages[v.page] = pages.get(v.page, 0) + 1

        try:

            total_duration += int(
                v.duration.replace("s","")
            )

        except:
            pass

    avg_duration = 0

    if total_visits > 0:

        avg_duration = round(
            total_duration / total_visits,
            1
        )

    page_html = ""

    for page,count in pages.items():

        page_html += f"""
        <div class="page-card">
            <h3>{page}</h3>
            <p>{count} visits</p>
        </div>
        """

    recent_html = ""

    for visit in visits[-10:]:

        recent_html += f"""
        <tr>
            <td>{visit.page}</td>
            <td>{visit.duration}</td>
            <td>{visit.device[:40]}</td>
        </tr>
        """

    html = f"""

    <!doctype html>

    <html>

    <head>

    <title>Admin Dashboard</title>

    <style>

    *{{
        margin:0;
        padding:0;
        box-sizing:border-box;
    }}

    body{{
        background:#050816;
        color:white;
        font-family:Inter,sans-serif;
        padding:40px;
    }}

    h1{{
        margin-bottom:30px;
        font-size:2.2rem;
    }}

    .stats{{
        display:grid;
        grid-template-columns:
        repeat(auto-fit,minmax(220px,1fr));

        gap:20px;

        margin-bottom:40px;
    }}

    .card{{
        background:rgba(255,255,255,.05);

        border:
        1px solid rgba(255,255,255,.08);

        padding:24px;

        border-radius:20px;
    }}

    .card h2{{
        font-size:2rem;
        margin-bottom:10px;
    }}

    .card p{{
        color:#94a3b8;
    }}

    .pages{{
        display:grid;

        grid-template-columns:
        repeat(auto-fit,minmax(180px,1fr));

        gap:18px;

        margin-bottom:40px;
    }}

    .page-card{{
        background:rgba(255,255,255,.05);

        border:
        1px solid rgba(255,255,255,.08);

        padding:18px;

        border-radius:16px;
    }}

    .page-card h3{{
        margin-bottom:10px;
    }}

    table{{
        width:100%;

        border-collapse:collapse;

        margin-top:20px;
    }}

    th,td{{
        padding:16px;

        border-bottom:
        1px solid rgba(255,255,255,.08);

        text-align:left;

        font-size:14px;
    }}

    th{{
        color:#7dd3fc;
    }}

    </style>

    </head>

    <body>

    <h1>
    Portfolio Analytics Dashboard
    </h1>

    <div class="stats">

        <div class="card">
            <h2>{total_visits}</h2>
            <p>Total Visits</p>
        </div>

        <div class="card">
            <h2>{unique_sessions}</h2>
            <p>Unique Sessions</p>
        </div>

        <div class="card">
            <h2>{avg_duration}s</h2>
            <p>Average Time Spent</p>
        </div>

    </div>

    <h2 style="margin-bottom:20px;">
    Most Visited Pages
    </h2>

    <div class="pages">

    {page_html}

    </div>

    <h2>
    Recent Activity
    </h2>

    <table>

        <tr>
            <th>Page</th>
            <th>Duration</th>
            <th>Device</th>
        </tr>

        {recent_html}

    </table>

    </body>

    </html>

    """

    return html
# ======================================================
# RUN SERVER
# ======================================================

# Run using:
# uvicorn main:app --reload