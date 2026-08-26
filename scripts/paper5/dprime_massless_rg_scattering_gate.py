"""Audit the exact massless tricritical-Ising-to-Ising scattering near-hit.

Fendley, Saleur, and Zamolodchikov give the exact mixed-chirality amplitude

    S_RL(theta) = -tanh(theta/2 - i*pi/4).

Its source-fixed kinematics imply theta = log(s/M^2), and the marked
projective quotient i(1-S)/(1+S) is identically exp(theta). This is an
algebraic D-prime near-hit, but the source's physical factorization law is the
Yang--Baxter product of pairwise scattering operators. It does not define the
induced binary response law S(theta_1+theta_2), mark S(0)=i as a physical
identity response, or identify a running scalar coupling with this complex
amplitude. The audit therefore keeps physical D-prime open.
"""

from __future__ import annotations

import argparse
import cmath
import json
import math
from pathlib import Path
from typing import Sequence


AUDIT_ID = "CRM5-DPRIME-IR-SAFE-EXACT-COMPOSITION-SOURCE-SEARCH-V2"
RUN_DATE = "2026-08-26"
STATUS = (
    "EXACT_MARKED_PROJECTIVE_AMPLITUDE_IDENTITY__"
    "PHYSICAL_C_AND_RUNNING_COUPLING_NOT_SOURCE_DEFINED"
)
OUTPUT_FILENAME = "DPRIME_MASSLESS_RG_SCATTERING_GATE_2026-08-26.json"


def massless_rl_amplitude(theta: float) -> complex:
    """Return the exact t=4 mixed-chirality massless scattering amplitude."""

    return -cmath.tanh(theta / 2.0 - 0.25j * math.pi)


def marked_projective_ratio(response: complex) -> complex:
    """Return the endpoint quotient normalized at the audit mark S(0)=i."""

    return 1j * (1.0 - response) / (1.0 + response)


def induced_rapidity_composition(left: complex, right: complex) -> complex:
    """Multiply marked ratios; this composition is audit-derived, not sourced."""

    ratio = marked_projective_ratio(left) * marked_projective_ratio(right)
    return (1.0 + 1j * ratio) / (1.0 - 1j * ratio)


def _complex_pair(value: complex) -> list[float]:
    return [float(value.real), float(value.imag)]


def _sample(theta: float) -> dict[str, object]:
    response = massless_rl_amplitude(theta)
    ratio = marked_projective_ratio(response)
    expected = math.exp(theta)
    return {
        "theta": theta,
        "s_over_M_squared": expected,
        "amplitude": _complex_pair(response),
        "amplitude_modulus": abs(response),
        "marked_ratio": _complex_pair(ratio),
        "ratio_absolute_error": abs(ratio - expected),
    }


def build_report() -> dict[str, object]:
    samples = [_sample(theta) for theta in (-6.0, -2.0, 0.0, 1.5, 5.0)]
    theta_left = -0.7
    theta_right = 1.9
    composed = induced_rapidity_composition(
        massless_rl_amplitude(theta_left), massless_rl_amplitude(theta_right)
    )
    expected_composed = massless_rl_amplitude(theta_left + theta_right)
    boundary_probe = 40.0
    lower = massless_rl_amplitude(-boundary_probe)
    upper = massless_rl_amplitude(boundary_probe)

    return {
        "audit_id": AUDIT_ID,
        "schema_version": "1.0.0",
        "run_date": RUN_DATE,
        "todo_source": "CRM-V TODO.md:95-102",
        "status": STATUS,
        "search_contract": {
            "new_source_family": "massless factorized scattering on an exact 1+1D RG flow",
            "excluded_reuse": [
                "local six-source quadratic-gravity corpus",
                "Bjorken effective-charge CSR transitivity as a physical response law",
                "2D Yang-Mills area composition as 4D scattering or RG time",
                "V1 FQHE boundary-conductance family",
                "V1 massive O(N) and quantum-graph composition controls",
                "RH project",
                "abc project",
            ],
        },
        "candidate": {
            "candidate_id": "TRICRITICAL_ISING_TO_ISING_MASSLESS_RL_AMPLITUDE",
            "theory": "unitary minimal-model flow M(4,5) to M(3,4) driven by Phi_13",
            "observable": "exact on-shell mixed-chirality two-particle amplitude S_RL(theta)",
            "source_formula": "S_RL(theta)=-tanh(theta/2-i*pi/4)",
            "equivalent_formula": "S_RL(theta)=(1+i*exp(theta))/(1-i*exp(theta))",
            "scale_map": {
                "source_momenta": "p_R=(M/2)exp(theta_R), p_L=-(M/2)exp(-theta_L)",
                "derived_lorentz_invariant": "s=M^2 exp(theta_R-theta_L)",
                "additive_coordinate": "theta=theta_R-theta_L=log(s/M^2)",
                "mass_coupling_relation": "M proportional to |delta_beta|^(5/4) for t=4",
            },
            "boundary_responses": {
                "theta_to_minus_infinity": "S_RL -> +1",
                "theta_to_plus_infinity": "S_RL -> -1",
                "finite_and_distinguishable": True,
                "probe_theta": boundary_probe,
                "probe_lower_amplitude": _complex_pair(lower),
                "probe_upper_amplitude": _complex_pair(upper),
                "probe_max_endpoint_error": max(abs(lower - 1.0), abs(upper + 1.0)),
            },
            "criteria": {
                "exact_nonperturbative_on_shell_amplitude": "SUPPORTED",
                "finite_distinct_boundary_amplitudes": "SUPPORTED",
                "declared_scale_map": "SUPPORTED_FROM_SOURCE_KINEMATICS",
                "source_defined_RG_crossover": "SUPPORTED_BY_TBA_C_FUNCTION",
                "gauge_status": "NON_GAUGE_SCALAR_QFT__NO_GAUGE_PARAMETER",
                "IR_status": "FINITE_UNIT_MODULUS_MASSLESS_INTEGRABLE_AMPLITUDE__NO_4D_INCLUSIVE_IR_SAFETY_CLAIM",
                "real_Paper_V_response_interval": "NOT_SUPPORTED__AMPLITUDE_LIES_ON_COMPLEX_UNIT_CIRCLE",
                "source_defined_neutral_identity_response": "NOT_SUPPORTED__S_RL_0_EQUALS_I_IS_AUDIT_MARKED",
                "exact_binary_response_composition": "NOT_SOURCE_DEFINED",
                "running_scalar_coupling_identified_with_response": "NOT_SOURCE_DEFINED",
            },
        },
        "marked_projective_audit": {
            "oriented_endpoints": {"b_minus": "+1", "b_plus": "-1"},
            "audit_mark": {"theta": 0.0, "response": [0.0, 1.0]},
            "normalized_ratio": "R(S)=i*(1-S)/(1+S)",
            "exact_identity": "R(S_RL(theta))=exp(theta)=s/M^2",
            "samples": samples,
            "maximum_sample_error": max(float(row["ratio_absolute_error"]) for row in samples),
            "algebraic_projective_identity_pass": True,
            "physical_Dprime_pass": False,
        },
        "induced_composition_control": {
            "definition": "C_induced(S1,S2)=R_inverse(R(S1)*R(S2))",
            "theta_inputs": [theta_left, theta_right],
            "composed_amplitude": _complex_pair(composed),
            "expected_S_of_theta_sum": _complex_pair(expected_composed),
            "absolute_error": abs(composed - expected_composed),
            "audit_identity": "S_RL(0)=i",
            "status": "EXACT_BUT_AUDIT_INDUCED__NOT_A_SOURCE_DEFINED_PHYSICAL_RESPONSE_LAW",
        },
        "physical_composition_gate": {
            "source_law": (
                "S12(theta12) S13(theta13) S23(theta23) = "
                "S23(theta23) S13(theta13) S12(theta12)"
            ),
            "source_interpretation": "Yang-Baxter consistency for a three-particle state",
            "missing_statement": "a binary law taking two response amplitudes to S_RL(theta1+theta2)",
            "category_error_blocked": (
                "pairwise operator factorization and rapidity-difference consistency are not "
                "composition of two scale responses"
            ),
            "pass": False,
        },
        "source_registry": {
            "FENDLEY_SALEUR_ZAMOLODCHIKOV_1993": {
                "kind": "external_primary",
                "citation": (
                    "Fendley, Saleur, and Zamolodchikov, Massless Flows II: "
                    "the exact S-matrix approach, International Journal of Modern Physics A 8 "
                    "(1993) 5751-5778"
                ),
                "url": "https://arxiv.org/abs/hep-th/9304051",
                "doi": "https://doi.org/10.1142/S0217751X93002277",
                "supports": [
                    "exact massless minimal-model S matrices and nonperturbative TBA c-function",
                    "mass/rapidity scale map and M proportional to |delta_beta|^((t+1)/4)",
                    "Yang-Baxter factorization equation (2.2)",
                    "t=4 formula S_LL=1 and S_RL=-tanh(theta/2-i*pi/4)",
                ],
            }
        },
        "summary": {
            "screened_new_source_families": 1,
            "algebraic_projective_near_hit_count": 1,
            "complete_physical_candidate_count": 0,
            "physical_composition_gate_open_count": 1,
            "running_coupling_response_gate_open_count": 1,
            "real_response_transfer_gate_open_count": 1,
            "physical_dprime_closed": False,
            "claim_upgrade_count": 0,
        },
        "claim_boundary": [
            "The exact marked quotient identity is an audit derivation from a source formula, not a source-defined response composition law.",
            "The source's Yang-Baxter equation composes pairwise scattering operators in a multiparticle consistency relation, not two RG responses.",
            "The complex unit-circle amplitude is not silently identified with Paper V's real response interval or with a running coupling.",
            "No physical D-prime derivation, 4D scattering transfer, cosmology, UV completion, RH result, or abc result is claimed.",
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
        f"{report['status']} algebraic_identity="
        f"{report['marked_projective_audit']['algebraic_projective_identity_pass']} "
        f"physical_candidates={report['summary']['complete_physical_candidate_count']}"
    )
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
