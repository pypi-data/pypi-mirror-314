from haizelabs_api.types.judge_call_params import (
    ContentTestContentInputOutputMessage,
)
from typing import Literal, Optional, List, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

import contextvars
import uuid
import json

AddType = Literal["INPUT", "OUTPUT"]


class Message(BaseModel):
    role: Literal["assistant", "user", "tool"]
    content: str
    name: Optional[str]


class SpanType(str, Enum):
    JUDGE = "JUDGE"
    APP = "APP"
    MODEL = "MODEL"
    FUNCTION = "FUNCTION"
    SCORER = "SCORER"


class EvaluatorResult(BaseModel):
    name: Optional[str] = None
    label: Optional[str] = None
    score: float


class LogBase(BaseModel): ...


# TODO: confirm that this works with new content objects
class Content(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    time: datetime = Field(default_factory=lambda: datetime.now())
    user_id: Optional[str] = None

    input_messages: Optional[List[ContentTestContentInputOutputMessage]] = Field(
        default_factory=list
    )
    output_messages: Optional[List[ContentTestContentInputOutputMessage]] = Field(
        default_factory=list
    )

    input_detections: Optional[List[EvaluatorResult]] = Field(default_factory=list)
    output_detections: Optional[List[EvaluatorResult]] = Field(default_factory=list)

    content_group_ids: Optional[List[str]] = Field(default_factory=list)

    start: Optional[datetime] = Field(default_factory=lambda: datetime.now())
    end: Optional[datetime] = Field(default_factory=lambda: datetime.now())


class Span(LogBase):
    name: str = None
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    trace_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    parent_id: str = None
    user_id: Optional[str] = None

    caller_id: Optional[str] = None

    content: Optional[Content] = None

    span_type: Optional[SpanType] = SpanType.APP

    start: datetime = Field(default_factory=lambda: datetime.now())
    end: datetime = Field(default_factory=lambda: datetime.now())

    metadata: Optional[Dict[str, Any]] = {}
    tags: Optional[Dict[str, Any]] = {}

    _context_token: Optional[contextvars.Token] = None

    def get_content(self):
        if not self.content:
            self.content = Content(
                id=self.id,
                time=self.start,
                start=self.start,
                end=self.end,
                user_id=self.user_id,
            )
        return self.content

    def set_input(self, input: Any, role: str = "user"):
        content = self.get_content()
        content.input_messages.append({"role": role, "content": json.dumps(input)})

    def set_output(self, output: Any, role: str = "user"):
        content = self.get_content()
        content.output_messages.append({"role": role, "content": json.dumps(output)})

    def add_evaluation(
        self,
        score: float,
        name: Optional[str] = None,
        label: Optional[str] = None,
        type: AddType = "INPUT",
    ):
        content = self.get_content()
        data = {"name": name, "label": label, "score": score}
        if type == "INPUT":
            content.input_evaluations.append(EvaluatorResult(**data))
        else:
            content.output_evaluations.append(EvaluatorResult(**data))

    def add_tag(self, key: str, value: Any):
        self.tags[key] = value

    def add_metadata(self, key: str, value: Any):
        self.metadata[key] = value

    def set_token(self, token: contextvars.Token):
        self._context_token = token

    def get_token(self):
        return self._context_token

    def reset_token(self):
        self._context_token = None

    def create_child(self, name: str):
        return Span(
            name=name,
            trace_id=self.trace_id,
            parent_id=self.id,
        )

    def begin(self):
        self.start = datetime.now()

    def finish(self):
        self.end = datetime.now()


class Trace(LogBase):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    name: Optional[str] = None
    start: datetime = Field(default_factory=lambda: datetime.now())
    end: datetime = Field(default_factory=lambda: datetime.now())
    user_id: Optional[str] = None

    root_content: Optional[Content] = None

    @staticmethod
    def create_from_span(span: Span):
        return Trace(
            id=span.trace_id,
            start=span.start,
            name=span.name,
            end=span.end,
            user_id=span.user_id,
            root_content=span.content,
        )
