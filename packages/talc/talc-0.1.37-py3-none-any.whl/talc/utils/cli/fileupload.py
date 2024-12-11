import os
import urllib.parse

import click
from talc.synthetic import Document
from talc.utils.cli.io import (
    Web,
)


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
                root = os.path.abspath(root)
                for path in files:
                    abs_path = os.path.join(root, path)
                    print(f"Reading file: {abs_path}")
                    document = read_document(abs_path)
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
    print(f"Reading file: {fp}")
    if fp.endswith(".md") or fp.endswith(".txt"):
        with open(fp, "r") as f:
            return Document(
                content=f.read().encode(encoding="utf-8", errors="ignore"),
                title=urllib.parse.quote_plus(os.path.basename(fp)),
                filepath=fp,
                content_type="text/markdown",
            )
    if fp.endswith(".txt"):
        with open(fp, "r") as f:
            return Document(
                content=f.read().encode(encoding="utf-8", errors="ignore"),
                title=urllib.parse.quote_plus(os.path.basename(fp)),
                filepath=os.path.basename(fp),
                content_type="text/plain",
            )
    elif fp.endswith(".pdf"):
        print(f"Reading pdf: {fp}")
        with open(fp, "rb") as f:
            return Document(
                content=f.read(),
                title=urllib.parse.quote_plus(os.path.basename(fp)),
                filepath=fp,
                content_type="application/pdf",
            )
    else:
        return None
