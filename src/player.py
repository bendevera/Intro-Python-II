from room import Room
from rich.console import Console
import random

console = Console()


class Player:
    def __init__(self, name: str, room: Room):
        self.name = name
        self.health = 100
        self.power = 0
        self.points = 0
        self.turns = 0
        self.visited = {}
        self.items = [None, None, None]
        self.change_room(room)
        self.room.show_data()

    def change_room(self, room: Room):
        self.room = room
        if room.name not in self.visited:
            self.visited[room.name] = True
            self.points += room.visit_points
        else:
            self.points += int(room.visit_points * .25)

    def show_items(self):
        console.print(
            f"[bold magenta]1. {self.items[0]} | 2. {self.items[1]} | 3. {self.items[2]}[/bold magenta]")
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
        console.print(f"[red]Loosing {damage} health[red].")
        self.health -= damage
        if self.health <= 0:
            console.print("[bold red]Took too much damage![/bold red]")
            return False
        return True

    def defend_attack(self, damage: int):
        if "sword" in self.items or "hatchet" in self.items:
            damage = int(damage / 2)
        console.print(f"[red]MONSTER ATTACK[red].")
        answer = random.randint(1, 6)
        while True:
            try:
                guess = int(input(f"Guess 1-6 to avoid {damage} damage: "))
                break
            except:
                console.print("Incorrect input, try again.")
        console.print(f"{answer} [red]vs.[/red] {guess}")
        if answer != guess:
            lived = self.take_damage(damage)
            return lived
        else:
            console.print(f"[green]Success![green] Avoided attack.")
            return True
