# CRM5-SMOOTH-COLLAR-OPERATIONS-CLASSIFICATION-V1

**Date:** 2026-08-26
**Scope:** Classify the smooth positive boundary-collar operations that are
compatible with the strict one-dimensional `D^pm` response channel
**Result:**
`COMPLETE_WITHIN_SMOOTH_STRICT_DPM_COLLAR_CLASS__DPRIME_IS_H_ZERO__NO_UV_CLAIM`

## Question and exact boundary

Paper V already proves that A--D, B-prime, and `D^pm` produce an Abel-coordinate
framework, and that D-prime selects the projective `tanh` representative. The
P1-10 healer report correctly observed that the admissible smooth collars had
not themselves been classified.

The phrase "all smooth collars" is too broad unless the class is stated. This
note classifies exactly the operations `C:[0,1]^2->[0,1]` that are

1. `C-infinity` on the closed positive square;
2. commutative and associative;
3. neutral at `0` and absorbing at `1`;
4. strictly increasing on the open positive face; and
5. the positive restriction of the cancellative one-dimensional `D^pm`
   channel.

This is the smooth strict Archimedean t-conorm subclass selected by the Paper-V
contract. It excludes nilpotent/noncancellative operations, ordinal sums with
interior idempotents, multi-channel or stochastic laws, and any demand for a
smooth value at the mixed signed compactification corners `(1,-1)` and
`(-1,1)`.

The standard continuous additive-generator context is source-bound to
Mesiarová-Zemánková, Proposition 1
([arXiv:1506.07820](https://arxiv.org/abs/1506.07820)). The signed strict
t-conorm extension as an Abelian group is source-bound to Grabisch, Marichal,
Mesiar, and Pap, Theorem 1, *Aggregation on bipolar scales*, Proc. 30th Linz
Seminar on Fuzzy Set Theory, pp. 46--51 (2009)
([institutional record](https://orbilu.uni.lu/handle/10993/9591)). Those sources
provide the continuous generator/group context. The `C-infinity` simple-zero,
canonical-collar, and D-prime-slice arguments below are proved here rather than
attributed to them.

## Classification theorem

Define the normalized invariant generator

```text
a(x) = partial_2 C(x,0),
phi(x) = integral_0^x dt/a(t).
```

The identity law gives `a(0)=1`, and the strict channel gives `a(x)>0` for
`0<=x<1`. Absorption gives `a(1)=0`.

### Necessity of a simple boundary zero

Write `L_y(x)=C(x,y)`. In Abel time `t=phi(y)`, `L_y` is the time-`t` flow of
the vector field `a(x) partial_x`. Since `x=1` is fixed, its boundary
derivative is

```text
partial_1 C(1,y) = exp(a'(1)*phi(y)).
```

If `a'(1)=0`, this derivative equals `1` for every `y<1`. Closed-square
smoothness instead implies

```text
partial_1 C(1,y) -> partial_1 C(1,1) = 0
```

as `y->1`, because `C(x,1)=1` is constant in `x`. This is a contradiction.
Positivity on the left of the zero already gives `a'(1)<=0`; therefore

```text
kappa := -a'(1) > 0.
```

The saturation zero is necessarily simple.

### The unique canonical collar

Set

```text
q(x) = exp(-kappa*phi(x)).
```

It obeys `a*q'=-kappa*q` and

```text
q(C(x,y)) = q(x)q(y).
```

Because `a(x)=kappa*(1-x)+O((1-x)^2)`, the quotient `q(x)/(1-x)` extends
smoothly and positively to the boundary. Thus `q` is a decreasing
`C-infinity` diffeomorphism from `[0,1]` onto `[1,0]`, with

```text
q(0)=1, q(1)=0, q'(0)=-kappa, q'(1)<0.
```

It is unique with these properties. Any other multiplicative collar `r` has
`-log r=c*phi`; hence `r=q^(c/kappa)`. Requiring both `r` and `q` to have a
simple boundary zero forces `c/kappa=1`.

Conversely, every decreasing smooth boundary diffeomorphism with these endpoint
values defines

```text
C_q(x,y) = q^(-1)(q(x)q(y)).
```

Pullback of multiplication proves smoothness, commutativity, associativity,
strictness, identity, and absorption. This proves necessity and sufficiency.

## Full h-gauge parameterization

Relative to the fixed projective collar

```text
q_0(x) = (1-x)/(1+x),
```

every canonical smooth collar, and no other one, is

```text
q_h(x) = q_0(x) exp(-2h(x)),
```

where

```text
h is C-infinity on [0,1],
h(0)=0,
1+(1-x^2)h'(x)>0 on [0,1].
```

The last inequality is exactly the condition `q_h'<0`. The associated
normalized generator is

```text
a_h(x)
  = (1+h'(0))*(1-x^2)/(1+(1-x^2)h'(x)).
```

Compatibility with the signed B-prime germ is equivalent to `h` admitting a
smooth odd extension through `x=0`. The familiar family

```text
h(x)=epsilon*x, epsilon>-1,
phi_epsilon(x)=atanh(x)+epsilon*x
```

is therefore only a one-dimensional slice of an infinite-dimensional smooth
collar gauge.

All members are smoothly conjugate to projective addition. With

```text
H_h = q_0^(-1) o q_h
```

one has

```text
H_h(C_h(x,y)) = C_0(H_h(x),H_h(y)),
C_0(x,y) = (x+y)/(1+xy).
```

This conjugacy is a mathematical coordinate statement, not a physical
selection of the response chart.

## Exact D-prime slice

For the fixed marked quotient `R=1/q_0`, the defect is exactly

```text
Delta_Dprime(x,y)
  = log R(C_h(x,y))-log R(x)-log R(y)
  = 2*(h(x)+h(y)-h(C_h(x,y))).
```

If D-prime holds, both `q_h` and `q_0` are multiplicative boundary-defining
coordinates for the same operation. Canonical-collar uniqueness then gives
`q_h=q_0`, hence `h=0`. Conversely `h=0` is the projective law. Therefore:

```text
D-prime holds exactly at h=0.
```

The classification explains, rather than removes, the physical content of
D-prime: every admissible collar is smoothly conjugate to the projective one,
but D-prime fixes the marked response coordinate itself.

## Reproduction

```bash
python scripts/paper5/smooth_collar_classification_gate.py
python -m pytest tests/test_smooth_collar_classification_gate.py -q
```

Artifact:

`results/paper5/SMOOTH_COLLAR_CLASSIFICATION_GATE_2026-08-26.json`

## Claim boundary

This closes P1-10 only within the explicitly declared smooth strict
one-dimensional Paper-V collar class. It does not derive the marked projective
chart from a UV theory, classify arbitrary compact-interval semigroups, extend
the law smoothly through mixed signed boundary corners, or establish any new
cosmology, RH, or abc result.
