from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# Import API routers
from backend.app.api import branding, content, sentiment, summarize, style
from backend.app.config import settings


app = FastAPI(
    title="BizForge API",
    description="AI-powered branding and content generation",
    version="1.0.0"
)

# -----------------------------
# CORS Middleware
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "api_keys_configured": bool(
            settings.GROQ_API_KEY and settings.HF_API_KEY
        )
    }


# -----------------------------
# Register Routers
# -----------------------------
app.include_router(branding.router, prefix="/branding", tags=["Branding"])
app.include_router(content.router, prefix="/content", tags=["Content"])
app.include_router(sentiment.router, prefix="/sentiment", tags=["Sentiment"])
app.include_router(summarize.router, prefix="/summarize", tags=["Summarize"])
app.include_router(style.router, prefix="/style", tags=["Style System"])
