import re
from oversimbot.nlp import word_cleaner
from oversimbot.nlp import word_lemmatizer
from oversimbot.dto import intent_response
import logging

logger = logging.getLogger('IntentRepository')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class IntentRepository:

    def __init__(self):
        self.intents = []
        self.phrase_to_intent = {}
        self.phrase_compressed = {}
        self.lemmatizer = word_lemmatizer.WordLemmatizer()
        self.cleaner = word_cleaner.WordCleaner()
        self.lookups = {}
        self.intentions_vocabluary = []


    def add_intent(self, intent_key):
        self.intents.append(intent_key)


    def add_phrase(self, intent_key, phrase):
        plain_phrase = re.sub(r"(\[.*\])", "", phrase).strip()
        # print(">>>> ", plain_phrase)
        self.phrase_to_intent[plain_phrase]=intent_key

    def add_compressed_phrase(self, phrase, compressed_list):
        plain_phrase = re.sub(r"(\[.*\])", "", phrase).strip()
        # print(">>>> ", plain_phrase)
        self.phrase_compressed[plain_phrase]=compressed_list


    def find_intent(self, phrase):
        """
            find intent by given text in repo
        """
        response = intent_response.IntentResponse()
        phrase = phrase.lower()

        logger.debug("[IntentRepository#find_intent] incomming phrase: {}".format(phrase))

        if(phrase in self.phrase_to_intent):
            response.key = self.phrase_to_intent[phrase]
            logger.debug("[IntentRepository#find_intent] static phrase found: {}".format(response))
            return response

        min_phrase = self.find_nearest_phrase(phrase)
        #if min phase not found, assume it is just lookup
        if(len(min_phrase)<=0):
            for lookup_id in self.lookups:
                if(phrase in self.lookups[lookup_id]):
                    response.key = self.phrase_to_intent["({})".format(lookup_id)]
                    response.entities[lookup_id]=phrase
                    logger.debug("[IntentRepository#find_intent] phrase as single lookup found: {}".format(response))
                    # print(["In::::", self.lookups[lookup_id], lookup_intent])
        else:
            logger.debug("[IntentRepository#find_intent] min_phrase: {}".format(min_phrase))
            #entities_exists_matcher = re.search('\[(.*)\]\((.*)\)', min_phrase)
            entities_exists_matcher = re.search('\((.*)\)', min_phrase)
            # There is pattern
            if(entities_exists_matcher):
                lookup_id = entities_exists_matcher.group(1)
                # logger.debug("[IntentRepository#find_intent] lookup_id: {}".format(lookup_id))
                lookup_list = []
                #is this lookup is known in repo
                if(lookup_id in self.lookups):
                    lookup_list = self.lookups[lookup_id]
                # logger.debug("[IntentRepository#find_intent] lookup_list: {}".format(lookup_list))

                for word in phrase.lower().split(" "):
                    if word in lookup_list:
                        response.entities[lookup_id]=word
                        break

                # logger.debug([phrase, min_phrase, entities_exists_matcher.group(1), entities_exists_matcher.group(2)])
            if(min_phrase in self.phrase_to_intent):
                response.key = self.phrase_to_intent[min_phrase]
            logger.debug("[IntentRepository#find_intent] response: {}".format(response))
        return response

    def find_nearest_phrase(self, phrase):
        """
            iterate through all phases in repo and get with smallest distance
        """
        plain_phrase = re.sub(r"(\[.*\])", "", phrase).strip()
        plain_phrase = re.sub(r"(\(.*\))", "", plain_phrase).strip()

        cleaned_phrase = self.cleaner.clean_stop_words(plain_phrase.split(" "))
        core_phrase = list(self.lemmatizer.find_word_core_list(cleaned_phrase).values())
        core_indx = []
        for core_word in core_phrase:
            if(core_word in self.intentions_vocabluary):
                core_indx.append(self.intentions_vocabluary.index(core_word))

        # logger.debug("[IntentRepository#find_nearest_phrase] input phrase: \nplain_phrase: {}\ncleaned_phrase:{}\ncore_phrase:{}\ncore_indx: {}".format(plain_phrase, cleaned_phrase,core_phrase,core_indx ))

        min_phrase =""

        if(len(core_indx)>0):
            min_phrase = self.find_nearest_phrase_by_coreidx(core_indx)

            # print([min_distance, min_phrase])
        return min_phrase

    def find_nearest_phrase_by_coreidx(self, core_indx):
        min_distance = 1000000
        min_phrase = ""


        for key in self.phrase_compressed:
            value =  self.phrase_compressed[key]

            distance = self.levenshtein(value, core_indx)
            # logger.debug("[IntentRepository#find_nearest_phrase] distance: {}".format([key, distance] ))
            if(min_distance>distance):
                min_distance = distance
                min_phrase = key
                print([key, value, core_indx, distance])
                logger.debug("[IntentRepository#find_nearest_phrase] compare result: {}".format([key, value, core_indx, distance] ))
        logger.debug("[IntentRepository#find_nearest_phrase] min_distance: {}; min_phrase: {}".format(min_distance, min_phrase ))
        return min_phrase

    def extract_sentences_for_intent(self, key):
        sentences = []
        phrase = self.phrase_to_intent[key]
        entities_exists_matcher = re.search('\[(.*)\]\((.*)\)', phrase)
        if(entities_exists_matcher):
            lookup_id = entities_exists_matcher.group(2)
            lookup_list = self.lookups[lookup_id]
            template_phrase = re.sub(r"(\[.*\])", "", phrase).strip()
            for lookup_value in lookup_list:
                plain_phrase = re.sub(r"(\(.*\))", lookup_value, template_phrase).strip()
                sentences.append(plain_phrase)
        else:
            sentences.append(phrase)
        return sentences

    def extract_sentences(self):
        sentences = []
        for phrase in self.phrase_to_intent.keys():
            entities_exists_matcher = re.search('\[(.*)\]\((.*)\)', phrase)
            if(entities_exists_matcher):
                lookup_id = entities_exists_matcher.group(2)
                lookup_list = self.lookups[lookup_id]
                template_phrase = re.sub(r"(\[.*\])", "", phrase).strip()
                for lookup_value in lookup_list:
                    plain_phrase = re.sub(r"(\(.*\))", lookup_value, template_phrase).strip()
                    sentences.append(plain_phrase)
            else:
                sentences.append(phrase)
        return sentences

    def extract_words(self):
        unique_words_dict = {}
        sentences = self.extract_sentences()
        for sentence in sentences:
            for word in sentence.split(" "):
                unique_words_dict[word] = ""
        unique_word_set = list(unique_words_dict.keys())
        unique_word_set.sort()
        return unique_word_set



# ///////////////////////////////////////////

    def levenshtein(self, s1, s2):
        if len(s1) < len(s2):
            return self.levenshtein(s2, s1)

        # len(s1) >= len(s2)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
                deletions = current_row[j] + 1       # than s2
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]


    def __str__(self):
        return str(self.__dict__)
