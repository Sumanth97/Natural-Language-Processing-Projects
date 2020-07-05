import sys
import os
import pickle
import math
import re
import fnmatch
from collections import defaultdict

directory = sys.argv[1]


class Learn:
    def __init__(self):
        pass

    def search_files(self, directory='.', extension=''):
        matches = []
        for root, dirnames, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames, extension):
                matches.append(os.path.join(root, filename))
        return matches

    def wordcount(self, data):
        count_words = defaultdict(lambda: [0, 0])
        for words, spham in data:
            for word in words:
                count_words[word][0 if spham == "spam" else 1] += 1
        return count_words

    def add_one_smoothing(self, dataset, hamlen, spamlen, buffer):
        Unique_count = self.wordcount(dataset)
        total_tokens = len(list(Unique_count.keys()))
        probdict = dict()
        smoot_ham = hamlen + total_tokens
        smooth_spam = spamlen + total_tokens

        for token, spham in Unique_count.items():
            if (spham[0] != spham[1] and sum(spham) > 1):
                spam_val = (spham[0] + 1) / smooth_spam
                ham_val = (spham[1] + 1) / smoot_ham
                if (spam_val != 0):
                    probdict[token] = [math.log(spam_val), 0]
                if (ham_val != 0):
                    probdict[token][1] = math.log(ham_val)
                buffer.append(token + ' ' + str(probdict[token][0]) + ' ' + str(probdict[token][1]) + '\n')

        return buffer

    def read_data(self, directory):
        train_ham_data = self.search_files(directory=directory, extension='*.ham.txt')
        train_spam_data = self.search_files(directory=directory, extension='*.spam.txt')

        s_list = []
        h_list = []
        for txtfile in train_ham_data:
            f = open(txtfile, "r", encoding="latin1")
            data = f.read().lower()
            h_list.append((list(set(re.findall("[a-z]+", data))), "ham"))

        for txtfile in train_spam_data:
            f = open(txtfile, "r", encoding="latin1")
            data = f.read().lower()
            s_list.append((list(set(re.findall("[a-z]+", data))), "spam"))
        dataset = s_list + h_list
        buffer = self.add_one_smoothing(dataset, len(h_list), len(s_list), [])
        f = open('nbmodel.txt', 'w', encoding='latin1')
        f.writelines(buffer)
        f.close()


if __name__ == '__main__':
    obj = Learn()
    obj.read_data(directory)