import unittest
from oversimbot.core import intent_repository

import logging

logger = logging.getLogger('oversimbot')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class IntentRepoTest(unittest.TestCase):

    def setUp(self):
        # self.lemmatizer = word_lemmatizer.WordLemmatizer()
        # self.cleaner = word_cleaner.WordCleaner()
        # self.intentions_vocabluary = self.build_intentions_vocabluary()
        pass



    def test_find_intents_with_pattern(self):
        intent_repo = intent_repository.IntentRepository()
        intent_repo.intentions_vocabluary = [
    "kel",
    "ag",
    "galim",
    "lab",
    "taip",
    "es",
    "lab",
    "neagl",
    "man",
    "kaip",
    "gal",
    "a\u0161",
    "skris",
    "ne\u017ein",
    "nelab",
    "plauk",
    "lab",
    "atsak",
    "j",
    "vard",
    "niekad",
    "dien",
    "\u010di",
    "laiv",
    "yr",
    "atrod",
    "perplauk",
    "tikr",
    "patink",
    "n",
    "va\u017e",
    "nepagalvoj",
    "m\u0117gst"
  ]
        intent_repo.lookups["person_name"] = ['vardenis','pavardenis']
        intent_repo.lookups["transprotation_option"] = ['automobiliu','dviračiu']

        intent_repo.phrase_compressed["mano vardas [vardenis](person_name)"] = [25]
        intent_repo.phrase_to_intent["mano vardas [vardenis](person_name)"]="my_name_is"
        intent_repo.phrase_compressed["a\u0161 m\u0117gstu va\u017eiuoti [automobiliu](transprotation_option)"]=[11,32,30]
        intent_repo.phrase_to_intent["a\u0161 m\u0117gstu va\u017eiuoti [automobiliu](transprotation_option)"]="prefered_travel_option"


        intent_repo.add_intent("test")
        self.add_phrase(intent_repo, "test", "labas")
        intent_repo.add_intent("prefered_travel_option")
        self.add_phrase(intent_repo,"prefered_travel_option", "aš mėgstu važiuoti [automobiliu](transprotation_option)")
        self.add_phrase(intent_repo,"prefered_travel_option", "patinka keliauti [dviračiu](transprotation_option)")
        intent_repo.add_intent("my_name_is")
        self.add_phrase(intent_repo, "my_name_is", "mano vardas [Mindas](person_name)")
        # print(intent_repo)
        intent1 = intent_repo.find_intent("mano vardas Pavardenis")
        print(intent1)
        intent2 = intent_repo.find_intent("aš mėgstu važiuoti automobiliu")

        # print(intent)
        self.assertEqual(intent1.key, 'my_name_is')
        self.assertEqual(intent1.entities["person_name"], 'pavardenis')
        self.assertEqual(intent2.key, 'prefered_travel_option')
        self.assertEqual(intent2.entities["transprotation_option"], 'automobiliu')


    def add_phrase(self, intent_repo, intent, phrase):
        # line = re.sub(r"(\[.*\])", "", line).strip()
        # line = re.sub(r"(\(.*\))", "", line).strip()
        # stopWords.clean_stop_words("mano vardas Vardenis".split(" "))
        intent_repo.add_phrase(intent, phrase)
