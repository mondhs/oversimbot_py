import re
import random
import logging

logger = logging.getLogger('ChatDomain')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class ChatDomain:

    def __init__(self):
        self.response_dict = {}
        print()

    def add_response(self, response_key, response_text):
        if(not response_key in self.response_dict):
            self.response_dict[response_key]=[]
        self.response_dict[response_key].append(response_text)

    def find_response(self, response_key, intent):
        """
            intent as dto.IntentResponse
        """
        if(not response_key in self.response_dict):
            return ""
        response_list = self.response_dict[response_key]
        response = random.choice(response_list)
        # logger.debug("[ChatDomain#find_response] {}. {}".format(response, intent))
        entities_exists_matcher = re.search('\{(.*)\}', response)
        # There is pattern
        if(entities_exists_matcher):
            entity_id = entities_exists_matcher.group(1)
            entity_value = "nesupratau"
            if(entity_id in intent.entities):
                entity_value = intent.entities[entity_id]
            logger.debug("[ChatDomain#find_response] {} replace debug {}=>{}".format(response, entity_id, entity_value))
            response = response.replace("{"+entity_id+"}",entity_value);
        return response

    def __str__(self):
        return str(self.__dict__)
