import time
import random


LIMITS = {"int8_t"   : "INT8",
          "uint8_t"  : "UINT8",
          "int16_t"  : "INT16",
          "uint16_t" : "UINT16",
          "int32_t"  : "INT32",
          "uint32_t" : "UINT32",
          "int"      : "INT",
          "uint"     : "UINT",
          "int64_t"  : "INT64",
          "uint64_t" : "UINT64",
          "double"   : "DBL",
          "float"    : "FLT"}

ARRAY_LEN_LIMIT = 10


class Type:
    def __init__(self, name):
        self.name = name;
        self.max = LIMITS[name] + "_MAX"
        self.min = LIMITS[name] + "_MIN"

    def __str__(self):
        return self.name

    def is_int(self):
        if self.name == "double" or self.name == "float":
            return False
        else:
            return True

    def get_rand_value(self, st = 0, end = 5000):
        if self.is_int():
            return random.randint(st, end)
        else:
            return random.uniform(st, end)

class Elem:
    def __init__(self, elem_type):
        self.val_type = elem_type
        self.value = self.val_type.min

    def __str__(self):
        return self.value

    def rand_fill(self):
        self.value = self.val_type.get_rand_value()

class Array:
    def __init__(self, elem_type, name, size):
        self.type = Type(elem_type)
        self.name = name
        self.size = size
        self.data = [Elem(self.type) for i in range(self.size)]

    def __str__(self):
        ret = str(self.type) + " " + self.name + " [" + str(self.size) + "] = {" + str(self.data[0].value)
        for i in range (1, self.size):
            ret += ", " + str(self.data[i].value)
        ret += "}"
        return ret

    def rand_fill(self):
        for i in range (self.size):
            self.data[i].rand_fill()

class Data:
    def __init__(self, size, name_base):
        self.size = size
        self.name_base = name_base
        self.array = [Array("int8_t", name_base + str(i), 1) for i in range(self.size)]

    def __str__(self):
        ret = self.array[0].__str__() + ";"
        for i in range (1, self.size):
            ret += "\n" + self.array[i].__str__() + ";"
        return ret

    def rand_fill(self, len_limit = ARRAY_LEN_LIMIT):
        param = []
        for i in range(self.size):
            val_type = random.choice(LIMITS.keys())
            size = random.randint(1, len_limit)
            param.append([val_type, self.name_base + str(i), size])
        self.array = [Array(param [i] [0], param [i] [1], param [i] [2]) for i in range(self.size)]
        for i in range (self.size):
            self.array[i].rand_fill()

class Loop:
    def __init__(self, iter_type, in_data, out_data):
        self.type = Type(iter_type)
        self.st = self.type.min
        self.end = self.type.max
        self.step = 1
        self.in_data = in_data
        self.out_data = out_data       
        self.rand_table = []
        for i in range(self.out_data.size):
            list_i = []
            for j in range(self.out_data.array[i].size):
                list_j = []
                for k in range(self.in_data.size):
                    list_k = []
                    for l in range(self.in_data.array[k].size):
                        list_k.append(0)
                    list_j.append(list_k)
                list_i.append(list_j)
            self.rand_table.append(list_i)
        print self.rand_table

 
    def __str__(self):
        return "for(" + str(self.type) + " i = " + str(self.st) + "; i < " \
               + str(self.end) + "; i += " + str(self.step) + ")" 

    def rand_fill(self):
        self.st = self.type.get_rand_value()
        self.end = self.type.get_rand_value()
        self.step = abs(self.type.get_rand_value())
        if (self.st > self.end):
            self.step = -1 * abs(self.type.get_rand_value())
         
############################################################################### 
random.seed(time.clock)

inp =  Data(5, "inp_")
inp.rand_fill()
print inp

out = Data(3, "out_")
out.rand_fill()
print out

a = Loop ("int", inp, out)
a.rand_fill()
print a
