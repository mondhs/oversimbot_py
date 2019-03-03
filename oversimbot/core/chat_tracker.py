
from oversimbot.core import story_repository
from oversimbot.core import intent_repository
from oversimbot.core import chat_domain
from oversimbot.dto import chat_context
from oversimbot.handler import handlers
import json
import logging

logger = logging.getLogger('ChatTracker')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class ChatTracker:

    def __init__(self):
        self.ctx = chat_context.ChateContext()
        self.chat_form = {}
        oversimbot_model = self.load_trained_data()

        self.chat_domain = chat_domain.ChatDomain()
        self.chat_domain.response_dict=oversimbot_model["domain__response_dict"]

        self.intent_repo = intent_repository.IntentRepository()
        self.intent_repo.intentions_vocabluary =oversimbot_model["intent__intentions_vocabluary"]
        self.intent_repo.intents =oversimbot_model["intent__intents"]
        self.intent_repo.lookups =oversimbot_model["intent__lookups"]
        self.intent_repo.phrase_compressed =oversimbot_model["intent__phrase_compressed"]
        self.intent_repo.phrase_to_intent =oversimbot_model["intent__phrase_to_intent"]

        self.story = story_repository.StoryRepository()
        self.story.intent_phrases =  oversimbot_model["story__intent_phrases"]
        self.story.intent_childs =  oversimbot_model["story__intent_childs"]

        self.handler_list = [handlers.NameUnderstoodHandler(), handlers.DontTravelHandler(), handlers.IdentifyFirstOstacleHandler(), handlers.SolveSecondChallangeHandler()]

    def load_trained_data(self):
        with open('oversimbot/data/oversimbot_model.json') as f:
            oversimbot_model = json.load(f)
        return oversimbot_model

    def find_action_list(self, aCtx, aIntent):
        """
        find_action_list
        """
        action_list = []
        if(aCtx.next_intents and not aIntent.key in aCtx.next_intents):
            logger.debug('[ChatTracker#find_response] "{}" is not expecected as next action: {}'.format(aIntent, aCtx.next_intents))
            action_list = ["cmd_not_clear"]
        else:
            logger.debug('[ChatTracker#find_response] currently expected intents: {}'.format(aCtx.next_intents))
            action_list = self.story.find_action(aIntent)
        return action_list


    def find_response(self,message):
        """
        find_response
        """
        logger.debug('[ChatTracker#find_response] >>> input message: {}'.format(message))
        logger.debug('[ChatTracker#find_response] ctx.previous_intents: {}'.format(">".join([ str(i.key) for i  in self.ctx.previous_intents])))
        intent = self.intent_repo.find_intent(message)
        logger.debug('[ChatTracker#find_response] intent: {}'.format(intent))
        action_list = self.find_action_list(self.ctx, intent)
        logger.debug('[ChatTracker#find_response] action_list: {}'.format(action_list))

        utter_keys_list = []
        for action_key in action_list :
            repsonse_keys = []
            for handler in self.handler_list:
                if(handler.does_supports(action_key, intent, self.ctx)):
                    repsonse_keys = handler.find_response(action_key, intent, self.ctx)
                    break
            if(repsonse_keys):
                utter_keys_list = repsonse_keys
                break
            else:
                utter_keys_list.append(action_key)

        response_list = []
        for utter_key in utter_keys_list :
            repsonse = self.chat_domain.find_response(utter_key, intent)
            if(repsonse):
                response_list.append(repsonse)
            else:
                logger.debug('[ChatTracker#find_response] repsonse not found for key: {}'.format(utter_key))




        if("cmd_utterance_reverted" in utter_keys_list):
            logger.debug('[ChatTracker#find_response] adding to for response for cmd_utterance_reverted')
            repsonse = self.chat_domain.find_response("utter_utterance_reverted", intent)
            response_list.insert(0,repsonse)
        elif("cmd_not_clear" in utter_keys_list):
            logger.debug('[ChatTracker#find_response] repeating last question per cmd_not_clear')
            repsonse = self.chat_domain.find_response("utter_not_clear", intent)
            response_list.append(repsonse)
            response_list.append(self.ctx.previous_responses[-1])
        elif("cmd_restart_dialog" in utter_keys_list):
            logger.debug('[ChatTracker#find_response] reseting a context per cmd_restart_dialog: ')
            self.ctx.next_intents = []
            self.ctx.previous_intents = []
        else:
            self.ctx.next_intents = self.story.find_next_intents(intent.key)
            logger.debug('[ChatTracker#find_response] calculated next intents: {}'.format(self.ctx.next_intents))
            self.ctx.previous_intents.append(intent)

        self.ctx.previous_responses = response_list
        logger.debug('[ChatTracker#find_response] <<< response: {}\n\n\n'.format(response_list))

        return response_list
