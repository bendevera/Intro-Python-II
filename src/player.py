from room import Room 
from rich.console import Console

console = Console()


class Player:
    def __init__(self, name: str, room: Room):
        self.name = name
        self.health = 100
        self.points = 0
        self.turns = 0
        self.visited = {}
        self.items = [None, None, None]
        self.change_room(room)
        self.__help()
        self.room.show_data()

    def __help(self):
        console.print("[bold cyan]Welcome to a python adventure.[/bold cyan]")
        console.print("Moves consist of an [u]action[/u] and [u]noun[/u].")
        console.print("Actions: [green]run[/green], [green]check[/green], [green]grab[/green]")
        console.print("Nouns: [i]n[/i], [i]s[/i], [i]e[/i], [i]w[/i]")
        print("\n\n")
    
    def __invalid_move(self, details=""):
        console.print(f"[red]Invalid move. {details} Try again.[/red]")
        print("\n")
    
    def make_move(self, move: str):
        move_pieces = move.split(" ")
        if len(move_pieces) == 2:
            self.process_move(move_pieces[0], move_pieces[1])
        else:
            self.__invalid_move("Move must consist of 2 parts seperated by a space.")
        
        console.print(f"[bold magenta]Turn: {self.turns}[/bold magenta] | [bold blue]Points: {self.points}[/bold blue] | [bold green]Health: {self.health}[/bold green]")
        print()
        console.print("Current room:")
        self.room.show_data()
    
    def process_move(self, action: str, noun: str):
        if action == "run":
            can_move = self.room.is_room(noun)
            if can_move:
                self.change_room(self.room.get_room(noun))
                self.turns += 1
            else:
                self.__invalid_move(f"Can't move {noun} of current room.")
        elif action == "check":
            if noun == "i":
                self.show_items()
            else:
                is_room = self.room.is_room(noun)
                if is_room:
                    room = self.room.get_room(noun)
                    room.show_preview()
                else:
                    self.__invalid_move(f"No room {noun} of current room.")
        elif action == "grab":
            try:
                self.grab_item(int(noun)-1)
                self.turns += 1
            except Exception as e:
                self.__invalid_move(f"{noun} is not a valid index for current room.")
        elif action == "drop":
            try:
                self.drop_item(int(noun)-1)
                self.turns += 1
            except:
                self.__invalid_move(f"{noun} is not a valid item index.")
        else:
            self.__invalid_move(f"{action} is not a valid action.")

    def change_room(self, room: Room):
        self.room = room
        if room.name not in self.visited:
            self.visited[room.name] = True
            self.points += room.visit_points
    
    def show_items(self):
        console.print(f"[bold magenta]1. {self.items[0]} | 2. {self.items[1]} | 3. {self.items[2]}[/bold magenta]")
        print("\n")
    
    def grab_item(self, item_index: int):
        item = self.room.items.pop(item_index)
        self.set_item(item)
    
    def set_item(self, item_name: str):
        item_set = False 
        for i in range(len(self.items)):
            if self.items[i] is None:
                self.items[i] = item_name
                item_set = True
                break
        if not item_set:
            dropped_item = int(input("Inventory Full. Item to drop (1-3): "))
            self.drop_item(dropped_item - 1)
        print("New inventory:")
        self.show_items()
    
    def drop_item(self, item_index):
        self.room.items.append(self.items[item_index])
        self.items[item_index] = None
    
    def take_damage(self, damage: int):
        console.print("Hit by monster!!")
        if "sword" in self.items:
            console.print(f"[red]Loosing {damage * .5} health[red].")
            self.health -= damage * .5
        else:
            console.print(f"[red]Loosing {damage} health[red].")
            self.health -= damage
        if self.health < 0:
            console.print("[bold red]Took too much damage![/bold red]")
            self.end_game()
    
    def end_game(self):
        console.print(f"[bold magenta]Turn: {self.turns}[/bold magenta] | [green]Points: {self.points}[/green]")
        console.print("[bold red]Goodbye.[/bold red]")
        exit()