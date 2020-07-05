import sys
import pycrfsuite
import hw2_corpus_tool as hwutil


class Tagger():
    def __init__(self):
        pass

    def word2features(self,words,turn):
        word = words[turn]
        dialogue_features = []

        if turn == 0:
            dialogue_features.append("Start")
        elif word.speaker != words[turn - 1].speaker:
            dialogue_features.append("Person_changed")
        if word.pos is not None:
            dialogue_features.extend(["TokenUtterance_" + postag_token.token for postag_token in word.pos])
            dialogue_features.extend(["POSTag_" + postag.pos for postag in word.pos])
        else:
            dialogue_features.append("None")

        return dialogue_features

    def trainModel(self,data):
        trainer = pycrfsuite.Trainer(verbose=False)
        for dialogues in hwutil.get_data(data):
            x_train = [self.word2features(dialogues, i) for i in range(len(dialogues))]
            y_train = [dialogue.act_tag for dialogue in dialogues]
            trainer.append(x_train, y_train)

        trainer.set_params({
            'c1': 1.0,  # coefficient for l1 penalty
            "c2": 1e-3,  # coefficient for L2 penalty
            'max_iterations': 50,  # stop earlier

            # include transitions that are possible, but not observed
            'feature.possible_transitions': True
        })

        trainer.train('baseline_model')

    def testModel(self,testdata, result):
        tagger = pycrfsuite.Tagger()
        tagger.open('baseline_model')
        with open(result, 'w') as opt_file:
            tp = 0
            files = 0
            for dialogue in hwutil.get_data(testdata):
                res = []
                res.extend(tagger.tag([self.word2features(dialogue, i) for i in range(len(dialogue))]))
                for x in res:
                    opt_file.write(x)
                    opt_file.write('\n')
                opt_file.write('\n')
                y_true = [utterance.act_tag for utterance in dialogue]
                files += len(res)
                for y_pred, y in zip(res, y_true):
                    if y_pred == y:
                        tp += 1
            accuracy = tp / files
            print("accuracy = ", accuracy)

if __name__ == '__main__':
    path = sys.argv[1]
    obj = Tagger()
    obj.trainModel(path)
    obj.testModel(sys.argv[2],sys.argv[3])
