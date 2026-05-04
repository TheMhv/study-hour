---
title: NUT-12 | Offline ecash signature validation
author: TheMhv
theme:
  name: catppuccin-macchiato
---

NUT-12: Offline ecash signature validation
---

# Overview

NUT-12 Defines a extension of Cashu protocol that allows users to verify Mint's signatures using only their public key. This allows offline payments to Cashu,more privacy and security for users.

<!-- pause -->

## The Problem

In base Cashu protocol, defined by NUT-00, every time that a user receives a ecash token they must request the Mint's public key to verify it. Because of that, the receiver must be able to reach the Mint at the moment of the transaction.

This makes offline payments unreliable and creates a privacy leak, every verification request leaks metadata to the Mint, that can be used to infer when and how often users are transacting.

<!-- pause -->

To fix this, NUT-12 defines a method that allows receivers to verify ecash tokens signature without requesting Mint's public key.


<!-- end_slide -->
<!-- alignment: center -->
<!-- jump_to_middle -->
How this fix works
---
<!-- end_slide -->
How this fix works
---

We use a **Discrete Log Equality (DLEQ)** proofs to prove that the Mint has used the same private key `a` for creating it's public key `A` and used the same private key for signing the Blinded Message `B'`.

The Mint will return DLEQ proof as additional field when return the signature `C'` for the Blinded Message `B'` on a mint or swap operation.

The Users can validate the signatures using this DLEQ proofs, without requesting some proof directly from Mint.

## Mint -> User

On a mint or swap operation, when the Mint *Bob* needs to sign the Blinded Message `B'` from *Alice* request:

<!-- pause -->
1. *Bob* will create a random nonce: `k`

<!-- pause -->
2. Calculate:
  - `R1 = kG`
  - `R2 = kB'`
  - `e = hash(R1, R2, A, C')`
  - `s = k + ea`

<!-- pause -->
3. Return `B'`, `e` and `s` to *Alice*

<!-- pause -->

When *Alice* receive the signature and the DLEQ proof, she can validate with:

<!-- pause -->
1. Calculating:
  - `R1 = sG - eA`
  - `R2 = sB' - eC'`
  - `e' = hash(R1, R2, A, C')`

<!-- pause -->
2. Compare `e'` with `e` received from *Bob*

<!-- pause -->
3. If is equal, `a` used in `A = aG` must be equal to `a` in `C' = aB'`

<!-- end_slide -->
How DLEQ is used in Cashu
---

## User -> User

When *Alice* sends a token to *Carol*, *Alice* needs to send the nonce `r` generated when token is minted.

<!-- pause -->
1. *Carol* will receive the proofs from *Alice*:
  - The ecash `Proof`: `(x, C)`
  - The DLEQ proof revealed by *Alice*: `(e, s)`
  - Blinding factor used in mint operation: `r`

<!-- pause -->
To verify a received token, *Carol* needs to:

<!-- pause -->
2. Reconstruct `B'` and `C'` using the blinded factor `r` received from *Alice*:
  - `Y = hash_to_curve(x)`
  - `C' = C + rA`
  - `B' = Y + rG`

<!-- pause -->
3. With those values, *Carol* can validate the DLEQ proof using same method as *Alice* used before:
  * Calculating:
    - `R1 = sG - eA`
    - `R2 = sB' - eC'`
    - `e' = hash(R1, R2, A, C')`
  * Compare `e'` with `e` received from *Alice*
  * If is equal, `a` used in `A = aG` must be equal to `a` in `C' = aB'`

<!-- end_slide -->
<!-- alignment: center -->
<!-- jump_to_middle -->
Why this works
---
<!-- end_slide -->
Why this works
---

When Mint create values:
`R1 = kG`
`R2 = kB'`

It blind the values using a random nonce `k` that User can remove using the `s` value.
`s` is just a `k` nonce plus the hash `e` signed by Mint: `s = k + ea`.

<!-- pause -->

The User can reach the same values removing the nonce `k` from returned values:
<!-- column_layout: [1, 1] -->
<!-- column: 0 -->
- `R1 = sG - eA`
<!-- column: 1 -->
- `R2 = sB' - eC'`

<!-- pause -->
<!-- reset_layout -->

Using substitutions, we can see how that works

<!-- column_layout: [1, 1] -->
<!-- column: 0 -->
- `R1 = (k+ea)G - e(aG)`
<!-- pause -->
- `R1 = kG + eaG - eaG`
<!-- pause -->
- `R1 = kG`

<!-- pause -->

<!-- column: 1 -->
- `R2 = (k+ea)B' - e(aB')`
<!-- pause -->
- `R2 = kB' - eaB' - eaB'`
<!-- pause -->
- `R2 = kB'`

<!-- pause -->
<!-- reset_layout -->

The User now can validate if `hash(R1, R2, A, C')` is equal to `e` received from Mint or another User. This proves that the private key `a` is used in same calculations:
- `A = aG`
- `C' = aB'`

<!-- end_slide -->
<!-- alignment: center -->
<!-- jump_to_middle -->
How it's implemented
---
<!-- end_slide -->
How it's implemented
---

## Mint to User: DLEQ in BlindedSignature

When Mint's return `BlindedSignature` on a response of minting or swapping operations, the response is extended in the following way to include the DLEQ proof:

<!-- pause -->

```json
{
  "id": "", // <str>
  "amount": 0, // <int>
  "C_": "", // <str>
  "dleq": {
    "e": "", // <str>
    "s": "" // <str>
  }
}
```

<!-- pause -->

## User to User: DLEQ in Proof

When a user communicate to another User, we extend the `Proof` object and include the DLEQ proof.

<!-- pause -->

```json
{
  "id": "", // <str>
  "amount": 0, // <int>
  "secret": "", // <str>
  "C": "", // <str>
  "dleq": {
    "e": "", // <str>
    "s": "", // <str>
    "r": "" // <str>
  }
}
```

New value `r` is the blinding factor of the first user was used to generate the `Proof`.

<!-- end_slide -->
References
---

- [NUT-00: Notation, Utilization, and Terminology](https://github.com/cashubtc/nuts/blob/main/00.md)
- [NUT-12: Offline ecash signature validation](https://github.com/cashubtc/nuts/blob/main/12.md)

<!-- end_slide -->
<!-- alignment: center -->
<!-- jump_to_middle -->
Questions?
---

<!-- end_slide -->
<!-- alignment: center -->
<!-- jump_to_middle -->
That's all Folks!
---
