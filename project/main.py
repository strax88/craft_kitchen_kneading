from fastapi import FastAPI

from core.api import router as health_router


from services.personality.api import UserRouter, GroupRouter, RoleRouter
from services.auth.api.routes import AuthRouter

app = FastAPI()  # lifespan=lifespan)
app.include_router(health_router)
app.include_router(UserRouter.router)
app.include_router(GroupRouter.router)
app.include_router(RoleRouter.router)
app.include_router(AuthRouter.router)
