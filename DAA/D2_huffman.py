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