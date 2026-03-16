from secp256k1lab.secp256k1 import Scalar, G
from random import randint
import json

def gen_keys():
    priv = Scalar(randint(0, Scalar.SIZE-1))
    pub = priv*G

    return (priv, pub)

ALICE = gen_keys()
BOB = gen_keys()

Z = ALICE[0]*BOB[1]
r = int(str(Z.x), 16)
P_ = BOB[1] + r*G

print("Alice", json.dumps({
    "e": ALICE[0].to_bytes().hex(),
    "E": str(ALICE[1].x),
    "Z": str(Z.x),
    "r": r,
    "P_": str(P_.x)
}, indent=2))

assert ALICE[0]*BOB[1] == BOB[0]*ALICE[1], "Z is not equal for Alice and Bob"

Z = BOB[0]*ALICE[1]
r = int(str(Z.x), 16)
P = P_ - r*G

print("Bob", json.dumps({
    "p": BOB[0].to_bytes().hex(),
    "pubkey": str(BOB[1].x),
    "E": str(ALICE[1].x),
    "Z": str(Z.x),
    "r": r,
    "P": str(P.x)
}, indent=2))

assert P == BOB[1], "P' is not the Bob public key"
