import unittest
from oversimbot.nlp import word_cleaner
from oversimbot.nlp import word_lemmatizer


class TestTracker(unittest.TestCase):

    def test_word_clenater(self):
        stopWords = word_cleaner.WordCleaner()
        response0 = stopWords.clean_stop_words("mano vardas Vardenis".split(" "))
        self.assertEqual(" ".join(response0), 'vardas Vardenis')

    def test_lemmantinzer(self):
        lemmatizer = word_lemmatizer.WordLemmatizer()
        response0 = lemmatizer.find_word_core("vardas")
        self.assertEqual(response0, 'vard')



if __name__ == '__main__':
    unittest.main()
