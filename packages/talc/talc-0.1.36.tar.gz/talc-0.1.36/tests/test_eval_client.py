import unittest
from unittest.mock import patch, MagicMock
import requests
from talc.talc_client import (
    TalcClient,
    KnowledgeBase,
)
from talc.synthetic import Document


class TestTalcClient(unittest.TestCase):
    def setUp(self):
        self.instance = TalcClient("mock_api_key", "mock_url.com")

    @patch("talc.requests.post")
    def test_upload_knowledge_base_success(self, mock_post):
        # Mocking the response from requests.post
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "kb_id",
            "friendly_name": "testKB",
            "documents": ["1", "2"],
        }
        mock_post.return_value = mock_response

        # Creating a mock Document list with byte content
        documents = [
            Document(
                filepath="doc1.txt",
                content=b"Sample content",
                content_type="text/plain",
            ),
            Document(
                filepath="doc2.txt",
                content=b"More sample content",
                content_type="text/plain",
            ),
        ]

        # Call the function
        kb = self.instance.upload_knowledge_base(documents, "testKB")

        # These assertions dont really do anything since they're just mocked above
        self.assertIsInstance(kb, KnowledgeBase)
        self.assertEqual(kb.id, "kb_id")
        self.assertEqual(kb.friendly_name, "testKB")
        self.assertEqual(len(kb.documents), len(documents))

        # Check if the request was made correctly
        mock_post.assert_called_once_with(
            "mock_url.com/kb/create/testKB",
            files=[
                ("files", ("doc1.txt", b"Sample content", "text/plain")),
                ("files", ("doc2.txt", b"More sample content", "text/plain")),
            ],
            headers={"X-TALC-API": "mock_api_key"},
        )

    @patch("talc.requests.post")
    def test_upload_knowledge_base_invalid_format(self, mock_post):
        # Creating a mock Document list with invalid content (not bytes)
        documents = [
            Document(
                filepath="doc1.txt",
                content="Invalid content",
                content_type="text/plain",
            ),
        ]

        with self.assertRaises(ValueError) as context:
            self.instance.upload_knowledge_base(documents, "testKB")

        # Ensure the error message is correct
        self.assertIsNotNone(str(context.exception))

        # Ensure the request was never made
        mock_post.assert_not_called()

    @patch("talc.requests.post")
    def test_upload_knowledge_base_http_error(self, mock_post):
        # Mocking the response to simulate an HTTP error
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "Internal Server Error"
        )
        mock_post.return_value = mock_response

        # Creating a mock Document list with byte content
        documents = [
            Document(
                filepath="doc1.txt",
                content=b"Sample content",
                content_type="text/plain",
            ),
        ]

        # Test for HTTP error
        with self.assertRaises(requests.exceptions.HTTPError):
            self.instance.upload_knowledge_base(documents, "testKB")

        # Check if the request was made correctly
        mock_post.assert_called_once_with(
            "mock_url.com/kb/create/testKB",
            files=[
                ("files", ("doc1.txt", b"Sample content", "text/plain")),
            ],
            headers={"X-TALC-API": "mock_api_key"},
        )


if __name__ == "__main__":
    unittest.main()
