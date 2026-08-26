# CRM5 LQA full two-coupling trajectory and tensor-projection audit

- **Bundle:** `CRM5-LQA-2D-TRAJECTORY-RPROJ-V1`
- **Status:** `FULL_2D_LARGE_N_TRAJECTORY__R_PROJECTION_DPRIME_FAIL__NO_EXACT_C`
- **Claim pass:** `false`
- **Preregistration:**
  [`CRM5_LQA_2D_TRAJECTORY_RPROJ_V1_PREREG_2026-08-26.md`](preregistrations/CRM5_LQA_2D_TRAJECTORY_RPROJ_V1_PREREG_2026-08-26.md),
  frozen in commit `3c07f3bb9f8c3fd8869268ba6cf0cc3cd50c9b7d` before execution

## Source branch

The audit uses only Liu, Quintin, and Afshordi, *Ultraviolet Completion of
the Big Bang in Quadratic Gravity*, Physical Review Letters 136, 111501
(2026), [DOI](https://doi.org/10.1103/6gtx-j455),
[arXiv:2510.18733v2](https://arxiv.org/abs/2510.18733).

The paper gives the full one-loop beta system for the two QQG couplings in
main Eq. (2), the large-matter solution in Supplemental Eq. (9), the explored
scale map `mu=sqrt(abs(R))`, and the tensor-to-scalar ratio in Supplemental
Eq. (26). The authors explicitly state that the physical status of the beta
functions remains debated and that the covariant RG-scale identification is
ambiguous.

## Complete preregistered trajectory

With `t=ln(mu/mu0)>0`, weighted matter count `N_m`, and
`b=lambda_0*N_m/(4*pi)^2`, the retained ordered state is

```text
z(t) = (lambda(t), xi(t)),
lambda(t) = lambda_0/(1+b*t),
xi(t) = 35*lambda_0^2*t/(8*pi^2*(1+b*t)).
```

No coupling was removed. Every result row contains both coordinates, both
analytic tangent components, both reduced beta components, and both full
Eq. (2) beta components. Across the frozen grid

```text
b in {0.1, 0.3, 1.0},
N_m in {100000, 1000000},
t/t_end in {1, 2, 4, 8, 16},
```

the results are:

- trajectory-identity residual at most `2.220e-16`;
- reduced two-component ODE residual at most `3.961e-16`; and
- unreduced Eq. (2) vector residual at most `1.797e-04`, below the
  preregistered `1e-3` approximation-window gate.

The trajectory obeys

```text
lambda/lambda_0 + xi/xi_infinity = 1,
xi_infinity = 70*lambda_0/N_m.
```

Consequently, the synthetic two-coupling contrast
`xi/xi_infinity-lambda/lambda_0` is exactly the earlier normalized
`xi`-only response. The full path validates that reduction as a property of
this approximate orbit; it does not create a second independent response.

## Frozen observable projection and D' result

The preregistered projection is the source's tensor-to-scalar ratio, not a
post-hoc coupling coordinate. On `L=ln(psi^2)=4t`, define

```text
D(t) = b*L^2 + 4*(L-2) = 16*b*t^2 + 16*t - 8,
r(t) = (1/3)*(32/D(t))^2,
x_r(t) = 1-r(t)/8.
```

Supplemental Eqs. (22)-(23) fix the inflation-end anchor
`r(t_end)=16`, hence `x_r(t_end)=-1`; the deep-UV limit is `r->0`, hence
`x_r->+1`. The projective generator reduces analytically to

```text
G_r(t) = (dx_r/dt)/(1-x_r^2)
       = 2*D_dot*D/(2*D^2-128/3).
```

This is not constant. It diverges when the inflation-end boundary is
approached from the interior and tends to zero in the deep UV. On the frozen
interior grid `t/t_end in {1.05,1.25,2,4,8,16}`, the relative quotient spread
is:

| `b` | Relative D' spread |
|---:|---:|
| 0.1 | `4.309` |
| 0.3 | `4.243` |
| 1.0 | `4.172` |

The tensor-r projection therefore **fails D'** in every preregistered case.

## Projection rank and booking decision

The coupling space is two-dimensional, but one RG orbit is a one-dimensional
curve. More importantly for the selected observable, the source states that
the Weyl-squared term vanishes on the homogeneous and isotropic background.
The tensor-r calculation is thus a rank-one cosmological projection of the
two-coupling branch. It differs nonlinearly from the earlier `xi` response,
but it does not supply an independent two-dimensional observable composition.

No exact nonperturbative binary composition law for `r` is defined by the
source. The result is therefore a model- and scale-map-bound D' failure, not a
physical D' derivation or no-go theorem. It does not upgrade Paper V or CRM.
