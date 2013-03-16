from bitstring import BitArray

from huffman import (Node, _bits_to_chars, _chars_to_bits, _get_freq,
                     _make_prefix, build_tree, decode, encode)


TEST_FILE = 'tmp.txt'


def test_encode():
    string = "abbb"
    encode(TEST_FILE, string)
    with open(TEST_FILE, 'rb') as bit_file:
        bits = BitArray(bit_file)
        assert bits.bin == '01110000'


def test_encode_returns_correct_tree():
    string = "abbb"
    smallest = Node(0.25, 'a', None, None)
    sec_smallest = Node(0.75, 'b', None, None)
    correct_tree = Node(1, None, smallest, sec_smallest)
    tree = encode(TEST_FILE, string)
    assert isinstance(tree, Node)
    assert correct_tree == tree


def test_decode_reverses_encode_simple():
    string = 'abbb'
    tree = encode(TEST_FILE, string)
    decoded = decode(TEST_FILE, tree)
    assert decoded.startswith(string)


def test_decode_reverses_encode_special():
    string = '! %'
    tree = encode(TEST_FILE, string)
    decoded = decode(TEST_FILE, tree)
    assert decoded.startswith(string)


def test_decode_reverses_encode_long():
    string = """In computer science and information theory, Huffman coding is
    an entropy encoding algorithm used for lossless data compression. The term
    refers to the use of a variable-length code table for encoding a source
    symbol (such as a character in a file) where the variable-length code table
    has been derived in a particular way based on the estimated probability of
    occurrence for each possible value of the source symbol. It was developed
    by David A. Huffman while he was a Ph.D. student at MIT, and published in
    the 1952 paper "A Method for the Construction of Minimum-Redundancy Codes.
    """
    tree = encode(TEST_FILE, string)
    decoded = decode(TEST_FILE, tree)
    assert decoded.startswith(string)


def test_decode_reverses_encode_unicode():
    string = 'Kærlighed og Øl!'
    tree = encode(TEST_FILE, string)
    decoded = decode(TEST_FILE, tree)
    assert decoded.startswith(string)


def test_build_tree_empty():
    string = ""
    tree = build_tree(string)
    assert tree is None


def test_build_tree():
    string = "abbb"
    tree = build_tree(string)
    assert isinstance(tree, Node)
    assert tree[1] is None
    assert tree[2][1] == 'a'
    assert tree[3][1] == 'b'


def test__bits_to_chars():
    smallest = Node(0.25, 'a', None, None)
    sec_smallest = Node(0.75, 'b', None, None)
    tree = Node(1, None, smallest, sec_smallest)
    assert _bits_to_chars(tree, '0') == 'a'
    assert _bits_to_chars(tree, '1') == 'b'


def test__bits_to_chars_multichars():
    smallest = Node(0.25, 'a', None, None)
    sec_smallest = Node(0.75, 'b', None, None)
    tree = Node(1, None, smallest, sec_smallest)
    assert _bits_to_chars(tree, '00') == 'aa'


def test__chars_to_bits():
    string = "ab"
    prefixes = {'a': '1111', 'b': '0000'}
    assert _chars_to_bits(string, prefixes) == '11110000'
    string = "abba"
    assert _chars_to_bits(string, prefixes) == '1111000000001111'
    string = "bab"
    prefixes = {'a': '11', 'b': '000'}
    assert _chars_to_bits(string, prefixes) == '00011000'


def test__chars_to_bits_always_in_bytes():
    """
    A returned bitstring % 8 should always be divisible by 8.

    If need be, the right side will be padded with zeros"""
    string = "ab"
    prefixes = {'a': '0', 'b': '1'}
    assert _chars_to_bits(string, prefixes) == '01000000'


def test_freq():
    assert _get_freq("") == {}
    assert _get_freq("a") == {"a": 1}
    assert _get_freq("abba") == {"a": 0.5, "b": 0.5}
    assert _get_freq("aab") == {"a": 2 / 3.0, "b": 1 / 3.0}


def test_prefix_helper():
    smallest = Node(1, 'a', None, None)
    sec_smallest = Node(2, 'b', None, None)
    tree = Node(3, None, smallest, sec_smallest)
    assert _make_prefix(tree) == {'a': '0', 'b': '1'}


def test_prefix_helper_inner_node():
    smallest = Node(1, 'a', None, None)
    sec_smallest = Node(2, 'b', None, None)
    third_smallest = Node(4, 'c', None, None)
    inner = Node(3, None, smallest, sec_smallest)
    tree = Node(7, None, inner, third_smallest)
    assert _make_prefix(tree) == {'a': '00', 'b': '01', 'c': '1'}
