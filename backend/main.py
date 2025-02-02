from fastapi import FastAPI
from pydantic import BaseModel

from rag import rag_pipeline

app = FastAPI()


class Question(BaseModel):
    question: str


class Answer(BaseModel):
    ansewr: str


@app.post("/submit")
def submit_question(question: Question):
    result = rag_pipeline.run(
        {
            "query_embedder": {"text": question.question},
            "prompt_builder": {"question": question.question},
        }
    )
    return result
