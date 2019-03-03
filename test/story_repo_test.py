import unittest
from oversimbot.core import story_repository

import logging

logger = logging.getLogger('oversimbot')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class IntentRepoTest(unittest.TestCase):

    def test_story_repo(self):
        pass
        # story_repo = story_repository.StoryRepository()
        #
        # story_repo.
        #
        # self.assertEqual(intent2.entities["transprotation_option"], 'automobiliu')
