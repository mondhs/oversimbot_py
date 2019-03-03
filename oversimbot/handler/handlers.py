
import logging

logger = logging.getLogger('Handler')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class Handler:
    def does_supports(self, action_name, intent, ctx):
        return False

    def find_response(action_name, intent, ctx):
        logger.debug(["Handler", ctx])
        return ["cmd_not_clear"]

class NameUnderstoodHandler(Handler):
    def does_supports(self, action_name, intent, ctx):
        return action_name == "action_check_name"

    def find_response(self, action_name, intent, ctx):
        logger.debug("[NameUnderstoodHandler]Check if person_name exists in : {}".format(intent.entities))
        if(not "person_name" in intent.entities):
            return ["cmd_not_clear"]


class DontTravelHandler(Handler):
    def does_supports(self, action_name, intent, ctx):
        return action_name == "action_dont_travel"

    def find_response(self, action_name, intent, ctx):
        prev_intent = ctx.previous_intents[-1].key
        logger.debug("[DontTravelHandler]previous intents : {}".format(prev_intent))
        if(prev_intent=="deny" or prev_intent == "dont_know"):
            return ["utter_please_comeback", "utter_bye"]
        return ["utter_encourage"]

class TranportationOptionsHandler(Handler):
    def does_supports(self, action_name, intent, ctx):
        return action_name == "action_transportation_options"

    def find_response(self, action_name, intent, ctx):
        # print(">>>>>>>>>>>>>>>> TranportationOptionsHandler" + str(intent))
        return []

class IdentifyFirstOstacleHandler(Handler):
    def does_supports(self, action_name, intent, ctx):
        return action_name == "action_identify_first_obstacle"

    def find_response(self, action_name, intent, ctx):

        if(not "first_obstacle" in intent.entities):
            return ["cmd_not_clear"]
        first_obstacle = intent.entities["first_obstacle"]
        # print(">>>>>>>>>>>>>>>> IdentifyFirstOstacleHandler: " + str(first_obstacle=="jūra"))
        if(first_obstacle=="bala"):
            return ["utter_no_swamp_in_map","cmd_utterance_reverted"]
        elif(first_obstacle=="vandenynas"):
            return ["utter_see_too_big","cmd_utterance_reverted"]
        elif(first_obstacle=="jūra"):
            return ["utter_see_too_big","cmd_utterance_reverted"]
        return []

class SolveSecondChallangeHandler(Handler):
    def does_supports(self, action_name, intent, ctx):
        return action_name == "action_identify_second_chalange"

    def find_response(self, action_name, intent, ctx):

        if(not "second_chalange" in intent.entities):
            return ["cmd_not_clear"]
        second_chalange = intent.entities["second_chalange"]
        # print(">>>>>>>>>>>>>>>> SolveSecondChallangeHandler: " + str(second_chalange))
        if(second_chalange=="burlaiviu"):
            return ["cmd_restart_dialog"]
        elif(second_chalange=="plaustu"):
            return ["utter_manpower_boat_too_slow","cmd_utterance_reverted"]
        elif(second_chalange=="irklente"):
            return ["utter_manpower_boat_too_slow","cmd_utterance_reverted"]
        elif(second_chalange=="motoru"):
            return ["utter_motor_boat_requires_maintainances","cmd_utterance_reverted"]
        return []
