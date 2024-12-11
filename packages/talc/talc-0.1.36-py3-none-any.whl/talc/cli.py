import asyncio
import csv as csvmod
import datetime
import json
import os
import pathlib
import random
from textwrap import indent
import time
from math import ceil
import urllib.parse

import click
from termcolor import colored

from talc.input_conversion import collect_input_specs, convert_inputs
from talc.knowledge_base import IngestionJobSpec, ScraperSpec
from talc.talc_client import (
    DatasetCreationJob,
    TalcClient,
    TestCaseWithRubric,
)
from talc.grading import (
    GradingSet,
    TestCaseResponse,
    ScoringRule,
    GradingPipeline,
)
from talc.synthetic import (
    QuestionGenerationConfig,
    Document,
    HyperlinkTaskConfig,
    ReferenceLinkTaskConfig,
)
from talc.utils.cli.config import load_config
from talc.utils.cli.io import (
    print_single_case,
    get_failures_and_warnings,
    Web,
    remove_invalid_uft8,
)
from talc.utils.cli.fileupload import parse_documents
from talc.utils.grading.defaults import DEFAULT_GRADER_CONFIG
from talc.utils.synthetic.defaults import (
    DEFAULT_HALLUCINATION_ARGS,
    DEFAULT_SIMPLE_ARGS,
    DEFAULT_MID_SIMPLE_ARGS,
)

talc_api_key: str | None = os.getenv("TALC_API_KEY", None)
talc_base_url: str = os.getenv("TALC_BASE_URL", "https://api.talcapi.com")


def poll_results(
    client: TalcClient,
    print_passed: bool,
    out_file: str | None,
    scoring_rules: list[ScoringRule],
):
    while True:
        run_info = client.get_results()
        print(f"Progress: {run_info.completion_progress * 100}%")
        if run_info.completion_progress >= 1:
            print("\n============================================================")
            print("Grading complete.")
            for key in run_info.grades.keys():
                print(f"{key}: {run_info.grades[key] * 100}%")

            print("============================================================\n")

            assert run_info.test_cases is not None

            failures, warnings = get_failures_and_warnings(
                run_info.test_cases, scoring_rules
            )

            passed = [
                case
                for case in run_info.test_cases
                if case not in failures and case not in warnings
            ]

            if out_file is not None:
                with open(
                    out_file, "w", newline="", encoding="utf-8", errors="replace"
                ) as csvfile:
                    writer = csvmod.writer(csvfile)
                    writer.writerow(
                        [
                            "id",
                            "question",
                            "expected_answer",
                            "result",
                            "failure",
                            "warning",
                            "grades",
                        ]
                    )
                    for case in run_info.test_cases:
                        writer.writerow(
                            [
                                case.id,
                                remove_invalid_uft8(case.question),
                                remove_invalid_uft8(case.expected_response),
                                remove_invalid_uft8(case.response),
                                True if case in failures else False,
                                True if case in warnings else False,
                                case.grades,
                            ]
                        )

            if print_passed and len(passed) > 0:
                print("=================PASSED=================")
                for case in passed:
                    print_single_case(case, "green")
            if len(warnings) > 0:
                print("=================WARNINGS=================")
                for warning in warnings:
                    print_single_case(warning, "yellow")
            if len(failures) > 0:
                print("=================FAILURES=================")
                for failure in failures:
                    print_single_case(failure, "red")
            if len(failures) > 0:
                return 1
            else:
                return 0

        time.sleep(2)


@click.group()
def evals():
    pass


@evals.command()
@click.option(
    "--api_key",
    default=talc_api_key,
    help="Talc API key. Can also be specified with the TALC_API_KEY environment variable.",
)
@click.option(
    "--in_file",
    prompt="Results CSV path",
    help="Path to CSV file to load results from. Columns should be 'id', 'result'. Header row is required and case sensitive.",
)
@click.option("--print_passed", is_flag=True, help="Print the passed test cases.")
@click.option("--out_file", default=None, help="Optionally save output as CSV.")
@click.option(
    "--config",
    default="all_passed",
    help="The name of the grader configuration to use.",
)
def eval(
    api_key: str | None,
    in_file: str,
    print_passed: bool,
    out_file: str,
    config: str,
):
    """Grade a test run from a CSV. Columns 'id' and 'result' are required, other columns will be ignored. CSV should have a header row."""

    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    client = TalcClient(api_key, talc_base_url)

    with open(in_file, newline="", encoding="utf-8", errors="replace") as csvfile:
        reader = csvmod.DictReader(csvfile)

        results = [
            TestCaseResponse(id=row["id"], response=row["result"]) for row in reader
        ]

    if config.endswith(".json"):
        loaded_config = GradingPipeline.parse_file(config)
    else:
        loaded_config = DEFAULT_GRADER_CONFIG

    grading_set = GradingSet(
        responses=results,
        pipeline=loaded_config,  # type: ignore
    )
    print("Grading " + str(len(results)) + " test cases.")
    run_info = client.start_run()
    client.submit_responses(grading_set)
    print("Submitted results. Beginning grading for run ID: " + run_info.id)

    res = poll_results(client, print_passed, out_file, loaded_config.scoring_rules)
    exit(res)


@evals.command()
@click.option(
    "--api_key",
    default=talc_api_key,
    help="Talc API key. Can also be specified with the TALC_API_KEY environment variable.",
)
@click.option("--run_id", prompt="Run ID", help="The ID of the run to get results for.")
@click.option("--print_passed", is_flag=True, help="Print the passed test cases.")
def get_results(api_key: str | None, run_id: str, print_passed: bool):
    """Get the grades for a test run."""

    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    client = TalcClient(api_key, talc_base_url, run_id)

    res = poll_results(client, print_passed, None, DEFAULT_GRADER_CONFIG.scoring_rules)

    exit(res)


@evals.command()
@click.option(
    "--api_key",
    default=talc_api_key,
    help="Talc API key. Can also be specified with the TALC_API_KEY environment variable.",
)
@click.option(
    "--csv",
    prompt="CSV path",
    help="Path to CSV file to upload. Column headers should be 'question' and 'expected_answer'. An optional source_text column can be included as well.",
)
@click.option("--name", prompt="Dataset name", help="The name of the dataset.")
def upload_manual_testset(api_key: str | None, csv: str, name: str):
    """Add a new dataset to the server."""

    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    client = TalcClient(api_key, talc_base_url)

    with open(csv, newline="", encoding="utf-8", errors="replace") as csvfile:
        reader = csvmod.DictReader(csvfile)

        try:
            dataset = [
                TestCaseWithRubric(
                    question=row["question"],
                    expected_response=row["expected_answer"],
                    scenario_data={},
                    id=None,
                    source_content=(
                        [row["source_text"]] if "source_text" in row else []
                    ),
                )
                for row in reader
            ]
        except KeyError:
            raise click.UsageError(
                "CSV file must have columns 'question' and 'expected_answer'. A header is required. An optional source_text column can be included."
            )

    dataset_id = client.upload_dataset(name, dataset)
    print(f"Dataset created with ID: {dataset_id}")


@evals.command()
@click.option(
    "--api_key",
    default=talc_api_key,
    help="Talc API key. Can also be specified with the TALC_API_KEY environment variable.",
)
@click.option(
    "--in_file",
    prompt="Input CSV path",
    help="Path to CSV file to upload. Columns should be 'question', 'expected_answer' and 'user_answer'. An optional source_text column can be included as well.",
)
@click.option(
    "--name",
    help="The name of the dataset.",
    default="Temp Dataset",
    required=False,
)
@click.option(
    "--out_file",
    help="Name of the output file",
    required=False,
)
@click.option("--print_passed", is_flag=True, help="Print the passed test cases.")
def upload_and_grade(
    api_key: str | None,
    in_file: str,
    name: str,
    out_file: str | None,
    print_passed: bool,
):
    """Upload a CSV with questions, reference answers, and user answers. Grade the user answers and return the grade. Column names must be 'question', 'expected_answer', and 'user_answer'."""

    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    client = TalcClient(api_key, talc_base_url)

    with open(in_file, newline="", encoding="utf-8", errors="replace") as csvfile:
        reader = csvmod.DictReader(csvfile)

        rows = [row for row in reader]

        assert "question" in rows[0]
        assert "expected_answer" in rows[0]
        assert "user_answer" in rows[0]

    dataset = [
        TestCaseWithRubric(
            question=row["question"],
            expected_response=row["expected_answer"],
            scenario_data={},
            id=None,
            source_content=([row["source_text"]] if "source_text" in row else []),
        )
        for row in rows
    ]

    dataset = client.upload_dataset(name, dataset)

    # Download the dataset to get the IDs
    data = client.get_dataset(dataset.id)

    # Map the IDs to the actual responses using the questions as a key

    id_map = {case.question: case.id for case in data}

    results = [
        TestCaseResponse(
            id=id_map[row["question"]],  # type: ignore
            response=row["user_answer"] if "user_answer" in row else "",
        )
        for row in rows
    ]

    # Create a run and submit the results
    run_info = client.start_run()

    # MAX TODO: Expose this config to the user
    grading_set = GradingSet(
        responses=results,
        pipeline=DEFAULT_GRADER_CONFIG,
    )
    client.submit_responses(grading_set)
    print("Submitted results. Beginning grading for run ID: " + run_info.id)

    res = poll_results(
        client, print_passed, out_file, DEFAULT_GRADER_CONFIG.scoring_rules
    )

    exit(res)


def poll_generation_job(
    client: TalcClient, dataset_job: DatasetCreationJob, suppress: bool
):
    lines_to_clear = 0

    def print_status():
        CLEAR_LINE = "\33[2K"
        MOVE_UP = "\033[A"
        MOVE_START = "\r"

        nonlocal lines_to_clear

        print((MOVE_UP + MOVE_START + CLEAR_LINE) * lines_to_clear, end="")

        to_output = ""
        to_output += (
            f"Dataset ID: {dataset_job.dataset_id}\n"
            f"Status: {dataset_job.status} (last updated {dataset_job.last_updated})\n"
        )
        if dataset_job.diagnostics is not None:
            if "kbs" in dataset_job.diagnostics:
                to_output += "KBs:\n"
                to_output += "".join(
                    [indent(kb, "\t") + "\n" for kb in dataset_job.diagnostics["kbs"]]
                )
            if "questions" in dataset_job.diagnostics:
                to_output += "Configs:\n"
                to_output += "".join(
                    [
                        indent(question, "\t") + "\n"
                        for question in dataset_job.diagnostics["questions"]
                    ]
                )

        print(to_output)
        lines_to_clear = to_output.count("\n") + 1

    while True:
        dataset_job = client.get_dataset_creation_job(dataset_job.id)
        not suppress and print_status()
        if dataset_job.status == "COMPLETE":
            break
        if dataset_job.status == "ERROR":
            print("Generation failed.")
            print(dataset_job.error)
            exit(1)
        time.sleep(2)


@evals.command()
@click.option(
    "--api_key",
    default=talc_api_key,
    help="Talc API key. Can also be specified with the TALC_API_KEY environment variable.",
)
@click.option("--out_file", default=None, help="Path to save the output to.")
@click.option(
    "--config",
    help="Path to a config file in JSON (simple) or python (advanced) format.",
    default=None,
    type=click.Path(exists=True),
)
@click.option(
    "--question_limit",
    default=10,
    type=click.INT,
    help="The number of questions to generate. If set in the config file, this will be ignored.",
)
@click.option(
    "--source",
    help="Input folder, single file path, or URL. Multiple allowed.",
    multiple=True,
    default=[],
)
@click.option(
    "--local_save",
    help="Should the knowledge base be saved locally?",
    default=True,
)
@click.option(
    "--suppress",
    help="Suppresses all terminal output besides dataset UUID.",
    default=False,
    is_flag=True,
)
def generate(
    api_key: str | None,
    config: str | None,
    out_file: str | None,
    question_limit: int,
    source: list[str],
    local_save: bool,
    suppress: bool,
):
    """Generate a dataset from a set of documents."""
    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    if out_file is None:
        out_file = (
            "questions_"
            + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            + ".csv"
        )

    client = TalcClient(api_key, talc_base_url)

    kb_override_id = None

    if len(source) > 0:
        documents = parse_documents(source)
        knowledge_base = client.upload_knowledge_base(
            documents,
            "questions_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"),
        )
        not suppress and print(f"Knowledge Base created with ID: {knowledge_base.id}")
        kb_override_id = knowledge_base.id

    if config is None:
        generation_configs = []

        s1 = DEFAULT_SIMPLE_ARGS.copy()
        s1.question_limit = ceil(question_limit / 3)
        generation_configs.append(s1)
        s2 = DEFAULT_MID_SIMPLE_ARGS.copy()
        s2.question_limit = ceil(question_limit / 3)
        generation_configs.append(s2)
        s3 = DEFAULT_HALLUCINATION_ARGS.copy()
        s3.question_limit = ceil(question_limit / 3)
        generation_configs.append(s3)

        if kb_override_id is None:
            raise click.UsageError(
                "No source documents provided. Please use the --source option or provide a config file."
            )

        generation_args = QuestionGenerationConfig(
            knowledge_bases=[kb_override_id],
            question_configs=generation_configs,
            name="questions_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"),
        )
    else:
        generation_args = load_config(config)
        if kb_override_id is not None:
            generation_args.knowledge_bases = [kb_override_id]
        elif len(generation_args.knowledge_bases) == 0:
            raise click.UsageError("No knowledge bases found in the config file.")
        if len(generation_args.question_configs) == 0:
            raise click.UsageError(
                "No question configurations found in the config file."
            )

    dataset_job = client.start_generate_dataset(
        config=generation_args,
    )

    poll_generation_job(client, dataset_job, suppress)

    not suppress and print(f"Dataset created with ID:")
    print(dataset_job.dataset_id)

    if not local_save:
        return

    dataset = client.get_dataset(dataset_job.dataset_id)
    with open(out_file, "w", newline="", encoding="utf-8", errors="replace") as csvfile:
        writer = csvmod.writer(csvfile)
        writer.writerow(["id", "question", "expected_answer", "sources", "type"])
        for case in dataset:
            generated_by: str = str(
                case.scenario_data.get("source_generator", "")
            ).removesuffix("QuestionGenerator")
            writer.writerow(
                [
                    case.id,
                    remove_invalid_uft8(case.question),
                    remove_invalid_uft8(case.expected_response),
                    case.scenario_data.get("source_document_urls", []),
                    generated_by,
                ]
            )

    not suppress and print(f"Dataset written to {out_file}")


@evals.command()
@click.option(
    "--api_key",
    default=talc_api_key,
    help="Talc API key. Can also be specified with the TALC_API_KEY environment variable.",
)
@click.option("--dataset", prompt="Dataset ID", help="The ID of the dataset to load.")
@click.option(
    "--out_file",
    help="Path to CSV file to save results to.",
)
@click.option(
    "--wait",
    is_flag=True,
    help="When set, waits for the dataset to finish generating and then downloads it.",
)
def get_dataset(dataset: str, api_key: str | None, out_file: str, wait: bool) -> None:
    """Download or pretty print a test dataset from the server."""

    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    client = TalcClient(api_key, talc_base_url)

    # If the dataset generation is not complete, print the status and exit
    dataset_job = client.get_dataset_status(dataset)
    if dataset_job.status != "COMPLETE":
        if wait:
            poll_generation_job(client, dataset_job, False)
        else:
            to_output = ""
            to_output += (
                f"Dataset ID: {dataset_job.dataset_id}\n"
                f"Status: {dataset_job.status} (last updated {dataset_job.last_updated})\n"
            )
            if dataset_job.diagnostics is not None:
                if "kbs" in dataset_job.diagnostics:
                    to_output += "KBs:\n"
                    to_output += "".join(
                        [
                            indent(kb, "\t") + "\n"
                            for kb in dataset_job.diagnostics["kbs"]
                        ]
                    )
                if "questions" in dataset_job.diagnostics:
                    to_output += "Configs:\n"
                    to_output += "".join(
                        [
                            indent(question, "\t") + "\n"
                            for question in dataset_job.diagnostics["questions"]
                        ]
                    )

            print(to_output)
            exit(0)

    data = client.get_dataset(dataset)
    with open(out_file, "w", newline="", encoding="utf-8", errors="replace") as csvfile:
        writer = csvmod.writer(csvfile)
        writer.writerow(["id", "question", "expected_answer", "sources", "type"])
        for case in data:
            generated_by: str = str(
                case.scenario_data.get("source_generator", "")
            ).removesuffix("QuestionGenerator")

            writer.writerow(
                [
                    case.id,
                    remove_invalid_uft8(case.question),
                    remove_invalid_uft8(case.expected_response),
                    case.scenario_data.get("source_document_urls", []),
                    generated_by,
                ]
            )


@evals.command
@click.option(
    "--api_key",
    default=talc_api_key,
    help="Talc API key. Can also be specified with the TALC_API_KEY environment variable.",
)
def list_datasets(api_key: str | None):
    """List the most recent datasets along with their status. Some of these may still be in the generation process."""
    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )
    client = TalcClient(api_key, talc_base_url)
    datasets_jobs = client.get_recent_datasets()

    datasets_jobs.sort(key=lambda x: x.last_updated, reverse=True)

    print(f"{'Name' : <25} {'ID' : <36} {'Status' : <20} {'Last Updated (desc)'}")
    for dataset in datasets_jobs:
        dataset_name = (
            dataset.name[:20] + "..."
            if dataset.name and len(dataset.name) > 20
            else "Unknown"
        )
        print(
            f"{dataset_name : <25} {dataset.id :<36} {dataset.status : <20} {str(dataset.last_updated)}"
        )


@evals.command()
@click.option(
    "--api_key",
    default=talc_api_key,
    help="Talc API key. Can also be specified with the TALC_API_KEY environment variable.",
)
@click.option(
    "--source",
    help="Input folder, single file path, or URL. Multiple allowed.",
    multiple=True,
    default=[],
)
@click.option(
    "--scraper",
    help="A JSON-formatted string containing the scraper configuration.",
    multiple=True,
    default=[],
)
@click.option(
    "--source_list",
    default=None,
    help="A list of sources to upload. Accepts a newline separated txt file of files, filepaths, or URLs to upload.",
)
@click.option(
    "--friendly_name",
    default=None,
    help="Brief text description of this knowledge base.",
)
def upload_kb(
    api_key: str | None,
    source: list[str],
    scraper: list[str],
    friendly_name: str | None,
    source_list: str | None,
):
    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    if friendly_name is None:
        raise click.UsageError(
            "No friendly name  provided. Please use the --friendly_name option to provide a brief description string"
        )

    if source_list is not None:
        with open(source_list, "r") as f:
            source = f.read().split("\n")
            source = [x for x in source if x != ""]

    client = TalcClient(api_key, talc_base_url)

    print("Validating sources...")
    converted_inputs = asyncio.run(convert_inputs(source))

    print("Uploading data...")
    spec_entries = asyncio.run(collect_input_specs(client, converted_inputs))

    for scraper_config in scraper:
        # should be of the form {"scraper-id": {...}}
        wrapper_object = json.loads(scraper_config)
        assert len(wrapper_object) == 1
        scraper_id = list(wrapper_object.keys())[0]
        scraper_config = wrapper_object[scraper_id]
        spec_entries.append(
            ScraperSpec(scraper_id=scraper_id, scraper_args=scraper_config)
        )

    print("Starting KB ingestion job...")
    ingestion_spec = IngestionJobSpec(
        kb_friendly_name=friendly_name,
        entries=list(spec_entries),
    )
    job_id = asyncio.run(client.ingest_knowledge_base(ingestion_spec))

    started_at = datetime.datetime.now()

    while True:
        waiting_for_seconds = (datetime.datetime.now() - started_at).total_seconds()
        print(
            f"\rWaiting for job (id={job_id}) to finish... ({waiting_for_seconds:.0f}s)",
            end="",
        )
        maybe_kb = asyncio.run(client.poll_ingestion_job(job_id))
        if maybe_kb:
            print(f"\nKnowledge Base created with ID: {maybe_kb.id}")
            return
        else:
            time.sleep(2)


@evals.command()
@click.option(
    "--api_key",
    default=talc_api_key,
    help="Talc API key. Can also be specified with the TALC_API_KEY environment variable.",
)
@click.option(
    "--file",
    help="Input file path. Multiple allowed.",
    multiple=True,
    default=[],
)
def preupload_file(
    api_key: str | None,
    file: list[str],
):
    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    async def run_file(client: TalcClient, fp: pathlib.Path):
        blob_hash, cached = await client.upload_knowledge_base_blob(fp)
        print(f"  {'(cached)' if cached else '        '}  {blob_hash.hex()}  {fp}")

    async def run():
        client = TalcClient(api_key, talc_base_url)
        await asyncio.gather(
            *[run_file(client, pathlib.Path(fp)) for fp in file],
        )

    asyncio.run(run())


@evals.command()
@click.option(
    "--api_key",
    default=talc_api_key,
    help="Talc API key. Can also be specified with the TALC_API_KEY environment variable.",
)
@click.option(
    "--kb_id",
    prompt="Knowledge Base ID",
    help="The ID of the knowledge base to run tasks on.",
)
@click.option(
    "--task_type",
    prompt="Task Type",
    help="The type of task to run on the knowledge base.",
    type=click.Choice(["Hyperlink", "ReferenceLink"], case_sensitive=False),
)
def run_kb_task(api_key: str | None, kb_id: str, task_type: str):
    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    client = TalcClient(api_key, talc_base_url)
    if task_type == "Hyperlink":
        task_config = HyperlinkTaskConfig(task_type="Hyperlink")
    elif task_type == "ReferenceLink":
        task_config = ReferenceLinkTaskConfig(task_type="ReferenceLink")

    client.run_knowledge_base_task(kb_id, task_config)

    print(f"Running task {task_type} on knowledge base {kb_id}.")


@evals.command()
@click.option(
    "--api_key",
    default=talc_api_key,
    help="Talc API key. Can also be specified with the TALC_API_KEY environment variable.",
)
def list_kbs(
    api_key: str | None,
):
    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )
    client = TalcClient(api_key, talc_base_url)
    kbs = client.list_kbs()

    kbs.sort(key=lambda x: x.created_at if x.created_at else 0, reverse=True)

    print(f"{'Name' : <25}{'ID' : <40}{'Created At (desc)'}")
    for kb in kbs:
        friendly_name = kb.friendly_name[:20] if kb.friendly_name is not None else ""
        print(f"{friendly_name : <25}{kb.id : <40}{str(kb.created_at)}")


def main():
    evals()
