# Rolling hash
I have been looking for rolling hash functions. Found FNV and Galois Hash of the AES-GCM specification that both resemble to a multiply accumlate structure.

In the accompanying code I described:
* how a linear multiply accumlate (which FNV is not, but Ghash-core is) can be used as a rolling hash function, ie. a one whose portions of data can be added to the begining, removed from the end, and btw. replaced anywhere inbetween, without having to recompute the whole hash,
* how such a hash may be calculated in arbitrarily many parallel computations, with a small summing up overhead at the very end.
