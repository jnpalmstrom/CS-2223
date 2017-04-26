# Name: Jack Palmstrom
# Date: 4/14/2017

import os
import heapq


# Create a class for the nodes of the Huffman Tree
class HeapNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __cmp__(self, other):
        if other is None:
            return -1

        if not isinstance(other, HeapNode):
            return -1

        return self.freq > other.freq


class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.code = {}
        self.rev_mapping = {}

    # Compression Functions -
    def make_frequency(self, text):

        frequency = {}

        for character in text:
            if not character in frequency:
                frequency[character] = 0

            frequency[character] += 1

        return frequency

    def make_heap(self, frequency):
        for key in frequency:
            node = HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while len(self.heap) > 1:
            first_node = heapq.heappop(self.heap)
            sec_node = heapq.heappop(self.heap)

            merged = HeapNode(None, first_node.freq + sec_node.freq)
            merged.left = first_node
            merged.right = sec_node

            heapq.heappush(self.heap, merged)

    def make_helper(self, root, current_code):

        if root is None:
            return

        if root.char is not None:

            self.code[root.char] = current_code
            self.rev_mapping[current_code] = root.char
            return

        self.make_helper(root.left, current_code + "0")
        self.make_helper(root.right, current_code + "1")

    def make_codes(self):

        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_helper(root, current_code)

    def get_encoded(self, text):

        encoded_txt = ""

        for character in text:
            encoded_txt += self.code[character]

        return encoded_txt

    def pad_encoded(self, encoded_txt):

        extra_padding = 8 - len(encoded_txt) % 8

        for index in range(extra_padding):
            encoded_txt += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_txt
        return encoded_text

    def get_byte_array(self, pad_encoded_txt):

        if len(pad_encoded_txt) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)

        b_arr = bytearray()

        for i in range(0, len(pad_encoded_txt), 8):
            byte = pad_encoded_txt[i:i + 8]
            b_arr.append(int(byte, 2))
        return b_arr

    def compress(self):

        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"

        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip()

            frequency = self.make_frequency(text)
            self.make_heap(frequency)
            self.merge_nodes()
            self.make_codes()

            encoded_text = self.get_encoded(text)
            padded_encoded_text = self.pad_encoded(encoded_text)

            b_arr = self.get_byte_array(padded_encoded_text)
            output.write(bytes(b_arr))

        print("The File has been compressed.")
        return output_path

    # Decompression Functions -
    def remove_padding(self, pad_encoded_text):

        pad_info = pad_encoded_text[:8]
        extra_padding = int(pad_info, 2)

        pad_encoded_text = pad_encoded_text[8:]
        encoded_txt = pad_encoded_text[:-1 * extra_padding]

        return encoded_txt

    def decode_text(self, encoded_text):

        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit

            if current_code in self.rev_mapping:
                character = self.rev_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decompress(self, input_path):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed" + ".txt"

        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ""

            some_bytes = file.read(1)
            while some_bytes != "":
                some_bytes = ord(some_bytes)
                some_bits = bin(some_bytes)[2:].rjust(8, '0')
                bit_string += some_bits
                some_bytes = file.read(1)

            encoded_text = self.remove_padding(bit_string)

            decompressed_text = self.decode_text(encoded_text)

            output.write(decompressed_text)

        print("The File has been decompressed.")
        return output_path
