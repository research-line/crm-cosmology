# CRM-V D-prime journal evidence ledger

- Ledger: `CRM5-DPRIME-EVIDENCE-LEDGER-JOURNAL-V1`
- Schema: `1.0.0`
- Entries: `14`
- Migrated prototype rows: `7`
- Source candidates: `7`
- Physical claim passes: `0`

## Required journal fields

`target | evidence_source | model_dependency | preregistered_controls | status`

## Entries

| Target | Evidence source IDs | Model dependency | Preregistered controls | Status | D' outcome |
|---|---|---|---|---|---|
| `canonical_arctanh` | `CRM5_RESIDUAL_LEDGER_2026` | `none__analytic_projective_abel_coordinate` | `positive_face_grid_x_y_0.05_to_0.95; fixed_projective_quotient_R; common_delta_threshold` | `CONTROL_PASS_PROJECTIVE` | `pass_control` |
| `scaled_2_arctanh` | `CRM5_RESIDUAL_LEDGER_2026` | `none__analytic_projective_abel_coordinate` | `positive_face_grid_x_y_0.05_to_0.95; fixed_projective_quotient_R; common_delta_threshold` | `CONTROL_PASS_PROJECTIVE` | `pass_control` |
| `collar_eps_plus_0.05` | `CRM5_RESIDUAL_LEDGER_2026` | `none__analytic_smooth_nonprojective_collar` | `positive_face_grid_x_y_0.05_to_0.95; fixed_projective_quotient_R; common_delta_threshold` | `CONTROL_FAIL_PROJECTIVE` | `fail_control` |
| `collar_eps_plus_0.10` | `CRM5_RESIDUAL_LEDGER_2026` | `none__analytic_smooth_nonprojective_collar` | `positive_face_grid_x_y_0.05_to_0.95; fixed_projective_quotient_R; common_delta_threshold` | `CONTROL_FAIL_PROJECTIVE` | `fail_control` |
| `collar_eps_minus_0.05` | `CRM5_RESIDUAL_LEDGER_2026` | `none__analytic_smooth_nonprojective_collar` | `positive_face_grid_x_y_0.05_to_0.95; fixed_projective_quotient_R; common_delta_threshold` | `CONTROL_FAIL_PROJECTIVE` | `fail_control` |
| `collar_cubic_plus_0.05` | `CRM5_RESIDUAL_LEDGER_2026` | `none__analytic_smooth_nonprojective_collar` | `positive_face_grid_x_y_0.05_to_0.95; fixed_projective_quotient_R; common_delta_threshold` | `CONTROL_FAIL_PROJECTIVE` | `fail_control` |
| `rg_scale_ratio_tanh_k1` | `CRM5_RESIDUAL_LEDGER_2026` | `synthetic_tanh_response_on_multiplicative_scale_semigroup` | `same_delta_threshold_as_collar_controls; r_grid_1.05_to_10; k_equals_1` | `SYNTHETIC_SCALE_COMPOSITION_PASS__NOT_PHYSICAL` | `pass_synthetic_not_physical` |
| `agravity_qed_gamma_gamma_unpolarized_sqamp_tree` | `CUNHA_LEHUM_2026` | `massless_tree_level_one_graviton_exchange_fixed_couplings` | `canonical_arctanh; collar_cubic_plus_0.05; natural_forward_and_backward_angle_anchors` | `NOT_DECIDABLE_SOURCE_INCOMPLETE` | `not_decidable` |
| `bjorken_effective_charge_alpha_g1` | `DEUR_ET_AL_2022; BRODSKY_LU_1995; DE_TERAMOND_ET_AL_2024` | `physical_effective_charge_plus_de_teramond_analytic_model` | `fixed_GDH_and_asymptotic_freedom_anchors; canonical_tanh_generator_positive_control; eleven_Q_values_0.001_to_100_GeV` | `MODEL_BOUND_DPRIME_FAIL__PHYSICAL_C_NOT_SOURCE_EXACT` | `fail_model_bound` |
| `u1_2d_yang_mills_wilson_loop_area_response` | `AROCA_KUBYSHIN_2000; WITTEN_1991; NGUYEN_2018` | `exact_pure_2d_U1_Yang_Mills_heat_kernel_area_law` | `exact_semigroup_identity; normalized_composition_associativity; two_finite_response_boundaries` | `EXACT_GAUGE_RESPONSE_COMPOSITION__DPRIME_FAIL__NOT_4D_SCATTERING_OR_RG` | `fail_model_bound` |
| `lqa_largeN_xi_in_log_mu` | `LIU_QUINTIN_AFSHORDI_2026; CRM5_GENERATOR_LEDGER_2026` | `large_N_one_loop_xi_projection__debated_physical_beta_functions` | `logistic_tanh_positive_control; cubic_abel_warp_negative_control; fixed_t_equals_log_mu_over_mu0` | `MODEL_BOUND_DPRIME_FAIL__SOURCE_PHYSICS_DEBATED` | `fail_model_bound` |
| `lqa_largeN_xi_in_log_log_mu` | `LIU_QUINTIN_AFSHORDI_2026; CRM5_GENERATOR_LEDGER_2026` | `same_large_N_xi_path__second_logarithm_reparametrization` | `same_source_path_as_standard_time_fail; tau_equals_log_log_mu_over_mu0; physical_time_justification_required` | `MATHEMATICAL_REPARAMETRIZATION_PASS__NOT_PHYSICAL_TIME` | `pass_reparametrization_not_physical` |
| `lqa_full_lambda_xi_trajectory_tensor_r_projection` | `LIU_QUINTIN_AFSHORDI_2026` | `preregistered_large_N_two_coupling_path_plus_FLRW_tensor_r_projection` | `two_coordinate_retention; reduced_and_full_beta_residuals; six_frozen_b_Nm_cases; source_tensor_r_anchor` | `FULL_2D_LARGE_N_TRAJECTORY__R_PROJECTION_DPRIME_FAIL__NO_EXACT_C` | `fail_model_bound` |
| `fqhe_nu_1_3_point_contact_conductance` | `FENDLEY_LUDWIG_SALEUR_1995; GHOSHAL_ZAMOLODCHIKOV_1994; KOSTRYKIN_SCHRADER_2001` | `exact_nu_1_3_boundary_sine_Gordon_TBA_transport_model` | `fixed_zero_and_e_squared_over_3h_conductance_boundaries; fixed_t_equals_log_T_over_TB; source_endpoint_powers_4_and_4_over_3; scalar_transmission_closure_counterexample` | `EXACT_IR_FINITE_TRANSPORT_DPRIME_FAIL__SCALAR_C_NOT_SOURCE_DEFINED` | `fail_model_bound` |

## Source registry

| ID | Kind | Citation | Locator |
|---|---|---|---|
| `CRM5_RESIDUAL_LEDGER_2026` | `internal_analytic` | CRM-V D-prime Residual Ledger, proof note and results (2026-06-21) | legacy-onedrive://CRM-V/DPRIME_RESIDUAL_LEDGER_2026-06-21 |
| `CRM5_GENERATOR_LEDGER_2026` | `internal_analytic` | CRM-V D-prime RG generator equivalence audit (2026-08-08) | legacy-onedrive://CRM-V/DPRIME_RG_GENERATOR_EQUIVALENCE_2026-08-08 |
| `CUNHA_LEHUM_2026` | `external_primary` | [Cunha and Lehum, Scattering amplitudes in dimensionless quadratic gravity coupled to QED (2026)](https://doi.org/10.1103/k79x-52gj) | Eqs. (17)-(19); gauge-fixing and forward/backward limits |
| `DEUR_ET_AL_2022` | `external_primary` | [Deur et al., Experimental determination of the QCD effective charge alpha_g1(Q), Particles 5, 171 (2022)](https://doi.org/10.3390/particles5020015) | effective-charge definition and measured low-Q behavior |
| `BRODSKY_LU_1995` | `external_primary` | [Brodsky and Lu, Commensurate Scale Relations in Quantum Chromodynamics, Physical Review D 51, 3652 (1995)](https://doi.org/10.1103/PhysRevD.51.3652) | renormalization-group transitivity for commensurate scales |
| `DE_TERAMOND_ET_AL_2024` | `external_primary` | [de Teramond et al., The strong coupling in the nonperturbative and near-perturbative regimes (2024)](https://arxiv.org/abs/2403.16126) | Eqs. (1), (4)-(6), analytic effective-charge model and beta function |
| `AROCA_KUBYSHIN_2000` | `external_primary` | [Aroca and Kubyshin, Study of Wilson loop functionals in 2D Yang-Mills theories, Annals of Physics 283 (2000)](https://doi.org/10.1006/aphy.2000.6044) | heat-kernel formulation and U(1) plane area law, Eq. (62) |
| `WITTEN_1991` | `external_primary` | [Witten, On quantum gauge theories in two dimensions, Communications in Mathematical Physics 141 (1991)](https://doi.org/10.1007/BF02100009) | gauge-invariant Wilson-line framework |
| `NGUYEN_2018` | `external_primary` | [Nguyen, Quantum Yang-Mills theory in two dimensions: exact versus perturbative, Communications in Mathematical Physics 357 (2018)](https://doi.org/10.1007/s00220-017-2942-6) | continuum Wilson-loop construction via group heat kernels |
| `LIU_QUINTIN_AFSHORDI_2026` | `external_primary` | [Liu, Quintin, and Afshordi, Ultraviolet Completion of the Big Bang in Quadratic Gravity, Physical Review Letters 136, 111501 (2026)](https://doi.org/10.1103/6gtx-j455) | main Eq. (2); Supplemental Eqs. (9), (22)-(26) |
| `FENDLEY_LUDWIG_SALEUR_1995` | `external_primary` | [Fendley, Ludwig, and Saleur, Exact conductance through point contacts in the nu=1/3 fractional quantum Hall effect, Physical Review Letters 74 (1995)](https://doi.org/10.1103/PhysRevLett.74.3005) | exact conductance, boundary S matrix, T_B scaling, and endpoint powers 4 and 4/3 |
| `GHOSHAL_ZAMOLODCHIKOV_1994` | `external_primary` | [Ghoshal and Zamolodchikov, Boundary S-matrix and boundary state in two-dimensional integrable quantum field theory, International Journal of Modern Physics A 9 (1994)](https://doi.org/10.1142/S0217751X94001552) | factorizable boundary S matrices and boundary sine-Gordon reflection structure |
| `KOSTRYKIN_SCHRADER_2001` | `external_primary` | [Kostrykin and Schrader, The generalized star product and the factorization of scattering matrices on graphs, Journal of Mathematical Physics 42 (2001)](https://doi.org/10.1063/1.1354641) | exact generalized-star-product composition of full unitary scattering matrices |

## Interpretation guard

The ledger keeps analytic controls, synthetic scale laws, source-incomplete
candidates, model-bound failures, and mathematical reparametrizations in
different status classes. A null metric means that D' was not evaluable; it
is not a numerical zero. Every physical/model candidate cites at least one
primary source, yet no row supplies the still-missing source-exact physical
binary response composition needed to close Paper V's physical D' gate.
