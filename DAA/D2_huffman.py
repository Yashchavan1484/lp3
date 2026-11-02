import heapq
from collections import Counter

class Node:
    def __init__(self, ch, freq, left=None, right=None):
        self.ch = ch
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


def huffman(text):
    heap = [Node(ch, freq) for ch, freq in Counter(text).items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        heapq.heappush(heap, Node(None, a.freq + b.freq, a, b))

    return heap[0]


def get_codes(node, code="", codes=None):
    if codes is None:
        codes = {}

    if node.ch is not None:
        codes[node.ch] = code or "0"
        return codes

    get_codes(node.left, code + "0", codes)
    get_codes(node.right, code + "1", codes)
    return codes


text = input("Enter text: ")

if text:
    root = huffman(text)
    codes = get_codes(root)
    encoded = "".join(codes[ch] for ch in text)

    print("Character Codes:", codes)
    print("Encoded Text:", encoded)
    print("Original Text:", text)

# Aim
# To compress text using Huffman coding by giving shorter binary codes to frequent characters and longer codes to rare ones.

# Theory
# Huffman coding is a lossless data compression technique (no information is lost).
# It uses variable-length codes: frequent characters get short codes, rare characters get long codes.
# It is a prefix code: no code is the beginning of another code, so decoding is never ambiguous.
# It is a greedy algorithm: at each step it merges the two lowest-frequency nodes.
# It builds a binary tree. Characters are at the leaves, a left edge means 0 and a right edge means 1.
# A min-heap is used to quickly get the two smallest-frequency nodes.

# Algorithm
# Count the frequency of each character.
# Make a leaf node for each character and put all nodes in a min-heap.
# While more than one node is in the heap:
# Remove the two nodes with the smallest frequency.
# Create a new parent node with frequency equal to their sum, and make the two nodes its children.
# Push the parent back into the heap.
# The last node left is the root of the Huffman tree.
# Traverse the tree from the root, adding “0” for left and “1” for right, to get each character’s code.
# Replace each character of the text with its code to get the encoded text.

# Dry run (text = “aaaabbc”)

# Frequencies: a = 4, b = 2, c = 1

# Take the two smallest, c(1) and b(2), and merge them into a node of frequency 3.
# Take the two smallest, that node (3) and a(4), and merge them into the root of frequency 7.
#         (7)
#        /   \
#     (3)     a
#     /  \
#    c    b

# Character	Code	Frequency	Bits used
# a	         1	        4	      4
# b	         01	        2	      4
# c	         00	        1	      2

# Encoded text: 1111 0101 00, which is 1111010100 (10 bits)
# Fixed-length coding needs 2 bits per character (3 symbols) × 7 = 14 bits

# Time and space complexity

# Let n = length of text and k = number of unique characters.

# Step	                                                Time
# Counting frequencies	                                O(n)
# Building heap (heapify)	                                O(k)
# Merging loop (k−1 merges, each with heap operations)	O(k log k)
# Generating codes (visit every node)	                    O(k)
# Encoding the text	                                    O(n)
# Total	                                                O(n + k log k)
