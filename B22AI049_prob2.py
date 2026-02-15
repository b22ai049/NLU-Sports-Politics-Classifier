import sys
import re
from collections import Counter, defaultdict

def get_stats(vocab):
    pairs = defaultdict(int)
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pairs[symbols[i], symbols[i+1]] += freq
    return pairs

def merge_vocab(pair, v_in):
    v_out = {}
    bigram = re.escape(' '.join(pair))
    # Ensures we merge only exact whitespace-separated pairs
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
    replacement = ''.join(pair)
    for word in v_in:
        w_out = p.sub(replacement, word)
        v_out[w_out] = v_in[word]
    return v_out

def main():
    if len(sys.argv) != 3:
        print("Usage: python B22AI049_prob2.py k corpus.txt")
        sys.exit(1)

    k = int(sys.argv[1])
    corpus_path = sys.argv[2]

    with open(corpus_path, 'r', encoding='utf-8') as f:
        words = f.read().split()

    # Initial vocab: characters separated by spaces with end-of-word marker
    vocab = Counter([' '.join(list(word)) + ' </w>' for word in words])

    for i in range(k):
        pairs = get_stats(vocab)
        if not pairs:
            break
        best = max(pairs, key=pairs.get)
        vocab = merge_vocab(best, vocab)
        print(f"Merge {i+1}: {best}")

    final_tokens = set()
    for word in vocab:
        for token in word.split():
            final_tokens.add(token)

    print("\nFinal Vocabulary:")
    print(sorted(list(final_tokens)))

if __name__ == "__main__":
    main()