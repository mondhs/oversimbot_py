import unittest
from oversimbot_train.parser import story_parser
from oversimbot_train.parser import intent_parser
from oversimbot_train.parser import domain_parser

from oversimbot.core import intent_repository
from oversimbot.dto import intent_response


import re

import logging

logger = logging.getLogger('oversimbot')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class TestParser(unittest.TestCase):

    def setUp(self):
        # self.lemmatizer = word_lemmatizer.WordLemmatizer()
        # self.cleaner = word_cleaner.WordCleaner()
        # self.intentions_vocabluary = self.build_intentions_vocabluary()
        pass



    def test_story_parer(self):
        storyParser = story_parser.StoryParser()
        story = storyParser.parse("oversimbot_train/data/stories_nao.md")
        # print(story.name)
        self.assertEqual(story.name, 'story_0phase_unhappy_path')

    def test_intent_parer(self):
        intentParser = intent_parser.IntentParser()
        intent_repo = intentParser.parse("oversimbot_train/data/nlu_data.md")
        # print(intent_repo)
        intent = intent_repo.find_intent("labas")
        # print(intent)
        self.assertEqual(intent.key, 'greet')


    def test_domain_parser(self):
        chatDomainParser = domain_parser.ChatDomainParser()
        chat_domain = chatDomainParser.parse("oversimbot_train/data/domain.yml")
        intent = intent_response.IntentResponse()
        intent.key = "ANY_CODE"
        # print(chat_domain)
        response = chat_domain.find_response("utter_bye", intent)
        # print(response)
        self.assertEqual(response, 'žaidimo pabaiga. ate')


    # def test_chat_trainer(self):
    #     trainer = chat_trainer.ChatTrainer()
    #     trainer.build_intentions_vocabluary()




if __name__ == '__main__':
    unittest.main()
