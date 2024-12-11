from pydantic import BaseModel, Field, SerializeAsAny  # type: ignore
from typing import Literal, Optional, Union, Annotated
from enum import Enum


class Document(BaseModel):
    """Represents a document used as a ground truth when generating tests."""

    # url: Optional[str] = None
    filepath: str
    title: Optional[str] = None
    content: bytes | str
    content_type: Optional[str] = "application/octet-stream"


class QuestionWithReason(BaseModel):
    reason: str = Field(
        description="Used for explaining the reasoning behind the question.",
        default="<Placeholder for reasoning>",
    )
    question: str = Field(description="The question text.")
    reference_answer: str = Field(description="The expected response.", default="")


class FilterConfig(BaseModel):
    """Configuration for filtering questions."""

    remove: list[str] = Field(
        description="A list of criteria under which to remove questions."
    )
    keep: list[str] = Field(
        description="A list of criteria under which to keep questions."
    )


class Variant(BaseModel):
    """A single way to vary question generation that can be used to express something like 'a typo occurs in 10% of questions'."""

    weight: float = Field(
        description="The weight of the variant in the distribution of questions.",
        default=1.0,
    )
    description: str = Field(description="A description of the variant.")


class VariantConfig(BaseModel):
    """Configuration for varying the question generation process."""

    name: str = Field(
        description="The name of the variant configuration.", default="default"
    )
    mode: Literal["generation", "rewording"] = Field(
        description="Determines if the variant is applied in the initial generation phase or later during rewording.",
        default="generation",
    )
    variants: list[Variant] = Field(
        description="A list of variants to use in the question generation process."
    )
    count: int = Field(
        description="The number of variants that are drawn for each question. Defaults to 1.",
        default=1,
    )


class TagConfig(BaseModel):
    """Configuration for skipping or only including documents with certain tags."""

    skip_tags: list[str] = Field(
        description="Documents with these tags will be skipped.",
        default=[],
    )
    keep_tags: list[str] = Field(
        description="If provided, only documents with these tags will be used.",
        default=[],
    )


class ModelProvider(str, Enum):
    ANY = "any"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    LOCAL = "local"


class QuestionGeneratorArgs(BaseModel):
    question_limit: int = Field(description="The number of questions to generate")
    provider: ModelProvider = Field(
        description="The model provider to use for generating and filtering questions. If set to 'any', the system will choose the best model based on internal testing.",
        default=ModelProvider.ANY,
    )
    filter_config: FilterConfig | None = Field(
        description="Configuration for filtering questions after generation.",
        default=None,
    )
    variants: list[VariantConfig] = Field(
        description="A list of ways to vary the question generation process.",
        default=[],
    )
    tags: TagConfig | None = Field(
        description="Configuration for skipping or only including documents with certain tags.",
        default=None,
    )


class SimpleQuestionGeneratorArgs(QuestionGeneratorArgs):
    question_type: Literal["SimpleQuestion"] = (
        "SimpleQuestion"  # Type discriminator used for deserialization. Do not change.
    )
    temperature: float | None = Field(
        description="The temperature to use when generating questions", default=None
    )
    positive_examples: list[QuestionWithReason] = Field(
        description="A list of few-shot examples of good questions to help guide the question generation"
    )
    negative_examples: list[QuestionWithReason] = Field(
        description="A list of few-shot examples of poorly phrased or incorrect questions to help guide the question generation",
        default=[],
    )
    extra_criteria: list[str] = Field(
        description="A list of extra criteria to evaluate the quality of the generated questions.",
        default=[],
    )


class HowToSimpleQuestionGeneratorArgs(QuestionGeneratorArgs):
    question_type: Literal["HowToSimpleQuestion"] = (
        "HowToSimpleQuestion"  # Type discriminator used for deserialization. Do not change.
    )
    temperature: float | None = Field(
        description="The temperature to use when generating questions", default=None
    )
    positive_examples: list[QuestionWithReason] = Field(
        description="A list of few-shot examples of good questions to help guide the question generation"
    )
    negative_examples: list[QuestionWithReason] = Field(
        description="A list of few-shot examples of poorly phrased or incorrect questions to help guide the question generation",
        default=[],
    )
    extra_criteria: list[str] = Field(
        description="A list of extra criteria to evaluate the quality of the generated questions.",
        default=[],
    )


class HallucinationInducingQuestionGeneratorArgs(QuestionGeneratorArgs):
    question_type: Literal["HallucinationInducing"] = (
        "HallucinationInducing"  # Type xdiscriminator used for deserialization. Do not change.
    )
    temperature: float | None = Field(
        description="The temperature to use when generating questions", default=None
    )
    positive_examples: list[QuestionWithReason] = Field(
        description="A list of few-shot examples of good questions to help guide the question generation"
    )
    negative_examples: list[QuestionWithReason] = Field(
        description="A list of few-shot examples of poorly phrased or incorrect questions to help guide the question generation",
        default=[],
    )
    extra_criteria: list[str] = Field(
        description="A list of extra criteria to evaluate the quality of the generated questions.",
        default=[],
    )


class LinkedTopicQuestionGeneratorArgs(QuestionGeneratorArgs):
    question_type: Literal["LinkedTopic"] = (
        "LinkedTopic"  # Type xdiscriminator used for deserialization. Do not change.
    )
    temperature: float | None = Field(
        description="The temperature to use when generating questions", default=None
    )
    positive_examples: list[QuestionWithReason] = Field(
        description="A list of few-shot examples of good questions to help guide the question generation"
    )
    negative_examples: list[QuestionWithReason] = Field(
        description="A list of few-shot examples of poorly phrased or incorrect questions to help guide the question generation",
        default=[],
    )
    extra_criteria: list[str] = Field(
        description="A list of extra criteria to evaluate the quality of the generated questions.",
        default=[],
    )


class HowToLinkedTopicQuestionGeneratorArgs(QuestionGeneratorArgs):
    question_type: Literal["HowToLinkedTopic"] = (
        "HowToLinkedTopic"  # Type xdiscriminator used for deserialization. Do not change.
    )
    temperature: float | None = Field(
        description="The temperature to use when generating questions", default=None
    )
    positive_examples: list[QuestionWithReason] = Field(
        description="A list of few-shot examples of good questions to help guide the question generation"
    )
    negative_examples: list[QuestionWithReason] = Field(
        description="A list of few-shot examples of poorly phrased or incorrect questions to help guide the question generation",
        default=[],
    )
    extra_criteria: list[str] = Field(
        description="A list of extra criteria to evaluate the quality of the generated questions.",
        default=[],
    )
    generator_population: int = Field(
        description="Internal parameter used to mutate the generator prompt. Must be at least one, defaults to 1.",
        ge=1,
        le=20,
        default=1,
    )


# This is a discriminated union. What we want is to have a list of question generator configs, and to be able to send that list from the client/cli to the server and have it correctly deserialize.
# Breaking it down:
#  - Union means the type GeneratorArgs can refer to EITHER SimpleQuestionGeneratorArgs or HallucinationInducingQuestionGeneratorArgs
#  - When deserializing one of these GeneratorArgs over the wire, look at the question_type field to determine which of the two we're currently deserializing. It's a constant with a different value for the two classes (SimpleQuestion or HallucinationInducing)
#  - The SerializeAsAny is just there to suppress some warnings caused by a bug in pydantic.
GeneratorArgs = SerializeAsAny[
    Annotated[
        Union[
            SimpleQuestionGeneratorArgs,
            HallucinationInducingQuestionGeneratorArgs,
            LinkedTopicQuestionGeneratorArgs,
            HowToLinkedTopicQuestionGeneratorArgs,
            HowToSimpleQuestionGeneratorArgs,
        ],
        Field(discriminator="question_type"),
    ]
]


class HyperlinkTaskConfig(BaseModel):
    task_type: Literal["Hyperlink"] = "Hyperlink"


class ReferenceLinkTaskConfig(BaseModel):
    task_type: Literal["ReferenceLink"] = "ReferenceLink"


KbJobArgs = SerializeAsAny[
    Annotated[
        Union[
            HyperlinkTaskConfig,
            ReferenceLinkTaskConfig,
        ],
        Field(discriminator="task_type"),
    ]
]


class QuestionGenerationConfig(BaseModel):
    """Root configuration object for generating questions."""

    name: str = Field(
        description="Friendly name for the configuration used in logging, error reporting and the UI."
    )
    knowledge_bases: list[str] = Field(
        description="List of knowledge bases to use for generating questions. Uses knowledge base UUIDs."
    )
    question_configs: list[GeneratorArgs] = Field(  # type: ignore
        description="List of question generator configurations."
    )
