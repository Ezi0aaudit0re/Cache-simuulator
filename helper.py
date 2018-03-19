"""
    This is a helper file for the program
"""

__author__ = "Aman Nagpal"
__email__ = "amannagpal4@gmail.com"


"""
    Print the array provided in its hex value
    :param: list
"""
def print_hex_value(list_name):
    for value in list_name:
        print(hex(value))



"""
    THis function gets input from user 
    :return: string in lower case letters

"""
def ask_question():
    ans = input("(R)ead, (W)rite or (D)isplay Cache ? Enter 'quit' to exit the program\n")
    ans = ans.lower()
    if (ans == "q" or ans == "exit" or ans == "quit"):
        exit(0)
    return ans



"""
    This function does the bitwise and comparision to isolate the particular field 
    It then shifts it to the end 
    :param: user_in -> hex value of the user_in 
    :param: bitmask -> The bitmask required to isolate a particular field
    :param: shift -> the number of bits to shift default 0
    :return: temp_value -> The shifted value

"""
def get_shifted_value(instr, bitmask, shift=0):
    # do a bitwise and 
    temp_value = (instr & bitmask)

    # do the logical shift
    temp_value >>= shift

    #return that shifted value
    return temp_value


"""
    This method checks if the value entered by user is within the range of data in memory
    [0x0) - 0x7ff]

"""
def user_in_check_range_in_memory(user_in):
    if(int(user_in, 16) <= 0x7ff):
        return True
    else:
        return False




