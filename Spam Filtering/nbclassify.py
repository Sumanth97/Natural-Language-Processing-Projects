import os
import sys
import pickle
import math
from glob import glob
import fnmatch

class Classification:
    def __init__(self):
        pass

    # def search_files(self,directory='.', extension=''):
    #
    #     matches = []
    #     for root, dirnames, filenames in os.walk(directory):
    #         for filename in fnmatch.filter(filenames, extension):
    #             matches.append(os.path.join(root, filename))
    #     return matches

    def classify(self,prob_spam, prob_ham, spam_dict, ham_dict, path):#file):
        res = dict()
        buffer = []

        for file in glob(path + '/**/*.txt', recursive=True):
            prob_token_spam = 0.0
            prob_token_ham = 0.0
            txtname = open(file, 'r', encoding='latin1')
            tokens = txtname.read().strip('\n').lower().split()
            txtname.close()
            for token in tokens:
                if spam_dict.get(token, 0.0) != 0.0:
                    prob_token_spam += spam_dict[token]
                if ham_dict.get(token, 0.0) != 0.0:
                    prob_token_ham += ham_dict[token]

            spam_count = prob_spam + prob_token_spam
            ham_count = prob_ham + prob_token_ham

            if spam_count >= ham_count:
                res[file] = 'spam'
                buffer.append('spam' + '\t' + file + '\n')
            else:
                res[file] = 'ham'
                buffer.append('ham' + '\t' + file + '\n')

        f = open('nboutput.txt', 'w', encoding='latin1')
        f.writelines(buffer)
        f.close()

    def read_data(self,directory):

        dataset = open('nbmodel.txt', 'r', encoding='latin1')
        prob_spam = float(dataset.readline().strip('\n').split()[1])
        prob_ham = float(dataset.readline().strip('\n').split()[1])

        prob_ham_dict = {}
        prob_spam_dict = {}
        for line in dataset.readlines():
            if line == '\n':
                break
            token, spam, ham = line.split(' ')
            prob_spam_dict[token] = float(spam)
            prob_ham_dict[token] = float(ham)

        self.classify(prob_spam, prob_ham, prob_spam_dict, prob_ham_dict, directory)


if __name__ == '__main__':
    obj = Classification()
    directory = sys.argv[1]
    #obj.read_data()
    obj.read_data(directory)