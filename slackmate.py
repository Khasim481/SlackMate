from time import sleep
from re import search
from slackclient import SlackClient
from rivescript import RiveScript


slack_client = SlackClient('xoxb-344585199425-z7yzbWZScASqKeBKO8UzD4S7')
slackmatebot_id = None


class GetReply(object):
    def __init__(self):
        self.bot = RiveScript()
        self.bot.load_directory("dialogues")
        self.bot.sort_replies()

    def get_response(self, user, message):
        return self.bot.reply(user, message)


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        slack_mate_bot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            for event in slack_client.rtm_read():
                print event
                if event["type"] == "message" and not "subtype" in event:
                    matches = search("^<@(|[WU].+?)>(.*)", event["text"])
                    if matches:
                        user_id, message = matches.group(1), matches.group(2).strip()
                    else:
                        user_id, message = None, None
                    if user_id == slack_mate_bot_id:
                        command, channel = message, event["channel"]
                        if command:
                            slack_client.api_call(
                                "chat.postMessage",
                                channel=channel,
                                text=GetReply().get_response(user="Khasim", message=command)
                            )
            sleep(1)
    else:
        from traceback import print_exc
        print_exc()
