from pydantic import BaseModel, Field


class SummarizeTopicResponse(BaseModel):
    message: str
    task_id: str = Field(None, example="9c5b78e2-15e4-413f-bc95-6f75d3ad3e48")


class ErrorResponse(BaseModel):
    error: str = Field(..., example="Summary not found.")


class SummaryData(BaseModel):
    _id: str
    topic_title: str = Field(..., example="Python Programming")
    summary: str = Field(..., example="Python is an interpreted, high-level and general-purpose programming language.")


class ReadSummaryResponse(BaseModel):
    summary: str = Field(..., example="Python is an interpreted, high-level and general-purpose programming language.")
