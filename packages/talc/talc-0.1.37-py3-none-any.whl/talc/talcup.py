"""
Some experimental patterns for simplifying using the CLI for testing; 
may or may not be helpful for real-world use cases.
"""

import pathlib
import os
import re
import shutil
import subprocess
import click
from pydantic import BaseModel
from pydantic_yaml import parse_yaml_file_as, to_yaml_file
from talc.synthetic import (
    GeneratorArgs,
    QuestionGenerationConfig,
    QuestionGeneratorArgs,
)

UUID_PATTERN = re.compile(
    "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
)

TALCUP_HOME = pathlib.Path.home() / "talc"

class LocalConfigSourceList(BaseModel):
    name: str
    sources: list[str] | None = None
    source_lists: list[str] | None = None


class LocalConfigRun(BaseModel):
    name: str
    questions: list[GeneratorArgs]
    sources: list[str] | None = None
    source_lists: list[str] | None = None


class LocalConfigFile(BaseModel):
    source_lists: list[LocalConfigSourceList] | None = None
    runs: list[LocalConfigRun] | None = None


class CachedKnowledgeBase(BaseModel):
    id: str
    sources: list[str]


class LocalConfig:
    source_lists: dict[str, LocalConfigSourceList]
    runs: dict[str, LocalConfigRun]

    def __init__(self):
        self.source_lists: dict[str, LocalConfigSourceList] = {}
        self.runs: dict[str, LocalConfigRun] = {}

    def add_source_list(self, list: LocalConfigSourceList):
        if list.name in self.source_lists:
            raise Exception(f"source list already exists: '{list.name}'")
        self.source_lists[list.name] = list

    def add_run(self, run: LocalConfigRun):
        if run.name in self.runs:
            raise Exception(f"run already exists: '{run.name}'")
        self.runs[run.name] = run

    def resolve_run(self, run_name: str) -> tuple[set[str], list[GeneratorArgs]]:
        if run_name not in self.runs:
            raise Exception(f"run does not exist: '{run_name}'")
        run = self.runs[run_name]
        sources = set()
        if run.sources is not None:
            for source in run.sources:
                sources.add(source)
        if run.source_lists is not None:
            for source_list in run.source_lists:
                for source in self.resolve_source_list(source_list):
                    sources.add(source)
        return sources, run.questions

    def resolve_source_list(self, source_list_name: str) -> set[str]:
        if source_list_name not in self.source_lists:
            raise Exception(f"source list does not exist: '{source_list_name}'")
        source_list = self.source_lists[source_list_name]
        sources = set()
        if source_list.sources is not None:
            for source in source_list.sources:
                sources.add(source)
        if source_list.source_lists is not None:
            for other_source_list_name in source_list.source_lists:
                for source in self.resolve_source_list(other_source_list_name):
                    sources.add(source)
        return sources


class LocalConfigLoader:

    def __init__(self):
        self.config_dir = TALCUP_HOME

    def _ensure_config_dir(self):
        if not self.config_dir.exists():
            self.config_dir.mkdir()

    def load(self) -> LocalConfig:
        self._ensure_config_dir()

        config = LocalConfig()
        for file in os.listdir(self.config_dir):
            if not file.endswith(".yaml"):
                continue
            parsed = parse_yaml_file_as(LocalConfigFile, self.config_dir / file)
            if parsed.source_lists:
                for source_list in parsed.source_lists:
                    config.add_source_list(source_list)
            if parsed.runs:
                for run in parsed.runs:
                    config.add_run(run)
        return config


class LocalConfigCacheLoader:

    def __init__(self):
        self.cache_dir = TALCUP_HOME / ".kb_cache"

    def _ensure_cache_dir(self):
        if not self.cache_dir.exists():
            self.cache_dir.mkdir()

    def add_cached_kb(self, kb_id: str, sources: set[str]):
        self._ensure_cache_dir()
        cached = CachedKnowledgeBase(id=kb_id, sources=list(sources))
        cached.id = kb_id
        cached.sources = list(sources)
        to_yaml_file(self.cache_dir / f"{kb_id}.yaml", cached)

    def find_cached_kbs(self, sources: set[str]) -> list[str]:
        self._ensure_cache_dir()
        kb_ids = []
        for file in os.listdir(self.cache_dir):
            if not file.endswith(".yaml"):
                continue
            parsed = parse_yaml_file_as(CachedKnowledgeBase, self.cache_dir / file)
            if set(parsed.sources) == sources:
                kb_ids.append(parsed.id)
        return kb_ids


@click.group()
def talcup():
    pass


@talcup.command(name="init")
def init_example():
    example_src_path = (
        pathlib.Path(__file__).resolve().parent / "talcup_example.yaml"
    ).resolve()
    example_dest_path = TALCUP_HOME / "example.yaml"
    if example_dest_path.exists():
        print(f"Can't create example at {example_dest_path}: a file already exists.")
        return
    shutil.copy(example_src_path, example_dest_path)
    print(f"Created an example config file at {example_dest_path}.")
    print("Try running:")
    print("  talcup list")
    print("  talcup show examplerun")
    print("  talcup gen examplerun")


def print_empty_message():
    print(f"No runs are defined. Add config files to {TALCUP_HOME}.")
    print("You can also run `talcup init` to create an example config file.")


@talcup.command(name="list")
def list_runs():
    config = LocalConfigLoader().load()
    if not config.runs or len(config.runs) == 0:
        print_empty_message()
        return

    run_names = sorted(config.runs)

    print(f"Available runs (from {TALCUP_HOME}):")
    for run in config.runs:
        meta: str
        try:
            sources, questions = config.resolve_run(run)
            meta = f"({len(sources)} sources, {len(questions)} question configs)"
        except:
            meta = "(couldn't be fully resolved due to an error)"
        print(f" - {run} {meta}")


@talcup.command
@click.argument("name")
def show(name: str):
    config = LocalConfigLoader().load()
    if not config.runs or len(config.runs) == 0:
        print_empty_message()
        return

    sources, questions = config.resolve_run(name)
    print("Sources:")
    for source in sources:
        print(f" - {source}")
    print("Questions:")
    for question in questions:
        print(f" - {question.question_type}")


@talcup.command
@click.option("--force-upload", is_flag=True)
@click.argument("name")
def gen(name: str, force_upload: bool):
    config = LocalConfigLoader().load()
    if not config.runs or len(config.runs) == 0:
        print_empty_message()
        return

    sources, questions = config.resolve_run(name)

    cache_loader = LocalConfigCacheLoader()
    maybe_kbs = cache_loader.find_cached_kbs(sources)
    ls_completed = subprocess.run(["talc", "list-kbs"], capture_output=True)
    actual_kbs = str(ls_completed.stdout, "utf-8")
    matching_kbs = [kb for kb in maybe_kbs if kb in actual_kbs]

    if len(matching_kbs) == 0 or force_upload:
        if force_upload:
            print("Forcing a new KB upload...")
        else:
            print("Couldn't find a cached KB; uploading one now...")
        args = ["talc", "upload-kb"]
        for source in sources:
            args.append("--source")
            args.append(source)
        args.append("--friendly_name")
        args.append(name)
        upload_completed = subprocess.run(args, capture_output=True)
        uploaded_kb_ids = UUID_PATTERN.findall(str(upload_completed.stdout, "utf-8"))
        if len(uploaded_kb_ids) != 1:
            raise Exception("expected upload-kb to return a single UUID")
        kb_id = uploaded_kb_ids[0]
        cache_loader.add_cached_kb(kb_id, sources)
        print(f"  Added KB: {kb_id}")
    else:
        kb_id = matching_kbs[0]
        print(f"Found cached KB: {kb_id}")

    parent_output_dir = TALCUP_HOME / "output"
    if not parent_output_dir.exists():
        parent_output_dir.mkdir()

    output_dir = parent_output_dir / name
    if not output_dir.exists():
        output_dir.mkdir()

    config = QuestionGenerationConfig(
        name=name, knowledge_bases=[kb_id], question_configs=questions
    )
    config_path = output_dir / "config.json"
    with open(config_path, "w") as f:
        f.write(config.model_dump_json(indent=4))

    print("\nRunning talc generate...\n")
    subprocess.run(
        ["talc", "generate", "--config", config_path], cwd=config_path.parent
    )


def main():
    talcup()
