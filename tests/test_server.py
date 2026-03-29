"""Unit tests for server.py helper functions."""

import pytest
from src.server import extract_video_id, format_timestamp


class TestExtractVideoId:
    def test_standard_watch_url(self):
        assert extract_video_id("https://www.youtube.com/watch?v=CDClFY-R0dI") == "CDClFY-R0dI"

    def test_watch_url_without_www(self):
        assert extract_video_id("https://youtube.com/watch?v=CDClFY-R0dI") == "CDClFY-R0dI"

    def test_mobile_url(self):
        assert extract_video_id("https://m.youtube.com/watch?v=CDClFY-R0dI") == "CDClFY-R0dI"

    def test_short_url(self):
        assert extract_video_id("https://youtu.be/CDClFY-R0dI") == "CDClFY-R0dI"

    def test_embed_url(self):
        assert extract_video_id("https://www.youtube.com/embed/CDClFY-R0dI") == "CDClFY-R0dI"

    def test_v_path_url(self):
        assert extract_video_id("https://www.youtube.com/v/CDClFY-R0dI") == "CDClFY-R0dI"

    def test_regex_fallback(self):
        assert extract_video_id("https://www.youtube.com/watch?v=CDClFY-R0dI&t=42s") == "CDClFY-R0dI"

    def test_invalid_url_raises(self):
        with pytest.raises(ValueError):
            extract_video_id("https://example.com/not-a-video")


class TestFormatTimestamp:
    def test_sub_minute(self):
        assert format_timestamp(45.0) == "0:45"

    def test_exact_minute(self):
        assert format_timestamp(60.0) == "1:00"

    def test_minutes_and_seconds(self):
        assert format_timestamp(125.7) == "2:05"

    def test_one_hour(self):
        assert format_timestamp(3600.0) == "1:00:00"

    def test_hours_minutes_seconds(self):
        assert format_timestamp(3723.0) == "1:02:03"

    def test_zero(self):
        assert format_timestamp(0.0) == "0:00"
