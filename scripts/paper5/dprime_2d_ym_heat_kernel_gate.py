"""Audit an exact 2D Yang--Mills Wilson-loop response against D'.

For U(1) Yang--Mills theory on the plane, the heat-kernel result for a
Wilson loop of area ``A`` and charge ``nu`` is

    w(A) = exp(-e_squared * nu**2 * A / 2) = exp(-kappa * A).

The fixed normalization ``x = 1 - 2 w`` exposes two finite response
boundaries and induces an exact binary composition.  This module checks the
composition and the projective-boundary quotient without transferring the
2D area law to a 4D scattering or renormalization-group claim.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence


CANDIDATE_ID = "CRM5-DPRIME-2DYM-HEAT-KERNEL-CANDIDATE-V1"
RUN_DATE = "2026-08-26"
STATUS = "EXACT_GAUGE_RESPONSE_COMPOSITION__DPRIME_FAIL__NOT_4D_SCATTERING_OR_RG"
DEFAULT_AREAS = (0.0, 0.25, 0.5, 1.0, 2.0, 4.0)
DEFAULT_KAPPA = 1.0
ARTIFACT_STEM = "DPRIME_2D_YM_HEAT_KERNEL_GATE_2026-08-26"

SOURCES = (
    {
        "citation": "Aroca and Kubyshin, Annals of Physics 283 (2000) 11-37",
        "doi": "https://doi.org/10.1006/aphy.2000.6044",
        "arxiv": "https://arxiv.org/abs/hep-th/9901155",
        "use": "heat-kernel formulation and exact U(1) plane area law",
    },
    {
        "citation": "Witten, Communications in Mathematical Physics 141 (1991) 153-209",
        "doi": "https://doi.org/10.1007/BF02100009",
        "use": "gauge-invariant Wilson-line framework for exact 2D Yang--Mills theory",
    },
    {
        "citation": "Nguyen, Communications in Mathematical Physics 357 (2018) 333-374",
        "doi": "https://doi.org/10.1007/s00220-017-2942-6",
        "arxiv": "https://arxiv.org/abs/1508.06305",
        "use": "rigorous continuum Wilson-loop construction via group heat kernels",
    },
)


@dataclass(frozen=True)
class CandidateAudit:
    """Claim-bounded classification of the candidate."""

    candidate_id: str = CANDIDATE_ID
    observable: str = "U(1) Wilson-loop expectation on the two-dimensional plane"
    theory_scope: str = "pure 2D U(1) Yang--Mills theory"
    gauge_invariant_physical_response: str = "supported"
    finite_distinct_response_boundaries: str = "supported"
    exact_binary_response_composition: str = "supported"
    additive_parameter: str = "supported_area"
    scattering_observable: str = "not_supported"
    renormalization_group_running: str = "not_supported_dimensionful_2d_coupling"
    dprime_projective_quotient: str = "fail_nonconstant"
    transfer_to_paper5_physical_dprime: str = "not_bookable"
    claim_pass: bool = False


def _finite_number(value: float, name: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _validate_area_kappa(area: float, kappa: float) -> tuple[float, float]:
    checked_area = _finite_number(area, "area")
    checked_kappa = _finite_number(kappa, "kappa")
    if checked_area < 0.0:
        raise ValueError("area must be non-negative")
    if checked_kappa <= 0.0:
        raise ValueError("kappa must be positive")
    return checked_area, checked_kappa


def _validate_response(response: float, name: str) -> float:
    checked = _finite_number(response, name)
    if checked < -1.0 or checked > 1.0:
        raise ValueError(f"{name} must lie in [-1, 1]")
    return checked


def wilson_response(area: float, kappa: float = DEFAULT_KAPPA) -> float:
    """Return the exact heat-kernel Wilson response ``exp(-kappa * area)``."""

    checked_area, checked_kappa = _validate_area_kappa(area, kappa)
    return math.exp(-checked_kappa * checked_area)


def normalized_response(area: float, kappa: float = DEFAULT_KAPPA) -> float:
    """Map the Wilson response to the fixed boundary interval [-1, 1]."""

    return 1.0 - 2.0 * wilson_response(area, kappa)


def compose_normalized(left: float, right: float) -> float:
    """Exact response law induced by multiplication of Wilson responses."""

    x = _validate_response(left, "left")
    y = _validate_response(right, "right")
    return 1.0 - (1.0 - x) * (1.0 - y) / 2.0


def generator(response: float, kappa: float = DEFAULT_KAPPA) -> float:
    """Return ``dx/dA = kappa * (1 - x)`` for the area flow."""

    x = _validate_response(response, "response")
    checked_kappa = _finite_number(kappa, "kappa")
    if checked_kappa <= 0.0:
        raise ValueError("kappa must be positive")
    return checked_kappa * (1.0 - x)


def dprime_quotient(response: float, kappa: float = DEFAULT_KAPPA) -> float:
    """Evaluate the D' quotient beta(x)/(1-x^2) on the open interval."""

    x = _validate_response(response, "response")
    if not -1.0 < x < 1.0:
        raise ValueError("D' quotient is defined only for -1 < response < 1")
    return generator(x, kappa) / (1.0 - x * x)


def build_rows(
    areas: Iterable[float] = DEFAULT_AREAS,
    kappa: float = DEFAULT_KAPPA,
) -> list[dict[str, float | None]]:
    """Build deterministic diagnostic rows for representative finite areas."""

    rows: list[dict[str, float | None]] = []
    for area in areas:
        checked_area, checked_kappa = _validate_area_kappa(area, kappa)
        response = wilson_response(checked_area, checked_kappa)
        normalized = 1.0 - 2.0 * response
        quotient = (
            dprime_quotient(normalized, checked_kappa)
            if -1.0 < normalized < 1.0
            else None
        )
        rows.append(
            {
                "area": checked_area,
                "wilson_response": response,
                "normalized_response": normalized,
                "generator": generator(normalized, checked_kappa),
                "dprime_quotient": quotient,
            }
        )
    return rows


def run_audit(kappa: float = DEFAULT_KAPPA) -> dict[str, object]:
    """Run analytic and numerical gates and return a serializable report."""

    _, checked_kappa = _validate_area_kappa(0.0, kappa)
    a1, a2, a3 = 0.35, 0.8, 1.25
    x1 = normalized_response(a1, checked_kappa)
    x2 = normalized_response(a2, checked_kappa)
    x3 = normalized_response(a3, checked_kappa)

    semigroup_exact = math.isclose(
        wilson_response(a1 + a2, checked_kappa),
        wilson_response(a1, checked_kappa) * wilson_response(a2, checked_kappa),
        rel_tol=1e-13,
        abs_tol=1e-15,
    )
    normalized_composition_exact = math.isclose(
        normalized_response(a1 + a2, checked_kappa),
        compose_normalized(x1, x2),
        rel_tol=1e-13,
        abs_tol=1e-15,
    )
    associative = math.isclose(
        compose_normalized(compose_normalized(x1, x2), x3),
        compose_normalized(x1, compose_normalized(x2, x3)),
        rel_tol=1e-13,
        abs_tol=1e-15,
    )
    quotient_at_zero = dprime_quotient(0.0, checked_kappa)
    quotient_at_half = dprime_quotient(0.5, checked_kappa)
    dprime_nonconstant = not math.isclose(
        quotient_at_zero,
        quotient_at_half,
        rel_tol=1e-13,
        abs_tol=1e-15,
    )

    return {
        "candidate": asdict(CandidateAudit()),
        "run_date": RUN_DATE,
        "status": STATUS,
        "formulae": {
            "kappa": "e_squared * nu_squared / 2",
            "wilson_response": "w(A) = exp(-kappa*A)",
            "normalization": "x(A) = 1 - 2*w(A)",
            "composition": "C(x,y) = 1 - (1-x)*(1-y)/2",
            "generator": "beta_x = dx/dA = kappa*(1-x)",
            "dprime_quotient": "beta_x/(1-x^2) = kappa/(1+x)",
        },
        "parameters": {"kappa": checked_kappa, "areas": list(DEFAULT_AREAS)},
        "analytic_boundaries": {
            "x_at_zero_area": -1.0,
            "x_at_infinite_area_limit": 1.0,
            "composition_identity": -1.0,
            "composition_absorber": 1.0,
        },
        "checks": {
            "wilson_semigroup": semigroup_exact,
            "normalized_composition": normalized_composition_exact,
            "composition_associative": associative,
            "finite_distinct_response_boundaries": True,
            "dprime_quotient_nonconstant": dprime_nonconstant,
            "dprime_pass": False,
            "paper5_claim_pass": False,
        },
        "dprime_witness": {
            "at_x_0": quotient_at_zero,
            "at_x_0_5": quotient_at_half,
            "identity_boundary_limit": "diverges_as_x_to_minus_1",
            "absorbing_boundary_limit": checked_kappa / 2.0,
        },
        "rows": build_rows(kappa=checked_kappa),
        "sources": list(SOURCES),
        "claim_boundary": [
            "The exact result is for pure two-dimensional U(1) Yang--Mills theory.",
            "Area is additive but is not a four-dimensional RG energy scale.",
            "The Wilson loop is a gauge response, not a scattering observable.",
            "The result does not derive physical D' for Paper V or CRM.",
        ],
    }


def _markdown_report(report: dict[str, object]) -> str:
    candidate = report["candidate"]
    checks = report["checks"]
    witness = report["dprime_witness"]
    assert isinstance(candidate, dict)
    assert isinstance(checks, dict)
    assert isinstance(witness, dict)

    lines = [
        "# 2D Yang--Mills heat-kernel D' candidate gate",
        "",
        f"- Candidate: `{candidate['candidate_id']}`",
        f"- Status: `{report['status']}`",
        f"- Claim pass: `{str(candidate['claim_pass']).lower()}`",
        "",
        "## Exact source-bound response",
        "",
        "For pure U(1) Yang--Mills theory on the plane, the heat-kernel Wilson-loop",
        "response is `w(A)=exp(-kappa*A)`, with `kappa=e_squared*nu_squared/2`.",
        "The fixed normalization `x=1-2w` gives the exact response law",
        "`C(x,y)=1-(1-x)(1-y)/2`, identity `-1`, and absorber `+1`.",
        "",
        "## Gate result",
        "",
        "| Gate | Result |",
        "|---|---|",
        f"| Exact Wilson semigroup | `{checks['wilson_semigroup']}` |",
        f"| Exact normalized composition | `{checks['normalized_composition']}` |",
        f"| Associativity | `{checks['composition_associative']}` |",
        f"| Finite distinct response boundaries | `{checks['finite_distinct_response_boundaries']}` |",
        f"| D' quotient constant | `{not checks['dprime_quotient_nonconstant']}` |",
        f"| Paper V claim pass | `{checks['paper5_claim_pass']}` |",
        "",
        "The area generator is `beta_x=kappa*(1-x)`. Therefore",
        "`beta_x/(1-x^2)=kappa/(1+x)`, which is not constant:",
        f"it equals `{witness['at_x_0']}` at `x=0` and",
        f"`{witness['at_x_0_5']}` at `x=0.5` for the audited normalization.",
        "This exact physical response composition fails D'.",
        "",
        "## Claim boundary",
        "",
        "This is a nonperturbative 2D gauge-response control case. It is not a 4D",
        "scattering observable, its additive area is not an RG energy scale, and the",
        "dimensionful 2D coupling supplies no source-bound running of this response.",
        "Nothing in this audit upgrades the conditional Paper V theorem or CRM claims.",
        "",
        "## Primary sources",
        "",
    ]
    for source in report["sources"]:
        assert isinstance(source, dict)
        links = [f"[DOI]({source['doi']})"]
        if "arxiv" in source:
            links.append(f"[arXiv]({source['arxiv']})")
        lines.append(f"- {source['citation']}: {source['use']} ({', '.join(links)}).")
    lines.append("")
    return "\n".join(lines)


def _write_text(path: Path, content: str) -> None:
    """Write UTF-8 text with stable LF endings on every supported Python."""

    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def write_artifacts(output_dir: Path, kappa: float = DEFAULT_KAPPA) -> list[Path]:
    """Write deterministic JSON, CSV, and Markdown audit artifacts."""

    report = run_audit(kappa)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{ARTIFACT_STEM}.json"
    csv_path = output_dir / f"{ARTIFACT_STEM}.csv"
    md_path = output_dir / f"{ARTIFACT_STEM}.md"

    _write_text(json_path, json.dumps(report, indent=2, sort_keys=True) + "\n")
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "area",
            "wilson_response",
            "normalized_response",
            "generator",
            "dprime_quotient",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(report["rows"])
    _write_text(md_path, _markdown_report(report))
    return [json_path, csv_path, md_path]


def _default_output_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "results" / "paper5"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kappa", type=float, default=DEFAULT_KAPPA)
    parser.add_argument("--output-dir", type=Path, default=_default_output_dir())
    args = parser.parse_args(argv)

    paths = write_artifacts(args.output_dir, args.kappa)
    report = run_audit(args.kappa)
    print(f"{report['status']} claim_pass={report['candidate']['claim_pass']}")
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
