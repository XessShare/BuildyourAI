"""
HexaHub MVP Backend
Self-hosted AI Workspace Platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="HexaHub API",
    description="Self-hosted AI Workspace Platform - MVP",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus Metrics
Instrumentator().instrument(app).expose(app)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "HexaHub API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint for deployment verification"""
    return {
        "status": "healthy",
        "service": "hexahub-backend",
        "database": "connected",  # TODO: Actual DB check
        "cache": "connected"  # TODO: Actual Redis check
    }


@app.get("/api/v1/agents")
async def list_agents():
    """List available AI agents"""
    return {
        "agents": [
            {
                "id": "content-creator",
                "name": "ContentCreatorAgent",
                "status": "available",
                "capabilities": ["video_scripts", "blog_posts", "social_media"]
            },
            {
                "id": "researcher",
                "name": "ResearcherAgent",
                "status": "available",
                "capabilities": ["web_research", "trend_analysis", "fact_checking"]
            },
            {
                "id": "analyst",
                "name": "AnalystAgent",
                "status": "available",
                "capabilities": ["data_analysis", "metrics", "reporting"]
            }
        ]
    }


@app.post("/api/v1/agents/{agent_id}/execute")
async def execute_agent(agent_id: str, task: dict):
    """Execute an agent task"""
    return {
        "task_id": "task_123",
        "agent_id": agent_id,
        "status": "queued",
        "message": "Task queued for execution"
    }


@app.get("/api/v1/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Get task execution status"""
    return {
        "task_id": task_id,
        "status": "completed",
        "progress": 100,
        "result": "Task completed successfully"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
