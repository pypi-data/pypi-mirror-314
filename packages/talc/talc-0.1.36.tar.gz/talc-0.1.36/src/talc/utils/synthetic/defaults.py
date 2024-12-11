from talc.synthetic import (
    QuestionWithReason,
    HallucinationInducingQuestionGeneratorArgs,
    SimpleQuestionGeneratorArgs,
    QuestionGenerationConfig,
)

DEFAULT_HALLUCINATION_ARGS = HallucinationInducingQuestionGeneratorArgs(
    question_limit=10,
    positive_examples=[
        QuestionWithReason(
            reason="The documentation describes ways to get the maximum and minimum values of a numpy array, but does not describe how to get the median value.",
            question="What numpy method of numpy.ndarray objects returns the indices of the median value along an axis?",
            reference_answer="There is no numpy.ndarray method that returns the indices of the median value along an axis.",
        ),
        QuestionWithReason(
            reason="The article describes the history of John D Rockefeller Sr. He died in 1937, so we can ask a question about something he did after that year in order to induce hallucination.",
            question="What job prompted John D Rockefeller Sr to move to Brazil in 1993?",
            reference_answer="John D Rockefeller Sr did not move to Brazil in 1993. He died in 1937.",
        ),
    ],
)

DEFAULT_SIMPLE_ARGS = SimpleQuestionGeneratorArgs(
    question_limit=10,
    positive_examples=[
        QuestionWithReason(
            question="Dippen Bay is an embayment along Kilbrannan Sound on the east coast of what peninsula?",
            reference_answer="Kintyre Peninsula",
            reason="The question is unambiguous and has a clear answer.",
        ),
        QuestionWithReason(
            question="Who currently owns the Bentley S1 Drophead Coupe orignally owned by John D Rockefeller Jr?",
            reference_answer="Henrik Frederiksen",
            reason="The question is specific and requires knowledge of a specific fact. It's not a generic question that could apply to any page, and has an unambiguous answer.",
        ),
    ],
)

DEFAULT_MID_SIMPLE_ARGS = SimpleQuestionGeneratorArgs(
    question_limit=10,
    positive_examples=[
        QuestionWithReason(
            question="A railway staton was opened by the Belfast and County Down Railway on June 3 1861. What was the original name of the station?",
            reference_answer="Groomsport and Bangor",
            reason="By avoiding using the current name of the station (but still providing enough context to identify the station), we can ask a question that is slightly more difficult than a simple question.",
        ),
        QuestionWithReason(
            question="In 1890, Grover Cleveland purchased a summer home. What event caused him to stop using the home?",
            reference_answer="The death of his daughter Ruth",
            reason="By refering to the topic indirectly (a summer home purchased in 1890, rather than the name of the home), we can make answering the question more difficult for models that are using retrieval-based methods.",
        ),
    ],
    extra_criteria=[
        "If there is a title of the page, avoid using it directly in the question. Instead, refer to the topic indirectly using other facts to specify it.",
    ],
)
