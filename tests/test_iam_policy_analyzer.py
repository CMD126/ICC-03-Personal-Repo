import json

from conftest import load

iam = load("05-cloud-security/exercises/iam-policy-analyzer/iam_policy_analyzer.py")


def severities(findings):
    return {sev for sev, _ in findings}


def test_public_wildcard_statement_is_critical():
    stmt = {"Effect": "Allow", "Principal": "*", "Action": "dynamodb:*", "Resource": "*"}
    *_, findings = iam.analyze_statement(stmt, 0)
    assert "CRITICAL" in severities(findings)
    assert any("wildcard on service" in msg for _, msg in findings)


def test_least_privilege_statement_is_clean():
    stmt = {
        "Effect": "Allow",
        "Action": ["s3:ListBucket"],
        "Resource": "arn:aws:s3:::my-bucket",
    }
    *_, findings = iam.analyze_statement(stmt, 1)
    assert findings == []


def test_sample_policy_loads(root):
    policy = iam.load_policy(str(root / "05-cloud-security/exercises/iam-policy-analyzer/sample_policy.json"))
    assert "Statement" in policy
    json.dumps(policy)  # round-trips cleanly
