import pytest

from app.cloud_storage import parse_cloudinary_url


def test_parse_cloudinary_url() -> None:
    result = parse_cloudinary_url("cloudinary://12345:secret-value@demo-cloud")

    assert result == {
        "cloud_name": "demo-cloud",
        "api_key": "12345",
        "api_secret": "secret-value",
    }


def test_parse_cloudinary_url_rejects_invalid_value() -> None:
    with pytest.raises(ValueError, match="CLOUDINARY_URL must use"):
        parse_cloudinary_url("demo-cloud")
