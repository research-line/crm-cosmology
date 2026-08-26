# Preregistration: LQA two-coupling trajectory and tensor projection

- **Bundle:** `CRM5-LQA-2D-TRAJECTORY-RPROJ-V1`
- **Frozen before execution:** `2026-08-26T10:07:00+02:00`
- **Scope:** one source-bound, claim-neutral audit of the full `(lambda, xi)`
  large-`N_m` trajectory; no Paper V or CRM claim upgrade

## Source branch fixed in advance

The only source branch admitted by this audit is Liu, Quintin, and Afshordi,
*Ultraviolet Completion of the Big Bang in Quadratic Gravity*, Physical Review
Letters 136, 111501 (2026), [DOI](https://doi.org/10.1103/6gtx-j455),
[arXiv:2510.18733v2](https://arxiv.org/abs/2510.18733).

The paper defines `t = ln(mu/mu0) > 0`, the two one-loop beta functions in
Eq. (2), and the large-matter solution in Supplemental Eq. (9):

```text
b = lambda_0 * N_m / (4*pi)^2
lambda(t) = lambda_0 / (1 + b*t)
xi(t) = 35*lambda_0^2*t / (8*pi^2*(1 + b*t))
```

Here `N_m` is the paper's weighted matter-field number, not the inflationary
e-fold count. The source explicitly treats these beta functions as debated and
the covariant scale choice as ambiguous. This audit fixes the paper's explored
branch `mu = sqrt(abs(R))`; with `psi = R/R0` and `R0 = mu0^2`, this gives
`L = ln(psi^2) = 4*t`.

## Trajectory preregistration

The full ordered state is

```text
z(t) = (lambda(t), xi(t)).
```

Neither coordinate may be discarded. Each output row must contain both
coordinates, both analytic path derivatives, both full Eq. (2) beta values,
and both reduced-large-`N_m` beta values. The exact trajectory identity to be
checked is

```text
lambda/lambda_0 + xi/xi_infinity = 1,
xi_infinity = 70*lambda_0/N_m.
```

The audit grid is frozen as follows:

```text
b in {0.1, 0.3, 1.0}
N_m in {100000, 1000000}
lambda_0 = 16*pi^2*b/N_m
t/t_end in {1, 2, 4, 8, 16}
```

These values span the endpoints and one interior value of the paper's stated
phenomenological window `0.1 <= b <= 1` and its stated matter range
`10^5 <= N_m <= 10^6`. No point may be removed after seeing a residual.

The inflation-end anchor is fixed by Supplemental Eqs. (22)-(23):

```text
L_end = (2/b) * (sqrt(1 + 2*(1 + 1/sqrt(3))*b) - 1)
t_end = L_end/4.
```

## Observable projection preregistration

The sole admissible projection is the source's tensor-to-scalar ratio from
Supplemental Eq. (26), evaluated on the complete two-coordinate trajectory:

```text
D(t) = b*L(t)^2 + 4*(L(t) - 2)
r(t) = (1/3) * (32/D(t))^2
x_r(t) = 1 - r(t)/8.
```

This projection is chosen before execution because `r` is an explicit
cosmological observable in the source. The anchors are source-defined by
`epsilon_V(t_end)=1`, hence `r(t_end)=16` and `x_r(t_end)=-1`, while the deep
UV limit is `r -> 0` and `x_r -> +1`. The projection is not injective evidence
for the whole coupling plane: on the homogeneous and isotropic background the
source states that the Weyl-squared term vanishes. That rank limitation must be
reported, not repaired with a post-hoc synthetic coupling coordinate.

The interior D-prime witness grid is frozen as

```text
t/t_end in {1.05, 1.25, 2, 4, 8, 16}.
```

The projective generator is evaluated only for `-1 < x_r < 1`:

```text
G_r(t) = (dx_r/dt)/(1 - x_r^2).
```

## Gates and decision rule

1. **Two-coordinate retention:** every case records the complete `z(t)` and
   tangent; missing either coordinate is an automatic invalid audit.
2. **Trajectory identity:** maximum absolute affine-invariant residual must be
   at most `1e-12`.
3. **Reduced ODE:** the analytic tangent must match the reduced large-`N_m`
   beta system to relative vector residual at most `1e-12`.
4. **Full Eq. (2) diagnostic:** the approximate trajectory must match the
   unreduced source beta system to relative vector residual at most `1e-3` on
   every frozen grid point. Failure invalidates use of the approximation on
   this grid; passing does not make the one-loop beta functions physical.
5. **Observable anchors:** `r(t_end)=16`, `x_r(t_end)=-1`, and the analytic
   limits `r(infinity)=0`, `x_r(infinity)=+1` must all hold.
6. **D-prime:** pass only if `G_r` is constant on the full interior witness
   grid for every preregistered `(b,N_m)` case, with relative spread at most
   `1e-10`, and the analytic expression is independent of `t`. Otherwise the
   model-bound observable projection fails D-prime.
7. **Physical transfer:** always `not_bookable` unless the same source branch
   independently supplies an exact nonperturbative binary composition law for
   `r`. The cited source does not preregister such a law, so this audit cannot
   close physical D-prime even if the numerical quotient were constant.

Required controls are the exact reduced-ODE solution, the full-beta residual,
the endpoint identities, and an explicit comparison with the prior `xi`-only
normalization. The final report must state whether the two-coordinate audit
adds independent information or collapses under the source's FLRW projection.
