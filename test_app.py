"""
Unit tests for the IBM OnePipeline DevSecOps V11 Flask microservice.

Discovered automatically by the pipeline `test` stage via:
  python -m unittest discover --start-directory . --pattern "test_*.py"

Test coverage:
  - GET /       status code, JSON body fields, Content-Type header
  - GET /health status code, JSON body, Content-Type header
  - 404 on an unknown route
"""

import json
import unittest

from app import app


class TestIndexRoute(unittest.TestCase):
    """Tests for the root route GET /"""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_status_code_is_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_content_type_is_json(self):
        response = self.client.get("/")
        self.assertIn("application/json", response.content_type)

    def test_body_status_field_is_ok(self):
        response = self.client.get("/")
        body = json.loads(response.data)
        self.assertEqual(body["status"], "ok")

    def test_body_contains_message_field(self):
        response = self.client.get("/")
        body = json.loads(response.data)
        self.assertIn("message", body)
        self.assertTrue(len(body["message"]) > 0)

    def test_only_get_method_allowed(self):
        response = self.client.post("/")
        self.assertEqual(response.status_code, 405)


class TestHealthRoute(unittest.TestCase):
    """Tests for the health-check probe GET /health"""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_status_code_is_200(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

    def test_content_type_is_json(self):
        response = self.client.get("/health")
        self.assertIn("application/json", response.content_type)

    def test_body_status_field_is_healthy(self):
        response = self.client.get("/health")
        body = json.loads(response.data)
        self.assertEqual(body["status"], "healthy")

    def test_body_is_exactly_one_field(self):
        """Health probe payload must stay minimal — no extraneous fields."""
        response = self.client.get("/health")
        body = json.loads(response.data)
        self.assertEqual(list(body.keys()), ["status"])

    def test_only_get_method_allowed(self):
        response = self.client.post("/health")
        self.assertEqual(response.status_code, 405)


class TestUnknownRoute(unittest.TestCase):
    """Verifies Flask returns 404 for undefined paths."""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_unknown_route_returns_404(self):
        response = self.client.get("/does-not-exist")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
