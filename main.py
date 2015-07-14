import time
import random

INP_ARRAY_NUM = 5
OUT_ARRAY_NUM = 5
ARRAY_LEN_LIMIT = 200

###############################################################################

LIMITS = {"int8_t"   : "INT8",
          "uint8_t"  : "UINT8",
          "int16_t"  : "INT16",
          "uint16_t" : "UINT16",
          "int32_t"  : "INT32",
          "uint32_t" : "UINT32",
          "int"      : "INT",
          "int64_t"  : "INT64",
          "uint64_t" : "UINT64"}

MAX_LIMITS_NUM = {"INT8_MAX"   : 127,
                  "UINT8_MAX"  : 255,
                  "INT16_MAX"  : 32767,
                  "UINT16_MAX" : 65535,
                  "INT32_MAX"  : 2147483647,
                  "UINT32_MAX" : 4294967295,
                  "INT_MAX"    : 2147483647,
                  "UINT_MAX"   : 4294967295,
                  "INT64_MAX"  : 9223372036854775807, 
                  "UINT64_MAX" : 18446744073709551615}

MIN_LIMITS_NUM = {"INT8_MIN"   : -128,
                  "UINT8_MIN"  : 0,
                  "INT16_MIN"  : -32768,
                  "UINT16_MIN" : 0,
                  "INT32_MIN"  : -2147483648,
                  "UINT32_MIN" : 0,
                  "INT_MIN"    : -2147483648,
                  "UINT_MIN"   : 0,
                  "INT64_MIN"  : -9223372036854775808,
                  "UINT64_MIN" : 0}

###############################################################################

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
        ret = "\t\t" + str(self.type) + " " + self.name + " [" + str(self.size) + "] = {" + str(self.data[0].value)
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

    def print_in_call(self):
        ret = self.array[0].name
        for i in range (1, self.size):
            ret += ", " + self.array[i].name
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
            for j in range(self.in_data.size):
                list_i.append(0)
            self.rand_table.append(list_i)
 
    def __str__(self):
        ret = "\t\tfor(" + str(self.type) + " i = " + str(self.st) + "; i < " \
               + str(self.end) + "; i += " + str(self.step) + ") {\n"
        for i in range(self.out_data.size):
            tmp_line = "\t\t\t\t"
            tmp_line += self.out_data.array[i].name + " [i] = "
            for j in range(self.in_data.size):
                tmp_line += "(" + str(self.rand_table[i][j]) + ") * " \
                            + self.in_data.array[j].name + " [i] + "
            ret += tmp_line [:-3] + ";\n"
        ret += "\t\t}\n"
        return ret

    def rand_fill(self):
        min_size = ARRAY_LEN_LIMIT
        for i in range(self.out_data.size):
            for j in range(self.in_data.size):
                min_size =  min(self.in_data.array[i].size, 
                                self.out_data.array[i].size, min_size)
                self.rand_table[i][j] = self.in_data.array[j].type.get_rand_value()

        self.st = 0
        self.end = min_size - 1
        self.step = random.randint(self.st, self.end)
        self.step = max(self.step, 1)

    def print_checksum(self):
        ret = "\t\tuint64_t checksum = UINT64_MAX;\n"
        for i in range(self.out_data.size):
            ret += "\t\tfor (int i = 0; i < " + str(self.out_data.array[i].size) + "; i++)\n"
            ret += "\t\t\t\tchecksum ^= (uint64_t)" + self.out_data.array[i].name + "[i];\n"
        return ret       
############################################################################### 
random.seed(time.clock)
#random.seed(10)

inp =  Data(INP_ARRAY_NUM, "inp_")
inp.rand_fill()

out = Data(OUT_ARRAY_NUM, "out_")
out.rand_fill()

loop = Loop ("int", inp, out)
loop.rand_fill()
###############################################################################

f = open("func.cpp", "w")

f.write("#include <stdint.h>\n")
f.write("#include <limits.h>\n")

f.write( "void func (")
f.write(out.print_as_param())
f.write(") {\n")
f.write(inp.__str__())
f.write("\n/////////////////////////////////////////////////////////////////////////////////////////////////////\n")
f.write(loop.__str__())
f.write("}")

f.close()
###############################################################################

t = open("test.cpp", "w")

t.write("#include <stdint.h>\n")
t.write("#include <limits.h>\n")
t.write("#include <stdio.h>\n")

t.write("extern void func (")
t.write(out.print_as_param())
t.write(");\n")

t.write("int main() {\n")
t.write(out.__str__())
t.write("\n\n\t\tfunc (")
t.write(out.print_in_call())
t.write(");\n\n")
t.write(loop.print_checksum())
t.write('\n\t\tprintf("%lu\\n", checksum);\n')
t.write("}")

t.close()
