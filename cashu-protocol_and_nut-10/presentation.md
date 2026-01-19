---
title: Cashu Protocol and Spending Conditions (NUT-10)
author: TheMhv
theme:
  name: catppuccin-macchiato
---

<!-- alignment: center -->
<!-- jump_to_middle -->
Cashu Protocol
---
<!-- end_slide -->

Cashu Protocol
---

# What is Cashu?

Cashu is a protocol that implements a Chaumian eCash system on top of Bitcoin. It enables private, bearer-style digital cash using Lightning Protocol.

Cashu allows building scalable solutions such as:
- Wallets
- Vouchers and gift cards
- Micropayment system
- Private payment application

<!-- pause -->

The Cashu protocol has two main components:
* The Mint
* The Wallet

<!-- end_slide -->

Cashu Protocol
---

## The Mint:
The Mint is responsible for:
  - Minting tokens
  - Melting tokens (redeeming for sats)
  - Swapping tokens

<!-- pause -->

Anyone can run a Mint and integrate Cashu payments into an app or service.

<!-- pause -->

The Mint acts as a custodian of sats on the Lightning Network, while issuing anonymous eCash tokens to users.

## The Wallet:

The wallet is a client-side application used by users.

<!-- pause -->

It is responsible for:
- Storing secrets and proofs
- Holding eCash tokens
- Communication with the Mint

<!-- pause -->

Cashu wallets are non-custodial with respect to secret; only the user controls their tokens.

> However, users must trust the Mint to actually hold and redeem the underlying sats.


<!-- end_slide -->

Cashu Protocol
---

# How does it work?

Imagine the following scenario: *Alice wants to send Bitcoin to Carol*.
 
<!-- pause -->

- Alice mints eCash tokens with a Mint:
  - Blind signatures are used
  - The Mint becomes custodian of the sats

<!-- pause -->

<!-- new_line -->
- Alice sends the eCash tokens to Carol

<!-- pause -->

<!-- new_line -->
- Carol has two options:

<!-- pause -->

<!-- new_line -->
- **Melt**:
  - Carol redeems the tokens with the same Mint
  - The Mint checks the tokens were never spent before
  - The Mint pays Carol the sats via Lightning

<!-- pause -->

<!-- new_line -->
- **Swap (most common case)**:
  - Carol swaps the received tokens for new ones
  - The Mint destroys the old tokens and issues fresh ones
  - Carol keeps the value without touching Lightning

<!-- end_slide -->


Cashu Protocol
---

# Why does it work?

Cashu uses blind Diffie-Hellman signatures to create anonymous eCash.

<!-- column_layout: [2, 1] -->
<!-- pause -->
<!-- column: 0 -->

- The Mint has a private key `k` and publishes a public key `K = kG`

<!-- column: 1 -->

```file +line_numbers
path: nut-0.py
language: python
start_line: 3
end_line: 4
```

```file +exec_replace +line_numbers +no_background
path: nut-0.py
language: python
start_line: 2
end_line: 5
```

<!-- column: 0 -->
<!-- pause -->

- The user generates a secret `x` and computes `Y = hash_to_curve(x)`

<!-- column: 1 -->

```file +line_numbers
path: nut-0.py
language: python
start_line: 20
end_line: 22
```

```file +exec_replace +line_numbers +no_background
path: nut-0.py
language: python
start_line: 8
end_line: 23
```

<!-- column: 0 -->
<!-- pause -->

- The user blinds `Y` and sends it to the mint: `B_ = Y + rG`

<!-- column: 1 -->
```file +line_numbers
path: nut-0.py
language: python
start_line: 28
end_line: 29
```

```file +exec_replace +line_numbers +no_background
path: nut-0.py
language: python
start_line: 25
end_line: 30
```
<!-- column: 0 -->
<!-- pause -->

- The Mint signs the blinded value `B_` without seeing `x`: `C_ = kB_`

<!-- column: 1 -->
```file +line_numbers
path: nut-0.py
language: python
start_line: 36
end_line: 36
```

```file +exec_replace +line_numbers +no_background
path: nut-0.py
language: python
start_line: 32
end_line: 37
```
<!-- column: 0 -->
<!-- pause -->

- The user unblinds the signature and obtains a valid token `(x, C)`: `C = C_ - rK = kY`

<!-- column: 1 -->
```file +line_numbers
path: nut-0.py
language: python
start_line: 45
end_line: 45
```

```file +exec_replace +line_numbers +no_background
path: nut-0.py
language: python
start_line: 39
end_line: 46
```
<!-- column: 0 -->
<!-- pause -->

### Result:
- The Mint can verify tokens: `k * hash_to_curve(x) == C`
- The Mint cannot link minting and spending
- Tokens behave like digital bearer cash

```file +line_numbers
path: nut-0.py
language: python
start_line: 53
end_line: 56
```

```file +exec_replace +line_numbers +no_background
path: nut-0.py
language: python
start_line: 48
end_line: 56
```

<!-- end_slide -->

Cashu Protocol
---

# Features

- **Untraceable**: The Mint does not know about the financial activity of its users.
<!-- pause -->
- **Bearer Token**: The *data* is the money. eCash can be embedded in data packages.
<!-- pause -->
- **Push UX**: Payer "throws" money at receiver. With an online inbox, can receive while offline.
<!-- pause -->
- **Programmable**: Complex spending conditions for eCash enforced by the mint.

<!-- pause -->
# Problems

- The Mint is a centralized service
<!-- pause -->
- Mints may face regulatory pressure
<!-- pause -->
- The Mint has custody of user funds
<!-- pause -->
- Users must securely back up their wallets: losing tokens means losing funds

<!-- end_slide -->

<!-- alignment: center -->
<!-- jump_to_middle -->

Questions?

<!-- end_slide -->

<!-- alignment: center -->
<!-- jump_to_middle -->
Spending Conditions (NUT-10)
---

<!-- end_slide -->

Spending Conditions (NUT-10)
---

# What is Spending Conditions?

Spending Conditions define rules that must be satisfied in order to spend eCash tokens.

- They add programmable logic to Cashu tokens
- Rules are enforced by the Mint at spend time
- Conditions do not break privacy or unlinkability

Examples:

- Pay to Public Key (P2PK)
- Hashed Timelock Contracts (HTLCs)

<!-- end_slide -->

Spending Conditions (NUT-10)
---

# Why use this?

Spending Conditions make eCash more flexible and powerful.

- Allows users to attach logic to tokens
- Enable integration with other protocols, like Lightning or Liquid
- Add security and safety features:
  - P2PK payments
  - Refund and recovery scenarios

<!-- end_slide --> 

Spending Conditions (NUT-10)
---

# How does it work?

When user performs a mint or swap operation, they can attach a spending condition following the NUT-10.

- The condition is encoded inside `Proof.secret`
- The Mint enforces the condition when the token is spent
- If the condition is not satisfied, the spend is rejected

<!-- pause -->

A spending condition includes:
- A **kind** identifying the condition type
- A **nonce** (random value)
- A **data** field specific to the condition
- Optional **tags** for additional metadata

<!-- pause -->
```json
[
	"<kind>",
	{
		"nonce": "<str>",
		"data": "<str>",
		"tags": [[ "key", "value1", "value2", "..."],  "..." ], // (optional)
	}
]
```

<!-- end_slide -->

Spending Conditions (NUT-10)
---

# Example: P2PK (NUT-11)

This condition locks a token to a public key.
Only the key holder can spend it.


```json
[
  "P2PK",
  {
    "nonce": "859d4935c4907062a6297cf4e663e2835d90d97ecdd510745d32f6816323a41f",
    "data": "0249098aa8b9d2fbec49ff8598feb17b592b986e62319a4fa488a3dc36387157a7",
    "tags": [["sigflag", "SIG_INPUTS"]]
  }
]
```

<!-- pause -->

To spend this token, the user must provide a valid signature.

```json
{
  "amount": 1,
  "secret": "[\"P2PK\",{\"nonce\":\"859d4935c4907062a6297cf4e663e2835d90d97ecdd510745d32f6816323a41f\",\"data\":\"0249098aa8b9d2fbec49ff8598feb17b592b986e62319a4fa488a3dc36387157a7\",\"tags\":[[\"sigflag\",\"SIG_INPUTS\"]]}]",
  "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
  "id": "009a1f293253e41e",
  "witness": "{\"signatures\":[\"60f3c9b766770b46caac1d27e1ae6b77c8866ebaeba0b9489fe6a15a837eaa6fcd6eaa825499c72ac342983983fd3ba3a8a41f56677cc99ffd73da68b59e1383\"]}"
}
```

<!-- pause -->

The Mint verifies that:
- The signature is valid
- The signature matches the public key in `secret.data`
- The token was not spent before

<!-- end_slide -->

Spending Conditions (NUT-10)
---

# Example: HTLC (NUT-14)

HTLCs allows tokens to be spent only if:
- A secret preimage is revealed
- Or a timeout expires (refund path)

This enables:
- Atomic swaps
- Lightning interoperability
- Trust-minimized payments

<!-- end_slide -->

Spending Conditions (NUT-10)
---

# Example: HTLC (NUT-14)

```json
[
  "HTLC",
  {
    "nonce": "da62796403af76c80cd6ce9153ed3746",
    "data": "6ca9323ce139c415fdac0ed3fa25691593a4d3a475d23db806f78077caee0262",
    "tags": [
      [
        "pubkeys",
        "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904"
      ],
      ["locktime", "1689418329"],
      [
        "refund",
        "033281c37677ea273eb7183b783067f5244933ef78d8c3f15b1a77cb246099c26e"
      ]
    ]
  }
]
```

### Receiver Pathway (hash lock)
The user can spend this token if knows the secret preimage.

```json
{
  "amount": 1,
  "secret": "[\"HTLC\",{\"nonce\":\"da62796403af76c80cd6ce9153ed3746\",\"data\":\"6ca9323ce139c415fdac0ed3fa25691593a4d3a475d23db806f78077caee0262\",\"tags\":[[\"pubkeys\",\"02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904\"],[\"locktime\",\"1689418329\"],[\"refund\",\"033281c37677ea273eb7183b783067f5244933ef78d8c3f15b1a77cb246099c26e\"]]}]",
  "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
  "id": "009a1f293253e41e",
  "witness": "{\"preimage\":[\"0000000000000000000000000000000000000000000000000000000000000001\"],\"signatures\":[\"60f3c9b766770b46caac1d27e1ae6b77c8866ebaeba0b9489fe6a15a837eaa6fcd6eaa825499c72ac342983983fd3ba3a8a41f56677cc99ffd73da68b59e1383\"}"
}
```

The Mint verifies:
- `SHA256(preimage) == Proof.secret.data`
- Signature matches `pubkeys`

<!-- end_slide -->

Spending Conditions (NUT-10)
---

# Example: HTLC (NUT-14)

```json
[
  "HTLC",
  {
    "nonce": "da62796403af76c80cd6ce9153ed3746",
    "data": "6ca9323ce139c415fdac0ed3fa25691593a4d3a475d23db806f78077caee0262",
    "tags": [
      [
        "pubkeys",
        "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904"
      ],
      ["locktime", "1689418329"],
      [
        "refund",
        "033281c37677ea273eb7183b783067f5244933ef78d8c3f15b1a77cb246099c26e"
      ]
    ]
  }
]
```

### Sender Pathway (timelocked refund)
If the secret is not revealed before timeout:

```json
{
  "amount": 1,
  "secret": "[\"HTLC\",{\"nonce\":\"da62796403af76c80cd6ce9153ed3746\",\"data\":\"6ca9323ce139c415fdac0ed3fa25691593a4d3a475d23db806f78077caee0262\",\"tags\":[[\"pubkeys\",\"02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904\"],[\"locktime\",\"1689418329\"],[\"refund\",\"033281c37677ea273eb7183b783067f5244933ef78d8c3f15b1a77cb246099c26e\"]]}]",
  "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
  "id": "009a1f293253e41e",
  "witness": "{\"signatures\":[\"60f3c9b766770b46caac1d27e1ae6b77c8866ebaeba0b9489fe6a15a837eaa6fcd6eaa825499c72ac342983983fd3ba3a8a41f56677cc99ffd73da68b59e1383\"]}"
}
```

The Mint verifies:
- Current time > `Proof.secret.tags.locktime`
- Signature matches `refund` public key

<!-- end_slide -->

<!-- alignment: center -->
<!-- jump_to_middle -->
Questions?
<!-- end_slide -->

<!-- alignment: center -->
<!-- jump_to_middle -->
Thank you!
---

**github.com/TheMhv**
