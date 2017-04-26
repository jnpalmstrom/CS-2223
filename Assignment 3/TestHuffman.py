from Huffman import HuffmanCoding

path = 'sample.txt'  # Change file path

h = HuffmanCoding(path)
output_path = h.compress()
h.decompress(output_path)
