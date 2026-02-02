from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from microshop.core.config import settings
from microshop.api_v1 import router as router_v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


@app.get('/')
async def root():
    return {'message': 'FastAPI is up and running'}


if __name__ == '__main__':
    uvicorn.run('microshop.main:app', reload=True)
