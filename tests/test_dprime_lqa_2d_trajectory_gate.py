import json
import math
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.paper5.dprime_lqa_2d_trajectory_gate import (
    ARTIFACT_STEM,
    B_GRID,
    FULL_BETA_TOLERANCE,
    N_MATTER_GRID,
    STATUS,
    SourceParameters,
    build_trajectory_rows,
    dprime_closed_form,
    dprime_quotient,
    end_time,
    full_source_beta,
    projected_response,
    reduced_large_n_beta,
    run_audit,
    tensor_to_scalar_ratio,
    trajectory_identity_residual,
    trajectory_state,
    trajectory_tangent,
    write_artifacts,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "paper5" / "dprime_lqa_2d_trajectory_gate.py"


@pytest.mark.parametrize(
    ("b", "n_matter"),
    [(0.0, 100_000), (-0.1, 100_000), (math.inf, 100_000), (0.1, 0)],
)
def test_source_parameters_reject_invalid_values(b, n_matter):
    with pytest.raises(ValueError):
        SourceParameters(b=b, n_matter=n_matter)


def test_trajectory_retains_both_coordinates_and_exact_identity():
    parameters = SourceParameters(b=0.3, n_matter=100_000)
    t = 7.0 * end_time(parameters)
    lambda_value, xi_value = trajectory_state(t, parameters)

    assert lambda_value > 0.0
    assert xi_value > 0.0
    assert trajectory_identity_residual(t, parameters) == pytest.approx(0.0, abs=1e-14)
    assert lambda_value / parameters.lambda_0 + xi_value / parameters.xi_infinity == pytest.approx(1.0)


def test_analytic_tangent_solves_reduced_large_n_system():
    parameters = SourceParameters(b=1.0, n_matter=1_000_000)
    t = 4.0 * end_time(parameters)
    state = trajectory_state(t, parameters)
    tangent = trajectory_tangent(t, parameters)
    reduced = reduced_large_n_beta(state[0], parameters)

    assert tangent[0] == pytest.approx(reduced[0], rel=1e-14)
    assert tangent[1] == pytest.approx(reduced[1], rel=1e-14)


def test_every_frozen_case_retains_full_beta_diagnostic_within_tolerance():
    rows = build_trajectory_rows()

    assert {float(row["b"]) for row in rows} == set(B_GRID)
    assert {int(row["n_matter"]) for row in rows} == set(N_MATTER_GRID)
    assert all("lambda" in row and "xi" in row for row in rows)
    assert max(float(row["full_vector_residual"]) for row in rows) <= FULL_BETA_TOLERANCE

    sample = rows[-1]
    parameters = SourceParameters(
        b=float(sample["b"]), n_matter=int(sample["n_matter"])
    )
    assert full_source_beta(
        float(sample["lambda"]), float(sample["xi"]), parameters
    ) == pytest.approx(
        (float(sample["full_beta_lambda"]), float(sample["full_beta_xi"]))
    )


def test_tensor_projection_has_preregistered_finite_anchors():
    parameters = SourceParameters(b=0.1, n_matter=100_000)
    t_end = end_time(parameters)

    assert tensor_to_scalar_ratio(t_end, parameters) == pytest.approx(16.0, rel=1e-12)
    assert projected_response(t_end, parameters) == pytest.approx(-1.0, rel=1e-12)
    assert tensor_to_scalar_ratio(1e8, parameters) == pytest.approx(0.0, abs=1e-24)
    assert projected_response(1e8, parameters) == pytest.approx(1.0, abs=1e-15)
    with pytest.raises(ValueError):
        tensor_to_scalar_ratio(0.99 * t_end, parameters)


def test_dprime_closed_form_matches_quotient_and_is_nonconstant():
    parameters = SourceParameters(b=0.3, n_matter=100_000)
    t_end = end_time(parameters)
    early = 1.05 * t_end
    late = 16.0 * t_end

    assert dprime_quotient(early, parameters) == pytest.approx(
        dprime_closed_form(early, parameters), rel=1e-12
    )
    assert dprime_quotient(late, parameters) == pytest.approx(
        dprime_closed_form(late, parameters), rel=1e-12
    )
    assert dprime_quotient(early, parameters) != pytest.approx(
        dprime_quotient(late, parameters)
    )
    # Use the reduced analytic form for the far-UV limit: x_r itself rounds
    # to exactly +1 before this scale in binary floating point.
    assert dprime_closed_form(1e8, parameters) == pytest.approx(0.0, abs=1e-6)
    with pytest.raises(ValueError):
        dprime_quotient(t_end, parameters)


def test_audit_reports_rank_limit_dprime_fail_and_no_transfer():
    report = run_audit()

    assert report["status"] == STATUS
    assert report["checks"]["trajectory_identity"] is True
    assert report["checks"]["reduced_ode"] is True
    assert report["checks"]["full_beta_window"] is True
    assert report["checks"]["dprime_pass"] is False
    assert report["checks"]["exact_binary_observable_composition_source_defined"] is False
    assert report["projection_audit"]["ambient_coupling_dimension"] == 2
    assert report["projection_audit"]["orbit_dimension"] == 1
    assert report["projection_audit"]["coupling_contrast_equals_prior_xi_normalization"] is True
    assert report["projection_audit"]["r_projection_equals_prior_xi_normalization"] is False
    assert report["candidate"]["physical_transfer"] == "not_bookable"
    assert report["candidate"]["claim_pass"] is False


def test_artifacts_are_deterministic_and_machine_readable(tmp_path):
    first_paths = write_artifacts(tmp_path / "first")
    second_paths = write_artifacts(tmp_path / "second")

    assert [path.name for path in first_paths] == [
        f"{ARTIFACT_STEM}.json",
        f"{ARTIFACT_STEM}_trajectory.csv",
        f"{ARTIFACT_STEM}_dprime.csv",
        f"{ARTIFACT_STEM}.md",
    ]
    for left, right in zip(first_paths, second_paths):
        assert left.read_bytes() == right.read_bytes()

    report = json.loads(first_paths[0].read_text(encoding="utf-8"))
    assert report["preregistration"]["frozen_before_execution"] is True
    assert report["checks"]["dprime_pass"] is False
    assert len(report["trajectory_rows"]) == 30
    assert len(report["dprime_rows"]) == 36


def test_cli_writes_all_preregistered_artifacts(tmp_path):
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--output-dir", str(tmp_path)],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert STATUS in completed.stdout
    assert "claim_pass=False" in completed.stdout
    assert len(list(tmp_path.glob(f"{ARTIFACT_STEM}*"))) == 4
