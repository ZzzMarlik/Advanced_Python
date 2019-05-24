"""
Code for compressing and decompressing using Huffman compression.
"""

from nodes import HuffmanNode, ReadNode


# ====================
# Helper functions for manipulating bytes


def get_bit(byte, bit_num):
    """ Return bit number bit_num from right in byte.

    @param int byte: a given byte
    @param int bit_num: a specific bit number within the byte
    @rtype: int

    >>> get_bit(0b00000101, 2)
    1
    >>> get_bit(0b00000101, 1)
    0
    """
    return (byte & (1 << bit_num)) >> bit_num


def byte_to_bits(byte):
    """ Return the representation of a byte as a string of bits.

    @param int byte: a given byte
    @rtype: str

    >>> byte_to_bits(14)
    '00001110'
    """
    return "".join([str(get_bit(byte, bit_num))
                    for bit_num in range(7, -1, -1)])


def bits_to_byte(bits):
    """ Return int represented by bits, padded on right.

    @param str bits: a string representation of some bits
    @rtype: int

    >>> bits_to_byte("00000101")
    5
    >>> bits_to_byte("101") == 0b10100000
    True
    """
    return sum([int(bits[pos]) << (7 - pos)
                for pos in range(len(bits))])


# ====================
# Functions for compression


def make_freq_dict(text):
    """ Return a dictionary that maps each byte in text to its frequency.

    @param bytes text: a bytes object
    @rtype: dict{int,int}

    >>> d = make_freq_dict(bytes([65, 66, 67, 66]))
    >>> d == {65: 1, 66: 2, 67: 1}
    True
    """
    dic = {}
    for cha in text:
        if cha not in dic:
            dic[cha] = 1
        else:
            dic[cha] += 1
    return dic


def huffman_tree(freq_dict):
    """ Return the root HuffmanNode of a Huffman tree corresponding
    to frequency dictionary freq_dict.

    @param dict(int,int) freq_dict: a frequency dictionary
    @rtype: HuffmanNode

    >>> freq = {2: 6, 3: 4}
    >>> t = huffman_tree(freq)
    >>> result1 = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> result2 = HuffmanNode(None, HuffmanNode(2), HuffmanNode(3))
    >>> t == result1 or t == result2
    True
    >>> freq = {2: 6}
    >>> t = huffman_tree(freq)
    >>> result1 = HuffmanNode(None, HuffmanNode(2))
    >>> result2 = HuffmanNode(None, None, HuffmanNode(2))
    >>> t == result1 or t == result2
    True
    """
    item = list(freq_dict.items())
    sort_lst = []
    # Get the items from the freq_dic
    # and put them in a new list in form of tuples(freq, symbol)
    for i in item:
        sort_lst.append((i[1], i[0]))
    sort_lst.sort()
    node_list = []
    # Get the list of tuples(freq, HuffmanNode(symbol))
    for i in sort_lst:
        node_list.append((i[0], HuffmanNode(i[1])))
    # Consider the situation that the dictionary only have one node
    if len(node_list) == 1:
        return HuffmanNode(None, node_list[0][1])
    # Get the root of the Huffmantree by adding up their freq and sort
    while len(node_list) > 1:
        m1 = node_list.pop(0)
        m2 = node_list.pop(0)
        new_node = HuffmanNode(None, m1[1], m2[1])
        node_list.append((m1[0] + m2[0], new_node))
        node_list.sort()
    return node_list[0][1]


def contains(node, value):
    """ Return whether the node contains the value.

    @param HuffmanNode node: a Huffman tree rooted at node 'node'
    @param object value: the value to search
    @rtype: bool

    >>> tree = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> contains(tree, 2)
    True
    """
    if node is None:
        return False
    else:
        return (node.symbol == value or
                contains(node.left, value) or
                contains(node.right, value))


def get_path(t, n):
    """ Return the prefix code for n given Huffmantree.

    @param HuffmanNode t: a Huffman tree
    @param object n: the value we want to find prefix code for
    @rtype: str

    >>> tree = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> print(get_path(tree, 2))
    1
    """
    if t is None:
        return ' '
    elif t.symbol == n:
        return ''
    else:
        if contains(t.left, n):
            return '0' + get_path(t.left, n)
        else:
            return '1' + get_path(t.right, n)


def gather_lists(list_):
    """
    Concatenate all the sublists of L and return the result.

    @param list[list[object]] list_: list of lists to concatenate
    @rtype: list[object]

    >>> gather_lists([[1, 2], [3, 4, 5]])
    [1, 2, 3, 4, 5]
    >>> gather_lists([[6, 7], [8], [9, 10, 11]])
    [6, 7, 8, 9, 10, 11]
    """
    new_list = []
    for l in list_:
        new_list += l
    return new_list


def get_leaf(t):
    """ Return the list of leaves of a tree t.

    @param HuffmanNode t: a Huffman tree node
    @rtype: list

    """
    if t is None:
        return []
    elif t.is_leaf():
        return [t.symbol]
    else:
        return gather_lists(([get_leaf(t.right)] if t.right else [])) \
               + gather_lists(([get_leaf(t.left)] if t.left else []))


def get_codes(tree):
    """ Return a dict mapping symbols from tree rooted at HuffmanNode to codes.

    @param HuffmanNode tree: a Huffman tree rooted at node 'tree'
    @rtype: dict(int,str)

    >>> tree = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> d = get_codes(tree)
    >>> d == {3: "0", 2: "1"}
    True
    """
    all_leaf = get_leaf(tree)
    dic = {}
    for a in all_leaf:
        dic[a] = get_path(tree, a)
    return dic


def number_internal(tree, n):
    """Number the internal nodes of tree t starting with n,
    and return the total number of internals

    @param HuffmanNode tree: Given HuffmanTree
    @param int n: start number
    @rtype: int

    >>> left = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> right = HuffmanNode(None, HuffmanNode(9), HuffmanNode(10))
    >>> tree = HuffmanNode(None, left, right)
    >>> number_internal(tree, 0)
    3
    >>> tree.left.number
    0
    >>> tree.right.number
    1
    >>> tree.number
    2
    """
    # Not leaf, recursion start
    if tree and not tree.is_leaf():
        n = number_internal(tree.left, n)
        n = number_internal(tree.right, n)
        tree.number = n
        return n + 1
    # leaf found
    else:
        return n


def number_nodes(tree):
    """ Number internal nodes in tree according to postorder traversal;
    start numbering at 0.

    @param HuffmanNode tree:  a Huffman tree rooted at node 'tree'
    @rtype: NoneType

    >>> left = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> right = HuffmanNode(None, HuffmanNode(9), HuffmanNode(10))
    >>> tree = HuffmanNode(None, left, right)
    >>> number_nodes(tree)
    >>> tree.left.number
    0
    >>> tree.right.number
    1
    >>> tree.number
    2
    """
    number_internal(tree, 0)


def avg_length(tree, freq_dict):
    """ Return the number of bits per symbol required to compress text
    made of the symbols and frequencies in freq_dict, using the Huffman tree.

    @param HuffmanNode tree: a Huffman tree rooted at node 'tree'
    @param dict(int,int) freq_dict: frequency dictionary
    @rtype: float

    >>> freq = {3: 2, 2: 7, 9: 1}
    >>> left = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> right = HuffmanNode(9)
    >>> tree = HuffmanNode(None, left, right)
    >>> avg_length(tree, freq)
    1.9
    """
    # Get the dictionary that contains {symbol: prefix code}
    cod_dic = get_codes(tree)
    lst = []
    i = 0
    # Calculate the avg_length of each nodes/symbols by
    # suming all prefix codes' length * freq and divide by total number of nodes
    for key in cod_dic:
        lst.append(len(cod_dic[key]) * freq_dict[key])
        i += freq_dict[key]
    return sum(lst)/i


def generate_compressed(text, codes):
    """ Return compressed form of text, using mapping in codes for each symbol.

    @param bytes text: a bytes object
    @param dict(int,str) codes: mappings from symbols to codes
    @rtype: bytes

    >>> d = {0: "0", 1: "10", 2: "11"}
    >>> text = bytes([1, 2, 1, 0])
    >>> result = generate_compressed(text, d)
    >>> [byte_to_bits(byte) for byte in result]
    ['10111000']
    >>> text = bytes([1, 2, 1, 0, 2])
    >>> result = generate_compressed(text, d)
    >>> [byte_to_bits(byte) for byte in result]
    ['10111001', '10000000']
    """
    l = []
    r = ''
    # Translate text into prefix codes
    for i in text:
        r += codes[i]
    # Calculate how many 0s we need to fill in
    reman = len(r) % 8
    r += (8 - reman) * '0'
    # Calculate how many 8s in order to slicing
    num = len(r) // 8
    for i in range(num):
        # translate each 8 bits into bytes and add them to the result
        l.append(bits_to_byte(r[8 * i:8 * i + 8]))
    return bytes(l)


def tree_to_bytes(tree):
    """ Return a bytes representation of the tree rooted at tree.

    @param HuffmanNode tree: a Huffman tree rooted at node 'tree'
    @rtype: bytes

    The representation should be based on the postorder traversal of tree
    internal nodes, starting from 0.
    Precondition: tree has its nodes numbered.

    >>> tree = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))
    [0, 3, 0, 2]
    >>> left = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> right = HuffmanNode(5)
    >>> tree = HuffmanNode(None, left, right)
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))
    [0, 3, 0, 2, 1, 0, 0, 5]
    """
    lst = []
    if tree:
        # Posteroder traversal of the tree
        left = tree_to_bytes(tree.left) if tree.left else bytes([])
        right = tree_to_bytes(tree.right) if tree.right else bytes([])
        # Check left
        if tree.left:
            if tree.left.is_leaf():
                # Left-Subtree doesn't exist, append 0 and its symbol
                lst.append(0)
                lst.append(tree.left.symbol)
            else:
                # Left_Subtree exist append, 1 and its number
                lst.append(1)
                lst.append(tree.left.number)
        # Check right
        if tree.right:
            if tree.right.is_leaf():
                # Right-Subtree doesn't exist, append 0 and its symbol
                lst.append(0)
                lst.append(tree.right.symbol)
            else:
                # Right-Subtree exist, append 0 and its symbol
                lst.append(1)
                lst.append(tree.right.number)
        return left + right + bytes(lst)


def num_nodes_to_bytes(tree):
    """ Return number of nodes required to represent tree (the root of a
    numbered Huffman tree).

    @param HuffmanNode tree: a Huffman tree rooted at node 'tree'
    @rtype: bytes
    """
    return bytes([tree.number + 1])


def size_to_bytes(size):
    """ Return the size as a bytes object.

    @param int size: a 32-bit integer that we want to convert to bytes
    @rtype: bytes

    >>> list(size_to_bytes(300))
    [44, 1, 0, 0]
    """
    # little-endian representation of 32-bit (4-byte)
    # int size
    return size.to_bytes(4, "little")


def compress(in_file, out_file):
    """ Compress contents of in_file and store results in out_file.

    @param str in_file: input file whose contents we want to compress
    @param str out_file: output file, where we store our compressed result
    @rtype: NoneType
    """
    with open(in_file, "rb") as f1:
        text = f1.read()
    freq = make_freq_dict(text)
    tree = huffman_tree(freq)
    codes = get_codes(tree)
    number_nodes(tree)
    print("Bits per symbol:", avg_length(tree, freq))
    result = (num_nodes_to_bytes(tree) + tree_to_bytes(tree) +
              size_to_bytes(len(text)))
    result += generate_compressed(text, codes)
    with open(out_file, "wb") as f2:
        f2.write(result)


# ====================
# Functions for decompression


def generate_tree_general(node_lst, root_index):
    """ Return the root of the Huffman tree corresponding
    to node_lst[root_index].

    The function assumes nothing about the order of the nodes in the list.

    @param list[ReadNode] node_lst: a list of ReadNode objects
    @param int root_index: index in the node list
    @rtype: HuffmanNode

    >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), \
    ReadNode(1, 1, 1, 0)]
    >>> generate_tree_general(lst, 2)
    HuffmanNode(None, HuffmanNode(None, HuffmanNode(10, None, None), \
HuffmanNode(12, None, None)), \
HuffmanNode(None, HuffmanNode(5, None, None), HuffmanNode(7, None, None)))
    """
    # Create a new HuffManTree
    node = HuffmanNode()
    root = node_lst[root_index]
    # Left-Subtree doesn't exist, left leaf will be the symbol of l_data
    if root.l_type == 0:
        node.left = HuffmanNode(root.l_data)
    # Left-Subtree exist, recursion start
    elif root.l_type == 1:
        node.left = generate_tree_general(node_lst, root.l_data)
    # Right-Subtree doesn't exist, right leaf will be the symbol of r_data
    if root.r_type == 0:
        node.right = HuffmanNode(root.r_data)
    # Right-Subtree exist, recursion start
    elif root.r_type == 1:
        node.right = generate_tree_general(node_lst, root.r_data)
    return node


def count_internal(n):
    """Return number of internal nodes of the given HuffmanNode n.

    @param HuffmanNode n: Given HuffmanNode n
    @rtype: int

    >>> left = HuffmanNode(None, HuffmanNode(99), HuffmanNode(100))
    >>> right = HuffmanNode(None, HuffmanNode(101), \
    HuffmanNode(None, HuffmanNode(97), HuffmanNode(98)))
    >>> tree = HuffmanNode(None, left, right)
    >>> count_internal(tree)
    4
    """
    acc = 0
    if n is None:
        return 0
    if not n.is_leaf():
        acc += 1
        acc += count_internal(n.left)
        acc += count_internal(n.right)
    return acc


def generate_tree_postorder(node_lst, root_index):
    """ Return the root of the Huffman tree corresponding
    to node_lst[root_index].

    The function assumes that the list represents a tree in postorder.

    @param list[ReadNode] node_lst: a list of ReadNode objects
    @param int root_index: index in the node list
    @rtype: HuffmanNode

    >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), \
    ReadNode(1, 0, 1, 0)]
    >>> generate_tree_postorder(lst, 2)
    HuffmanNode(None, HuffmanNode(None, HuffmanNode(5, None, None), \
HuffmanNode(7, None, None)), \
HuffmanNode(None, HuffmanNode(10, None, None), HuffmanNode(12, None, None)))
    """
    node = HuffmanNode()
    root = node_lst[root_index]
    # Right-Subtree doesn't exist, right leaf will be the symbol of r_data
    if root.r_type == 0:
        node.right = HuffmanNode(root.r_data)
    # Right-Subtree exist, new root will be the index of the orignal root - 1 by
    # the proporty of postorder
    elif root.r_type == 1:
        node.right = generate_tree_postorder(node_lst, root_index - 1)
    # Left-Subtree doesn't exist, left leaf will be the symbol of l_data
    if root.l_type == 0:
        node.left = HuffmanNode(root.l_data)
    # Left-Subtree exist, new root will be the index of the orignal root
    # minus the number of internal nodes of the right subtree
    elif root.l_type == 1:
        node.left = generate_tree_postorder(
            node_lst, root_index - count_internal(node.right) - 1)
    return node


def generate_uncompressed(tree, text, size):
    """ Use Huffman tree to decompress size bytes from text.

    @param HuffmanNode tree: a HuffmanNode tree rooted at 'tree'
    @param bytes text: text to decompress
    @param int size: how many bytes to decompress from text.
    @rtype: bytes

    """
    s = ''
    l = []
    # Translate byte to bits from given text
    for i in text:
        s += byte_to_bits(i)
    # Mark the beginning of the tree
    temp = tree
    for num in s:
        if temp:
            if num == '0':
                temp = temp.left
            if num == '1':
                temp = temp.right
            # Reach the leaf and add the symbol
            if temp and temp.is_leaf():
                l.append(temp.symbol)
                # Go back to the beginning of the tree
                temp = tree
                # Reach the max size
                if len(l) == size:
                    return bytes(l)
    return bytes(l)


def bytes_to_nodes(buf):
    """ Return a list of ReadNodes corresponding to the bytes in buf.

    @param bytes buf: a bytes object
    @rtype: list[ReadNode]

    >>> bytes_to_nodes(bytes([0, 1, 0, 2]))
    [ReadNode(0, 1, 0, 2)]
    """
    lst = []
    for i in range(0, len(buf), 4):
        l_type = buf[i]
        l_data = buf[i+1]
        r_type = buf[i+2]
        r_data = buf[i+3]
        lst.append(ReadNode(l_type, l_data, r_type, r_data))
    return lst


def bytes_to_size(buf):
    """ Return the size corresponding to the
    given 4-byte little-endian representation.

    @param bytes buf: a bytes object
    @rtype: int

    >>> bytes_to_size(bytes([44, 1, 0, 0]))
    300
    """
    return int.from_bytes(buf, "little")


def uncompress(in_file, out_file):
    """ Uncompress contents of in_file and store results in out_file.

    @param str in_file: input file to uncompress
    @param str out_file: output file that will hold the uncompressed results
    @rtype: NoneType
    """
    with open(in_file, "rb") as f:
        num_nodes = f.read(1)[0]
        buf = f.read(num_nodes * 4)
        node_lst = bytes_to_nodes(buf)
        # use generate_tree_general or generate_tree_postorder here
        tree = generate_tree_general(node_lst, num_nodes - 1)
        size = bytes_to_size(f.read(4))
        with open(out_file, "wb") as g:
            text = f.read()
            g.write(generate_uncompressed(tree, text, size))


# ====================
# Other functions

def improve_tree(tree, freq_dict):
    """ Improve the tree as much as possible, without changing its shape,
    by swapping nodes. The improvements are with respect to freq_dict.

    @param HuffmanNode tree: Huffman tree rooted at 'tree'
    @param dict(int,int) freq_dict: frequency dictionary
    @rtype: NoneType

    >>> left = HuffmanNode(None, HuffmanNode(99), HuffmanNode(100))
    >>> right = HuffmanNode(None, HuffmanNode(101), \
    HuffmanNode(None, HuffmanNode(97), HuffmanNode(98)))
    >>> tree = HuffmanNode(None, left, right)
    >>> freq = {97: 26, 98: 23, 99: 20, 100: 16, 101: 15}
    >>> improve_tree(tree, freq)
    >>> avg_length(tree, freq)
    2.31
    """
    freq_lst = []
    for key, value in freq_dict.items():
        freq_lst.append((value, key))
    freq_lst.sort()
    # Level-order visit code from class notes
    lst_tree = [tree]
    while not len(lst_tree) == 0:
        next_tree = lst_tree.pop(0)
        for c in [next_tree.left, next_tree.right]:
            if c is not None:
                lst_tree.append(c)
        # Change the orignal symbol into a better one
        if next_tree.is_leaf():
            symbol = freq_lst.pop()
            next_tree.symbol = symbol[1]

if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config="huffman_pyta.txt")
    import doctest
    doctest.testmod()

    import time

    mode = input("Press c to compress or u to uncompress: ")
    if mode == "c":
        fname = input("File to compress: ")
        start = time.time()
        compress(fname, fname + ".huf")
        print("compressed {} in {} seconds."
              .format(fname, time.time() - start))
    elif mode == "u":
        fname = input("File to uncompress: ")
        start = time.time()
        uncompress(fname, fname + ".orig")
        print("uncompressed {} in {} seconds."
              .format(fname, time.time() - start))
