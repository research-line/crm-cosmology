"""Audit the exact projective law in integrable Ising-defect fusion.

He, Jiang, and Liu define fusion as the short-distance limit ``ma -> 0``
of two non-topological Ising defects.  Their exact amplitudes close on the
same defect family, with

    g_f = (g_1 + g_2) / (1 + g_1 g_2 / 4).

Consequently ``x = g/2`` obeys the projective law
``x_f = (x_1 + x_2)/(1 + x_1 x_2)`` and the marked quotient
``(1+x)/(1-x)`` multiplies exactly.  This is a source-defined physical fusion
control, unlike an audit-induced scattering composition.

It does not yet close Paper V's physical D-prime gate.  The audited source
restricts the no-bound-state branch to ``0 <= g <= 2``; ``x`` is a static
defect-coupling label rather than a signed running scalar response; and the
source explicitly leaves open when defect fusion can be interpreted as an RG
flow.  The scales ``ma`` and ``mR`` do not define ``g(mu)`` or an additive RG
scale homomorphism.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Sequence


AUDIT_ID = "CRM5-DPRIME-INTEGRABLE-DEFECT-FUSION-SOURCE-SEARCH-V1"
RUN_DATE = "2026-08-26"
STATUS = (
    "EXACT_SOURCE_DEFINED_ISING_DEFECT_FUSION_DPRIME_SEMIGROUP__"
    "RG_RUNNING_AND_SIGNED_CHANNEL_NOT_SOURCE_DEFINED"
)
OUTPUT_FILENAME = "DPRIME_INTEGRABLE_DEFECT_FUSION_GATE_2026-08-26.json"


def _check_source_branch_coupling(coupling: float) -> None:
    if not 0.0 <= coupling <= 2.0:
        raise ValueError("the audited no-bound-state branch requires 0 <= g_I <= 2")


def ising_defect_angle(coupling: float) -> float:
    """Return the source branch chi=-2 arctan(g_I/2)."""

    _check_source_branch_coupling(coupling)
    return -2.0 * math.atan(coupling / 2.0)


def fuse_defect_couplings(left: float, right: float) -> float:
    """Return the exact fused Ising-defect coupling in source Eq. (3.23)."""

    _check_source_branch_coupling(left)
    _check_source_branch_coupling(right)
    return (left + right) / (1.0 + left * right / 4.0)


def normalized_coupling(coupling: float) -> float:
    """Normalize the audited positive branch to x=g_I/2 in [0,1]."""

    _check_source_branch_coupling(coupling)
    return coupling / 2.0


def fuse_normalized_couplings(left: float, right: float) -> float:
    """Return x_f=(x_1+x_2)/(1+x_1*x_2) on the positive semigroup."""

    if not 0.0 <= left <= 1.0 or not 0.0 <= right <= 1.0:
        raise ValueError("the audited normalized branch requires 0 <= x <= 1")
    return (left + right) / (1.0 + left * right)


def marked_projective_ratio(response: float) -> float:
    """Return Paper V's marked projective quotient for an interior x."""

    if not 0.0 <= response < 1.0:
        raise ValueError("the finite quotient requires 0 <= x < 1")
    return (1.0 + response) / (1.0 - response)


def dprime_defect(left: float, right: float) -> float:
    """Return the exact-log quotient defect for the source fusion law."""

    fused = fuse_normalized_couplings(left, right)
    return (
        math.log(marked_projective_ratio(fused))
        - math.log(marked_projective_ratio(left))
        - math.log(marked_projective_ratio(right))
    )


def transmission_amplitude(theta: float, coupling: float) -> complex:
    """Return the exact parity-invariant Ising-defect transmission amplitude."""

    chi = ising_defect_angle(coupling)
    if coupling == 0.0:
        return 1.0 + 0.0j
    denominator = math.sinh(theta) - 1j * math.sin(chi)
    return math.cos(chi) * math.sinh(theta) / denominator


def reflection_amplitude(theta: float, coupling: float) -> complex:
    """Return the exact parity-invariant Ising-defect reflection amplitude."""

    chi = ising_defect_angle(coupling)
    if coupling == 0.0:
        return 0.0 + 0.0j
    denominator = math.sinh(theta) - 1j * math.sin(chi)
    return 1j * math.sin(chi) * math.cosh(theta) / denominator


def fused_amplitudes(theta: float, left: float, right: float) -> tuple[complex, complex]:
    """Return the exact multiple-scattering fusion amplitudes at ma=0."""

    transmission_left = transmission_amplitude(theta, left)
    transmission_right = transmission_amplitude(theta, right)
    reflection_left = reflection_amplitude(theta, left)
    reflection_right = reflection_amplitude(theta, right)
    denominator = 1.0 - reflection_left * reflection_right
    transmission = transmission_left * transmission_right / denominator
    reflection = reflection_left + (
        transmission_left**2 * reflection_right / denominator
    )
    return transmission, reflection


def reflection_probability(theta: float, coupling: float) -> float:
    """Return the measurable single-channel reflection probability |R|^2."""

    return abs(reflection_amplitude(theta, coupling)) ** 2


def _complex_pair(value: complex) -> list[float]:
    return [float(value.real), float(value.imag)]


def _composition_sample(left: float, right: float) -> dict[str, float]:
    fused = fuse_normalized_couplings(left, right)
    quotient_fused = marked_projective_ratio(fused)
    quotient_product = marked_projective_ratio(left) * marked_projective_ratio(right)
    return {
        "x_left": left,
        "x_right": right,
        "x_fused": fused,
        "quotient_fused": quotient_fused,
        "quotient_product": quotient_product,
        "quotient_absolute_error": abs(quotient_fused - quotient_product),
        "Dprime_defect": dprime_defect(left, right),
    }


def _amplitude_sample(theta: float, left: float, right: float) -> dict[str, object]:
    fused_coupling = fuse_defect_couplings(left, right)
    fused_transmission, fused_reflection = fused_amplitudes(theta, left, right)
    expected_transmission = transmission_amplitude(theta, fused_coupling)
    expected_reflection = reflection_amplitude(theta, fused_coupling)
    return {
        "theta": theta,
        "g_left": left,
        "g_right": right,
        "g_fused": fused_coupling,
        "fused_transmission": _complex_pair(fused_transmission),
        "single_defect_transmission": _complex_pair(expected_transmission),
        "transmission_absolute_error": abs(fused_transmission - expected_transmission),
        "fused_reflection": _complex_pair(fused_reflection),
        "single_defect_reflection": _complex_pair(expected_reflection),
        "reflection_absolute_error": abs(fused_reflection - expected_reflection),
    }


def build_report() -> dict[str, object]:
    composition_samples = [
        _composition_sample(left, right)
        for left, right in ((0.15, 0.25), (0.4, 0.35), (0.72, 0.18))
    ]
    amplitude_samples = [
        _amplitude_sample(theta, left, right)
        for theta, left, right in ((-1.3, 0.4, 0.8), (0.7, 1.0, 0.6), (2.2, 1.4, 0.3))
    ]
    boundary_theta = 0.8
    transparent_transmission = transmission_amplitude(boundary_theta, 0.0)
    transparent_reflection = reflection_amplitude(boundary_theta, 0.0)
    reflective_transmission = transmission_amplitude(boundary_theta, 2.0)
    reflective_reflection = reflection_amplitude(boundary_theta, 2.0)

    probability_theta = 0.7
    probability_left_coupling = 0.8
    probability_right_coupling = 0.6
    probability_fused_coupling = fuse_defect_couplings(
        probability_left_coupling, probability_right_coupling
    )
    probability_left = reflection_probability(probability_theta, probability_left_coupling)
    probability_right = reflection_probability(probability_theta, probability_right_coupling)
    probability_fused = reflection_probability(probability_theta, probability_fused_coupling)
    probability_odds_left = probability_left / (1.0 - probability_left)
    probability_odds_right = probability_right / (1.0 - probability_right)
    probability_odds_fused = probability_fused / (1.0 - probability_fused)
    probability_Dprime_defect = (
        math.log(probability_odds_fused)
        - math.log(probability_odds_left)
        - math.log(probability_odds_right)
    )

    return {
        "audit_id": AUDIT_ID,
        "schema_version": "1.0.0",
        "run_date": RUN_DATE,
        "todo_source": "CRM-V TODO.md:95-102",
        "status": STATUS,
        "search_contract": {
            "new_source_family": "integrable line-defect fusion in two-dimensional Ising field theory",
            "screened_primary_sources": 2,
            "excluded_reuse": [
                "local six-source quadratic-gravity corpus",
                "Bjorken effective-charge CSR transitivity",
                "2D Yang-Mills heat-kernel control",
                "FQHE conductance and generic scattering-star-product controls",
                "massless minimal-model RG-flow scattering amplitude",
                "RH project",
                "abc project",
            ],
        },
        "candidate": {
            "candidate_id": "NON_TOPOLOGICAL_ISING_DEFECT_FUSION",
            "theory": "massive Ising field theory with a parity-invariant integrable line defect",
            "source_operation": "short-distance defect fusion ma -> 0",
            "physical_data": "exact reflection and transmission amplitudes",
            "source_coupling_law": "g_I,f=(g_I,1+g_I,2)/(1+g_I,1*g_I,2/4)",
            "normalized_law": "x_f=(x_1+x_2)/(1+x_1*x_2), x=g_I/2",
            "source_branch": {
                "coupling_domain": "0 <= g_I <= 2",
                "normalized_domain": "0 <= x <= 1",
                "reason": "the source excludes negative g_I because it produces a bound state",
                "neutral_element": "g_I=0 gives T=1 and R=0",
                "upper_boundary": "g_I=2 is purely reflective",
                "full_signed_reversible_channel": False,
            },
            "scale_variables": {
                "fusion_separation": "ma, with fusion defined by ma -> 0",
                "finite_size_TBA_scale": "mR",
                "source_defined_running_coupling": None,
                "source_defined_additive_RG_time_for_fusion": None,
            },
            "criteria": {
                "exact_nonperturbative_scattering_data": "SUPPORTED",
                "source_defined_exact_binary_physical_fusion": "SUPPORTED",
                "source_defined_neutral_transparent_defect": "SUPPORTED_BY_EXACT_AMPLITUDES",
                "projective_quotient_on_normalized_coupling": "EXACT_ON_POSITIVE_SEMIGROUP",
                "two_sided_signed_response_interval": "NOT_SOURCE_AUDITED",
                "coupling_is_running_scalar_response": "NOT_SOURCE_DEFINED",
                "fusion_is_RG_semigroup": "EXPLICITLY_LEFT_OPEN_BY_SOURCE",
                "declared_scale_map_to_running_coupling": "NOT_SOURCE_DEFINED",
                "scalar_observable_inherits_projective_law": "NOT_ESTABLISHED",
                "gauge_status": "NON_GAUGE_ISING_FIELD_THEORY__NO_GAUGE_PARAMETER",
                "IR_status": "EXACT_1PLUS1D_ELASTIC_DEFECT_SCATTERING__NO_4D_IR_TRANSFER",
            },
        },
        "exact_projective_semigroup_control": {
            "marked_quotient": "R_D(x)=(1+x)/(1-x)",
            "exact_identity": "R_D(x_f)=R_D(x_1)R_D(x_2)",
            "abel_coordinate": "artanh(x_f)=artanh(x_1)+artanh(x_2)",
            "source_defined_composition": True,
            "positive_semigroup_Dprime_pass": True,
            "full_Paper_V_Dprime_pass": False,
            "samples": composition_samples,
            "maximum_quotient_error": max(
                float(row["quotient_absolute_error"]) for row in composition_samples
            ),
            "maximum_absolute_Dprime_defect": max(
                abs(float(row["Dprime_defect"])) for row in composition_samples
            ),
        },
        "amplitude_closure_control": {
            "source_formulas": {
                "transmission": "T_f=T_1*T_2/(1-R_1*R_2)",
                "reflection": "R_f=R_1+T_1^2*R_2/(1-R_1*R_2)",
            },
            "same_family_closure": True,
            "samples": amplitude_samples,
            "maximum_amplitude_error": max(
                max(
                    float(row["transmission_absolute_error"]),
                    float(row["reflection_absolute_error"]),
                )
                for row in amplitude_samples
            ),
        },
        "boundary_control": {
            "probe_theta": boundary_theta,
            "g_I_0": {
                "transmission": _complex_pair(transparent_transmission),
                "reflection": _complex_pair(transparent_reflection),
                "interpretation": "transparent neutral defect",
            },
            "g_I_2": {
                "transmission": _complex_pair(reflective_transmission),
                "reflection": _complex_pair(reflective_reflection),
                "reflection_probability": abs(reflective_reflection) ** 2,
                "interpretation": "purely reflective boundary of the audited branch",
            },
            "topology_gate": (
                "the neutral response is the lower endpoint of the audited positive branch, "
                "not an interior mark between two source-audited response boundaries"
            ),
        },
        "scalar_observable_transfer_control": {
            "observable": "fixed-rapidity reflection probability p_R=|R(theta,g_I)|^2",
            "theta": probability_theta,
            "g_inputs": [probability_left_coupling, probability_right_coupling],
            "g_fused": probability_fused_coupling,
            "p_left": probability_left,
            "p_right": probability_right,
            "p_fused": probability_fused,
            "signed_endpoint_normalization": "y=2*p_R-1",
            "marked_quotient": "(1+y)/(1-y)=p_R/(1-p_R)",
            "quotient_fused": probability_odds_fused,
            "quotient_product": probability_odds_left * probability_odds_right,
            "Dprime_defect": probability_Dprime_defect,
            "neutral_location": "p_R(g_I=0)=0 is an endpoint, not an interior signed identity",
            "projective_law_inherited": False,
            "reason": (
                "the exact projective law is on the coupling label x=g_I/2; the source does "
                "not identify x with the scalar probability or defect g-function"
            ),
        },
        "RG_transfer_gate": {
            "fusion_definition": "ma -> 0 at fixed defect labels",
            "finite_size_response": "the defect g-function depends on mR",
            "missing_beta_function": "no source equation beta_I(g_I)=d g_I/d log(mu)",
            "missing_homomorphism": "no source map from additive RG time to repeated fusion",
            "source_open_question": (
                "the source asks when fusion can be interpreted as an RG flow"
            ),
            "pass": False,
        },
        "source_registry": {
            "HE_JIANG_LIU_2026": {
                "kind": "external_primary_preprint",
                "citation": (
                    "Yang He, Yunfeng Jiang, and Yuxiao Liu, Fusion of Integrable Defects "
                    "and the Defect g-Function, arXiv:2605.20688v1 (2026)"
                ),
                "url": "https://arxiv.org/abs/2605.20688",
                "supports": [
                    "fusion as the ma -> 0 short-distance limit",
                    "exact effective reflection and transmission amplitudes in Eq. (3.20)",
                    "same-family Ising coupling law in Eq. (3.23)",
                    "positive coupling branch and purely reflective g_I=2 endpoint",
                    "mR-dependent defect g-function and the open fusion-versus-RG question",
                ],
            },
            "DELFINO_MUSSARDO_SIMONETTI_1994": {
                "kind": "external_primary_historical",
                "citation": (
                    "G. Delfino, G. Mussardo, and P. Simonetti, Scattering Theory and "
                    "Correlation Functions in Statistical Models with a Line of Defect, "
                    "Nuclear Physics B 432 (1994) 518-550"
                ),
                "url": "https://arxiv.org/abs/hep-th/9409076",
                "doi": "https://doi.org/10.1016/0550-3213(94)90032-9",
                "supports": [
                    "exact Ising-defect reflection and transmission amplitudes",
                    "weak-strong coupling duality and reflecting self-dual points",
                    "multi-defect scattering setting",
                ],
            },
        },
        "summary": {
            "screened_new_source_families": 1,
            "source_defined_exact_fusion_count": 1,
            "exact_projective_positive_semigroup_count": 1,
            "complete_physical_candidate_count": 0,
            "running_coupling_gate_open_count": 1,
            "signed_reversible_channel_gate_open_count": 1,
            "scalar_observable_transfer_gate_open_count": 1,
            "physical_dprime_closed": False,
            "claim_upgrade_count": 0,
        },
        "claim_boundary": [
            "The exact D-prime algebra is retained as a source-defined positive defect-fusion semigroup control.",
            "The normalized variable x=g_I/2 is a static defect-coupling label, not a source-defined running scalar response.",
            "The audited source branch does not establish Paper V's full signed reversible interval with an interior neutral response.",
            "The spatial fusion limit ma -> 0 is not relabelled as additive RG time or as a beta-function trajectory.",
            "No physical Paper-V D-prime derivation, 4D transfer, cosmology, UV completion, RH result, or abc result is claimed.",
        ],
    }


def write_report(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_report(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _default_output() -> Path:
    return Path(__file__).resolve().parents[2] / "results" / "paper5" / OUTPUT_FILENAME


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=_default_output())
    args = parser.parse_args(argv)
    path = write_report(args.output)
    report = build_report()
    print(
        f"{report['status']} positive_semigroup_Dprime="
        f"{report['exact_projective_semigroup_control']['positive_semigroup_Dprime_pass']} "
        f"physical_candidates={report['summary']['complete_physical_candidate_count']}"
    )
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
