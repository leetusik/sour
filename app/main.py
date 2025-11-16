import logging.config
from contextlib import asynccontextmanager  # 1. Import the context manager
from fastapi import FastAPI
from app.api.v1.router import api_v1_router
from app.logging_config import LOGGING_CONFIG

# Apply the logging configuration
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("app.main")


# --- 2. Define the new lifespan manager ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on "startup"
    logger.info("--- Application Startup ---")
    yield
    # Code to run on "shutdown"
    logger.info("--- Application Shutdown ---")


# --- 3. Create the app and pass the lifespan ---
app = FastAPI(
    title="Sour API",
    description="API for the Sour project",
    version="1.0.0",
    lifespan=lifespan,  # <-- Register the lifespan here
)

# Include the v1 router
app.include_router(api_v1_router, prefix="/api/v1")

# --- 4. The old @app.on_event methods are now deleted ---


# Keep your health check
@app.get("/health", tags=["health"])
async def health_check():
    logger.debug("Health check requested")
    return {"status": "OK"}
