# Rolling hash
I have been looking for rolling hash functions. Found FNV and Galois Hash of the AES-GCM specification that both resemble to multiply accumlate algorithm.

In the accompanying code I described:
* how a linear multiply accumlate (which FNV is not, bit GHash is) can be used as a rolling hash function, ie. a one that portions of data can be added to the begining, removed from the end, and replaced anywhere, without having to recomputing the whole hash,
* how such a hash may be computed in arbitrarily many parallel computations, with a small summing up overhead at the very end.
