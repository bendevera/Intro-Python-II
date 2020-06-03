from rich.console import Console

console = Console()


class Room:
    def __init__(self, name, description, visit_points, items):
        self.name = name
        self.description = description
        self.visit_points = visit_points
        self.items = items
        self.link_rooms()

    def link_rooms(self, n=None, s=None, e=None, w=None):
        self.n_to = n
        self.s_to = s
        self.e_to = e
        self.w_to = w

    def is_room(self, direction):
        if direction == "n":
            if self.n_to is not None:
                return True
        elif direction == "s":
            if self.s_to is not None:
                return True
        elif direction == "w":
            if self.w_to is not None:
                return True
        elif direction == "e":
            if self.e_to is not None:
                return True
        return False

    def get_room(self, direction):
        if direction == "n":
            return self.n_to
        elif direction == "s":
            return self.s_to
        elif direction == "w":
            return self.w_to
        elif direction == "e":
            return self.e_to
        return None

    def show_preview(self):
        console.print(f"[bold]{self.name}[/bold]", justify="center")
        console.print(f"-> {self.description}", style="white on black")
        print()

    def show_data(self):
        self.show_preview()
        if len(self.items) > 0:
            console.print("[magenta]Items:[/magenta]")
            console.print(
                " ".join([str(num+1)+". "+item for num,
                          item in enumerate(self.items)]),
                justify="center")
        n = None if self.n_to is None else self.n_to.name
        s = None if self.s_to is None else self.s_to.name
        w = None if self.w_to is None else self.w_to.name
        e = None if self.e_to is None else self.e_to.name
        console.print(f"N: {n}", justify="center")
        console.print(f"E: {e}", justify="right")
        console.print(f"W: {w}", justify="left")
        console.print(f"S: {s}", justify="center")
        print("\n")
