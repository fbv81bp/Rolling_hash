def rolling_hash_by_mac(list):
    hash = 0
    for byte in list:
        hash += byte
        hash *= 0x01000193
        hash %= 2**32
    return(hash)

#powers of the multiplier on each list member in the result
#         6     5     4     3     2     1
list1 = [0x58, 0x76, 0x54, 0x3a, 0xbe, 0xcd]
list2 = [0x58, 0x67, 0x54, 0x3a, 0xeb, 0xcd]


x = rolling_hash_by_mac(list1)
y = rolling_hash_by_mac(list2)
print('1st hash:', x)
print('2nd hash:', y)


#TEST MODIFICATION OF DATA

x -= 0x76*0x01000193**5%2**32
x -= 0xbe*0x01000193**2%2**32
if x<0:
    x += 2**32
print('after erasing "0x76" and "0xbe" form 1st:', x)


y -= 0x67*0x01000193**5%2**32
y -= 0xeb*0x01000193**2%2**32
if y<0:
    y += 2**32
print('after erasing "0x67" and "0xeb" form 2nd:', y)


#TEST ROLLING PROPERTY

x = rolling_hash_by_mac(list1[0:5]) #queue length is 5
print('before shifting queue:', x)

#manually shifting hash value

x -= list1[0]*0x01000193**5%2**32 #queue length is 5
if x<0:
    x += 2**32

x += list1[5]
x *= 0x01000193
x %= 2**32
print('shifting queue test:', x)

print('expected after shifting queue:', rolling_hash_by_mac(list1[1:6])) #queue length is 5


#HASHING IN PARALLEL FOR PERFOMANCE
def rolling_hash_by_mac_parallel(list, par):
    hash = [0 for x in range(par)] #the fields of the array can be computed parallelly
    par_mult = 0x01000193**par
    bulk = (len(list)-par)//par
    for i in range(par):
        for j in range(bulk): #parallelly computable loops for the list length whole multiple parts
            hash[i] += list[j*par+i]
            hash[i] *= par_mult
            hash[i] %= 2**32
    rest = (len(list)-par)%par
    for k in range(rest): #parallelly computable loop for mostly the rest of the list
        hash[k] += list[-par-rest+k]
        hash[k] *= par_mult
        hash[k] %= 2**32
    sum = 0
    for l in range(par): #multiplying the last "par" long portion with ascending powers
        hash[(l+rest)%par] += list[-par+l]
        hash[(l+rest)%par] *= 0x01000193**(par-l-1)
        sum %= 2**32
    for m in range(par): #summing up results of possibly parallel computations
        sum += hash[m]
        sum %= 2**32
    sum *= 0x01000193
    sum %= 2**32
    return(sum)

list3 = [0x58, 0x76, 0x54, 0x3a, 0xbe, 0x58, 0x76, 0x54, 0x3a, 0xbe, 0xcd]

print('parallel 1st:', rolling_hash_by_mac_parallel(list3[0:-2], 4))
print('parallel 2nd:', rolling_hash_by_mac_parallel(list3[1:-1], 4))
print('expected 1st:', rolling_hash_by_mac(list3[0:-2]))
print('expected 2nd:', rolling_hash_by_mac(list3[1:-1]))
