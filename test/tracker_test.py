import unittest
from oversimbot.core import chat_tracker


class TestTracker(unittest.TestCase):

    def _test_chat_tracker_happy_path(self):
        chatTracker = chat_tracker.ChatTracker()
        # chatTracker.intent_dict.lookups["person_name"] = ['vardenis','pavardenis']
        # chatTracker.intent_dict.lookups["transprotation_option"] = ['automobiliu','dviračiu']
        chatTracker.find_response("labas")
        chatTracker.find_response("mano vardas Vardenis")
        chatTracker.find_response("taip")
        chatTracker.find_response("man patinka keliauti pėsčiomis")
        chatTracker.find_response("čia yra ežeras")
        chatTracker.find_response("galima plaukti")
        response = chatTracker.find_response("ate")
        self.assertEqual(response, ['žaidimo pabaiga. ate'])


    def _test_chat_tracker_repetitive(self):
        chatTracker = chat_tracker.ChatTracker()
        chatTracker.find_response("labas")
        chatTracker.find_response("mano vardas")
        chatTracker.find_response("mano vardas jogaila")
        chatTracker.find_response("labas")
        response = chatTracker.find_response("Ne")
        response = chatTracker.find_response("Ne")
        response = chatTracker.find_response("Ne")
        self.assertEqual(response[1], 'žaidimo pabaiga. ate')

    def test_chat_tracker_uncertain_positive(self):
        chatTracker = chat_tracker.ChatTracker()
        chatTracker.find_response("labas")
        chatTracker.find_response("labas")
        chatTracker.find_response("mano vardas jogaila")
        chatTracker.find_response("Nežinau")
        chatTracker.find_response("taip")
        chatTracker.find_response("Nežinau")
        chatTracker.find_response("man patinka skristi lėktuvu")
        chatTracker.find_response("Nežinau")
        chatTracker.find_response("čia yra Bala")
        chatTracker.find_response("Nežinau")
        chatTracker.find_response("manau čia Jūra")
        chatTracker.find_response("manau čia Ežeras")
        chatTracker.find_response("Nežinau")
        chatTracker.find_response("galima plaukti irklente")
        chatTracker.find_response("plaukti valtimi")
        chatTracker.find_response("ate")
        chatTracker.find_response("labas")
        # chatTracker.find_response("Nežinau")
        # chatTracker.find_response("manau čia Ežeras")




if __name__ == '__main__':
    unittest.main()
