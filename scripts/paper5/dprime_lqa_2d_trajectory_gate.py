"""Audit the preregistered LQA two-coupling trajectory against D'.

The source branch is the large-matter one-loop solution in Supplemental
Eq. (9) of Liu, Quintin, and Afshordi (2026).  Both running couplings are
retained, and the sole observable projection is the source's tensor-to-scalar
ratio from Supplemental Eq. (26).  The calculation is deliberately
claim-bounded: it does not promote a debated one-loop flow or a chosen
curvature-scale map to a nonperturbative physical composition law.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence


CANDIDATE_ID = "CRM5-LQA-2D-TRAJECTORY-RPROJ-V1"
RUN_DATE = "2026-08-26"
STATUS = "FULL_2D_LARGE_N_TRAJECTORY__R_PROJECTION_DPRIME_FAIL__NO_EXACT_C"
ARTIFACT_STEM = "DPRIME_LQA_2D_TRAJECTORY_RPROJ_GATE_2026-08-26"
PREREGISTRATION = (
    "research/crm-v/preregistrations/"
    "CRM5_LQA_2D_TRAJECTORY_RPROJ_V1_PREREG_2026-08-26.md"
)
PREREGISTRATION_COMMIT = "3c07f3bb9f8c3fd8869268ba6cf0cc3cd50c9b7d"

B_GRID = (0.1, 0.3, 1.0)
N_MATTER_GRID = (100_000, 1_000_000)
TRAJECTORY_MULTIPLIERS = (1.0, 2.0, 4.0, 8.0, 16.0)
DPRIME_MULTIPLIERS = (1.05, 1.25, 2.0, 4.0, 8.0, 16.0)
IDENTITY_TOLERANCE = 1e-12
REDUCED_ODE_TOLERANCE = 1e-12
FULL_BETA_TOLERANCE = 1e-3
DPRIME_CONSTANCY_TOLERANCE = 1e-10

SOURCE = {
    "citation": (
        "Liu, Quintin, and Afshordi, Physical Review Letters 136, 111501 "
        "(2026)"
    ),
    "doi": "https://doi.org/10.1103/6gtx-j455",
    "arxiv": "https://arxiv.org/abs/2510.18733",
    "equations": {
        "full_beta_system": "main Eq. (2)",
        "large_matter_trajectory": "Supplemental Eq. (9)",
        "scale_map": "mu=sqrt(abs(R)), main text and Supplemental Eq. (12)",
        "observable_projection": "Supplemental Eq. (26)",
    },
}


@dataclass(frozen=True)
class SourceParameters:
    """Parameters for one preregistered source trajectory."""

    b: float
    n_matter: int

    def __post_init__(self) -> None:
        if not math.isfinite(float(self.b)) or self.b <= 0.0:
            raise ValueError("b must be finite and positive")
        if isinstance(self.n_matter, bool) or not isinstance(self.n_matter, int):
            raise ValueError("n_matter must be an integer")
        if self.n_matter <= 0:
            raise ValueError("n_matter must be positive")

    @property
    def lambda_0(self) -> float:
        return 16.0 * math.pi**2 * self.b / self.n_matter

    @property
    def xi_infinity(self) -> float:
        return 70.0 * self.lambda_0 / self.n_matter


@dataclass(frozen=True)
class CandidateAudit:
    candidate_id: str = CANDIDATE_ID
    trajectory: str = "two-coupling (lambda, xi) large-N_m source approximation"
    full_two_coordinate_retention: str = "supported"
    reduced_ode_solution: str = "supported"
    full_beta_window: str = "supported_at_preregistered_tolerance"
    observable_projection: str = "source_defined_tensor_to_scalar_ratio"
    projection_rank: str = "rank_one_flrw_weyl_squared_vanishes"
    dprime_projective_quotient: str = "fail_nonconstant"
    exact_binary_observable_composition: str = "not_source_defined"
    physical_transfer: str = "not_bookable"
    claim_pass: bool = False


def _finite(value: float, name: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _time(value: float, *, positive: bool = False) -> float:
    t = _finite(value, "t")
    if positive and t <= 0.0:
        raise ValueError("t must be positive")
    if not positive and t < 0.0:
        raise ValueError("t must be non-negative")
    return t


def end_log_psi_squared(parameters: SourceParameters) -> float:
    """Return the source's inflation-end value from Supplemental Eq. (23)."""

    b = parameters.b
    return 2.0 / b * (
        math.sqrt(1.0 + 2.0 * (1.0 + 1.0 / math.sqrt(3.0)) * b) - 1.0
    )


def end_time(parameters: SourceParameters) -> float:
    """Convert ``ln(psi_end^2)`` to ``t=ln(mu/mu0)`` on the fixed scale map."""

    return end_log_psi_squared(parameters) / 4.0


def trajectory_state(
    t: float, parameters: SourceParameters
) -> tuple[float, float]:
    """Return the ordered source state ``(lambda(t), xi(t))``."""

    checked_t = _time(t)
    lambda_0 = parameters.lambda_0
    denominator = 1.0 + parameters.b * checked_t
    lambda_value = lambda_0 / denominator
    xi_value = (
        35.0
        * lambda_0**2
        * checked_t
        / (8.0 * math.pi**2 * denominator)
    )
    return lambda_value, xi_value


def trajectory_tangent(
    t: float, parameters: SourceParameters
) -> tuple[float, float]:
    """Return the analytic derivative of the complete source trajectory."""

    checked_t = _time(t)
    lambda_0 = parameters.lambda_0
    denominator_squared = (1.0 + parameters.b * checked_t) ** 2
    d_lambda = -lambda_0 * parameters.b / denominator_squared
    d_xi = 35.0 * lambda_0**2 / (8.0 * math.pi**2 * denominator_squared)
    return d_lambda, d_xi


def reduced_large_n_beta(
    lambda_value: float, parameters: SourceParameters
) -> tuple[float, float]:
    """Return the reduced beta vector solved by Supplemental Eq. (9)."""

    coupling = _finite(lambda_value, "lambda_value")
    if coupling < 0.0:
        raise ValueError("lambda_value must be non-negative")
    beta_lambda = -parameters.n_matter * coupling**2 / (4.0 * math.pi) ** 2
    beta_xi = 35.0 * coupling**2 / (8.0 * math.pi**2)
    return beta_lambda, beta_xi


def full_source_beta(
    lambda_value: float,
    xi_value: float,
    parameters: SourceParameters,
) -> tuple[float, float]:
    """Return the unreduced two-coupling beta vector from main Eq. (2)."""

    coupling_lambda = _finite(lambda_value, "lambda_value")
    coupling_xi = _finite(xi_value, "xi_value")
    if coupling_lambda < 0.0 or coupling_xi < 0.0:
        raise ValueError("the audited branch requires non-negative couplings")
    loop_factor = (4.0 * math.pi) ** 2
    beta_xi = -(
        coupling_xi**2
        - 36.0 * coupling_lambda * coupling_xi
        - 2520.0 * coupling_lambda**2
    ) / (36.0 * loop_factor)
    beta_lambda = -(
        (
            (1617.0 + 90.0 * parameters.n_matter) * coupling_lambda
            - 20.0 * coupling_xi
        )
        * coupling_lambda
        / (90.0 * loop_factor)
    )
    return beta_lambda, beta_xi


def _relative_vector_residual(
    actual: tuple[float, float], expected: tuple[float, float]
) -> float:
    residual = math.hypot(actual[0] - expected[0], actual[1] - expected[1])
    scale = max(math.hypot(actual[0], actual[1]), 1e-300)
    return residual / scale


def trajectory_identity_residual(t: float, parameters: SourceParameters) -> float:
    lambda_value, xi_value = trajectory_state(t, parameters)
    return lambda_value / parameters.lambda_0 + xi_value / parameters.xi_infinity - 1.0


def log_psi_squared(t: float) -> float:
    """Apply the preregistered source scale map: ``L=ln(psi^2)=4t``."""

    return 4.0 * _time(t, positive=True)


def observable_denominator(t: float, parameters: SourceParameters) -> float:
    log_psi_sq = log_psi_squared(t)
    return parameters.b * log_psi_sq**2 + 4.0 * (log_psi_sq - 2.0)


def tensor_to_scalar_ratio(t: float, parameters: SourceParameters) -> float:
    """Return the source's model-bound tensor-to-scalar ratio, Eq. (26)."""

    checked_t = _time(t, positive=True)
    if checked_t < end_time(parameters) * (1.0 - 1e-13):
        raise ValueError("the preregistered observable window begins at t_end")
    denominator = observable_denominator(checked_t, parameters)
    if denominator <= 0.0:
        raise ValueError("observable denominator must be positive")
    return (32.0 / denominator) ** 2 / 3.0


def projected_response(t: float, parameters: SourceParameters) -> float:
    """Normalize the source observable between its two fixed finite anchors."""

    return 1.0 - tensor_to_scalar_ratio(t, parameters) / 8.0


def projected_response_derivative(t: float, parameters: SourceParameters) -> float:
    """Return ``dx_r/dt`` analytically on the preregistered scale branch."""

    checked_t = _time(t, positive=True)
    if checked_t <= end_time(parameters):
        raise ValueError("the open projected response starts above t_end")
    denominator = observable_denominator(checked_t, parameters)
    denominator_derivative = 32.0 * parameters.b * checked_t + 16.0
    return 256.0 * denominator_derivative / (3.0 * denominator**3)


def dprime_quotient(t: float, parameters: SourceParameters) -> float:
    """Return ``(dx_r/dt)/(1-x_r^2)`` on the open response interval."""

    response = projected_response(t, parameters)
    if not -1.0 < response < 1.0:
        raise ValueError("D-prime quotient requires -1 < x_r < 1")
    return projected_response_derivative(t, parameters) / (1.0 - response**2)


def dprime_closed_form(t: float, parameters: SourceParameters) -> float:
    """Return the algebraically reduced projective generator witness."""

    checked_t = _time(t, positive=True)
    if checked_t <= end_time(parameters):
        raise ValueError("D-prime quotient requires t > t_end")
    denominator = observable_denominator(checked_t, parameters)
    denominator_derivative = 32.0 * parameters.b * checked_t + 16.0
    anchor_constant = 128.0 / 3.0
    return (
        2.0
        * denominator_derivative
        * denominator
        / (2.0 * denominator**2 - anchor_constant)
    )


def _cases() -> list[SourceParameters]:
    return [
        SourceParameters(b=b, n_matter=n_matter)
        for b in B_GRID
        for n_matter in N_MATTER_GRID
    ]


def build_trajectory_rows() -> list[dict[str, float | int]]:
    rows: list[dict[str, float | int]] = []
    for parameters in _cases():
        t_end = end_time(parameters)
        for multiplier in TRAJECTORY_MULTIPLIERS:
            t = multiplier * t_end
            lambda_value, xi_value = trajectory_state(t, parameters)
            tangent = trajectory_tangent(t, parameters)
            reduced_beta = reduced_large_n_beta(lambda_value, parameters)
            full_beta = full_source_beta(lambda_value, xi_value, parameters)
            r_value = tensor_to_scalar_ratio(t, parameters)
            response = 1.0 - r_value / 8.0
            xi_only_response = 2.0 * xi_value / parameters.xi_infinity - 1.0
            coupling_contrast = (
                xi_value / parameters.xi_infinity
                - lambda_value / parameters.lambda_0
            )
            rows.append(
                {
                    "b": parameters.b,
                    "n_matter": parameters.n_matter,
                    "lambda_0": parameters.lambda_0,
                    "xi_infinity": parameters.xi_infinity,
                    "t_end": t_end,
                    "t_multiplier": multiplier,
                    "t": t,
                    "lambda": lambda_value,
                    "xi": xi_value,
                    "d_lambda_dt": tangent[0],
                    "d_xi_dt": tangent[1],
                    "reduced_beta_lambda": reduced_beta[0],
                    "reduced_beta_xi": reduced_beta[1],
                    "full_beta_lambda": full_beta[0],
                    "full_beta_xi": full_beta[1],
                    "trajectory_identity_residual": trajectory_identity_residual(
                        t, parameters
                    ),
                    "reduced_vector_residual": _relative_vector_residual(
                        tangent, reduced_beta
                    ),
                    "full_vector_residual": _relative_vector_residual(
                        tangent, full_beta
                    ),
                    "tensor_to_scalar_ratio": r_value,
                    "projected_response_x_r": response,
                    "prior_xi_only_response": xi_only_response,
                    "two_coupling_contrast": coupling_contrast,
                }
            )
    return rows


def build_dprime_rows() -> list[dict[str, float | int]]:
    rows: list[dict[str, float | int]] = []
    for parameters in _cases():
        t_end = end_time(parameters)
        for multiplier in DPRIME_MULTIPLIERS:
            t = multiplier * t_end
            quotient = dprime_quotient(t, parameters)
            closed_form = dprime_closed_form(t, parameters)
            rows.append(
                {
                    "b": parameters.b,
                    "n_matter": parameters.n_matter,
                    "t_end": t_end,
                    "t_multiplier": multiplier,
                    "t": t,
                    "lambda": trajectory_state(t, parameters)[0],
                    "xi": trajectory_state(t, parameters)[1],
                    "tensor_to_scalar_ratio": tensor_to_scalar_ratio(t, parameters),
                    "projected_response_x_r": projected_response(t, parameters),
                    "dx_r_dt": projected_response_derivative(t, parameters),
                    "dprime_quotient": quotient,
                    "dprime_closed_form": closed_form,
                    "closed_form_residual": quotient - closed_form,
                }
            )
    return rows


def run_audit() -> dict[str, object]:
    trajectory_rows = build_trajectory_rows()
    dprime_rows = build_dprime_rows()

    max_identity = max(abs(float(row["trajectory_identity_residual"])) for row in trajectory_rows)
    max_reduced_residual = max(float(row["reduced_vector_residual"]) for row in trajectory_rows)
    max_full_residual = max(float(row["full_vector_residual"]) for row in trajectory_rows)
    max_closed_form_residual = max(abs(float(row["closed_form_residual"])) for row in dprime_rows)
    max_contrast_residual = max(
        abs(float(row["two_coupling_contrast"]) - float(row["prior_xi_only_response"]))
        for row in trajectory_rows
    )
    max_projection_difference = max(
        abs(float(row["projected_response_x_r"]) - float(row["prior_xi_only_response"]))
        for row in trajectory_rows
    )

    case_summaries: list[dict[str, float | int | bool]] = []
    for parameters in _cases():
        trajectory_case = [
            row
            for row in trajectory_rows
            if row["b"] == parameters.b and row["n_matter"] == parameters.n_matter
        ]
        dprime_case = [
            row
            for row in dprime_rows
            if row["b"] == parameters.b and row["n_matter"] == parameters.n_matter
        ]
        quotient_values = [float(row["dprime_quotient"]) for row in dprime_case]
        quotient_mean = sum(quotient_values) / len(quotient_values)
        relative_spread = (max(quotient_values) - min(quotient_values)) / max(
            abs(quotient_mean), 1e-300
        )
        case_summaries.append(
            {
                "b": parameters.b,
                "n_matter": parameters.n_matter,
                "lambda_0": parameters.lambda_0,
                "t_end": end_time(parameters),
                "max_full_vector_residual": max(
                    float(row["full_vector_residual"]) for row in trajectory_case
                ),
                "dprime_relative_spread": relative_spread,
                "dprime_constant": relative_spread <= DPRIME_CONSTANCY_TOLERANCE,
            }
        )

    first_parameters = _cases()[0]
    r_end = tensor_to_scalar_ratio(end_time(first_parameters), first_parameters)
    x_end = projected_response(end_time(first_parameters), first_parameters)
    dprime_constant_numerically = all(
        bool(summary["dprime_constant"]) for summary in case_summaries
    )
    dprime_constant_analytically = False
    dprime_pass = dprime_constant_numerically and dprime_constant_analytically

    checks = {
        "full_two_coordinate_rows": all(
            "lambda" in row and "xi" in row for row in trajectory_rows + dprime_rows
        ),
        "trajectory_identity": max_identity <= IDENTITY_TOLERANCE,
        "reduced_ode": max_reduced_residual <= REDUCED_ODE_TOLERANCE,
        "full_beta_window": max_full_residual <= FULL_BETA_TOLERANCE,
        "observable_end_anchor_r_16": math.isclose(r_end, 16.0, rel_tol=1e-12, abs_tol=1e-12),
        "observable_end_anchor_x_minus_1": math.isclose(x_end, -1.0, rel_tol=1e-12, abs_tol=1e-12),
        "observable_uv_limit_r_0": True,
        "observable_uv_limit_x_plus_1": True,
        "dprime_closed_form": max_closed_form_residual <= 1e-12,
        "dprime_constant_numerically": dprime_constant_numerically,
        "dprime_constant_analytically": dprime_constant_analytically,
        "dprime_pass": dprime_pass,
        "exact_binary_observable_composition_source_defined": False,
        "paper5_claim_pass": False,
    }

    return {
        "candidate": asdict(CandidateAudit()),
        "run_date": RUN_DATE,
        "status": STATUS,
        "preregistration": {
            "path": PREREGISTRATION,
            "commit": PREREGISTRATION_COMMIT,
            "frozen_before_execution": True,
        },
        "source": SOURCE,
        "parameter_grid": {
            "b": list(B_GRID),
            "n_matter": list(N_MATTER_GRID),
            "trajectory_multipliers": list(TRAJECTORY_MULTIPLIERS),
            "dprime_multipliers": list(DPRIME_MULTIPLIERS),
        },
        "formulae": {
            "trajectory": [
                "lambda=lambda_0/(1+b*t)",
                "xi=35*lambda_0^2*t/(8*pi^2*(1+b*t))",
            ],
            "trajectory_identity": "lambda/lambda_0 + xi/xi_infinity = 1",
            "scale_map": "L=ln(psi^2)=4*t",
            "observable": "r=(1/3)*(32/(b*L^2+4*(L-2)))^2",
            "normalization": "x_r=1-r/8",
            "dprime_closed_form": (
                "G_r=2*D_dot*D/(2*D^2-128/3), "
                "D=16*b*t^2+16*t-8"
            ),
        },
        "tolerances": {
            "trajectory_identity": IDENTITY_TOLERANCE,
            "reduced_ode": REDUCED_ODE_TOLERANCE,
            "full_beta_window": FULL_BETA_TOLERANCE,
            "dprime_constancy": DPRIME_CONSTANCY_TOLERANCE,
        },
        "maxima": {
            "trajectory_identity_residual": max_identity,
            "reduced_vector_residual": max_reduced_residual,
            "full_vector_residual": max_full_residual,
            "dprime_closed_form_residual": max_closed_form_residual,
            "coupling_contrast_vs_prior_xi_residual": max_contrast_residual,
            "r_projection_vs_prior_xi_difference": max_projection_difference,
        },
        "checks": checks,
        "case_summaries": case_summaries,
        "trajectory_rows": trajectory_rows,
        "dprime_rows": dprime_rows,
        "projection_audit": {
            "source_observable": "tensor-to-scalar ratio r",
            "orbit_dimension": 1,
            "ambient_coupling_dimension": 2,
            "flrw_weyl_squared_term": "vanishes_on_source_background",
            "coupling_contrast_equals_prior_xi_normalization": max_contrast_residual <= 1e-12,
            "r_projection_equals_prior_xi_normalization": max_projection_difference <= 1e-12,
            "independent_two_dimensional_observable_composition": False,
        },
        "analytic_limits": {
            "at_t_end": {"r": 16.0, "x_r": -1.0, "dprime": "diverges_from_interior"},
            "as_t_to_infinity": {"r": 0.0, "x_r": 1.0, "dprime": 0.0},
        },
        "claim_boundary": [
            "The trajectory is a large-matter one-loop approximation, not a nonperturbative solution.",
            "The source states that the physical beta functions remain debated.",
            "The fixed map mu=sqrt(abs(R)) is one ambiguous covariant scale choice.",
            "FLRW removes the Weyl-squared background direction, so the observable projection is rank one.",
            "The source defines no exact nonperturbative binary composition law for r.",
            "No Paper V or CRM claim is upgraded.",
        ],
    }


def _write_text(path: Path, content: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError("cannot write an empty CSV")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def _markdown_report(report: dict[str, object]) -> str:
    candidate = report["candidate"]
    checks = report["checks"]
    maxima = report["maxima"]
    projection = report["projection_audit"]
    summaries = report["case_summaries"]
    assert isinstance(candidate, dict)
    assert isinstance(checks, dict)
    assert isinstance(maxima, dict)
    assert isinstance(projection, dict)
    assert isinstance(summaries, list)

    lines = [
        "# LQA full two-coupling trajectory and tensor-projection D' gate",
        "",
        f"- Candidate: `{candidate['candidate_id']}`",
        f"- Status: `{report['status']}`",
        f"- Claim pass: `{str(candidate['claim_pass']).lower()}`",
        f"- Preregistration commit: `{report['preregistration']['commit']}`",
        "",
        "## Frozen source branch",
        "",
        "The audit retains the complete large-matter source trajectory",
        "`z(t)=(lambda(t),xi(t))` from Supplemental Eq. (9) and evaluates the",
        "source's tensor-to-scalar ratio `r` from Supplemental Eq. (26) on the",
        "fixed scale map `mu=sqrt(abs(R))`. No coordinate is discarded.",
        "",
        "## Gate result",
        "",
        "| Gate | Result | Maximum residual |",
        "|---|---|---:|",
        f"| Complete two-coordinate rows | `{checks['full_two_coordinate_rows']}` | -- |",
        f"| Trajectory identity | `{checks['trajectory_identity']}` | `{maxima['trajectory_identity_residual']:.3e}` |",
        f"| Reduced large-N ODE | `{checks['reduced_ode']}` | `{maxima['reduced_vector_residual']:.3e}` |",
        f"| Full Eq. (2) window diagnostic | `{checks['full_beta_window']}` | `{maxima['full_vector_residual']:.3e}` |",
        f"| Tensor-r finite anchors | `{checks['observable_end_anchor_r_16'] and checks['observable_end_anchor_x_minus_1']}` | -- |",
        f"| D' quotient constant | `{checks['dprime_pass']}` | -- |",
        f"| Exact binary observable C source-defined | `{checks['exact_binary_observable_composition_source_defined']}` | -- |",
        f"| Paper V claim pass | `{checks['paper5_claim_pass']}` | -- |",
        "",
        "## Frozen-grid summaries",
        "",
        "| b | N_m | lambda_0 | max full-beta residual | D' relative spread |",
        "|---:|---:|---:|---:|---:|",
    ]
    for summary in summaries:
        assert isinstance(summary, dict)
        lines.append(
            "| {b:.1f} | {n_matter:d} | {lambda_0:.6e} | "
            "{max_full_vector_residual:.3e} | {dprime_relative_spread:.3e} |".format(
                **summary
            )
        )
    lines.extend(
        [
            "",
            "## D' decision",
            "",
            "With `D=16*b*t^2+16*t-8`, the projective generator is",
            "`G_r=2*D_dot*D/(2*D^2-128/3)`. It depends explicitly on `t`,",
            "diverges when approached from the inflation-end anchor, and tends",
            "to zero in the deep-UV limit. The source observable therefore fails",
            "D' throughout every preregistered parameter case.",
            "",
            "## Projection and claim boundary",
            "",
            f"The ambient coupling space is two-dimensional, but the audited orbit has dimension `{projection['orbit_dimension']}`.",
            "The source's homogeneous/isotropic background removes the",
            "Weyl-squared contribution. The synthetic two-coupling contrast",
            "collapses exactly to the prior xi-only normalization; the physical",
            "tensor-r projection is different, but remains a rank-one trajectory",
            "projection. No independent two-dimensional observable composition is",
            "obtained, and the source supplies no exact nonperturbative binary law",
            "for `r`. The result is model- and scale-map-bound and cannot be booked",
            "as physical D' or as a Paper V/CRM claim.",
            "",
            "## Primary source",
            "",
            "- Liu, Quintin, and Afshordi, Physical Review Letters 136, 111501",
            "  (2026): [DOI](https://doi.org/10.1103/6gtx-j455),",
            "  [arXiv](https://arxiv.org/abs/2510.18733).",
            "",
        ]
    )
    return "\n".join(lines)


def write_artifacts(output_dir: Path) -> list[Path]:
    report = run_audit()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{ARTIFACT_STEM}.json"
    trajectory_csv_path = output_dir / f"{ARTIFACT_STEM}_trajectory.csv"
    dprime_csv_path = output_dir / f"{ARTIFACT_STEM}_dprime.csv"
    md_path = output_dir / f"{ARTIFACT_STEM}.md"

    _write_text(json_path, json.dumps(report, indent=2, sort_keys=True) + "\n")
    _write_csv(trajectory_csv_path, report["trajectory_rows"])
    _write_csv(dprime_csv_path, report["dprime_rows"])
    _write_text(md_path, _markdown_report(report))
    return [json_path, trajectory_csv_path, dprime_csv_path, md_path]


def _default_output_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "results" / "paper5"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=_default_output_dir())
    args = parser.parse_args(argv)

    paths = write_artifacts(args.output_dir)
    report = run_audit()
    print(f"{report['status']} claim_pass={report['candidate']['claim_pass']}")
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
