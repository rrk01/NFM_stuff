"""
Elo Bot - Generate matchmaking for players and calculate matchmaking rating after matches.
Author - rz#1337
"""

import discord
from discord.ext import commands
import math
import random
import threading
import time


class Player:  # Player class. name = username, elo = mmr
    raw_name = ""  # Raw username with hashtag
    display_name = ""  # Display nickname
    elo = -1.0  # default mmr
    in_game = False  # True if the Player is in-game
    current_game = None  # Becomes a Game if in_game is True

    def __init__(self, raw_name, display_name, elo=1000.0):
        self.raw_name = raw_name
        self.display_name = display_name
        self.elo = elo

    def get_raw_name(self):  # Getters and setters
        return self.raw_name

    def set_raw_name(self, raw_name):
        self.raw_name = raw_name

    def get_display_name(self):
        return self.display_name

    def set_display_name(self, display_name):
        self.display_name = display_name

    def get_elo(self):
        return self.elo

    def set_elo(self, elo):
        self.elo = elo

    def is_in_game(self):
        return self.in_game

    def set_in_game(self, ig):
        self.in_game = ig

    def get_current_game(self):
        return self.current_game

    def set_current_game(self, current_game):
        self.current_game = current_game

    def __eq__(self, other):
        return self.raw_name == other.get_raw_name()

    def __lt__(self, other):  # Less than
        return self.elo < other.get_elo()

    def __le__(self, other):  # Less than or equal to
        return self <= other.get_elo()

    def __gt__(self, other):  # Greater than
        return self.elo > other.get_elo()

    def __ge__(self, other):  # Greater than or equal to
        return self.elo >= other.get_elo()

    def __add__(self, other):  # Adding Players together
        self.set_elo(self.get_elo() + other.get_elo())

    def __sub__(self, other):  # Subtracting two Players
        self.set_elo(self.get_elo() - other.get_elo())

    def __repr__(self):  # toString function, prints raw name and elo
        return str(self.raw_name) + "," + str(self.display_name) + "," + str(self.elo)

    def play(self, player2):  # win = True: winner, win = False: loser
        '''win = False
        win_probabilities = find_win_probability(self.elo, player2.get_elo())
        rand_num = random.uniform(0, 100)
        if rand_num <= win_probabilities[0]:  # if win
            win = True
            if self.elo > player2.elo:
                elo_change = 20 / (1 + math.pow(10, (self.elo - player2.elo) / 400))
            else:
                elo_change = 20 - (20 / (1 + math.pow(10, (player2.elo - self.elo) / 400)))
            self.elo += elo_change
            player2.elo -= elo_change
            print("player1 win")
        else:  # if lose
        win = False'''
        if self.get_elo() < player2.get_elo():
            elo_change = 20 / (1 + math.pow(10, (player2.elo - self.elo) / 400))
        else:
            elo_change = 20 - (20 / (1 + math.pow(10, (self.elo - player2.elo) / 400)))
        self.set_elo(self.get_elo() - elo_change)
        player2.set_elo(player2.get_elo() + elo_change)
        #  print("player2 win")
        channel = client.get_channel(962084399778791494)  # Gets channel from internal cache
        client.loop.create_task(channel.send(f'```Match finished. Elo change: +/- {round(elo_change, 2)}```'))  # Sends message to channel
        current_time = time.ctime(time.time())
        print(f"{current_time}\t+/- " + str(elo_change))


class Game:  # The match in progress
    p1 = None
    p2 = None
    p3 = None
    p4 = None

    def __init__(self, p1, p2, p3=Player("", "", -1.0), p4=Player("", "", -1.0)):
        p1.set_in_game(True)
        p1.set_current_game(self)
        self.p1 = p1
        p2.set_in_game(True)
        p2.set_current_game(self)
        self.p2 = p2
        p3.set_in_game(True)
        p3.set_current_game(self)
        self.p3 = p3
        p4.set_in_game(True)
        p4.set_current_game(self)
        self.p4 = p4

    def get_players(self):
        return [self.p1, self.p2, self.p3, self.p4]

    def __repr__(self):
        to_print = "```"
        to_print += f'{self.p1.get_display_name()} ({self.p1.get_elo()}) vs {self.p2.get_display_name()} ({self.p2.get_elo()})'
        to_print += "```"
        return to_print

    def __del__(self):
        self.p1.set_current_game(None)
        self.p1.set_in_game(False)
        self.p2.set_current_game(None)
        self.p2.set_in_game(False)
        self.p3.set_current_game(None)
        self.p3.set_in_game(False)
        self.p4.set_current_game(None)
        self.p4.set_in_game(False)
        #  channel = client.get_channel(962084399778791494)  # Gets channel from internal cache
        #  client.loop.create_task(channel.send(f'Match finished.'))  # Sends message to channel


def find_win_probability(elo1, elo2):  # Calculates % chance of win for each player based on elo
    elo2 = 100 / (1 + math.pow(10, (elo1 - elo2) / 400))
    elo1 = 100 - elo2
    print(f'a: {elo1}%, b: {elo2}%')

    return elo1, elo2


def clear_file(filename):  # Deletes all content from specified text file.
    file = open(filename, "w")
    file.close()


# Function to do insertion sort in descending order on leaderboard[] from GeeksForGeeks
def sort(arr):
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):

        key = arr[i]

        # Move elements of arr[0..i-1], that are
        # less than key, to one position ahead
        # of their current position
        j = i - 1
        while j >= 0 and key > arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


# ---- ALMIGHTY TOKEN ---- #
TOKEN = 'insert your token here'
# ------------------------ #

client = discord.Client()

leaderboard = []  # List of Players in order based on elo
queue = []  # List of Players waiting for a match
global queue_timer
# queue_timer = -1.0  # Counts down to 0 from 10 minutes to find a match. Changes based on how many Players in queue.
t = threading.Thread()  # Placeholder variable for timer threads


def queue_timer_adjust():  # Changes queue timer based on various factors
    global queue_timer
    queue_time_set = 60/(queue.__len__())
    # if queue_timer > queue_time_set or queue_timer < 1:
    queue_timer = queue_time_set
    queue_timer_minutes = round(queue_timer/60, 2)
    channel = client.get_channel(962084399778791494)  # Gets channel from internal cache
    client.loop.create_task(channel.send(f'Queue pops in {queue_timer_minutes} minutes.'))  # Sends message to channel


def queue_pop():  # Runs when queue timer ends.
    games = []  # List of games created when queue pops.
    channel = client.get_channel(962084399778791494)  # Gets channel from internal cache
    current_time = time.ctime(time.time())
    print(f'{current_time}\tQueue popped.')
    client.loop.create_task(channel.send(f'Queue popped.'))  # Sends message to channel
    lowest_elo_diff = [-1, -1, 999.9]
    while len(queue) > 0:  # Empties queue
        if len(queue) >= 2:  # Replace 2 with game size later - this is hard coded rn.
            for x in range(0, len(
                    queue)):  # Loops through to find optimal matches. x and y represent position of item in queue[].
                for y in range(0, len(queue)):
                    if x == y:
                        continue
                    elif abs(queue[x].get_elo() - queue[y].get_elo()) < lowest_elo_diff[2]:
                        lowest_elo_diff = [x, y, abs(queue[x].get_elo() - queue[y].get_elo())]

            games.append(Game(queue[lowest_elo_diff[0]], queue[lowest_elo_diff[1]]))
            q_len_debug = len(queue)
            queue[lowest_elo_diff[0]].set_in_game(True)
            queue[lowest_elo_diff[1]].set_in_game(True)
            current_time = time.ctime(time.time())
            print(f'{current_time}\tAdded {queue[lowest_elo_diff[0]].get_display_name()} to match and removed them from queue.')
            queue.pop(lowest_elo_diff[0])
            print(f'{current_time}\tAdded {queue[lowest_elo_diff[1] - 1].get_display_name()} to match and removed them from queue.')
            queue.pop(lowest_elo_diff[1] - 1)
        else:
            break

        for x in games:
            current_time = time.ctime(time.time())
            print(f'{current_time}\tMatch found: {x}')
            client.loop.create_task(channel.send(f'```Match found!```\n{x}'))

    return


# --- File -> leaderboard[] --- #
file = open("leaderboard.txt", "r")
lines = file.readlines()
count = 0
for line in lines:  # Format of file: PlayerRawName,PlayerDisplayName,Elo ex. Kid Iraqi#2000,Toa,1000.0
    current_time = time.ctime(time.time())
    line = line.replace("\n", "")
    temp_raw_name = line.split(",")[0]
    temp_display_name = line.split(",")[1]
    temp_elo = float(line.split(",")[2])
    print(f'{current_time}\t{temp_raw_name}, {temp_display_name}, {temp_elo}')
    leaderboard.append(Player(temp_raw_name, temp_display_name, temp_elo))
# ----------------------------- #


sort(leaderboard)  # Make sure the leaderboard is sorted upon starting the bot.
file.close()


@client.event
async def on_ready():  # Login confirmation message
    current_time = time.ctime(time.time())
    print(f'{current_time}\t', end='')
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):  # When a message is sent in the server
    if message.author == client.user:  # Bot ignores its own messages
        return

    current_time = time.ctime(time.time())
    raw_name = str(message.author)  # Discord username including hashtag
    display_name = str(message.author.display_name)
    user_message = str(message.content)  # String of a user's message
    channel = str(message.channel.name)  # Text channel the message was sent
    print(f'{current_time}\t{raw_name} ({display_name}): {user_message} ({channel})')  # Print chat messages to console

    if message.channel.name == 'bot' and user_message.startswith("!"):  # User message must start with '!' for bot to recognize it as a command.
        if user_message.lower() == '!join':  # Adds user to queue with this command.
            if leaderboard.__len__() == 0:  # If leaderboard is empty.
                await message.channel.send(f'Please register your name on the leaderboard using \'!register\'.')

            for x in queue:  # Checks queue to see if the player is already in it.
                if x.get_raw_name() == raw_name:
                    await message.channel.send(f'{display_name} is already in queue.')
                    return

            for x in leaderboard:  # Traverses leaderboard
                if x.get_raw_name() == raw_name:  # If user has registered and is not already in queue.
                    if x.is_in_game():  # If user is in game.
                        await message.channel.send(f'{display_name} is in game. Finish the match to re-queue.')
                        await message.channel.send(f'{x.get_current_game()}')
                        return
                    queue.append(x)  # Adds Player x to the queue
                    await message.channel.send(f'{display_name} added to queue.')  # Queue add confirmation message.
                    global t
                    if t.is_alive():  # Hopefully terminates thread if another Player is added to queue.
                        print(f'{current_time}\tTHREAD CANCELED.')
                        t.cancel()
                    queue_timer_adjust()  # Adjusts the queue timer based on how many Players are in queue.
                    t = threading.Timer(queue_timer, queue_pop)
                    t.start()  # Start new thread for the queue timer
                    return

            await message.channel.send(f'Please register your name on the leaderboard using \'!register\'.')
            return

        if user_message.lower() == '!leave':  # Adds user to queue with this command.
            for x in range(queue.__len__()):  # Checks queue to see if the player is already in it.
                if queue[x].get_raw_name() == raw_name:
                    queue.pop(x)
                    await message.channel.send(f'{display_name} has been removed from the queue.')
                    return

            await message.channel.send(f'{display_name} is not currently in a queue.')
            return

        if user_message.lower() == '!loss' or user_message.lower() == '!submit loss':
            for x in leaderboard:
                if x.get_raw_name() == raw_name:
                    if not x.is_in_game():
                        await message.channel.send(f'{display_name} is not currently in a match.')
                        return
                    opponent = None
                    for y in x.get_current_game().get_players():
                        if x.get_raw_name() != y.get_raw_name():
                            opponent = y
                            break

                    x.play(opponent)  # Calculates elo change.
                    x.set_current_game(None)  # Reset flags.
                    x.set_in_game(False)
                    opponent.set_current_game(None)
                    opponent.set_in_game(False)
                    sort(leaderboard)  # Reorganize leaderboard.
                    file = open("leaderboard.txt", "w")  # Overwrite file with sorted leaderboard.
                    for y in leaderboard:
                        file.write(f'{y}\n')  # Writes newly registered Player to file.

                    file.close()
                    return

        if user_message.lower() == '!lb':  # Displays leaderboard in a chat message.
            to_print = "```--- LEADERBOARD ---\n"  # String to print at the end.
            position_counter = 1
            for x in leaderboard:
                to_print += f'{position_counter}. '
                to_print += f'{x.get_display_name()}\t\t{round(x.get_elo())}\n'
                position_counter += 1
            to_print += "```"
            await message.channel.send(to_print)

        if user_message.lower() == '!showq' or user_message.lower() == '!queue':  # Shows queue
            to_print = "``` -- QUEUE --\n"
            for x in queue:
                to_print += f'{x.get_display_name()}\n'

            to_print += "```"
            await message.channel.send(to_print)

        if user_message.lower() == '!qtime':
            await message.channel.send(f'Queue pops in {queue_timer} seconds.')

        if user_message.lower() == '!register':  # Adds user to leaderboard with this command or changes display name.
            if leaderboard.__len__() == 0:  # If leaderboard is empty.
                leaderboard.append(Player(raw_name, display_name))  # Adds new Player to the leaderboard.
                file = open("leaderboard.txt", "a")
                file.write(f'{leaderboard[0]}\n')  # Writes newly registered Player to file.
                file.close()
                await message.channel.send(f'{raw_name} ({display_name}) is now registered to play.')  # Confirmation message.
                return

            for x in leaderboard:  # Traverses leaderboard
                if x.get_raw_name() == raw_name and x.get_display_name() == display_name:  # Checks if user has registered and is using the same display name.
                    await message.channel.send(f'{raw_name} ({display_name}) is already registered!')  # Don't add existing user.
                    return
                elif x.get_raw_name() == raw_name and not x.get_display_name() == display_name:  # If user has changed their display name.
                    x.set_display_name(display_name)
                    await message.channel.send(f'Display name updated to {display_name}.')
                    file = open("leaderboard.txt", "w")
                    for y in leaderboard:  # Rewrite file with updated display name.
                        file.write(f'{y}\n')

                    file.close()
                    return

            new_player = Player(raw_name, display_name)
            leaderboard.append(new_player)  # Adds new Player to the leaderboard.
            sort(leaderboard)
            file = open("leaderboard.txt", "w")
            for y in leaderboard:
                file.write(f'{y}\n')  # Writes newly registered Player to file.

            file.close()
            await message.channel.send(f'{raw_name} ({display_name}) is now registered to play.')  # Confirmation message.
            return


client.run(TOKEN)
