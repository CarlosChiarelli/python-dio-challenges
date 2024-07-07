from fastapi import FastAPI

from workoutapi.routers import api_router
from fastapi_pagination import add_pagination

app = FastAPI(title="WorkoutApi")
app.include_router(api_router)
add_pagination(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
