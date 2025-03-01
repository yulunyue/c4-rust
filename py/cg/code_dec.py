import struct
class DecodeBase16K:
    @staticmethod
    def encode_b16k(binary_file: str) -> (int, list):
        with open(binary_file, 'rb') as file:
            buffer = file.read()
        
        encoded_values = []
        encoded_values.reserve(len(buffer) * 6 // 5)
        code = 0
        for index, byte in enumerate(buffer):
            byte_value = byte
            if index % 7 == 0:
                code = byte_value << 6
            elif index % 7 == 1:
                code |= byte_value >> 2
                code += 0x5000
                encoded_values.append(code)
                code = (byte_value & 3) << 12
            elif index % 7 == 2:
                code |= byte_value << 4
            elif index % 7 == 3:
                code |= byte_value >> 4
                code += 0x5000
                encoded_values.append(code)
                code = (byte_value & 0xf) << 10
            elif index % 7 == 4:
                code |= byte_value << 2
            elif index % 7 == 5:
                code |= byte_value >> 6
                code += 0x5000
                encoded_values.append(code)
                code = (byte_value & 0x3f) << 8
            elif index % 7 == 6:
                code |= byte_value
                code += 0x5000
                encoded_values.append(code)
                code = 0
        
        if len(buffer) % 7 > 0:
            code += 0x5000
            encoded_values.append(code)
        
        return len(buffer), encoded_values

    @staticmethod
    def decode_b16k() -> list:
        length = NNLEN // 2
        index = 0
        code = 0
        byte_value = 0
        position = 0
        characters = NNSTR.encode('utf-16le')  # assuming NNSTR is a string
        output = []
        output.reserve(length)
        
        while length > 0:
            length -= 1
            if ((1 << index) & 0x2b) != 0:
                code = characters[position] - 0x5000
                position += 1
            if index % 7 == 0:
                byte_value = (code >> 6) & 0xff
                output.append(byte_value)
                byte_value = ((code & 0x3f) << 2) & 0xff
            elif index % 7 == 1:
                byte_value |= (code >> 12) & 0xff
                output.append(byte_value)
            elif index % 7 == 2:
                byte_value = ((code >> 4) & 0xff)
                output.append(byte_value)
                byte_value = ((code & 0xf) << 4) & 0xff
            elif index % 7 == 3:
                byte_value |= (code >> 10) & 0xff
                output.append(byte_value)
            elif index % 7 == 4:
                byte_value = ((code >> 2) & 0xff)
                output.append(byte_value)
                byte_value = ((code & 3) << 6) & 0xff
            elif index % 7 == 5:
                byte_value |= (code >> 8) & 0xff
                output.append(byte_value)
            elif index % 7 == 6:
                byte_value = code & 0xff
                output.append(byte_value)

            index = (index + 1) % 7
        
        return output

    @staticmethod
    def f16_to_f32(i: int) -> float:
        if (i & 0x7FFF) == 0:
            return struct.unpack('f', struct.pack('I', (i << 16)))[0]
        
        half_sign = (i & 0x8000)
        half_exp = (i & 0x7C00)
        half_man = (i & 0x03FF)

        if half_exp == 0x7C00:
            if half_man == 0:
                return struct.unpack('f', struct.pack('I', (half_sign << 16) | 0x7F80_0000))[0]
            else:
                return struct.unpack('f', struct.pack('I', (half_sign << 16) | 0x7FC0_0000 | (half_man << 13)))[0]
        
        sign = half_sign << 16
        unbiased_exp = (half_exp >> 10) - 15
        if half_exp == 0:
            e = (half_man).bit_length() - 6
            exp = (127 - 15 - e) << 23
            man = (half_man << (14 + e)) & 0x7F_FF_FF
            return struct.unpack('f', struct.pack('I', sign | exp | man))[0]
        
        exp = ((unbiased_exp + 127) << 23)
        man = (half_man & 0x03FF) << 13
        return struct.unpack('f', struct.pack('I', sign | exp | man))[0]