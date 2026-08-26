"""Build the verified compact-bump separation witness for Paper V Axiom C.

The witness replaces the old oscillatory ``tanh(g) cos(epsilon g)`` sketch.
It preserves finite positive-branch capacity, the odd local expansion, the
global odd extension, and the endpoint saturation limit, while its derivative
is strictly negative at a predeclared interior point.  It does not claim the
global response homomorphism D-plus/minus, which would force monotonicity.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Callable, Sequence


AUDIT_ID = "CRM5-DPRIME-TANH-EPSILON-BUMP-C-INDEPENDENCE-SEPARATION-V1"
RUN_DATE = "2026-08-26"
STATUS = "EXACT_C_SEPARATION_WITNESS__A_B_BPRIME_ENDPOINT_PASS__DPM_NOT_CLAIMED"
OUTPUT_FILENAME = "AXIOM_C_BUMP_SEPARATION_GATE_2026-08-26.json"

CENTER = 2.0
WIDTH = 0.25
EPSILON = 1.0 / 50.0
WITNESS_G = 17.0 / 8.0


def compact_bump(z: float) -> float:
    """Normalized standard C-infinity bump with support [-1, 1]."""

    if abs(z) >= 1.0:
        return 0.0
    return math.exp(1.0 - 1.0 / (1.0 - z * z))


def compact_bump_derivative(z: float) -> float:
    """Derivative of :func:`compact_bump`, including the zero extension."""

    if abs(z) >= 1.0:
        return 0.0
    return compact_bump(z) * (-2.0 * z / (1.0 - z * z) ** 2)


def odd_bump(g: float) -> float:
    """Odd pair of translated compact bumps centered at plus/minus CENTER."""

    return compact_bump((g - CENTER) / WIDTH) - compact_bump((g + CENTER) / WIDTH)


def odd_bump_derivative(g: float) -> float:
    return (
        compact_bump_derivative((g - CENTER) / WIDTH)
        - compact_bump_derivative((g + CENTER) / WIDTH)
    ) / WIDTH


def response(g: float) -> float:
    """The frozen separation witness sigma(g)."""

    return math.tanh(g) + EPSILON * odd_bump(g)


def response_derivative(g: float) -> float:
    return 1.0 / math.cosh(g) ** 2 + EPSILON * odd_bump_derivative(g)


def _bisect_root(
    function: Callable[[float], float],
    left: float,
    right: float,
    iterations: int = 100,
) -> float:
    left_value = function(left)
    right_value = function(right)
    if left_value == 0.0:
        return left
    if right_value == 0.0:
        return right
    if left_value * right_value > 0.0:
        raise ValueError(f"root is not bracketed on [{left}, {right}]")
    for _ in range(iterations):
        midpoint = (left + right) / 2.0
        midpoint_value = function(midpoint)
        if left_value * midpoint_value <= 0.0:
            right = midpoint
        else:
            left = midpoint
            left_value = midpoint_value
    return (left + right) / 2.0


def _log_headroom_ratio_derivative(z: float) -> float:
    """Derivative of log(epsilon*b(z)/(1-tanh(2+z/4)))."""

    bump_term = -2.0 * z / (1.0 - z * z) ** 2
    deficit_term = 0.5 / (1.0 + math.exp(-(4.0 + z / 2.0)))
    return bump_term + deficit_term


def headroom_certificate() -> dict[str, float | bool | str]:
    """Return the unique positive maximizer of the bump/headroom ratio.

    For z<0 the log-ratio derivative is positive.  For z>0 its first term is
    strictly decreasing with derivative at most -2, while the logistic term's
    derivative is at most 1/16.  Hence the root bracketed below is the unique
    global maximizer on (-1, 1).
    """

    maximizing_z = _bisect_root(_log_headroom_ratio_derivative, 0.0, 0.5)
    maximizing_g = CENTER + WIDTH * maximizing_z
    ratio = EPSILON * compact_bump(maximizing_z) / (1.0 - math.tanh(maximizing_g))
    return {
        "maximizing_z": maximizing_z,
        "maximizing_g": maximizing_g,
        "maximum_bump_to_headroom_ratio": ratio,
        "strictly_below_one": ratio < 1.0,
        "uniqueness_argument": (
            "log-ratio rises on (-1,0); on (0,1) its derivative is strictly "
            "decreasing because the bump term derivative is <=-2 and the "
            "logistic correction derivative is <=1/16"
        ),
    }


def monotonicity_certificate() -> dict[str, float | bool | str | list[float]]:
    left_root = _bisect_root(response_derivative, 2.0, WITNESS_G)
    right_root = _bisect_root(response_derivative, 2.225, 2.2375)
    witness_value = response(WITNESS_G)
    witness_derivative = response_derivative(WITNESS_G)
    return {
        "witness_g": WITNESS_G,
        "witness_z": (WITNESS_G - CENTER) / WIDTH,
        "witness_response": witness_value,
        "witness_derivative": witness_derivative,
        "exact_derivative_expression": "sech(17/8)^2-(32/225)*exp(-1/3)",
        "negative_at_witness": witness_derivative < 0.0,
        "numerical_negative_interval": [left_root, right_root],
        "endpoint_saturation_retained": True,
        "limit_g_to_infinity": 1.0,
    }


def build_report() -> dict[str, object]:
    headroom = headroom_certificate()
    monotonicity = monotonicity_certificate()
    first_turning_point = monotonicity["numerical_negative_interval"][0]
    local_maximum = response(first_turning_point)

    return {
        "audit_id": AUDIT_ID,
        "schema_version": "1.0.0",
        "run_date": RUN_DATE,
        "todo_source": "CRM-V TODO.md:135-142",
        "review_source": "Paper5_HEILER_2026-07-03.md:P1-7",
        "status": STATUS,
        "witness": {
            "response": "sigma(g)=tanh(g)+(1/50)*psi(g)",
            "odd_bump": "psi(g)=b(4*(g-2))-b(4*(g+2))",
            "base_bump": "b(z)=exp(1-1/(1-z^2)) for |z|<1; b(z)=0 otherwise",
            "parameters": {
                "center": CENTER,
                "width": WIDTH,
                "epsilon": EPSILON,
            },
            "support": [
                [-CENTER - WIDTH, -CENTER + WIDTH],
                [CENTER - WIDTH, CENTER + WIDTH],
            ],
            "positive_branch_support": [CENTER - WIDTH, CENTER + WIDTH],
            "local_identity": "sigma(g)=tanh(g) for |g|<=7/4",
            "local_series": "g-g^3/3+O(g^5)",
        },
        "capacity_certificate": {
            "positive_branch_nonnegative": True,
            "outside_positive_support": "sigma(g)=tanh(g) in [0,7/4] and [9/4,infinity)",
            "headroom_ratio": headroom,
            "largest_local_response": local_maximum,
            "largest_local_response_point": first_turning_point,
            "strict_capacity_pass": bool(headroom["strictly_below_one"]),
        },
        "monotonicity_certificate": monotonicity,
        "axiom_ledger": {
            "A_finite_positive_branch_capacity": "PASS__ZERO_LE_SIGMA_LT_ONE",
            "B_local_odd_expansion_positive_slope": "PASS__IDENTICAL_TO_TANH_NEAR_ZERO",
            "B_prime_global_odd_extension": "PASS__BY_CONSTRUCTION",
            "C_monotone_control": "FAIL__SIGMA_PRIME_NEGATIVE_AT_17_OVER_8",
            "C_endpoint_saturation_clause": "PASS__COMPACT_PERTURBATION_VANISHES_AT_INFINITY",
            "D_response_composition": "NOT_CLAIMED",
            "D_plus_minus_global_group_homomorphism": "INCOMPATIBLE__NONMONOTONE_RESPONSE_IS_NONINJECTIVE",
            "D_prime_projective_quotient": "OUT_OF_SCOPE",
        },
        "summary": {
            "verified_clean_C_witness": True,
            "separates_C_from": ["A", "B", "B_prime", "endpoint_saturation"],
            "does_not_separate_C_from": ["global_D_plus_minus_homomorphism"],
            "old_tanh_cosine_example_replaced": True,
            "claim_upgrade_count": 0,
        },
        "claim_boundary": [
            "The witness proves only that A, B, B-prime, and endpoint saturation do not by themselves imply monotonicity.",
            "It is not a model satisfying the global response homomorphism D-plus/minus; that hypothesis forces monotonicity.",
            "No physical UV derivation, D-prime derivation, cosmology result, RH result, or abc result is claimed.",
        ],
    }


def write_report(path: Path) -> Path:
    report = build_report()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _default_output() -> Path:
    return Path(__file__).resolve().parents[2] / "results" / "paper5" / OUTPUT_FILENAME


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=_default_output())
    args = parser.parse_args(argv)
    path = write_report(args.output)
    report = build_report()
    certificate = report["monotonicity_certificate"]
    print(
        f"{report['status']} sigma_prime={certificate['witness_derivative']:.12g} "
        f"headroom_ratio={report['capacity_certificate']['headroom_ratio']['maximum_bump_to_headroom_ratio']:.12g}"
    )
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
