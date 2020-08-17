#A more compact version of the algorithm that can be executed parallelly.

list1 = [0x58, 0x76, 0x54, 0x3a, 0xbe, 0x58, 0x76, 0x54, 0xbe, 0xcd, 0x45, 0x66, 0x85, 0x65]
#        ^     ^     ^     ^     ^     ^     ^     ^     ^     ^     ^     ^     ^     ^
# Par=4: bulk  bulk  bulk  bulk  bulk  bulk  bulk  bulk  bulk  bulk  bulk  bulk  rest  rest 
#                                                                          desc  desc  desc

def parallel_roling_mac_hash(list, par):
    multiplier = 0x01000193 #algorithm parameter

    hash = [0 for x in range(par)] #the fields of the array can be computed parallelly
    mult_powers = [multiplier**(x+1) for x in range(par)]
    list_length = len(list)
    bulk = list_length//par
    rest = list_length%par

    for i in range(rest): #"rest" number of threads have to go one step further
        for j in range(bulk + 1):
            index = j * par + i
            hash[i] += list[index]
            if index > list_length-par:
                mult_index  = -par + (list_length - index) - 1 #going from highest power to first order
                hash[i] *= mult_powers[mult_index]
            else:
                hash[i] *= mult_powers[-1]
            hash[i] %= 2**32

    for i in range(rest,par): #threads for calculating the remaining data
        for j in range(bulk):
            index = j * par + i
            hash[i] += list[index]
            if index > list_length-par:
                mult_index  = -par + (list_length - index) - 1 #going from highest power to first order
                hash[i] *= mult_powers[mult_index]
            else:
                hash[i] *= mult_powers[-1]
            hash[i] %= 2**32
 
    sum = 0
    for i in range(par): #summing up results of the parallel computations (single threaded mostly)
        sum += hash[i]
        sum %= 2**32
    
    return(sum)


#TESTING

def rolling_hash_by_mac(list):
    hash = 0
    for byte in list:
        hash += byte
        hash *= 0x01000193
        hash %= 2**32
    return(hash)

print('parallel:', parallel_roling_mac_hash(list1,3))
print('parallel:', parallel_roling_mac_hash(list1,5))
print('parallel:', parallel_roling_mac_hash(list1,8))
print('expected:', rolling_hash_by_mac(list1))
