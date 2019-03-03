
# Thanks to https://github.com/minven/nlp-lt/blob/master/nlp_helpers/stop_words.csv

class WordCleaner:
    def __init__(self):
        self.stop_word_list = self.load_words().split()

    def clean_stop_words(self, text_list):
        rtn_list = []
        for word in text_list:
            if(word in self.stop_word_list):
                continue
            else:
                rtn_list.append(word)
        return rtn_list

    def load_words(self):
        return GLOBAL_STOP_WORDS

GLOBAL_STOP_WORDS = """o
bet
tačiau
jei
ir
su
man
mano
tau
tavo
"""
