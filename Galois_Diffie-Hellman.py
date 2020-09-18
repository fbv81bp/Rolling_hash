# Diffie-Hellman like computation using AES_GCM's Galois hash's rolling hash property

def Galois_Mult(x, y):
    res = 0
    for i in range(127, -1, -1):
        res ^= x * ((y >> i) & 1)  # branchless
        x = (x >> 1) ^ ((x & 1) * 0xE1000000000000000000000000000000)
    return res

def Galois_Power(h, mask):
    h_pows = h
    gc_hash = 0
    for m in range(128):
        gc_hash ^= h_pows * (mask & 1) # adding powers of 2 if corresponding mask bit is 1
        h_pows = Galois_Mult(h_pows, h_pows) # calculating h's powers of 2
        mask >>= 1 # shift out used mask bit
    return(gc_hash)

# shared initial vector
H  = 0xc1aca11ed44055ad4ac001caffe1a77e

# Alice's secret
As = 0x64899328639863198635298635298635

# Bob's secret
Bs = 0xbacecabdceadbecdabfbdcfaeddfecde

# Exchanged messages
Amsg = Galois_Power(H, As)
Bmsg = Galois_Power(H, Bs)
print(hex(Amsg))
print(hex(Bmsg))
print()

# computing shared secret
Acomputes = Galois_Power(Bmsg, As)
Bcomputes = Galois_Power(Amsg, Bs)

# check output
print(hex(Acomputes))
print(hex(Bcomputes))
print(Acomputes == Bcomputes)

