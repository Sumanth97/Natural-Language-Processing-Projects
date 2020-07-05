import sys
import pycrfsuite
import hw2_corpus_tool as hwutil


class Tagger():
    def __init__(self):
        self.inter = {'what','when','how','where'}

    def word2features(self,words,turn):
        word = words[turn]
        dialogue_features = []

        if turn == 0:
            dialogue_features.append("Start")
        elif(word.speaker != words[turn - 1].speaker):
            dialogue_features.append("Person_changed")
        if(word.pos is not None):
            dialogue_features.extend(["TokenUtterance_" + postag_token.token for postag_token in word.pos])
            n = len(word.pos)
            for i in range(0,n):
                if(i+1<n):
                    dialogue_features.extend(["BigramToken_" + word.pos[i].token + " "+ word.pos[i+1].token])
                else:
                    dialogue_features.extend(["BigramToken_" + word.pos[i].token])
            dialogue_features.extend(["BiGroupToken_" + word.pos[i].token for i in range(0,len(word.pos),2)])
            dialogue_features.extend(["TriGroupToken_" + word.pos[i].token for i in range(0, len(word.pos), 3)])
            dialogue_features.extend(["POSTag_" + postag.pos for postag in word.pos])
        else:
            dialogue_features.append("None")

        if (word.text.istitle()):
            dialogue_features.append("Title")
        text = word.text.split()
        word_text = word.text.lower()
        if (text[0].lower() in self.inter or '?' in text[-1].lower()):
            dialogue_features.append("Interrogative")
        if (text[0].lower() == "yeah"):
            dialogue_features.append("Answer")
        if ("yes" in word_text or "agree" in word_text):
            dialogue_features.append("Agreement")
        if ("think" in word_text or "believe" in word_text):
            dialogue_features.append("Opinion")
        if ("Uh-huh" in word_text or "oh" in word_text):
            dialogue_features.append("Acknowledge")
        if ("um" in word_text):
            dialogue_features.append("Decisive")
        if ('--' in word_text or '-/' in word_text):
            dialogue_features.append("Interruptive")
        if ("'" in word_text):
            dialogue_features.append("Abbrevative")

        num = False
        for x in text:
            if(x.isnumeric() == True):
                num = True
                break
        if(num):
            dialogue_features.append("Numbers")
        else:
            dialogue_features.append("No Numbers")
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

        trainer.train('advanced_model')

    def testModel(self,testdata, result):
        tagger = pycrfsuite.Tagger()
        tagger.open('advanced_model')
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
