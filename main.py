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


class Type:
    def __init__(self, name):
        self.name = name;
        self.max = LIMITS[name] + "_MAX"
        self.min = LIMITS[name] + "_MIN"

class Data:
    def __init__(self, data_type, size):
        self.type = Type(data_type)
        self.size = size    

    def __

a = Type("float")
print a.name
print a.max
print a.min

b = Data("int64_t", 20)
print b.type.name
print b.type.max
print b.type.min
print b.size

