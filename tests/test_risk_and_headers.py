import pytest
from conftest import load

risk = load("02-grc/exercises/risk-assessment-tool/risk_assessment_tool.py")
headers = load("07-appsec/exercises/web-headers-checker/web_headers_checker.py")


@pytest.mark.parametrize(
    ("score", "level"),
    [(1, "LOW"), (4, "LOW"), (5, "MEDIUM"), (12, "HIGH"), (15, "CRITICAL"), (25, "CRITICAL")],
)
def test_risk_severity_bands(score, level):
    assert risk.get_severity(score)[0] == level


def test_every_likelihood_impact_score_has_a_band():
    for likelihood in range(1, 6):
        for impact in range(1, 6):
            assert risk.get_severity(likelihood * impact)[0] != "UNKNOWN"


@pytest.mark.parametrize(
    ("score", "total", "expected"),
    [(7, 7, "A"), (5, 7, "B"), (4, 7, "C"), (3, 10, "D"), (0, 7, "F")],
)
def test_header_grade(score, total, expected):
    assert headers.grade(score, total) == expected
