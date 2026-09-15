from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.query import router
from app.core.config import settings
from app.services.retrieval import Retriever
from app.services.generation import Generator


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Loading vector store...")

    app.state.retriever = Retriever(
        settings.vector_store_path
    )

    print("Initializing Groq client...")

    app.state.generator = Generator(
        api_key=settings.groq_api_key,
        model_name=settings.groq_model
    )

    print("Backend is ready.")

    yield


app = FastAPI(
    title="RAG Assistant API",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(router)