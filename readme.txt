Author - Aman Nagpal 
Email - amannagpal4@gmail.com


This program simulates a direct mapped cache and write back mode of writing to memory. 

The memory size is 2k we use a list to represent a memory. 
We fill the memory with dummy values between 0 - 255


The cache has 16 slots 
Block Size is also 16


Please use python 3 to run this code 

When ever we are converting a string to a hex value we do int(<num>, 16) because hex is base 16

Handling of dirty bit that is from 0 - 1 is handled by block class

constants are defined in constants.py 

there are various helper functions that are in helper.py 

cache.py has a class that represents a block in cache

###########################
to run the code:

python main.py 
