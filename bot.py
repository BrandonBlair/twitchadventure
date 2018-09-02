'''
Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at
    http://aws.amazon.com/apache2.0/
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
'''

import sys
import irc.bot
import requests
import random
from time import time

from game.escape.cabin.mysterious_cabin import CabinMystery
from game.adventure.campaigns.deep_dungeon import DeepDungeon
from game.adventure.races import races

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel
        self.mystery = CabinMystery()
        self.adventure = DeepDungeon()

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)


    def on_welcome(self, c, e):
        print('Joining ' + self.channel)

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)
        print("Successfully joined?")

    def on_pubmsg(self, c, e):

        # If a chat message starts with an exclamation point, try to run it as a command
        chat_cmd = e.arguments[0]
        if chat_cmd[0] == '!':
            self.do_command(e, chat_cmd[1:])
        return

    def do_command(self, e, cmd):
        c = self.connection
        print("command recvd:", cmd)
        cmd_tokens = cmd.lower().split(' ')

        # Poll the API to get current game.
        if cmd_tokens[0] == "game":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' is currently playing ' + r['game'])

        # Poll the API the get the current status of the stream
        elif cmd_tokens[0] == "title":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' channel title is currently ' + r['status'])

        # Provide basic information to viewers for specific commands
        elif cmd_tokens[0] == "mystery":
            if len(cmd_tokens) == 1:
                message = self.mystery.describe_current_step()

            elif cmd_tokens[1] == "inventory":
                message = ', '.join(self.mystery.inventory)
            elif cmd_tokens[1] == "search":
                message = self.mystery.current_step.search(character)
            else:
                message = self.mystery.attempt(cmd[8:])  # Ignore mystery command and space
            c.privmsg(self.channel, message)

        elif cmd_tokens[0] == "adventure":
            print("Length of cmd tokens {}".format(len(cmd_tokens)))
            twitch_user = e.source.split('@')[0].split('!')[1]  # Derive user from myname!myname@twitch.tmi.com
            if twitch_user in self.adventure.adventurers:
                pass
            else:
                race = random.choice(races)
                self.adventure.add_character(name=twitch_user, race=race)
                msg = f"{twitch_user} has joined the adventure! They will be playing {twitch_user} the {race}"
                c.privmsg(self.channel, msg)
            if len(cmd_tokens) == 1:
                message = self.adventure.current_room.full_desc

            elif cmd_tokens[1] == "inventory":
                message = ', '.join(self.adventure.inventory)
            elif cmd_tokens[1] == "search":
                player = self.adventure.adventurers.get(twitch_user)
                search_msg = self.adventure.current_room.search(player)
                message = search_msg
            else:
                message = self.mystery.attempt(cmd[8:])  # Ignore mystery command and space
            c.privmsg(self.channel, message)

        elif cmd == "schedule":
            message = "This is an example bot, replace this text with your schedule text."
            c.privmsg(self.channel, message)

        # The command was not recognized
        else:
            c.privmsg(self.channel, "Did not understand command: " + cmd)

def main():
    if len(sys.argv) != 5:
        print("Usage: twitchbot <username> <client id> <token> <channel>")
        sys.exit(1)

    username  = sys.argv[1]
    client_id = sys.argv[2]
    token     = sys.argv[3]
    channel   = sys.argv[4]

    bot = TwitchBot(username, client_id, token, channel)
    bot.start()

if __name__ == "__main__":
    main()