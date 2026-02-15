import math
import re

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

class NaiveBayes:
    def __init__(self):
        self.pos_word_counts = Counter()
        self.neg_word_counts = Counter()
        self.pos_total = 0
        self.neg_total = 0
        self.vocab = set()

    def train(self, pos_file, neg_file):
        with open(pos_file, 'r') as f:
            for line in f:
                tokens = tokenize(line)
                self.pos_word_counts.update(tokens)
                self.vocab.update(tokens)
                self.pos_total += 1
        
        with open(neg_file, 'r') as f:
            for line in f:
                tokens = tokenize(line)
                self.neg_word_counts.update(tokens)
                self.vocab.update(tokens)
                self.neg_total += 1

    def predict(self, sentence):
        tokens = tokenize(sentence)
        v_size = len(self.vocab)
        
        # Log priors
        pos_score = math.log(self.pos_total / (self.pos_total + self.neg_total))
        neg_score = math.log(self.neg_total / (self.pos_total + self.neg_total))
        
        pos_words_sum = sum(self.pos_word_counts.values())
        neg_words_sum = sum(self.neg_word_counts.values())

        for token in tokens:
            # Laplace smoothing:(count+1)/(totalwords+vocabsize)
            pos_score += math.log((self.pos_word_counts[token] + 1) / (pos_words_sum + v_size))
            neg_score += math.log((self.neg_word_counts[token] + 1) / (neg_words_sum + v_size))
            
        return "POSITIVE" if pos_score > neg_score else "NEGATIVE"

from collections import Counter
if __name__ == "__main__":
    nb = NaiveBayes()
    nb.train('pos.txt', 'neg.txt') # Ensure these files are in the directory only for safety
    
    print("Naive Bayes Classifier Trained.")
    while True:
        user_sentence = input("\nEnter a sentence to classify (or 'exit'): ")
        if user_sentence.lower() == 'exit': break
        print(f"Sentiment: {nb.predict(user_sentence)}")
