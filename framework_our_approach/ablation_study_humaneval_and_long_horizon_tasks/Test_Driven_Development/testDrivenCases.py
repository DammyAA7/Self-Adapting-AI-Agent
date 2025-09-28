import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from Unit_Test.functions import *
import csv

@pytest.fixture(autouse=True)
def temp_movie_csv(tmp_path, monkeypatch):
    tmp_dir = tmp_path / "temp_movies"
    tmp_dir.mkdir()
    csv_file = tmp_dir / "movie.csv"
    with open(csv_file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["title", "year"])
        writer.writerow(["The Matrix", "1999"])
        writer.writerow(["Inception", "2010"])
    monkeypatch.chdir(tmp_dir)
    yield

def legacy_report_v1():
    return movie_api()

def dashboard_v2():
    return movie_api()

def jsonld_export_v3():
    return movie_api()

def test_movie_api_v1_returns_list_of_titles():
    titles = legacy_report_v1()
    assert isinstance(titles, list)
    assert titles == ["The Matrix", "Inception"]

def test_movie_api_standalone_fallback_behaves_as_v1():
    result = movie_api()
    assert isinstance(result, list)
    assert result == ["The Matrix", "Inception"]

def test_movie_api_v2_returns_dict_with_metadata():
    data = dashboard_v2()
    assert isinstance(data, dict)
    assert data.get("count") == 2
    assert data.get("source") == "movie.csv"
    assert data.get("titles") == ["The Matrix", "Inception"]

def test_movie_api_v3_returns_jsonld_structure():
    payload = jsonld_export_v3()
    assert isinstance(payload, dict)
    assert payload.get("@context") == "http://schema.org"
    assert payload.get("@type") == "MovieCollection"
    assert payload.get("name") == "All Movies"
    has_part = payload.get("hasPart")
    assert isinstance(has_part, list)
    expected = [
        {"@type": "Movie", "name": "The Matrix"},
        {"@type": "Movie", "name": "Inception"}
    ]
    assert has_part == expected

def test_movie_api_with_empty_csv_returns_empty_results(tmp_path, monkeypatch):
    tmp_dir = tmp_path / "empty_movies"
    tmp_dir.mkdir()
    csv_file = tmp_dir / "movie.csv"
    with open(csv_file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["title", "year"])
    monkeypatch.chdir(tmp_dir)
    titles = legacy_report_v1()
    assert isinstance(titles, list)
    assert titles == []
    data = dashboard_v2()
    assert data.get("count") == 0
    assert data.get("titles") == []
    payload = jsonld_export_v3()
    assert payload.get("hasPart") == []

def test_movie_api_missing_csv_returns_none(tmp_path, monkeypatch):
    tmp_dir = tmp_path / "no_movies"
    tmp_dir.mkdir()
    monkeypatch.chdir(tmp_dir)
    result = movie_api()
    assert result is None

def test_movie_api_integration_multiple_calls(tmp_path, monkeypatch):
    tmp_dir = tmp_path / "multi_movies"
    tmp_dir.mkdir()
    csv_file = tmp_dir / "movie.csv"
    with open(csv_file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["title"])
        writer.writerow(["Avatar"])
    monkeypatch.chdir(tmp_dir)
    titles1 = legacy_report_v1()
    assert titles1 == ["Avatar"]
    data2 = dashboard_v2()
    assert data2["titles"] == ["Avatar"]
    payload3 = jsonld_export_v3()
    assert payload3["hasPart"] == [{"@type": "Movie", "name": "Avatar"}]

if __name__ == "__main__":
    pytest.main([__file__])