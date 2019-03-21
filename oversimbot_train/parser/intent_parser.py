import re
import logging
from oversimbot.core import intent_repository
import json

logger = logging.getLogger('ChatTracker')



class IntentParser:
    def __init__(self):
        print()


    def parse(self, file_path):
        f = open(file_path)
        intent_repo = intent_repository.IntentRepository()
        # trained_data = self.load_trained_data()
        # intent_repo.intentions_vocabluary = trained_data["core_words"]
        # intent_repo.lookups = trained_data["lookups"]
        last_intent = ""
        last_lookup = ""
        with(f):
            for line in f:
                # print(line)
                line = re.sub(r"(<!--.*-->)", "", line.strip())
                line = re.sub(r"({.*})", "", line.strip())
                if(line.startswith("## intent:")):
                    line = line.replace("## intent:","").strip()
                    last_intent = line
                    last_lookup = ""
                    intent_repo.add_intent(last_intent)
                elif(line.startswith("## lookup:")):
                    line = line.replace("## lookup:","").strip()
                    last_intent = ""
                    last_lookup = line
                    intent_repo.lookups[last_lookup]=[]
                elif(line.startswith("-")):
                    line = line.replace("-","").strip()
                    # line = re.sub(r"(\[.*\])", "", line).strip()
                    # line = re.sub(r"(\(.*\))", "", line).strip()
                    line = line.replace("!", "").replace("?","")
                    line = line.lower()
                    # print(line)
                    if(last_intent):
                        intent_repo.add_phrase(last_intent, line)
                    elif(last_lookup):
                        intent_repo.lookups[last_lookup].append(line)
        return intent_repo
