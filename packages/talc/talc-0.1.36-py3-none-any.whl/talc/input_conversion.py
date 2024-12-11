import asyncio
import datetime
import os
import pathlib
from typing import Awaitable, Callable, Iterable, TypeAlias

import click
import aiopath
from httpx import URL
from talc.knowledge_base import FileUploadSpec, IngestionEntrySpec, PublicUrlSpec
from talc.synthetic import Document
from talc.talc_client import TalcClient
from talc.utils.cli.io import Web

ConvertedInput: TypeAlias = (
    IngestionEntrySpec | Callable[[TalcClient], Awaitable[IngestionEntrySpec]]
)


async def collect_input_specs(
    client: TalcClient, converted_inputs: Iterable[ConvertedInput]
) -> list[IngestionEntrySpec]:
    async def collect_one(
        client: TalcClient, converted_input: ConvertedInput
    ) -> IngestionEntrySpec:
        if isinstance(converted_input, IngestionEntrySpec):
            return converted_input
        return await converted_input(client)

    return await asyncio.gather(
        *(collect_one(client, converted_input) for converted_input in converted_inputs)
    )


async def convert_inputs(raw_inputs: list[str]) -> Iterable[ConvertedInput]:
    return [
        spec
        for specs in await asyncio.gather(
            *(convert_input(raw_input) for raw_input in raw_inputs)
        )
        for spec in specs
    ]


async def convert_input(raw_input: str) -> Iterable[ConvertedInput]:
    if raw_input.startswith("http") or raw_input.startswith("https"):
        return [await convert_web_input(raw_input)]
    if await aiopath.AsyncPath(raw_input).is_dir():
        return await convert_directory_input(raw_input)
    if await aiopath.AsyncPath(raw_input).is_file():
        return [await convert_file_input(raw_input)]
    raise click.UsageError(
        f"Invalid input; expected a URL or directory/file path: '{raw_input}'"
    )


async def convert_web_input(raw_input: str) -> ConvertedInput:
    try:
        parsed = URL(raw_input)
        if not parsed.scheme and parsed.netloc:
            raise ValueError(f"Invalid URL: '{raw_input}'")
    except Exception:
        raise click.UsageError(f"Invalid URL: '{raw_input}'")

    # TODO handle intranet vs public distinction
    return PublicUrlSpec(url=raw_input)


async def convert_file_input(raw_input: str) -> ConvertedInput:
    file_path = pathlib.Path(raw_input)
    if not await aiopath.AsyncPath(file_path).exists():
        raise click.UsageError(f"File not found: '{raw_input}'")

    async def handler(client: TalcClient):
        blob_hash, cached = await client.upload_knowledge_base_blob(file_path)
        print(
            f"  {'(cached)' if cached else '        '}  {blob_hash.hex()}  {file_path}"
        )
        return FileUploadSpec(
            uploaded_at=datetime.datetime.now(tz=datetime.timezone.utc),
            original_filename=file_path.name,
            blob_hash=blob_hash,
        )

    return handler


async def convert_directory_input(raw_input: str) -> Iterable[ConvertedInput]:
    async def walk(dir_path: aiopath.AsyncPath):
        async for path in dir_path.iterdir():
            if await path.is_dir():
                async for p in walk(path):
                    yield p
            else:
                yield path

    file_paths = [p async for p in walk(aiopath.AsyncPath(raw_input))]
    return await asyncio.gather(*(convert_file_input(str(p)) for p in file_paths))


def parse_documents(input_path: list[str]) -> list[Document]:
    documents: list[Document] = []
    web = Web()
    # Figure out what kind of document each file is, and load it into a list of Document objects
    for f in input_path:
        # If it's a URL, load it locally and scrape
        if f.startswith("http") or f.startswith("https"):
            scraped = web.scrape(f)
            if len(scraped) > 0:
                for doc in scraped:
                    documents.append(doc)
        elif os.path.isdir(f):
            for root, _, files in os.walk(f):
                for path in files:
                    document = read_document(os.path.join(root, path))
                    if document is not None:
                        documents.append(document)
                    else:
                        # TODO: [Resolve handling] Current behavior is to gracefully skip if unsupported file within directory, but we throw error if unsupported file is provided directly as only input.
                        print(
                            f"Skipping file with unknown extension {path} in directory {root}."
                        )
        elif os.path.isfile(f):
            document = read_document(f)
            if document is not None:
                documents.append(document)
            else:
                raise click.UsageError(
                    "Unsupported file type. Only .md and .pdf files are supported."
                )
        else:
            raise click.UsageError(
                "File not found or invalid URL. Please provide a valid file path or URL."
            )
    return documents


def read_document(fp: str) -> Document | None:
    """
    Read a document from a file path as either text or bytes.
    Currently supported extensions: [.pdf, .md, .txt]
    """
    if fp.endswith(".md") or fp.endswith(".txt"):
        with open(fp, "r") as f:
            return Document(
                content=f.read().encode(encoding="utf-8", errors="ignore"),
                title=f.name,
                filepath=os.path.basename(fp),
                content_type="text/markdown",
            )
    if fp.endswith(".txt"):
        with open(fp, "r") as f:
            return Document(
                content=f.read().encode(encoding="utf-8", errors="ignore"),
                title=f.name,
                filepath=os.path.basename(fp),
                content_type="text/plain",
            )
    elif fp.endswith(".pdf"):
        print(f"Reading pdf: {fp}")
        with open(fp, "rb") as f:
            return Document(
                content=f.read(),
                title=os.path.basename(fp),
                filepath=fp,
                content_type="application/pdf",
            )
    else:
        return None
