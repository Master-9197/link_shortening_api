from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.authorization import router as links_router
from app.db.database import create_tables, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    print("Database reloaded!")
    yield
    print("Shutting down")
    
    
app = FastAPI(lifespan=lifespan, title="Link Shortening API")
app.include_router(links_router)


# async def main():
#     config = uvicorn.Config(
#         app="main:app",
#         log_level="info",
#         reload=True
#     )
    
#     server = uvicorn.Server(config)
#     await server.serve()
    
    
# if __name__ == "__main__":
#     asyncio.run(main())