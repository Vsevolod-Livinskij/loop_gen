import time
import random


LIMITS = {"int8_t"   : "INT8",
          "uint8_t"  : "UINT8",
          "int16_t"  : "INT16",
          "uint16_t" : "UINT16",
          "int32_t"  : "INT32",
          "uint32_t" : "UINT32",
          "int"      : "INT",
          "int64_t"  : "INT64",
          "uint64_t" : "UINT64",
          "double"   : "DBL",
          "float"    : "FLT"}

ARRAY_LEN_LIMIT = 3

MAX_LIMITS_NUM = {"INT8_MAX"   : 127,
                  "UINT8_MAX"  : 255,
                  "INT16_MAX"  : 32767,
                  "UINT16_MAX" : 65535,
                  "INT32_MAX"  : 2147483647,
                  "UINT32_MAX" : 4294967295,
                  "INT_MAX"    : 2147483647,
                  "UINT_MAX"   : 4294967295,
                  "INT64_MAX"  : 9223372036854775807, 
                  "UINT64_MAX" : 18446744073709551615,
                  "DBL_MAX"    : 18446744073709551615,
                  "FLT_MAX"    : 18446744073709551615}

MIN_LIMITS_NUM = {"INT8_MIN"   : -128,
                  "UINT8_MIN"  : 0,
                  "INT16_MIN"  : -32768,
                  "UINT16_MIN" : 0,
                  "INT32_MIN"  : -2147483648,
                  "UINT32_MIN" : 0,
                  "INT_MIN"    : -2147483648,
                  "UINT_MIN"   : 0,
                  "INT64_MIN"  : -9223372036854775808,
                  "UINT64_MIN" : 0,
                  "DBL_MIN"    : -18446744073709551615,
                  "FLT_MIN"    : -18446744073709551615}


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

    def get_rand_value(self):
        st = MIN_LIMITS_NUM[self.min]
        end = MAX_LIMITS_NUM[self.max] 
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

    def print_as_param(self):
        return  str(self.type) + "* " + self.name

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

    def print_as_param(self):
        ret = self.array[0].print_as_param()
        for i in range (1, self.size):
            ret += ", " + self.array[i].print_as_param()
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
        self.st = 0
        self.end = 1
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
 
    def __str__(self):
        ret = "for(" + str(self.type) + " i = " + str(self.st) + "; i < " \
               + str(self.end) + "; i += " + str(self.step) + ") {\n"
        for i in range(self.out_data.size):
            tmp_line = ""
            for j in range(self.out_data.array[i].size):
                tmp_line += self.out_data.array[i].name + " [" + str(j) + "] = "
                for k in range(self.in_data.size):
                    for l in range(self.in_data.array[k].size):
                        tmp_line += str(self.rand_table[i][j][k][l]) + " * " \
                               + self.in_data.array[k].name + " [" + str(l) + "] + "
                ret += tmp_line [:-3] + ";\n"
        ret += "}\n"
        return ret

    def rand_fill(self):
        max_size = -1
        for i in range(self.out_data.size):
            for j in range(self.out_data.array[i].size):
                max_size = max(self.out_data.array[i].size, max_size)
                for k in range(self.in_data.size):
                    for l in range(self.in_data.array[k].size):
                        max_size =  max(self.in_data.array[i].size, max_size)
                        self.rand_table[i][j][k][l] = self.in_data.array[k].type.get_rand_value()
        
        self.st = 0
        self.end = random.randint(0, max_size + 1)
        self.step = random.randint(self.st, self.end)
############################################################################### 
random.seed(time.clock)
#random.seed(10)

inp =  Data(5, "inp_")
inp.rand_fill()

out = Data(3, "out_")
out.rand_fill()

loop = Loop ("int", inp, out)
loop.rand_fill()
###############################################################################

print "#include <stdint.h>"
print "#include <limits.h>\n"

print "void foo ("
print out.print_as_param()
print ") {\n"
print inp
print "//***************************************"
print loop
print "}"
