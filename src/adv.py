from room import Room
from player import Player
from monster import Monster
from rich.console import Console
import random

console = Console()

# Declare all the rooms
rooms = {
    'outside': {
        'name': "Outside Cave Entrance",
        'description': "North of you, the cave mount beckons",
        'points': 10
    },
    'foyer': {
        'name': "Foyer",
        'description': """Dim light filters in from the south. Dusty
        passages run north and east.""",
        'points': 10
    },
    'overlook': {
        'name': "Grand Overlook",
        'description': """A steep cliff appears before you, falling
        into the darkness. Ahead to the north, a light flickers in
        the distance, but there is no way across the chasm.""",
        'points': 10
    },
    'narrow': {
        'name': "Narrow Passage",
        'description': """The narrow passage bends here from west
        to north. The smell of gold permeates the air.""",
        'points': 10
    },
    'treasure': {
        'name': "Treasure Chamber",
        'description': """You've found the long-lost treasure
        chamber! Sadly, it has already been completely emptied by
        earlier adventurers. The only exit is to the south.""",
        'points': 10
    },
    'bridge': {
        'name': "Mystical Bridge",
        'description': """Dare to crosss?""",
        'points': 5
    },
    'castle': {
        'name': "Castle",
        'description': """Known to hold treasure""",
        'points': 100
    },
    'garden': {
        'name': "Garden",
        'description': """Lookout for traps""",
        'points': -20
    },

    'garden_shed': {
        'name': "Garden Shed",
        'description': """What a shed""",
        'points': 5
    }
}
room_list = list(rooms.keys())
random.shuffle(room_list)
item_list = ["sword", "hatchet", "glasses"]


class Game:
    def __init__(self, room_data, room_name_list, item_list):
        self.rooms = {}
        self.room_list = room_name_list
        self.item_list = item_list
        for num, key in enumerate(self.room_list):
            data = room_data[key]
            if num <= len(item_list)-1:
                items = [item_list[num]]
            else:
                items = []
            curr_room = Room(
                data['name'], data['description'], data['points'], items)
            self.rooms[key] = curr_room
        self.link_all_rooms(self.rooms)
        self.monster_list = []
        self.__help()
        # Make a new player object that is currently in the 'outside' room.
        players_name = input("Player's name: ")
        monster_count = int(input("Monster count: "))
        self.my_player = Player(players_name, self.rooms['outside'])
        for i in range(monster_count):
            self.monster_list.append(Monster(
                str(i), self.get_random_room(self.rooms, self.room_list)))

    def link_all_rooms(self, rooms):
        # Link rooms together
        rooms['outside'].link_rooms(n=rooms['foyer'], s=rooms['bridge'])
        rooms['bridge'].link_rooms(
            n=rooms['outside'], e=rooms['castle'], w=rooms['garden'])
        rooms['garden'].link_rooms(e=rooms['bridge'], s=rooms['garden_shed'])
        rooms['garden_shed'].link_rooms(n=rooms['garden'])
        rooms['castle'].link_rooms(w=rooms['bridge'])
        rooms['foyer'].link_rooms(
            n=rooms['overlook'], s=rooms['outside'], e=rooms['narrow'])
        rooms['overlook'].link_rooms(s=rooms['foyer'])
        rooms['narrow'].link_rooms(n=rooms['treasure'], w=rooms['foyer'])
        rooms['treasure'].link_rooms(s=rooms['narrow'])

    def get_random_room(self, rooms, room_list):
        return rooms[room_list[random.randint(0, len(room_list)-1)]]

    def get_adjacent_room(self, room: Room):
        directions = ["n", "s", "e", "w"]
        while True:
            direction = directions[random.randint(0, 3)]
            if room.is_room(direction):
                return room.get_room(direction)

    def __help(self):
        console.print("[bold cyan]Welcome to a python adventure.[/bold cyan]")
        console.print(
            "Game moves mostly consist of an [u]action[/u] and [u]noun[/u].")
        console.print(
            "Actions: [green]run[/green], [green]check[/green], [green]grab[/green]")
        console.print(
            "Examples: [bold]run (n, s, e, w)[/bold], [bold]check (i, n, s, e, w)[/bold], and [bold]grab (item #)[/bold]")
        console.print(
            "Other one letter moves: [i]q (quit)[/i], [i]w (wait)[/i]")
        print("\n")

    def __invalid_move(self, details=""):
        console.print(f"[red]Invalid move. {details} Try again.[/red]")
        print("\n")

    def make_move(self, move: str):
        move_pieces = move.split(" ")
        if len(move_pieces) == 2:
            self.process_move(move_pieces[0], move_pieces[1])
        else:
            self.__invalid_move(
                "Move must consist of 2 parts seperated by a space.")
        console.print(
            f"[bold magenta]Turn: {self.my_player.turns}[/bold magenta] | [bold blue]Points: {self.my_player.points}[/bold blue] | [bold green]Health: {self.my_player.health}[/bold green]")
        print()
        console.print("Current room:")
        self.my_player.room.show_data()

    def process_move(self, action: str, noun: str):
        if action == "run":
            can_move = self.my_player.room.is_room(noun)
            if can_move:
                self.my_player.change_room(self.my_player.room.get_room(noun))
                self.my_player.turns += 1
            else:
                self.__invalid_move(f"Can't move {noun} of current room.")
        elif action == "check":
            if noun == "i":
                self.my_player.show_items()
            else:
                is_room = self.my_player.room.is_room(noun)
                if is_room:
                    room = self.my_player.room.get_room(noun)
                    room.show_preview()
                else:
                    self.__invalid_move(f"No room {noun} of current room.")
        elif action == "grab":
            try:
                self.my_player.grab_item(int(noun)-1)
                self.my_player.turns += 1
            except:
                self.__invalid_move(
                    f"{noun} is not a valid index for current room.")
        elif action == "drop":
            try:
                self.my_player.drop_item(int(noun)-1)
                self.my_player.turns += 1
            except:
                self.__invalid_move(f"{noun} is not a valid item index.")
        elif action == "use":
            try:
                item_name = noun
                if item_name in self.my_player.items:
                    if item_name == "glasses":
                        console.print(
                            "[bold]Using glasses to find monsters![/bold]")
                        for elem in self.monster_list:
                            monster_room = elem.room.name
                            console.print(
                                f"[red]Monster in {monster_room}[/red]")
                    else:
                        self.__invalid_move(
                            f"Can't use {noun} for a use action right now")
                self.my_player.turns += 1
            except:
                self.__invalid_move()
        else:
            self.__invalid_move(f"{action} is not a valid action.")

    def play(self):
        # Write a loop to play the game.
        while True:
            move = input("-----> ").strip()
            if move == "q":
                self.end_game()
            elif move == "w":
                pass
            else:
                self.make_move(move)
            for elem in self.monster_list:
                if elem.room.name == self.my_player.room.name:
                    damage = elem.attack()
                    lived = self.my_player.defend_attack(damage)
                    if not lived:
                        self.end_game()
                elem.change_room(self.get_adjacent_room(elem.room))

    def end_game(self):
        console.print(
            f"[bold magenta]Turn: {self.my_player.turns}[/bold magenta] | [green]Points: {self.my_player.points}[/green]")
        console.print("[bold red]Goodbye.[/bold red]")
        exit()


if __name__ == "__main__":
    this_game = Game(rooms, room_list, item_list)
    this_game.play()
