from oversimbot_train.parser import story_parser
from oversimbot_train.parser import intent_parser
from oversimbot_train.parser import domain_parser
from oversimbot.nlp import word_cleaner
from oversimbot.nlp import word_lemmatizer
import json
import re
import os

class ChatTrainer:
    def __init__(self):
        pass

    def parse_files(self):
        tained_data={}
        storyParser = story_parser.StoryParser()
        story = storyParser.parse("oversimbot_train/data/stories_nao.md")
        print(["test1", story.intent_phrases])

        intentParser = intent_parser.IntentParser()
        intent_repo = intentParser.parse("oversimbot_train/data/nlu_data.md")
        intentions_vocabluary = self.build_intentions_vocabluary(intent_repo)
        # print(intentions_vocabluary)
        intent_repo.intentions_vocabluary = intentions_vocabluary
        self.upadate_intent_indexes(intent_repo, intentions_vocabluary)

        chatDomainParser = domain_parser.ChatDomainParser()
        chat_domain = chatDomainParser.parse("oversimbot_train/data/domain.yml")

        tained_data["story__intent_phrases"]=story.intent_phrases
        tained_data["story__intent_childs"]=story.intent_childs

        tained_data["intent__intents"]=intent_repo.intents
        tained_data["intent__phrase_to_intent"]=intent_repo.phrase_to_intent
        tained_data["intent__phrase_compressed"]=intent_repo.phrase_compressed
        tained_data["intent__lookups"]=intent_repo.lookups
        tained_data["intent__intentions_vocabluary"]=intent_repo.intentions_vocabluary

        tained_data["domain__response_dict"]=chat_domain.response_dict


        return tained_data


    def upadate_intent_indexes(self, intent_repo, intentions_vocabluary):
        phrases = intent_repo.phrase_to_intent.keys()
        for phrase in phrases:
            entities_exists_matcher = re.search('\[(.*)\]\((.*)\)', phrase)
            #is needed search for entities
            if(entities_exists_matcher):
                plain_phrase = re.sub(r"(\[.*\])", "", phrase).strip()
                plain_phrase = re.sub(r"(\(.*\))", "", plain_phrase).strip()
                cleaned_phrase = intent_repo.cleaner.clean_stop_words(plain_phrase.split(" "))
                core_phrase = list(intent_repo.lemmatizer.find_word_core_list(cleaned_phrase).values())
                core_indx = []
                for core_word in core_phrase:
                    core_indx.append(intentions_vocabluary.index(core_word))
                # print([phrase, m.group(1), m.group(2), core_phrase, core_indx])
                intent_repo.add_compressed_phrase(phrase, core_indx)


    def build_intentions_vocabluary(self, intent_repo):
        phrases = intent_repo.phrase_to_intent.keys()
        words = []

        for phrase in phrases:
            plain_phrase = re.sub(r"(\[.*\])", "", phrase).strip()
            plain_phrase = re.sub(r"(\(.*\))", "", plain_phrase).strip()
            words.extend(plain_phrase.split(" "))

        # print(words)
        unique_word = intent_repo.cleaner.clean_stop_words(set(words))
        core_words = intent_repo.lemmatizer.find_word_core_list(unique_word)
        # print(unique_word)
        # print(core_words)
        return list(core_words.values())

    def generate_dialog_chart(self, trained_data):
        """
        dot -Tps test.dot -o out.ps
        """
        story = trained_data["story__intent_childs"]
        result = []
        for parent_key in story.keys():
            parent_val = parent_key if parent_key else "O"
            for child_key in story[parent_key]:
                line = parent_val + " -> " + child_key
                result.append(line)
        for intent_key in trained_data["story__intent_phrases"]:
                phrases = trained_data["story__intent_phrases"][intent_key]
                for phrase in phrases:
                    line = intent_key + " -> " + phrase  +  "[style=dotted]"
                    result.append(line)
        result_str = "/*dot -Tpng story_map.dot -o out.png*/\n"+"digraph G {\n"+";\n\t".join(result)+"\n}"

        return result_str



if __name__ == '__main__':

    trainer = ChatTrainer()
    tained_data = trainer.parse_files()
    story_map_dot = trainer.generate_dialog_chart(tained_data)
    with open("./target/story_map.dot", "w") as outfile:
        outfile.write(story_map_dot)
    print("graph story representation: dot -Tpng target/story_map.dot -o target/out.png")
    with open("./target/oversimbot_model.json", "w") as outfile:
        json.dump(tained_data, outfile)
    # print(json.dumps(tained_data,sort_keys=True, indent=2))

    print("File saved to ./target/oversimbot_model.json")
