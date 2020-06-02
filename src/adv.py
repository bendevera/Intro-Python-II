from room import Room
from player import Player
from monster import Monster

# Declare all the rooms
room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons"),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""", items=["key"], visit_points=10),
    'bridge': Room("Mystical Bridge", "Dare to crosss?", items=["sword"]),
    'castle': Room("Castle", "Known to hold treasure", items=["treasure"]),
    'garden': Room("Garden", "Lookout for traps",  visit_points=-5)
}
room_list = room.keys()


# Link rooms together
room['outside'].link_rooms(n=room['foyer'], s=room['bridge'])
room['bridge'].link_rooms(n=room['outside'], e=room['castle'], w=room['garden'])
room['garden'].link_rooms(e=room['bridge'])
room['castle'].link_rooms(w=room['bridge'])
room['foyer'].link_rooms(n=room['overlook'], s=room['outside'], e=room['narrow'])
room['overlook'].link_rooms(s=room['foyer'])
room['narrow'].link_rooms(n=room['treasure'], w=room['foyer'])
room['treasure'].link_rooms(s=room['narrow'])


# Make a new player object that is currently in the 'outside' room.
players_name = input("Player's name: ")
my_player = Player(players_name, room['outside'])

# Write a loop to play the game.
while True:
    move = input("-----> ").strip()
    if move == "q":
        print("Goodbye.")
        exit()
    my_player.make_move(move)
