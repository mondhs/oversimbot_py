import re
import logging
from oversimbot.core import story_repository

logger = logging.getLogger('oversimbot')



class StoryParser:
    def __init__(self):
        pass


    def parse(self, file_path):
        f = open(file_path)
        story_repo = story_repository.StoryRepository()
        last_intent = ""
        with(f):
            for line in f:
                # print(line)
                line = re.sub(r"(<!--.*-->)", "", line.strip())
                line = re.sub(r"({.*})", "", line.strip())
                if(line.startswith("##")):
                    story_repo.name = line.replace("##","").strip()
                    last_intent=""
                elif(line.startswith("*")):
                    line = line.replace("*","").strip()
                    story_repo.add_intent(line, last_intent)
                    last_intent = line
                elif(line.startswith("-")):
                    line = line.replace("-","").strip()
                    story_repo.add_action(last_intent, line)

        # print(story_repo)
        logger.debug("[StoryParser#parse] {}".format(story_repo))

        return story_repo
