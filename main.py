"""
    This program implements direct mapped cache and write back system for writing 
    BLOCK SIZE = 16 bytes
    MEMORY SIZE = 2048 bytes
    CACHE SIZE = 16 SLOTS
    Block # size = (2 * 4 slots) = 4 bits = 1 hex
    Block Offset size = (2 * 4 block size) = 4 bits = 1 hex
    BLOCK BEGIN 0x0
    BLOCK END 0xF

"""

__author__ = "Aman Nagpal"
__email__ = "amannagpal4@gmail.com"


from cache import Block
from helper import *
from constants import *




def main():
    # create an array of length 2048
    memory = [None] * MEM_SIZE
    # initialize the cache with empty blocks to act as cache just started

    cache = [Block(i) for i in range(CACHE_SIZE)]

    # initialize the memory with values
    memory = [key % 16 for key,value in enumerate(memory) ]

    while(True):
        ans = ask_question()
        # check if user wanted to read
        if(ans == "r" or ans == "read"):
            read(cache, memory)
        elif(ans == "w" or ans == "write"):
            #Write 
            pass
        elif(ans == "d" or ans == "display"):
            display_cache(cache)
        else:
            print("Please enter a correct input")


"""
    This fnction takes in the user_in and splits it 
    :param: user_in the input by user
    :return: (tag, block_number, block_offset)
"""
def split(user_in):
    tag = get_shifted_value(user_in, TAG_BITMASK, 8)
    block_offset = get_shifted_value(user_in, BLOCK_OFFSET_BITMASK)
    block_num = get_shifted_value(user_in, BLOCK_NUMBER_BITMASK, 4)
    return (hex(tag), hex(block_num), hex(block_offset))
    


def read(cache, memory):
    user_in = input("What address would you like to read: ")

    # sanity check user doensot enter value which is not even in cache 
    # if entered value is greater than 0x7ff
    if user_in_check_range_in_memory(user_in) == False:
        print("The value you entered is not even in memory")
        return 



    try:
        user_in = int(user_in, 16)
    except Exception:
        print("Please enter a correct hex value")
        return

    tag, block_num, block_offset = split(user_in)

    # check if value is in cache
    value = check_in_cache(cache, tag, block_num, block_offset)
    
    # check if we didnt find cache 
    if value == None:
        # didnt find in cache 
        copy_from_memory_to_cache(user_in, memory, cache)
        value = check_in_cache(cache, tag, block_num, block_offset)
        if(value):
            print("Value: {} (Cache MISS)".format(value))
        else:
            print("Something went wrong cannot copy from memory to cache")

    else:
        # cache hit 
        print("Value: {} (Cache HIT)".format(value))


"""
    this function looks if a particlar value is in cache
    :param: cache -> The cache to look in 
    :param: tag    
    :param: block_offset
    :param: block_number
    :return: value / None if nothing is found
"""
def check_in_cache(cache, tag, block_num, block_offset):
    slot = cache[int(block_num, 16)]
    value = slot.get_value(tag, block_offset)
    return value



"""
    This function copies from memory to cache 
    Copies from the begning to the end 
    :param: user_in -> THe address user requested
"""
def copy_from_memory_to_cache(user_in, memory, cache):
    block_begin = user_in
    # get the begning value of the block
    block_begin >>= BLOCK_BEGIN_SHIFT
    block_begin <<= BLOCK_BEGIN_SHIFT

    block_end = block_begin + (BLOCK_SIZE - 1) # 15 more from 7a0 16 more would lead to 7b0

    # get the end value of the block
    # we do (end + 1) because block goes to arr[start_included : end not_incldued]
    block_data = memory[block_begin: (block_end + 1) ] 


    # add to the cache

    # get tag, block number, block offset
    (tag, block_num, block_offset) = split(user_in)

    cache[int(block_num, 16)].put_in_cache(tag, block_data)


def display_cache(cache):
    print("SLOT \t VALID \t TAG \t DATA")
    for slot in cache:
        print("{} \t {} \t {} \t {} \t".format(hex(getattr(slot, "_block_number")), getattr(slot, "_valid_bit"), getattr(slot, "_tag"), [value if value == None else hex(value) for value in getattr(slot, "_data")]))
    



if __name__ == "__main__":
    main()





