from fastapi import APIRouter, Request

from app.schemas.query import QueryRequest, QueryResponse


router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "ok"
    }


@router.post("/query", response_model=QueryResponse)
def query(
    request: Request,
    data: QueryRequest
):

    retriever = request.app.state.retriever
    generator = request.app.state.generator

    documents = retriever.retrieve(
        data.question,
        k=2
    )

    answer, sources = generator.generate(
        data.question,
        documents
    )

    return QueryResponse(
        answer=answer,
        sources=sources
    )