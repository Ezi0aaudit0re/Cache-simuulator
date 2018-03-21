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
    # we modulo with 256 so that we can store 255 values in bit 0xff 0 - 255 or 1 - 256
    memory = [key % 256 for key,value in enumerate(memory) ]



    while(True):
        ans = ask_question()
        #ans = "w"
        # check if user wanted to read
        if(ans == "r" or ans == "read"):
            read(cache, memory)
        elif(ans == "w" or ans == "write"):
            write(memory, cache) 
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
    


"""
    This function reads from cache 
    If there is a cache miss it will get data from memory 
"""
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
            print("At the byte the value is: {} (Cache MISS)".format(hex(value)))
        else:
            print("Something went wrong cannot copy from memory to cache")

    else:
        # cache hit 
        print("At the byte the value is: {} (Cache HIT)".format(hex(value)))


"""
    this function looks if a particlar value is in cache
    :param: cache -> The cache to look in 
    :param: tag    
    :param: block_offset
    :param: block_number
    :return: value / None if nothing is found
"""
def check_in_cache(cache, tag, block_num, block_offset):

    # check if the valid bit is set to 1
    if(getattr(cache[int(block_num, 16)], "_valid_bit")):
        # find that value at the specifed slot
        slot = cache[int(block_num, 16)]
        value = slot.get_value(tag, block_offset)
        return value
    else:
        return None



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

    # get tag, block number, block offset
    (tag, block_num, block_offset) = split(user_in)


    # check if Dirty bit is 1 then update memory
    if(getattr(cache[int(block_num, 16)], "_dirty_bit")):
        update_memory(cache, memory, user_in, block_num)

    # get the end value of the block
    # we do (end + 1) because block goes to arr[start_included : end not_incldued]
    block_data = memory[block_begin: (block_end + 1) ] 


    

    # add to the cache
    cache[int(block_num, 16)].put_in_cache(tag, block_data)





"""
    This function updates the memory if the dirty bit / modified bit is 1
    :param: cache -> the cache to copy from
    :param: memory -> the main memory 
    :address: -> int representation of the address user reqeusted that block from cache to be copied to memory 
    :block_num: -> str representation of a hex number
"""
def update_memory(cache, memory, address, block_num):
    # check if we have a dirty bit and the memory needs to be updated
    begin_memory = address
    begin_memory >>= 4
    begin_memory <<= 4
    end_memory = begin_memory + (BLOCK_SIZE - 1)


    # get data from the cache
    data = getattr(cache[int(block_num, 16)], "_data")

    # replace the starting to the end block with new values
    memory[begin_memory : (end_memory + 1)] = data





"""
    This function gets input from the user and writes to the cache 
    If the address is not in cache then it will get cache from memory
    and then write to it. 
    Updates the Dirty Bit of that slot to 1 
    :param: memory, cache 
"""
def write(memory, cache):
    # get address from user 
    address = input("What address(in HEX) would you want to write to: ")

    # user can enter a hex
    # hex eg = 24
    try:
        address = int(address, 16)
    except Exception:
        print("Please enter a valid address in hex")
        return

    # check if user entered range is in memory also func takes string hex representation
    if(user_in_check_range_in_memory(hex(address))):
        value = input("Please enter a value(in hex) to store at this address EG 2f: ")
        try:
            value = int(value, 16)
        except Exception:
            print("Please enter a correct value")
            return 


        (tag, block_num, block_offset) = split(address)

        # check valid bit to see if it is a cache miss or cache hit 
        if(check_in_cache(cache, tag, block_num, block_offset)):
            # cache hit
            # write to cache
            cache[int(block_num, 16)].update_address(tag, int(block_offset, 16), value)
            print("The value {} has been saved to the address {} (CACHE HIT)".format(hex(value), hex(address)))
        else:
            # chache miss
            copy_from_memory_to_cache(address, memory, cache)
            print("The value {} has been saved to the address {} (CACHE MISS)".format(hex(value), hex(address)))

        






"""
    This function displays the cache
    :param: cache
"""
def display_cache(cache):
    print("SLOT \t VALID \t TAG \t DIRTY \t DATA")
    for slot in cache:
        print("{} \t {} \t {} \t {} \t {}".format(hex(getattr(slot, "_block_number")), getattr(slot, "_valid_bit"), getattr(slot, "_tag"), getattr(slot, "_dirty_bit"), [value if value == None else hex(value) for value in getattr(slot, "_data")]))
    



if __name__ == "__main__":
    main()





