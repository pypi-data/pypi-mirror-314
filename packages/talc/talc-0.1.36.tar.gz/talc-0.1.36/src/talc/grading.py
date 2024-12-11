from typing import Literal
from pydantic import BaseModel, ConfigDict, Extra, SerializeAsAny  # type: ignore


class TestCaseResponse(BaseModel):
    """Represents the results of running a single test case."""

    id: str
    response: str


class GraderConfig(BaseModel):
    """The basic configuration used to run a grader. Most graders will have additional configuration options derived from this class."""

    grader: str
    config_name: str
    description: str

    model_config = ConfigDict(
        extra="allow",  # type: ignore
    )


class ScoringRule(BaseModel):
    """Represents the rules used to take a list of grades and produce a final score."""

    graders: list[str]
    level: Literal["warn", "fail"]
    mode: Literal["allow_any_pass", "require_all_pass"]


class GradingPipeline(BaseModel):
    """Configures a pipeline of graders that should be run on a test case."""

    graders: list[SerializeAsAny[GraderConfig]]
    scoring_rules: list[ScoringRule]


class FewShotConfig(BaseModel):
    reason: str
    question: str
    correct_answer: str | None
    user_answer: str
    grade: str


class FactualityGraderConfig(GraderConfig):
    """Configuration for the factuality grader."""

    few_shot_examples: list[FewShotConfig]
    additional_pass_criteria: list[str]
    additional_fail_criteria: list[str]


class FailIfGraderConfig(GraderConfig):
    """Configuration for the grader that checks for explicitly disallowed cases. Passes if the response does not match any of the fail_criteria, fails if it does."""

    fail_criteria: list[str]
    """The criteria that, if met, will cause the grader to fail the test case. e.g, 'If the response contains 'as an AI language model'.'"""


class GradingSet(BaseModel):
    """Represents a set of test cases that should be graded, and the methods for grading them."""

    responses: list[TestCaseResponse]
    pipeline: GradingPipeline
