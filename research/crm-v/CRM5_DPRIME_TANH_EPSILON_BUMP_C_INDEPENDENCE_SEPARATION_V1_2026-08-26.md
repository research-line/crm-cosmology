# CRM5-DPRIME-TANH-EPSILON-BUMP-C-INDEPENDENCE-SEPARATION-V1

**Date:** 2026-08-26
**Scope:** Verify the compactly supported odd-bump witness requested by the
CRM-V P1-7 review and freeze its exact independence claim boundary
**Result:**
`EXACT_C_SEPARATION_WITNESS__A_B_BPRIME_ENDPOINT_PASS__DPM_NOT_CLAIMED`

## Question

Can the flawed oscillatory sketch

`tanh(g) cos(epsilon g)`

be replaced by a single explicit smooth response that

1. stays in `0 <= sigma(g) < 1` for every `g >= 0`;
2. is globally odd and agrees with `tanh` near the origin, so the local odd
   expansion and positive slope are unchanged;
3. still tends to `1` at positive infinity; but
4. has `sigma'(g) < 0` at an explicit point?

The review source is the internal healer report
`Paper5_HEILER_2026-07-03.md`, item P1-7. A narrow ResearchAgent arXiv/PubMed
query returned no source that contributes to this elementary construction; no
external physics paper is therefore used to inflate the evidential status.

## Frozen witness

Let the normalized standard bump be

```text
b(z) = exp(1 - 1/(1-z^2))   for |z| < 1,
b(z) = 0                    for |z| >= 1.
```

It is `C-infinity`, nonnegative, even, compactly supported, and satisfies
`b(0)=1`. Define the odd translated pair and response

```text
psi(g)   = b(4(g-2)) - b(4(g+2)),
sigma(g) = tanh(g) + (1/50) psi(g).
```

The support of `psi` is

```text
[-9/4,-7/4] union [7/4,9/4].
```

Because `b` is even, `psi` and `sigma` are odd. For `|g| <= 7/4`, the
perturbation vanishes identically, hence

```text
sigma(g) = tanh(g) = g - g^3/3 + O(g^5).
```

This preserves the local Axiom-B expansion with `c1=1` and supplies the global
odd extension B-prime without a fitted coefficient.

## Capacity certificate

On the positive branch the negative translated bump is absent. Outside
`[7/4,9/4]`, `sigma=tanh`, so only this compact interval needs checking. Put
`g=2+z/4`, `-1<z<1`, and compare the perturbation with the remaining headroom:

```text
rho(z) = ((1/50) b(z))/(1-tanh(2+z/4)).
```

The derivative of `log rho` is

```text
-2z/(1-z^2)^2 + 1/(2(1+exp(-4-z/2))).
```

It is positive for `z<0`. For `z>0` it is strictly decreasing: the derivative
of its bump term is at most `-2`, whereas the derivative of the logistic
correction is at most `1/16`. Thus there is one global maximum. Bisection of
that predeclared equation gives

```text
z_max   = 0.2222662410677798,
g_max   = 2.055566560266945,
rho_max = 0.5887518864565877 < 1.
```

Therefore the bump never consumes the available distance to `1`. Since both
`tanh(g)` and the positive-branch bump are nonnegative, Axiom A holds globally
on `g>=0`. The first local response maximum is about
`0.9871157932621778`, still strictly below `1`.

## Exact monotonicity failure

At the frozen witness point `g=17/8`, the positive bump coordinate is `z=1/2`,
where `b(1/2)=exp(-1/3)`. Direct differentiation yields

```text
sigma'(17/8)
  = sech(17/8)^2 - (32/225) exp(-1/3)
  = -0.04644330953106972 < 0.
```

The two numerical turning points are

```text
2.083907131241724 and 2.2266146875098096,
```

so the derivative is negative between them. Because the perturbation has
compact support, `sigma(g)->1` as `g->infinity`: only the monotonicity clause of
Axiom C fails, not its endpoint-saturation clause.

## Exact separation boundary

The witness proves

```text
A + B + B-prime + endpoint saturation  does not imply  C monotonicity.
```

It does **not** prove that C is independent of the full global response law.
The nonmonotone response is noninjective and cannot be a global homomorphism
from the additive control group into the cancellative response group. In the
machine-readable ledger this is recorded as

```text
D_response_composition = NOT_CLAIMED
D^pm_global_group_homomorphism = INCOMPATIBLE
```

This agrees with the already proved global monotonicity lemma: under the full
`D^pm` homomorphism gate and positive identity slope, monotonicity follows.

## Reproduction

```bash
python scripts/paper5/axiom_c_bump_separation_gate.py
python -m pytest tests/test_axiom_c_bump_separation_gate.py -q
```

Artifact:

`results/paper5/AXIOM_C_BUMP_SEPARATION_GATE_2026-08-26.json`

## Claim boundary

This bundle repairs one separation sketch. It does not establish pairwise
independence of the entire axiom set, a physical UV or D-prime derivation, a
new cosmology result, or any RH or abc result.
