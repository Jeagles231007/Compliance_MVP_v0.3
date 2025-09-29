import os
# import pytest
from policy_generator import generate_policy, save_to_docx, save_to_pdf

# def test_generate_policy_returns_text():
#    api_key = os.getenv("OPENAI_API_KEY")
#   assert api_key, "OPENAI_API_KEY must be set"
#
#   result = generate_policy("Privacy Policy", "TestCorp",
#                           "UK", "Finance", "10 Employees")
# assert isinstance(result, str)
# assert len(result) > 50


class DummyClient:
    def chat(self):
        return self

    def completions(self):
        return self

    def create(self, **kwargs):
        _ = kwargs
        return type("Response", (), {
            "choices": [type("Choice", (), {"message": type("Message", (), {"content": "Test Policy Content"})()})]
        })()


def test_generate_policy(monkeypatch):
    import policy_generator
    monkeypatch.setattr(policy_generator, "get_api_key", lambda: "fake-key")
    monkeypatch.setattr(policy_generator, "client", DummyClient())

    result = generate_policy("TestCo", "Finance", "UK",
                             "Small", "Privacy Policy")
    assert "Test Policy Content" in result


def test_save_to_docx(tmp_path):
    file_path = tmp_path / "policy.docx"
    save_to_docx("Sample Policy Text", str(file_path))
    assert os.path.exists(file_path)
    assert file_path.stat().st_size > 0
