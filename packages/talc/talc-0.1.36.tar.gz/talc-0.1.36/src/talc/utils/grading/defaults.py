from talc.grading import (
    GradingSet,
    GraderConfig,
    FactualityGraderConfig,
    FewShotConfig,
    FailIfGraderConfig,
    GradingPipeline,
    ScoringRule,
)

DEFAULT_FACTUALITY_GRADER_CONFIG = FactualityGraderConfig(
    grader="FactualityGrader",
    config_name="DefaultFactualityGraderConfig",
    description="The default configuration for the factuality grader.",
    few_shot_examples=[
        FewShotConfig(
            question="What command is used to install the Python SDK for modelscope?",
            correct_answer="The Python SDK for modelscope can be installed using `pip install modelscope` command.",
            user_answer="pip install modelscope",
            grade="PASS",
            reason="The user answer specifies the correct command.",
        ),
    ],
    additional_pass_criteria=[
        "It's ok if the user response includes extra information as long as it does not contradict the reference answer.",
        "If the expected answer is 'I don't know' or similar, then any answer that expresses a definite answer should be considered a failing grade.",
    ],
    additional_fail_criteria=[],
)

DEFAULT_SOURCE_CONTENT_FACTUALITY_GRADER_CONFIG = FactualityGraderConfig(
    grader="SourceContentFactualityGrader",
    config_name="DefaultSourceContentFactualityGraderConfig",
    description="The default configuration for the source content factuality grader.",
    few_shot_examples=[
        FewShotConfig(
            question="What command is used to install the Python SDK for modelscope?",
            correct_answer="The Python SDK for modelscope can be installed using `pip install modelscope` command.",
            user_answer="pip install modelscope",
            grade="PASS",
            reason="The user answer specifies the correct command.",
        ),
    ],
    additional_pass_criteria=[
        "It's ok if the user response includes extra information as long as it does not contradict the source contents.",
    ],
    additional_fail_criteria=[],
)

DEFUALT_FAIL_IF_GRADER_CONFIG = FailIfGraderConfig(
    grader="FailIfGrader",
    config_name="DefaultFailIfGraderConfig",
    description="The default configuration for the fail-if grader.",
    fail_criteria=[
        "The AI responding breaks character by using phrases like 'as an AI agent' or similar.",
    ],
)

DEFAULT_GRADER_CONFIG = GradingPipeline(
    graders=[
        DEFAULT_FACTUALITY_GRADER_CONFIG,
    ],
    scoring_rules=[
        ScoringRule(
            graders=["DefaultFactualityGraderConfig"],
            level="fail",
            mode="require_all_pass",
        )
    ],
)
