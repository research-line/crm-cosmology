"""Classify the smooth strict positive boundary collars used by Paper V.

The classification is deliberately limited to the positive face of a smooth,
strict, cancellative one-dimensional response law.  It does not classify
nilpotent t-conorms, noncancellative ordinal sums, multi-channel laws, or a
compactification of the mixed signed corners.  Within the declared class, a
unique boundary-defining multiplicative coordinate ``q`` exists, every law is
smoothly conjugate to the projective representative, and D-prime is exactly
the zero-gauge slice.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence


AUDIT_ID = "CRM5-SMOOTH-COLLAR-OPERATIONS-CLASSIFICATION-V1"
RUN_DATE = "2026-08-26"
STATUS = (
    "COMPLETE_WITHIN_SMOOTH_STRICT_DPM_COLLAR_CLASS__"
    "DPRIME_IS_H_ZERO__NO_UV_CLAIM"
)
OUTPUT_FILENAME = "SMOOTH_COLLAR_CLASSIFICATION_GATE_2026-08-26.json"


@dataclass(frozen=True)
class CollarProfile:
    """A finite smooth gauge h in q_h=q_0*exp(-2h)."""

    name: str
    expression: str
    h: Callable[[float], float]
    h_prime: Callable[[float], float]
    odd_extension: bool


def linear_profile(epsilon: float) -> CollarProfile:
    return CollarProfile(
        name=f"linear_eps_{epsilon:+.2f}",
        expression=f"h(x)={epsilon:.12g}*x",
        h=lambda x: epsilon * x,
        h_prime=lambda _x: epsilon,
        odd_extension=True,
    )


def cubic_profile(epsilon: float) -> CollarProfile:
    return CollarProfile(
        name=f"cubic_eps_{epsilon:+.2f}",
        expression=f"h(x)={epsilon:.12g}*x^3",
        h=lambda x: epsilon * x**3,
        h_prime=lambda x: 3.0 * epsilon * x * x,
        odd_extension=True,
    )


PROJECTIVE = linear_profile(0.0)
AUDIT_PROFILES = (
    PROJECTIVE,
    linear_profile(-0.75),
    linear_profile(0.25),
    linear_profile(1.0),
    cubic_profile(0.30),
)


def projective_collar(x: float) -> float:
    """The fixed D-prime boundary quotient inverse q_0=1/R."""

    return (1.0 - x) / (1.0 + x)


def collar_q(x: float, profile: CollarProfile) -> float:
    """Canonical boundary-defining multiplicative coordinate q_h."""

    return projective_collar(x) * math.exp(-2.0 * profile.h(x))


def collar_q_derivative(x: float, profile: CollarProfile) -> float:
    if x == 1.0:
        return -0.5 * math.exp(-2.0 * profile.h(1.0))
    q = collar_q(x, profile)
    return q * (-2.0 / (1.0 - x * x) - 2.0 * profile.h_prime(x))


def collar_inverse(value: float, profile: CollarProfile) -> float:
    """Invert the decreasing diffeomorphism q_h:[0,1]->[1,0]."""

    if not 0.0 <= value <= 1.0:
        raise ValueError("collar coordinate must lie in [0,1]")
    if value == 1.0:
        return 0.0
    if value == 0.0:
        return 1.0
    left = 0.0
    right = 1.0
    for _ in range(100):
        middle = (left + right) / 2.0
        if collar_q(middle, profile) > value:
            left = middle
        else:
            right = middle
    return (left + right) / 2.0


def compose(x: float, y: float, profile: CollarProfile) -> float:
    return collar_inverse(collar_q(x, profile) * collar_q(y, profile), profile)


def projective_compose(x: float, y: float) -> float:
    return (x + y) / (1.0 + x * y)


def canonical_kappa(profile: CollarProfile) -> float:
    """The simple-zero rate kappa=-a'(1)=-q'(0)."""

    return 2.0 * (1.0 + profile.h_prime(0.0))


def canonical_generator(x: float, profile: CollarProfile) -> float:
    """Generator a_h=q_h*q_h'(0)/q_h'."""

    numerator = (1.0 + profile.h_prime(0.0)) * (1.0 - x * x)
    denominator = 1.0 + (1.0 - x * x) * profile.h_prime(x)
    return numerator / denominator


def gauge_map_to_projective(x: float, profile: CollarProfile) -> float:
    """H_h=q_0^{-1} o q_h, conjugating C_h to projective addition."""

    q = collar_q(x, profile)
    return (1.0 - q) / (1.0 + q)


def fixed_projective_defect(x: float, y: float, profile: CollarProfile) -> float:
    composed = compose(x, y, profile)

    def log_r(value: float) -> float:
        return math.log((1.0 + value) / (1.0 - value))

    return log_r(composed) - log_r(x) - log_r(y)


def gauge_coboundary(x: float, y: float, profile: CollarProfile) -> float:
    composed = compose(x, y, profile)
    return 2.0 * (profile.h(x) + profile.h(y) - profile.h(composed))


def _maximum_residuals(profile: CollarProfile) -> dict[str, float]:
    points = (0.0, 0.07, 0.19, 0.37, 0.58, 0.79, 0.93, 1.0)
    interior = points[:-1]
    identity = 0.0
    absorbing = 0.0
    multiplicative = 0.0
    associativity = 0.0
    conjugacy = 0.0
    defect_formula = 0.0

    for x in points:
        identity = max(identity, abs(compose(x, 0.0, profile) - x))
        absorbing = max(absorbing, abs(compose(x, 1.0, profile) - 1.0))
    for x in interior:
        for y in interior:
            combined = compose(x, y, profile)
            multiplicative = max(
                multiplicative,
                abs(
                    collar_q(combined, profile)
                    - collar_q(x, profile) * collar_q(y, profile)
                ),
            )
            conjugacy = max(
                conjugacy,
                abs(
                    gauge_map_to_projective(combined, profile)
                    - projective_compose(
                        gauge_map_to_projective(x, profile),
                        gauge_map_to_projective(y, profile),
                    )
                ),
            )
            defect_formula = max(
                defect_formula,
                abs(
                    fixed_projective_defect(x, y, profile)
                    - gauge_coboundary(x, y, profile)
                ),
            )
            for z in (0.11, 0.43, 0.83):
                associativity = max(
                    associativity,
                    abs(
                        compose(combined, z, profile)
                        - compose(x, compose(y, z, profile), profile)
                    ),
                )

    return {
        "identity": identity,
        "absorbing_boundary": absorbing,
        "multiplicative_collar": multiplicative,
        "associativity": associativity,
        "projective_conjugacy": conjugacy,
        "exact_defect_coboundary": defect_formula,
    }


def _profile_audit(profile: CollarProfile) -> dict[str, object]:
    grid = [index / 2000.0 for index in range(2001)]
    admissibility_values = [
        1.0 + (1.0 - x * x) * profile.h_prime(x) for x in grid
    ]
    q_derivatives = [collar_q_derivative(x, profile) for x in grid]
    witness_x = 0.20
    witness_y = 0.35
    defect = fixed_projective_defect(witness_x, witness_y, profile)
    return {
        "name": profile.name,
        "h_expression": profile.expression,
        "odd_signed_extension": profile.odd_extension,
        "admissibility_margin": min(admissibility_values),
        "strictly_decreasing_q": max(q_derivatives) < 0.0,
        "q_at_identity": collar_q(0.0, profile),
        "q_at_boundary": collar_q(1.0, profile),
        "q_prime_at_identity": collar_q_derivative(0.0, profile),
        "q_prime_at_boundary": collar_q_derivative(1.0, profile),
        "kappa": canonical_kappa(profile),
        "generator_at_identity": canonical_generator(0.0, profile),
        "generator_at_boundary": canonical_generator(1.0, profile),
        "fixed_R_defect_at_x_0p20_y_0p35": defect,
        "D_prime_pass": abs(defect) < 1e-12,
        "maximum_residuals": _maximum_residuals(profile),
    }


def build_report() -> dict[str, object]:
    profile_audits = [_profile_audit(profile) for profile in AUDIT_PROFILES]
    return {
        "audit_id": AUDIT_ID,
        "schema_version": "1.0.0",
        "run_date": RUN_DATE,
        "status": STATUS,
        "todo_source": "CRM-V TODO.md:135-142",
        "review_source": "Paper5_HEILER_2026-07-03.md:P1-10",
        "classification_scope": {
            "positive_face": "[0,1]^2",
            "hypotheses": [
                "C is C-infinity on the closed positive square",
                "C is commutative and associative",
                "0 is neutral and 1 is absorbing",
                "C is strictly increasing on the open positive face",
                "the interior law belongs to the cancellative D-plus/minus channel",
            ],
            "excluded": [
                "nilpotent or noncancellative t-conorms",
                "ordinal sums with interior idempotents",
                "multi-channel or stochastic response laws",
                "smoothness at the mixed compactified signed corners (1,-1) and (-1,1)",
            ],
        },
        "classification_theorem": {
            "generator": "a(x)=partial_2 C(x,0)",
            "simple_boundary_zero": "a(1)=0 and kappa=-a'(1)>0",
            "normalized_abel_coordinate": "phi(x)=integral_0^x dt/a(t), phi'(0)=1",
            "canonical_collar": "q(x)=exp(-kappa*phi(x))",
            "canonical_collar_properties": (
                "q is the unique C-infinity decreasing boundary-defining "
                "diffeomorphism with q(0)=1 and q(C)=q(x)q(y)"
            ),
            "converse": "C_q(x,y)=q^{-1}(q(x)q(y))",
            "projective_relative_parameterization": (
                "q_h(x)=((1-x)/(1+x))*exp(-2h(x)); "
                "h in C-infinity[0,1], h(0)=0, "
                "1+(1-x^2)h'(x)>0"
            ),
            "signed_B_prime_condition": (
                "h admits a smooth odd extension through x=0; equivalently "
                "-log(q_h) has a smooth odd extension"
            ),
            "generator_in_h_gauge": (
                "a_h(x)=(1+h'(0))*(1-x^2)/(1+(1-x^2)h'(x))"
            ),
            "smooth_conjugacy": (
                "H_h=q_0^{-1} o q_h and "
                "H_h(C_h(x,y))=C_0(H_h(x),H_h(y))"
            ),
            "projective_slice": "D-prime holds if and only if h=0",
            "fixed_R_defect": (
                "Delta_Dprime(x,y)=2*(h(x)+h(y)-h(C_h(x,y)))"
            ),
        },
        "necessity_proof_ledger": [
            "D-plus/minus gives a(x)>0 in the interior and the Abel flow",
            "absorption gives a(1)=0",
            "if a'(1)=0, every finite-time translation has boundary derivative 1",
            "closed-square smoothness instead forces that derivative to tend to 0 at (1,1)",
            "therefore a'(1)<0 and the boundary zero is simple",
            "the regular-singular ODE a*q'=-kappa*q makes q/(1-x) smooth and positive",
            "multiplicativity follows from Abel additivity",
            "a second multiplicative boundary-defining coordinate differs by q^c; a simple zero forces c=1",
        ],
        "sufficiency_proof_ledger": [
            "a decreasing C-infinity boundary diffeomorphism q has a C-infinity inverse",
            "multiplication on [0,1] is C-infinity, commutative, associative, neutral at 1, and absorbing at 0",
            "pullback by q gives the complete smooth strict positive collar law",
        ],
        "source_binding": [
            {
                "source": "Mesiarova-Zemankova, arXiv:1506.07820 (2015), Proposition 1",
                "role": "standard continuous strict t-conorm additive-generator context",
            },
            {
                "source": "Grabisch, Marichal, Mesiar, Pap, Aggregation on bipolar scales (2009), Theorem 1",
                "role": "signed strict t-conorm extension as an Abelian group",
            },
            {
                "source": "current audit",
                "role": "C-infinity boundary simple-zero, canonical-q, h-gauge, and D-prime slice proof",
            },
        ],
        "profile_audits": profile_audits,
        "summary": {
            "complete_within_declared_smooth_strict_class": True,
            "infinite_dimensional_h_gauge_exposed": True,
            "D_prime_unique_in_marked_projective_chart": True,
            "all_collars_smoothly_conjugate": True,
            "physical_UV_selection_derived": False,
            "claim_upgrade_count": 0,
        },
        "claim_boundary": [
            "This is a mathematical classification of the declared one-dimensional smooth strict positive-face collar class.",
            "It is not a classification of every smooth associative operation on a compact interval.",
            "Smooth conjugacy does not make D-prime physically automatic; D-prime fixes the marked projective response chart.",
            "No UV derivation, cosmology result, RH result, or abc result is claimed.",
        ],
    }


def write_report(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(build_report(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def _default_output() -> Path:
    return Path(__file__).resolve().parents[2] / "results" / "paper5" / OUTPUT_FILENAME


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=_default_output())
    args = parser.parse_args(argv)
    path = write_report(args.output)
    report = build_report()
    nonprojective = [
        audit
        for audit in report["profile_audits"]
        if not audit["D_prime_pass"]
    ]
    max_residual = max(
        max(audit["maximum_residuals"].values())
        for audit in report["profile_audits"]
    )
    print(
        f"{report['status']} profiles={len(report['profile_audits'])} "
        f"nonprojective={len(nonprojective)} max_residual={max_residual:.12g}"
    )
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
