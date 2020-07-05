import sys

directory = sys.argv[1]

class evaluate:
    def __init__(self):
        pass
    def calculate_score(self, filename):
        f= open(filename,'r',encoding="latin1")
        data = f.readlines()
        tp=tn=fp=fn=0
        for line in data:
            arr = line.strip().strip('\n').split("\t")
            if(arr[0] == "spam" and arr[1].__contains__("spam")):
                tp += 1
            elif(arr[0] == "ham" and arr[1].__contains__("ham")):
                tn += 1
            elif(arr[0] == "spam" and arr[1].__contains__("ham")):
                fp += 1
            elif(arr[0] == "ham" and arr[1].__contains__("spam")):
                fn += 1


        precision_spam = tp/(tp+fp) if (tp+fp)!=0 else 0
        precision_ham = tn/(tn+fn)  if (tn+fn) != 0 else 0
        recall_spam = tp/(tp+fn) if (tp+fn) != 0 else 0
        recall_ham = tn/(tn+fp) if(tn+fp) != 0 else 0
        f1_spam = (2*precision_spam*recall_spam)/(precision_spam+recall_spam) if precision_spam+recall_spam != 0 else 0
        f1_ham = 2*float(precision_ham*recall_ham)/float(precision_ham+ recall_ham) if precision_ham+recall_ham !=0 else 0

        print("Precision spam :",precision_spam,"\n"+ "Recall spam: ",recall_spam)
        print("Precision ham :",precision_ham, "\n"+ "Recall ham: ",recall_ham)
        print("F1 score spam: ", f1_spam,"\n" + "F1 score ham: ", f1_ham)

if __name__ == '__main__':
    obj = evaluate()
    obj.calculate_score(directory)
