import os
import csv
from textwrap import indent, wrap
from typing import Literal
from termcolor import colored
from talc.talc_client import (
    GradedTestCase,
)
from talc.synthetic import Document
from talc.grading import ScoringRule
import requests
import aiohttp
from readabilipy import simple_json_from_html_string
from markdownify import markdownify as md


class Web:
    def __get_readable(self, url, html: str, use_readability: bool = True):
        """Parse HTML and return the knowledge base as a list of documents. Only used when as_bytes=False."""
        readable = simple_json_from_html_string(html, use_readability=use_readability)
        content = md(readable["plain_content"])
        document = Document(
            title=url,
            content=content,
            filepath=url,
            content_type="text/markdown",
        )
        return [document]

    def scrape(self, url: str, use_readability: bool = True) -> list[Document]:
        """Synchronously scrape a webpage and return a list of Documents."""
        # Note: Moving linking and chunking to later stages after kb upload.

        print("Scraping doc: " + url)
        response = requests.get(url)

        text: str = response.text

        raw_bytes: bytes = response.content
        if response.headers.get("Content-Type") == "text/html":
            title = simple_json_from_html_string(text, use_readability=use_readability)[
                "title"
            ]
        else:
            title = url
        document = Document(
            title=url,
            content=raw_bytes,
            filepath=url,
            content_type=response.headers.get(
                "Content-Type"
            ),  # Note: supabase storage saves text/html as text/plain for security reasons
        )
        return [document]

    async def ascrape(
        self, url: str, use_readability: bool = True, as_bytes=True
    ) -> list[Document]:
        """Asynchronously scrape a webpage and return a list of Documents."""
        # Note: Moving linking and chunking to later stages after kb upload.

        print("Scraping doc: " + url)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()

                text: str = await response.text()
                if as_bytes:
                    raw_bytes: bytes = await response.read()
                    title = simple_json_from_html_string(
                        text, use_readability=use_readability
                    )["title"]
                    document = Document(
                        title=url,
                        content=raw_bytes,
                        filepath=url,
                        content_type=response.headers.get(
                            "Content-Type"
                        ),  # Note: supabase storage saves text/html as text/plain for security reasons
                    )
                    return [document]
                else:
                    return self.__get_readable(
                        url, text, use_readability=use_readability
                    )


# Ugly terminal output functions
def print_single_case(case: GradedTestCase, color: Literal["red", "yellow", "green"]):

    try:
        terminal_width = max(60, os.get_terminal_size().columns)
    except OSError:
        terminal_width = 80

    response_wrapped = "\n".join(
        wrap(f"Response: {case.response}", terminal_width - 10)
    )
    expected_wrapped = "\n".join(
        wrap(f"Expected: {case.expected_response}", terminal_width - 10)
    )
    question_wrapped = "\n".join(
        wrap(f"{case.id}: {case.question}\n", terminal_width - 10)
    )

    print(colored(question_wrapped, color, attrs=["bold"]))
    print(indent(response_wrapped, "\t"))
    print(indent(expected_wrapped, "\t"))
    for grade in case.grades:
        if grade.score >= 1:
            continue
        else:
            grader_color = color
        grade_wrapped = "\n".join(
            wrap(
                f"{grade.grader} {'PASS' if grade.score >= 1.0 else 'FAIL'}: {grade.reason}",
                terminal_width - 10,
            )
        )
        print(colored(grade_wrapped, grader_color))
    print("---------------------------------------------")


def get_failures_and_warnings(
    test_cases: list[GradedTestCase], scoring_rules: list[ScoringRule]
):

    failures = []
    warnings = []

    # Now we need to loop through the rules defined in the scoring rules and
    # determine which cases need to be considered failures vs warnings.
    # This is ugly because it needs to support "any" and "all" scoring.
    for test_case in test_cases:
        for scoring_rule in scoring_rules:
            # determine if the test case has grades for all of the graders for this rule
            eligible = all(
                [
                    any(map(lambda x: x.grader == grader, test_case.grades))
                    for grader in scoring_rule.graders
                ]
            )
            if eligible and scoring_rule.mode == "allow_any_pass":
                all_fail = all(
                    [
                        all(
                            map(
                                lambda x: x.grader != grader or x.score < 1,
                                test_case.grades,
                            )
                        )
                        for grader in scoring_rule.graders
                    ]
                )
                if all_fail:
                    if scoring_rule.level == "fail":
                        failures.append(test_case)
                    elif scoring_rule.level == "warn":
                        warnings.append(test_case)
            elif eligible and scoring_rule.mode == "require_all_pass":
                any_fail = any(
                    [
                        any(
                            map(
                                lambda x: x.grader == grader and x.score < 1,
                                test_case.grades,
                            )
                        )
                        for grader in scoring_rule.graders
                    ]
                )
                if any_fail:
                    if scoring_rule.level == "fail":
                        failures.append(test_case)
                    elif scoring_rule.level == "warn":
                        warnings.append(test_case)

    return failures, warnings


def remove_invalid_uft8(text: str) -> str:
    return text.encode("utf-8", "ignore").decode("utf-8")
