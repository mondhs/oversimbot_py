import logging

logger = logging.getLogger('StoryRepository')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class StoryRepository:

    def __init__(self):
        self.name = ""
        self.intent_phrases = {}
        self.intent_childs = {}

    def add_intent(self, intent_key, parent_key):
        child_key_list = intent_key.split(" OR ")
        parent_key_list = parent_key.split(" OR ")
        for subparent in parent_key_list:
            if(not subparent in self.intent_childs):
                self.intent_childs[subparent]=[]
            for subchild in child_key_list:
                self.intent_phrases[subchild]=[]
                if(not subchild in self.intent_childs[subparent]):
                    self.intent_childs[subparent].append(subchild)

    def add_action(self, intent_key, action_key):
        intent_key_list = intent_key.split(" OR ")
        for subintent in intent_key_list:
            if(not action_key in self.intent_phrases[subintent]):
                self.intent_phrases[subintent].append(action_key)
        # print(self.intent_phrases)


    def find_action(self, intent):
        """
            intent as dto.IntentResponse
        """
        intent_key = intent.key
        return self.intent_phrases[intent_key]

    def find_next_intents(self, intent_key):
        if(intent_key in self.intent_childs):
            next_intents = self.intent_childs[intent_key]
            return next_intents
        return []

    def __str__(self):
        return str(self.__dict__)
