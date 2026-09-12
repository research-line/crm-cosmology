import json
import math
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.paper5.dprime_2d_ym_heat_kernel_gate import (
    ARTIFACT_STEM,
    STATUS,
    compose_normalized,
    dprime_quotient,
    generator,
    normalized_response,
    run_audit,
    wilson_response,
    write_artifacts,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "paper5" / "dprime_2d_ym_heat_kernel_gate.py"


@pytest.mark.parametrize(
    ("area", "kappa"),
    [(-0.1, 1.0), (1.0, 0.0), (1.0, -1.0), (math.inf, 1.0)],
)
def test_wilson_response_rejects_invalid_parameters(area, kappa):
    with pytest.raises(ValueError):
        wilson_response(area, kappa)


def test_exact_wilson_semigroup_and_normalized_composition():
    kappa = 0.73
    area_left = 0.41
    area_right = 1.17
    left = normalized_response(area_left, kappa)
    right = normalized_response(area_right, kappa)

    assert wilson_response(area_left + area_right, kappa) == pytest.approx(
        wilson_response(area_left, kappa) * wilson_response(area_right, kappa)
    )
    assert compose_normalized(left, right) == pytest.approx(
        normalized_response(area_left + area_right, kappa)
    )


def test_composition_has_boundaries_and_is_associative():
    identity = -1.0
    absorber = 1.0
    x, y, z = -0.4, 0.1, 0.75

    assert compose_normalized(identity, x) == pytest.approx(x)
    assert compose_normalized(absorber, x) == pytest.approx(absorber)
    assert compose_normalized(compose_normalized(x, y), z) == pytest.approx(
        compose_normalized(x, compose_normalized(y, z))
    )
    with pytest.raises(ValueError):
        compose_normalized(-1.01, x)


def test_generator_and_dprime_quotient_are_analytic_and_nonconstant():
    kappa = 1.2
    assert generator(0.0, kappa) == pytest.approx(kappa)
    assert dprime_quotient(0.0, kappa) == pytest.approx(kappa)
    assert dprime_quotient(0.5, kappa) == pytest.approx(2.0 * kappa / 3.0)
    assert dprime_quotient(0.0, kappa) != pytest.approx(
        dprime_quotient(0.5, kappa)
    )
    with pytest.raises(ValueError):
        dprime_quotient(-1.0, kappa)
    with pytest.raises(ValueError):
        dprime_quotient(1.0, kappa)


def test_audit_fails_claim_transfer_for_explicit_reasons():
    report = run_audit()
    candidate = report["candidate"]

    assert report["status"] == STATUS
    assert report["checks"]["wilson_semigroup"] is True
    assert report["checks"]["normalized_composition"] is True
    assert report["checks"]["composition_associative"] is True
    assert report["checks"]["dprime_quotient_nonconstant"] is True
    assert report["checks"]["dprime_pass"] is False
    assert candidate["scattering_observable"] == "not_supported"
    assert candidate["renormalization_group_running"].startswith("not_supported")
    assert candidate["dprime_projective_quotient"] == "fail_nonconstant"
    assert candidate["claim_pass"] is False


def test_artifacts_are_deterministic_and_machine_readable(tmp_path):
    first = tmp_path / "first"
    second = tmp_path / "second"
    first_paths = write_artifacts(first)
    second_paths = write_artifacts(second)

    assert [path.name for path in first_paths] == [
        f"{ARTIFACT_STEM}.json",
        f"{ARTIFACT_STEM}.csv",
        f"{ARTIFACT_STEM}.md",
    ]
    for left, right in zip(first_paths, second_paths, strict=True):
        assert left.read_bytes() == right.read_bytes()

    report = json.loads(first_paths[0].read_text(encoding="utf-8"))
    assert report["candidate"]["claim_pass"] is False
    assert report["checks"]["dprime_pass"] is False


def test_cli_writes_the_three_audit_artifacts(tmp_path):
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--output-dir", str(tmp_path)],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert STATUS in completed.stdout
    assert "claim_pass=False" in completed.stdout
    assert len(list(tmp_path.glob(f"{ARTIFACT_STEM}.*"))) == 3
