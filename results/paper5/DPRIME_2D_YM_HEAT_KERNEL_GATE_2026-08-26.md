# 2D Yang--Mills heat-kernel D' candidate gate

- Candidate: `CRM5-DPRIME-2DYM-HEAT-KERNEL-CANDIDATE-V1`
- Status: `EXACT_GAUGE_RESPONSE_COMPOSITION__DPRIME_FAIL__NOT_4D_SCATTERING_OR_RG`
- Claim pass: `false`

## Exact source-bound response

For pure U(1) Yang--Mills theory on the plane, the heat-kernel Wilson-loop
response is `w(A)=exp(-kappa*A)`, with `kappa=e_squared*nu_squared/2`.
The fixed normalization `x=1-2w` gives the exact response law
`C(x,y)=1-(1-x)(1-y)/2`, identity `-1`, and absorber `+1`.

## Gate result

| Gate | Result |
|---|---|
| Exact Wilson semigroup | `True` |
| Exact normalized composition | `True` |
| Associativity | `True` |
| Finite distinct response boundaries | `True` |
| D' quotient constant | `False` |
| Paper V claim pass | `False` |

The area generator is `beta_x=kappa*(1-x)`. Therefore
`beta_x/(1-x^2)=kappa/(1+x)`, which is not constant:
it equals `1.0` at `x=0` and
`0.6666666666666666` at `x=0.5` for the audited normalization.
This exact physical response composition fails D'.

## Claim boundary

This is a nonperturbative 2D gauge-response control case. It is not a 4D
scattering observable, its additive area is not an RG energy scale, and the
dimensionful 2D coupling supplies no source-bound running of this response.
Nothing in this audit upgrades the conditional Paper V theorem or CRM claims.

## Primary sources

- Aroca and Kubyshin, Annals of Physics 283 (2000) 11-37: heat-kernel formulation and exact U(1) plane area law ([DOI](https://doi.org/10.1006/aphy.2000.6044), [arXiv](https://arxiv.org/abs/hep-th/9901155)).
- Witten, Communications in Mathematical Physics 141 (1991) 153-209: gauge-invariant Wilson-line framework for exact 2D Yang--Mills theory ([DOI](https://doi.org/10.1007/BF02100009)).
- Nguyen, Communications in Mathematical Physics 357 (2018) 333-374: rigorous continuum Wilson-loop construction via group heat kernels ([DOI](https://doi.org/10.1007/s00220-017-2942-6), [arXiv](https://arxiv.org/abs/1508.06305)).
