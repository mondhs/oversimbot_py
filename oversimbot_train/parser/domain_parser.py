import re
from oversimbot.core import chat_domain

class ChatDomainParser:
    def __init__(self):
        print()

    def parse(self, file_path):
        f = open(file_path)
        domain = chat_domain.ChatDomain()
        last_param = ""
        response_key = ""
        with(f):
            for line in f:
                # print(line)
                line = re.sub(r"(<!--.*-->)", "", line.strip())
                # line = re.sub(r"({.*})", "", line.strip())
                if(line.startswith("templates")):
                    last_param = line
                elif(last_param.startswith("templates:")):
                    if(line.startswith("- text:")):
                        line = line.replace("- text:","").strip().lower()
                        line = line.replace("\"","")
                        # print(response_key, line)
                        domain.add_response(response_key, line)
                    elif(line.startswith("utter")):
                        # print(line)
                        line = line.replace(":","")
                        response_key = line.strip().lower()
        return domain
