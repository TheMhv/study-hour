# - The Mint has a private key `k` and publishes a public key `K = kG`
from secp256k1lab.secp256k1 import G
k = 0x123 # Mint private key
K = k*G # Mint public key
print(f'K: {K.x}')

# - The user generates a secret `x` and computes `Y = hash_to_curve(x)`
from hashlib import sha256
from secp256k1lab.secp256k1 import GE
def hash_to_curve(x: bytes):
    DOMAIN_SEPARATOR = b"Secp256k1_HashToCurve_Cashu_"
    msg_hash = sha256(DOMAIN_SEPARATOR + x).digest()
    counter = 0
    while counter < 2**16:
        y = sha256(msg_hash + counter.to_bytes(4, 'little')).digest()
        try:
            return GE.from_bytes_compressed(b'\x02' + y)
        except:
            counter += 1
# hash_to_curve(x) = PublicKey('02' || SHA256(SHA256(b"Secp256k1_HashToCurve_Cashu_" || x) || counter))
x = b'secret'
Y = hash_to_curve(x)
print(f'Y: {Y.x}')

from secp256k1lab.secp256k1 import G, GE
Y = GE(0x5dccd27047d10d4900b8d2c4ea6795702c2d1fbe1d3fd0d1cd4b18776b12ddc0,0xe0aac02830118a3f32dbd8be47a6b3b47a00a5e3e651da7dd522d7f2b1255b40)
# - The user blinds `Y` and sends it to the mint: `B_ = Y + rG`
r = int.from_bytes(b'random blind factor')
B_ = Y+(r*G) # User blinds Y
print(f'B_: {B_.x}')

from secp256k1lab.secp256k1 import G, GE
k = 291
B_ = GE(0xce1fa59d7935d7043458e295851a0319b2ff689291707bfc9b241fc613bf2b49,0x7dd61a4dab5c36898236c7c9a280707d469d25b3a863d8aa85ec2fb4d779d516)
# - The Mint signs the blinded value `B_` without seeing `x`: `C_ = kB_`
C_ = k*B_ # Mint sign blinded value
print(f'C_: {C_.x}')

from secp256k1lab.secp256k1 import GE
x = b'secret'
r = int.from_bytes(b'random blind factor')
K = GE(0x9bdf9e67a5d0c9956a075a010fe762beb633500431dee78efebc527e53313b33,0x94264621a5960e0ee24c27926f16cad2907f2636762e8d5a17e94afd8e9d2bb0)
C_ = GE(0x45b56346c1ea87f6bd5e262229f299ba53939b398e2d833bcc70fe66ffcb6655,0x253db9d818714f360cf725ee8dec61c432d5a49cd86c3cfdc94b8d37123124c5)
# - The user unblinds the signature and obtains a valid token `(x, C)`: `C = C_ - rK = kY`
C = C_ - r*K # User can unblind C_
print(f'C: {C.x}')

from secp256k1lab.secp256k1 import GE
C = GE(0xa7910eb5049f897c6b98b5e4edb80b9ee5dd173722a9c91bd3e2b05b0e8e960a,0xe48e6a41e3c2e8d18ba164f73927ea9e26f9d5c3069793b3c4f57f1b3795701b)
k = 291
Y = GE(0x5dccd27047d10d4900b8d2c4ea6795702c2d1fbe1d3fd0d1cd4b18776b12ddc0,0xe0aac02830118a3f32dbd8be47a6b3b47a00a5e3e651da7dd522d7f2b1255b40)
# - The Mint can verify tokens: `k * hash_to_curve(x) == C`
if (k*Y == C):
    print("valid")
else:
    print("invalid")
