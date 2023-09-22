import struct
import binascii

odd_primes = [
       3,    5,    7,   11,   13,   17,   19,   23,   29,   31,   37,   41,   43,   47,   53,   59,
      61,   67,   71,   73,   79,   83,   89,   97,  101,  103,  107,  109,  113,  127,  131,  137,
     139,  149,  151,  157,  163,  167,  173,  179,  181,  191,  193,  197,  199,  211,  223,  227,
     229,  233,  239,  241,  251,  257,  263,  269,  271,  277,  281,  283,  293,  307,  311,  313,
     317,  331,  337,  347,  349,  353,  359,  367,  373,  379,  383,  389,  397,  401,  409,  419,
     421,  431,  433,  439,  443,  449,  457,  461,  463,  467,  479,  487,  491,  499,  503,  509,
     521,  523,  541,  547,  557,  563,  569,  571,  577,  587,  593,  599,  601,  607,  613,  617,
     619,  631,  641,  643,  647,  653,  659,  661,  673,  677,  683,  691,  701,  709,  719,  727,
     733,  739,  743,  751,  757,  761,  769,  773,  787,  797,  809,  811,  821,  823,  827,  829,
     839,  853,  857,  859,  863,  877,  881,  883,  887,  907,  911,  919,  929,  937,  941,  947,
     953,  967,  971,  977,  983,  991,  997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051,
    1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171,
    1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289,
    1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427,
    1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523,
    1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597, 1601, 1607, 1609, 1613, 1619, 1621,
]
class Xorshift:
    def __init__(self, seed):
        self.states = [0x6C078966, 0xDD5254A5, 0xB9523B81, 0x03DF95B3]

        # initialize internal states
        if seed == 0:
            return
        seed = seed ^ (seed >> 30)
        seed = (seed * (0x6C078966 - 1)) & 0xFFFFFFFF
        seed = seed + 1
        self.states[0] = seed

        seed = seed ^ (seed >> 30)
        seed = (seed * (0x6C078966 - 1)) & 0xFFFFFFFF
        seed = seed + 2
        self.states[1] = seed

        seed = seed ^ (seed >> 30)
        seed = (seed * (0x6C078966 - 1)) & 0xFFFFFFFF
        seed = seed + 3
        self.states[2] = seed

    def xorshift(self, arg):
        x = self.states[0]
        y = self.states[3]

        self.states[0] = self.states[1]
        self.states[1] = self.states[2]
        self.states[2] = self.states[3]
        x = x ^ ((x << 11) & 0xFFFFFFFF)
        x = x ^ ((x >> 8) & 0xFFFFFFFF)
        y = y ^ ((y >> 19) & 0xFFFFFFFF)
        self.states[3] = x ^ y
        if arg == 0:
            return self.states[3]
        return self.states[3] % arg

class YWCipher(Xorshift):
    def __init__(self, seed, count):
        self.table = [x for x in range(0x100)]
        super().__init__(seed)

        # generate table
        for i in range(count):
            r = self.xorshift(0x10000)
            r1, r2 = r & 0xFF, (r >> 8) & 0xFF
            if r1 != r2:
                a, b = self.table[r1], self.table[r2]
                self.table[a], self.table[b] = self.table[b], self.table[a]

    def encrypt(self, data):
        out = bytearray()
        for i, x in enumerate(data):
            if i % 0x100 == 0:
                #print("block {}".format((i & 0xff00) >> 8))
                ka = odd_primes[self.table[(i & 0xff00) >> 8]]
            kb = self.table[ka * (i + 1) & 0xff]
            out.append(data[i] ^ kb)
        return out

    def decrypt(self, data):
        return encrypt(self, data)

def yw_proc(data, isEncrypt, key=None, head=None, validator=None):
    out = bytearray()
    length = len(data)
    new_crc32 = struct.unpack("<I", data[-8:-4])[0]
    seed = struct.unpack("<I", data[-4:])[0]
    if not isEncrypt:
        if binascii.crc32(data[:-8]) != new_crc32:
            raise Exception("Checksum does not match")
    c = YWCipher(seed, 0x1000)
    out += c.encrypt(data[:-8])
    out += data[-8:]
    if isEncrypt:
        new_crc32 = binascii.crc32(out[:-8])
        struct.pack_into("<I", out, length - 8, new_crc32)
    return bytes(out)