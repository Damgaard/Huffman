from collections import Counter, namedtuple
from bitstring import BitArray, BitStream, ReadError
from heapq import heapify, heappop, heappush


Node = namedtuple('Node', 'weight char left right')
LEFT_BIT = '0'
RIGHT_BIT = '1'


def encode(path, string, tree=None):
    """
    Take the string, huffman encode it and save it at path.

    If tree is not given, the most optimal huffman encoding will be calculated
    and used as tree.
    """
    tree = tree or build_tree(string)
    prefixes = _make_prefix(tree)
    bitstring = _chars_to_bits(string, prefixes)
    _dump(path, bitstring)
    return tree


def decode(path, tree):
    """Decode the huffman encoded file at path with encoding in tree."""
    with open(path, 'rb') as bitfile:
        bitstring = BitArray(bitfile).bin
    return _bits_to_chars(tree, bitstring)


def build_tree(string):
    """Build the huffman tree."""
    freq = _get_freq(string)
    if not freq:
        return None
    heap = [Node(weight, key, None, None) for key, weight in freq.iteritems()]
    heapify(heap)
    while len(heap) > 1:
        left = heappop(heap)
        right = heappop(heap)
        new_node = Node(left.weight + right.weight, None, left, right)
        heappush(heap, new_node)
    return heap.pop()


def _bits_to_chars(tree, bitstring):
    """Decode the bitstring using the huffman tree."""
    def next_char(node):
        if node.char is not None:
            return node.char
        try:
            bit = bitstream.read('bin:1')
        except ReadError, e:
            if e.msg.startswith('Reading off the end of the data.'):
                return ''
            raise
        next_node = node.left if bit == LEFT_BIT else node.right
        return next_char(next_node)
    bitstream = BitStream(bin=bitstring)
    result = []
    while bitstream.pos != bitstream.length:
        result.append(next_char(tree))
    return "".join(result)


def _chars_to_bits(string, prefixes):
    """Takes a string and returns a huffman encoded bitstring."""
    bitstring = "".join(prefixes[ch] for ch in string)
    if len(bitstring) % 8:
        bitstring += (8 - len(bitstring) % 8) * LEFT_BIT
    return bitstring


def _dump(path, bitstring):
    """_dump the bitstring as a bitarray into the file at path."""
    with open(path, 'wb') as outfile:
        bitarray = BitArray(bin=bitstring)
        outfile.write(bitarray.bytes)


def _get_freq(string):
    """Returns a dict of the frequencies of chars in the string."""
    freq = Counter(string)
    for key, value in freq.iteritems():
        freq[key] = value / float(len(string))
    return freq


def _make_prefix(tree):
    """Make prefixes for the chars in the tree."""
    def prefix_helper(node, prefix):
        if node.char is not None:
            return [(node.char, prefix)]
        else:
            return (prefix_helper(node.left, prefix + LEFT_BIT)
                    + prefix_helper(node.right, prefix + RIGHT_BIT))
    return {key: value for (key, value) in prefix_helper(tree, '')}
