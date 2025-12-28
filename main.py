from fastapi import FastAPI,Depends
from src.core.config import settings
import uvicorn
from src.api.users import user_router
from src.api.rooms import room_router
from src.api.dependencies import get_current_user
from src.models.user import User

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    
)

app.include_router(user_router)
app.include_router(room_router)


@app.get("/healthcheck")
async def health_check(current_user: User = Depends(get_current_user)):
    return {
        "status": "ok",
        "project_name": settings.PROJECT_NAME,
        "version": settings.VERSION
    }
    

    
if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)
    
    