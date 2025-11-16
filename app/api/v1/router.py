from fastapi import APIRouter
from app.api.v1 import jobs  # Import the jobs.py router

# 1. Create the main v1 router
api_v1_router = APIRouter()

# 2. Include the 'jobs' router
# All routes from jobs.py will now be prefixed with '/jobs'
# The 'tags' will group them nicely in your /docs
api_v1_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])

# 3. As you add more resources, just import and include them here
# from . import users
# api_v1_router.include_router(users.router, prefix="/users", tags=["users"])