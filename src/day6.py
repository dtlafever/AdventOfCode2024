import re
from enum import Enum
from pydantic import BaseModel, Field

GUARD_RE_EXP = r"(\^|\>|\<|v)"
OBSTRUCTION = "#"
EMPTY_SPACE = "."
OFF_GRID    = "&"

class SpaceEnum(Enum):
    empty = "."
    obstruction = "#"
    off = "&"

class DirectionEnum(Enum):
    up = "^"
    down = "v"
    left = "<"
    right = ">"

class Space(BaseModel):
    x: int
    y: int
    character: SpaceEnum

class Orientation(BaseModel):
    x: int
    y: int
    direction: DirectionEnum

    def __str__(self):
        return f"x={self.x}y={self.y}c={self.direction.value}"

    def get_x_y_str(self) -> str:
        return f"x={self.x}y={self.y}"

    # def __eq__(self, other) -> bool:
    #     return self.x == other.x and self.y == other.y and self.direction == other.direction

    def get_next_direction(self) -> DirectionEnum:
        if self.direction == DirectionEnum.up:
            return DirectionEnum.right
        elif self.direction == DirectionEnum.right:
            return DirectionEnum.down
        elif self.direction == DirectionEnum.down:
            return DirectionEnum.left
        elif self.direction == DirectionEnum.left:
            return DirectionEnum.up

class Grid(BaseModel):
    board: list[list[str]]
    size_x: int
    size_y: int

    def update_at_location(self, x: int, y: int, character: str):
        self.board[y][x] = character

class Game(BaseModel):
    grid: Grid
    guard: Orientation

    def is_out_of_bounds(self, new_x: int, new_y: int) -> bool:
        if (new_x < 0 or
            new_x >= self.grid.size_x or
            new_y < 0 or
            new_y >= self.grid.size_y):
            return True
        return False

    def get_incoming_space(self) -> Space:
        # defaults to OFF_GRID character incase the guard walks off the grid
        next_space = Space(x=-1, y=-1, character=SpaceEnum.off)

        new_x = self.guard.x
        new_y = self.guard.y
        if self.guard.direction == DirectionEnum.up:
            new_y -= 1
        elif self.guard.direction == DirectionEnum.down:
            new_y += 1
        elif self.guard.direction == DirectionEnum.left:
            new_x -= 1
        elif self.guard.direction == DirectionEnum.right:
            new_x += 1

        if not self.is_out_of_bounds(new_x, new_y):
            next_space.character = SpaceEnum(self.grid.board[new_y][new_x])
            next_space.x = new_x
            next_space.y = new_y
        return next_space

    def traverse_grid(self):
        visited_orientations: list[str] = [] # for tracking loops to end early
        visited_spaces: set[str] = set(self.guard.get_x_y_str()) # for tracking unique visited places
        is_traversal_complete: bool = False

        while not is_traversal_complete:
            if str(self.guard) in visited_orientations:
                # we have already traversed here with this specific orientation, so we are in a loop.
                is_traversal_complete = True
                break

            visited_orientations.append(self.guard)
            next_space = self.get_incoming_space()
            if next_space.character == SpaceEnum.obstruction:
                # invalid next location, rotate
                self.guard.direction = self.guard.get_next_direction()

                # update the grid to rotate the guard
                self.grid.update_at_location(self.guard.x, self.guard.y, self.guard.direction.value)
            elif next_space.character == SpaceEnum.off:
                # we are off the grid, stop traversing
                is_traversal_complete = True
            elif next_space.character == SpaceEnum.empty:
                # update the grid to remove the guard from the current location
                self.grid.update_at_location(self.guard.x, self.guard.y, SpaceEnum.empty.value)

                # valid next location, move guard to that new space
                self.guard.x = next_space.x
                self.guard.y = next_space.y

                # update the grid to move the guard
                self.grid.update_at_location(next_space.x, next_space.y, self.guard.direction.value)

                visited_spaces.add(self.guard.get_x_y_str())

        # HACK: there is some weird stuff happening where the string representation of visited locations
        # gets split up into single character strings
        hack_bad_visit_counts = 0
        for ele in visited_spaces:
                if len(ele) < 2:
                    hack_bad_visit_counts += 1
        return len(visited_spaces) - hack_bad_visit_counts

def puzzle1():

    guard = Orientation(x=-1,y=-1, direction=DirectionEnum.up)

    grid_list = []
    grid_size_x = 0
    grid_size_y = 0
    with open("../data/input6.txt", "r") as f:
        for line in f:
            stripped_line = list(line.strip())
            stripped_line.append(EMPTY_SPACE) # add extra space to grid for later bounds check
            if grid_size_x == 0:
                # x has not been set, lets do that now
                grid_size_x = len(stripped_line)

            grid_list.append(stripped_line)
            grid_size_y += 1

            # find guard and set position and direction
            if guard.x == -1 or guard.y == -1:
                guard_match = re.search(GUARD_RE_EXP, line.strip())
                if guard_match is not None:
                    guard.x = guard_match.start()
                    guard.y = grid_size_y - 1 # minus 1 for 0 indexed
                    guard.direction = DirectionEnum(guard_match[0])
    # traverse grid

    grid = Grid(board=grid_list, size_x=grid_size_x, size_y=grid_size_y)
    # for row in grid.board:
    #     print(row)

    game = Game(grid=grid, guard=guard)
    total_visited_spaces = game.traverse_grid()

    print(f"Total Visited Spaces: {total_visited_spaces}")


def puzzle2():
    pass

def main():
    puzzle1()
    puzzle2()

if __name__ == "__main__":
    main()
    # 5398 too high
    # 4904 too high