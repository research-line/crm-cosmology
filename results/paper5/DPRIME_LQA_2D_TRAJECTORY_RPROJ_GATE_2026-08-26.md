# LQA full two-coupling trajectory and tensor-projection D' gate

- Candidate: `CRM5-LQA-2D-TRAJECTORY-RPROJ-V1`
- Status: `FULL_2D_LARGE_N_TRAJECTORY__R_PROJECTION_DPRIME_FAIL__NO_EXACT_C`
- Claim pass: `false`
- Preregistration commit: `3c07f3bb9f8c3fd8869268ba6cf0cc3cd50c9b7d`

## Frozen source branch

The audit retains the complete large-matter source trajectory
`z(t)=(lambda(t),xi(t))` from Supplemental Eq. (9) and evaluates the
source's tensor-to-scalar ratio `r` from Supplemental Eq. (26) on the
fixed scale map `mu=sqrt(abs(R))`. No coordinate is discarded.

## Gate result

| Gate | Result | Maximum residual |
|---|---|---:|
| Complete two-coordinate rows | `True` | -- |
| Trajectory identity | `True` | `2.220e-16` |
| Reduced large-N ODE | `True` | `3.961e-16` |
| Full Eq. (2) window diagnostic | `True` | `1.797e-04` |
| Tensor-r finite anchors | `True` | -- |
| D' quotient constant | `False` | -- |
| Exact binary observable C source-defined | `False` | -- |
| Paper V claim pass | `False` | -- |

## Frozen-grid summaries

| b | N_m | lambda_0 | max full-beta residual | D' relative spread |
|---:|---:|---:|---:|---:|
| 0.1 | 100000 | 1.579137e-04 | 1.797e-04 | 4.309e+00 |
| 0.1 | 1000000 | 1.579137e-05 | 1.797e-05 | 4.309e+00 |
| 0.3 | 100000 | 4.737410e-04 | 1.797e-04 | 4.243e+00 |
| 0.3 | 1000000 | 4.737410e-05 | 1.797e-05 | 4.243e+00 |
| 1.0 | 100000 | 1.579137e-03 | 1.797e-04 | 4.172e+00 |
| 1.0 | 1000000 | 1.579137e-04 | 1.797e-05 | 4.172e+00 |

## D' decision

With `D=16*b*t^2+16*t-8`, the projective generator is
`G_r=2*D_dot*D/(2*D^2-128/3)`. It depends explicitly on `t`,
diverges when approached from the inflation-end anchor, and tends
to zero in the deep-UV limit. The source observable therefore fails
D' throughout every preregistered parameter case.

## Projection and claim boundary

The ambient coupling space is two-dimensional, but the audited orbit has dimension `1`.
The source's homogeneous/isotropic background removes the
Weyl-squared contribution. The synthetic two-coupling contrast
collapses exactly to the prior xi-only normalization; the physical
tensor-r projection is different, but remains a rank-one trajectory
projection. No independent two-dimensional observable composition is
obtained, and the source supplies no exact nonperturbative binary law
for `r`. The result is model- and scale-map-bound and cannot be booked
as physical D' or as a Paper V/CRM claim.

## Primary source

- Liu, Quintin, and Afshordi, Physical Review Letters 136, 111501
  (2026): [DOI](https://doi.org/10.1103/6gtx-j455),
  [arXiv](https://arxiv.org/abs/2510.18733).
