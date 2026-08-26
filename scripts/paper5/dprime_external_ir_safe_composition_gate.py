"""Build the external IR-safe scattering/composition audit for CRM-V D-prime.

The source-bound near-candidate is the exact nu=1/3 fractional-quantum-Hall
point-contact conductance of Fendley, Ludwig, and Saleur.  The script records
two independent kill gates:

* its exact endpoint powers give unequal projective-generator limits; and
* exact scattering-matrix composition does not descend to a binary law for a
  scalar transmission probability or for the TBA-integrated conductance.

No fitted parameters or post-hoc response coordinate enter either check.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Sequence


AUDIT_ID = "CRM5-DPRIME-EXTERNAL-IR-SAFE-COMPOSITION-SEARCH-V1"
RUN_DATE = "2026-08-26"
STATUS = "EXACT_IR_FINITE_TRANSPORT_DPRIME_FAIL__SCALAR_C_NOT_SOURCE_DEFINED"
OUTPUT_FILENAME = "DPRIME_EXTERNAL_IR_SAFE_COMPOSITION_GATE_2026-08-26.json"


def projective_endpoint_limits(
    lower_response_power: float = 4.0,
    upper_deficit_power: float = 4.0 / 3.0,
) -> tuple[float, float]:
    """Return endpoint limits of beta_x/(1-x^2) for x=2G/G0-1.

    If G/G0 ~ A exp(p_minus*t) at the lower boundary and
    1-G/G0 ~ B exp(-p_plus*t) at the upper boundary, the projective
    generator tends to p_minus/2 and p_plus/2, independently of A and B.
    """

    return lower_response_power / 2.0, upper_deficit_power / 2.0


def serial_transmission_probability(propagation_phase: float) -> float:
    """Transmission of two identical lossless 50/50 one-channel scatterers.

    Choose t_1=t_2=1/sqrt(2) and r_1=r_2=i/sqrt(2).  Exact serial
    scattering-matrix composition gives

        T_total(phi) = 1 / (5 + 4 cos(2 phi)).

    The individual probabilities stay T_1=T_2=1/2, while the aggregate
    probability changes with the phase retained by the full S matrices.
    """

    return 1.0 / (5.0 + 4.0 * math.cos(2.0 * propagation_phase))


def build_report() -> dict[str, object]:
    lower_limit, upper_limit = projective_endpoint_limits()
    phase_zero = serial_transmission_probability(0.0)
    phase_half_pi = serial_transmission_probability(math.pi / 2.0)

    return {
        "audit_id": AUDIT_ID,
        "schema_version": "1.0.0",
        "run_date": RUN_DATE,
        "todo_source": "CRM-V TODO.md:95-102",
        "status": STATUS,
        "search_contract": {
            "required": [
                "physical gauge-independent or gauge-invariant scattering/transport observable",
                "two finite distinguishable source-predeclared boundary responses",
                "independently source-defined exact nonperturbative binary response composition",
                "coupling running or source-defined RG crossover on a declared additive scale",
                "IR-finite validity window",
            ],
            "excluded_reuse": [
                "local six-source quadratic-gravity corpus",
                "Bjorken effective-charge CSR transitivity as a physical response law",
                "2D Yang-Mills area composition as 4D scattering or RG time",
                "RH project",
                "abc project",
            ],
        },
        "primary_near_candidate": {
            "candidate_id": "FQHE_NU_1_3_POINT_CONTACT_CONDUCTANCE",
            "observable": "linear point-contact conductance G(T/T_B) at filling fraction nu=1/3",
            "physical_scope": "integrable boundary sine-Gordon description of fractional-quantum-Hall edge transport",
            "boundary_scale": "T_B proportional to lambda^(1/(1-nu))",
            "additive_control": "t=log(T/T_B)",
            "fixed_normalization": "x=2*G/G0-1 with G0=e^2/(3h)",
            "boundary_responses": {
                "t_to_minus_infinity": "G/G0 -> 0 and x -> -1",
                "t_to_plus_infinity": "G/G0 -> 1 and x -> +1",
                "finite_and_distinguishable": True,
            },
            "source_asymptotics": {
                "lower_response": "G/G0 ~ A*(T/T_B)^4",
                "upper_deficit": "1-G/G0 ~ B*(T_B/T)^(4/3)",
                "lower_response_power": 4.0,
                "upper_deficit_power": 4.0 / 3.0,
                "coefficient_independence": "A and B cancel from the endpoint generator limits",
            },
            "criteria": {
                "physical_transport_observable": "SUPPORTED",
                "gauge_status": "PHYSICAL_CONDUCTANCE__NO_GAUGE_FIXING_PARAMETER__NO_SEPARATE_GAUGE_THEOREM_CLAIMED",
                "finite_distinct_boundaries": "SUPPORTED",
                "source_exact_nonperturbative_scaling_function": "SUPPORTED",
                "declared_boundary_RG_crossover": "SUPPORTED",
                "IR_finite_endpoints": "SUPPORTED_IN_THE_NU_1_3_TRANSPORT_MODEL",
                "exact_binary_scalar_conductance_composition": "NOT_SOURCE_DEFINED",
            },
            "composition_boundary": {
                "exact_object": "momentum-dependent 2x2 kink/antikink boundary S matrix",
                "physical_observable_construction": "G is a TBA-weighted momentum integral of |S_++|^2 and occupation factors",
                "missing_object": "a closed binary law C(G1,G2) for the conductance itself",
                "forbidden_substitution": "one-by-one quasiparticle scattering or S-matrix unitarity is not a binary conductance law",
            },
        },
        "dprime_endpoint_gate": {
            "generator": "beta_x/(1-x^2) with beta_x=dx/dt",
            "lower_limit_formula": "p_minus/2",
            "upper_limit_formula": "p_plus/2",
            "lower_limit": lower_limit,
            "upper_limit": upper_limit,
            "absolute_gap": abs(lower_limit - upper_limit),
            "constant_generator_required": True,
            "dprime_pass": False,
            "status": "SOURCE_ASYMPTOTIC_DPRIME_FAIL",
        },
        "scalar_composition_counterexample": {
            "source_class": "exact serial composition of full unitary scattering matrices",
            "individual_transmission_probabilities": [0.5, 0.5],
            "phase_zero_total_transmission": phase_zero,
            "phase_half_pi_total_transmission": phase_half_pi,
            "same_scalar_inputs_different_output": not math.isclose(
                phase_zero, phase_half_pi, rel_tol=0.0, abs_tol=1e-15
            ),
            "conclusion": "no phase-blind binary law C(T1,T2) can reproduce exact S-matrix composition",
        },
        "external_composition_controls": [
            {
                "class": "factorized O(N) sigma-model scattering",
                "positive": "massive asymptotically-free 1+1D theory with an exact factorized S matrix",
                "kill_gate": "multiparticle operator factorization is not a closed real scalar response law with marked absorbing boundaries",
                "status": "EXACT_AMPLITUDE_COMPOSITION_ONLY",
            },
            {
                "class": "quantum-graph generalized star product",
                "positive": "exact composition rule for full unitary on-shell scattering matrices",
                "kill_gate": "scalar transmission loses phase/channel data and the source supplies no coupling running or RG response path",
                "status": "EXACT_MATRIX_COMPOSITION__SCALAR_AND_RG_GATES_FAIL",
            },
        ],
        "source_registry": {
            "FENDLEY_LUDWIG_SALEUR_1995": {
                "kind": "external_primary",
                "citation": "Fendley, Ludwig, and Saleur, Exact Conductance through Point Contacts in the nu=1/3 Fractional Quantum Hall Effect, Physical Review Letters 74 (1995) 3005",
                "url": "https://arxiv.org/abs/cond-mat/9408068",
                "doi": "https://doi.org/10.1103/PhysRevLett.74.3005",
                "supports": "exact conductance, boundary S matrix, T_B scaling, finite endpoints, and powers 4 and 4/3",
            },
            "GHOSHAL_ZAMOLODCHIKOV_1994": {
                "kind": "external_primary",
                "citation": "Ghoshal and Zamolodchikov, Boundary S-Matrix and Boundary State in Two-Dimensional Integrable Quantum Field Theory, International Journal of Modern Physics A 9 (1994) 3841",
                "url": "https://arxiv.org/abs/hep-th/9306002",
                "doi": "https://doi.org/10.1142/S0217751X94001552",
                "supports": "factorizable boundary S matrices and boundary sine-Gordon reflection structure",
            },
            "KOSTRYKIN_SCHRADER_2001": {
                "kind": "external_primary",
                "citation": "Kostrykin and Schrader, The Generalized Star Product and the Factorization of Scattering Matrices on Graphs, Journal of Mathematical Physics 42 (2001) 1563",
                "url": "https://arxiv.org/abs/math-ph/0008022",
                "doi": "https://doi.org/10.1063/1.1354641",
                "supports": "exact generalized-star-product composition of full unitary scattering matrices",
            },
            "ZAMOLODCHIKOV_ZAMOLODCHIKOV_1979": {
                "kind": "external_primary",
                "citation": "A. B. Zamolodchikov and Al. B. Zamolodchikov, Factorized S-matrices in two dimensions as the exact solutions of certain relativistic quantum field theory models, Annals of Physics 120 (1979) 253",
                "url": "https://doi.org/10.1016/0003-4916(79)90391-9",
                "supports": "exact multiparticle factorization and the massive asymptotically-free O(N) sigma-model S matrix",
            },
            "MARINO_REIS_2020": {
                "kind": "external_primary",
                "citation": "Marino and Reis, Renormalons in integrable field theories, JHEP 04 (2020) 160",
                "url": "https://arxiv.org/abs/1909.12134",
                "doi": "https://doi.org/10.1007/JHEP04(2020)160",
                "supports": "O(N) beta-function coefficients, running scale, and exact charged-channel S matrix",
            },
        },
        "summary": {
            "screened_external_classes": 3,
            "complete_candidate_count": 0,
            "source_bound_dprime_fail_count": 1,
            "scalar_composition_gate_open_count": 1,
            "physical_dprime_closed": False,
            "claim_upgrade_count": 0,
        },
        "claim_boundary": [
            "The D-prime failure is source-bound to the nu=1/3 point-contact conductance and t=log(T/T_B).",
            "The exact boundary S matrix is not silently identified with the integrated scalar conductance.",
            "The O(N) and graph results are composition controls, not four-dimensional quantum-gravity candidates.",
            "No physical D-prime derivation, cosmology, UV completion, RH result, or abc result is claimed.",
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
    print(
        f"{report['status']} lower={report['dprime_endpoint_gate']['lower_limit']} "
        f"upper={report['dprime_endpoint_gate']['upper_limit']} "
        f"complete_candidates={report['summary']['complete_candidate_count']}"
    )
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
