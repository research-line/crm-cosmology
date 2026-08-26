# CRM5 D' candidate audit: exact 2D Yang--Mills heat-kernel response

- **Bundle:** `CRM5-DPRIME-2DYM-HEAT-KERNEL-CANDIDATE-V1`
- **Status:** `EXACT_GAUGE_RESPONSE_COMPOSITION__DPRIME_FAIL__NOT_4D_SCATTERING_OR_RG`
- **Claim pass:** `false`

## Question and source boundary

The tested candidate is the gauge-invariant Wilson-loop expectation in pure
two-dimensional U(1) Yang--Mills theory on the plane. Aroca and Kubyshin give
the heat-kernel continuum result

`w(A) = exp[-(e_squared/2) * nu_squared * A] = exp(-kappa*A)`.

This is an exact nonperturbative response as a function of enclosed area. The
same sources support the heat-kernel and gauge-invariant Wilson-loop setting;
Nguyen supplies a rigorous continuum construction. They do **not** identify
this response as a 4D scattering observable or its area as a 4D RG scale.

Primary sources:

- Aroca and Kubyshin, *Study of Wilson loop functionals in 2D Yang--Mills
  theories*, Annals of Physics 283 (2000),
  [DOI](https://doi.org/10.1006/aphy.2000.6044),
  [arXiv](https://arxiv.org/abs/hep-th/9901155). The U(1) plane result is
  displayed as Eq. (62).
- Witten, *On quantum gauge theories in two dimensions*, Communications in
  Mathematical Physics 141 (1991),
  [DOI](https://doi.org/10.1007/BF02100009).
- Nguyen, *Quantum Yang--Mills theory in two dimensions: exact versus
  perturbative*, Communications in Mathematical Physics 357 (2018),
  [DOI](https://doi.org/10.1007/s00220-017-2942-6),
  [arXiv](https://arxiv.org/abs/1508.06305).

## Exact composition and boundaries

For adjacent additive areas,

`w(A1+A2) = w(A1) w(A2)`.

Use the fixed normalization `x(A)=1-2w(A)`. Then `x(0)=-1` and
`lim[A->infinity] x(A)=+1`, both finite and distinct. Multiplication of `w`
induces

`C(x,y) = 1 - (1-x)(1-y)/2`.

This binary law is associative, has identity `-1`, and has absorbing boundary
`+1`. The composition is derived from the exact response rather than borrowed
from the Paper V collar.

## D' result

The area generator is

`beta_x = dx/dA = kappa(1-x)`.

Therefore the projective-boundary quotient is

`beta_x/(1-x_squared) = kappa/(1+x)`.

It is nonconstant on `(-1,1)`: for example it equals `kappa` at `x=0` and
`2*kappa/3` at `x=1/2`. It diverges toward the identity boundary and tends to
`kappa/2` toward the absorbing boundary. The exact physical response law thus
**fails D'**.

## Booking decision

This is a useful exact negative control: exact gauge-response composition and
finite response boundaries do not by themselves imply D'. It does not close
the Paper V physical gate because:

1. the observable is a Wilson-loop response, not a scattering observable;
2. the additive variable is 2D area, not a 4D RG energy scale;
3. the 2D coupling is dimensionful and no source-bound running of the same
   response was identified; and
4. D' fails directly.

No theorem, Paper V, or CRM claim is upgraded by this audit.
