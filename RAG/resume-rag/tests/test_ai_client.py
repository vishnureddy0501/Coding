import httpx

from app.ai_client import _gemini_error


def make_response(status_code: int, message: str = "") -> httpx.Response:
    request = httpx.Request("POST", "https://example.test")
    return httpx.Response(
        status_code,
        request=request,
        json={"error": {"message": message}},
    )


def test_quota_error_is_actionable() -> None:
    error = _gemini_error(make_response(429), "generate an answer")
    assert "quota or rate limit" in str(error)


def test_bad_request_keeps_provider_explanation() -> None:
    error = _gemini_error(make_response(400, "Unknown field: temperature"), "generate")
    assert "Unknown field: temperature" in str(error)
