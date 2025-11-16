from fastapi import FastAPI
from app.api.v1.router import api_v1_router  # 1. Import your main v1 router

# 2. Create the main app instance
app = FastAPI(
    title="Sour API",
    description="API for the Sour project",
    version="1.0.0"
)

# 3. Include the v1 router with the /api/v1 prefix
# All routes from api_v1_router will be prefixed with /api/v1
app.include_router(api_v1_router, prefix="/api/v1")

# 4. Keep your health check at the root, outside the API
@app.get("/health", tags=["health"])
async def health_check():
    """Performs a basic health check."""
    return {"status": "OK"}