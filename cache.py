"""
    This file consists of Block class 
    The class encapclates various attribuutes and methods associated with Block
"""

from constants import *

class Block:

    def __init__(self, slot_num):
        self._dirty_bit = 0
        self._valid_bit = 0
        self._tag = 0x00
        self._block_number = slot_num
        self._data = [None] * BLOCK_SIZE

    """
        This method is called to put value from memory to cache
    """
    def put_in_cache(self, tag, data):
        self._valid_bit = 1
        self._tag = tag
        self._data = data

    """
        This method returns the value at a particlar location if valid bit is 1
    """
    def get_value(self, tag, offset):
        if self._valid_bit == 1 and tag == self._tag:
           print(self._tag)
           return self._data[int(offset, 16)]
        else:
            print("Cache miss occuured")
            return None
        


    def __str__(self):
        return "Dirty Bit: {}, Valid Bit: {}, Tag: {}, Block #: {}, Block Start: {}, Block End: {}".format(self._dirty_bit, self._valid_bit, self._tag, hex(self._block_number), self._data[0], self._data[len(self._data) - 1])
