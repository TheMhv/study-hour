from secp256k1lab.secp256k1 import Scalar, G
from random import randint, choice
from hashlib import sha256

# Gen public keys
keys = []
for i in range(10):
    p = Scalar(randint(0, Scalar.SIZE-1)) # private key
    P = p*G # public key
    keys.append((p, P))

# Generate a scalar `e` and compute their public key `E`
e = Scalar(randint(0, Scalar.SIZE-1))
E = e*G

# For each public key `P`, do:
i = 0
secret_pks = {}
for (priv, pub) in keys:
    # a. A shared secret
    Zx = (e*pub).x
    # A index
    # i
    # blind scalar
    ri = Scalar(int.from_bytes(
        sha256(b"Cashu_P2PK_v1" + Zx.to_bytes() + str(i).encode()).digest()
    ))
    # Blind public key
    P_ = pub + (ri*G)
    # Construct the secret with P'
    secret_pks[i] = P_
    i += 1

### Recebedor
(rec_priv, rec_pub) = choice(keys)
# Read `E` from `p2pk_e` and the index `i`
# Calculate unique shared secret
Zx = (rec_priv * E).x
print("Receiver Public Key:", rec_pub.x)
for i, P_ in secret_pks.items():
    # Blinded scalar
    ri = Scalar(int.from_bytes(
        sha256(b"Cashu_P2PK_v1" + Zx.to_bytes() + str(i).encode()).digest()
    ))
    # Calculate the public point from ri
    Ri = ri*G
    # Unblind the public key
    P = P_ - Ri
    # validate if x(P) == x(pG)
    if P.x == rec_pub.x:
        print(P.x)
