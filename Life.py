
"""
    Name: Caspar Grevelhörster
    Date: 27 11 2020
    Assignment name: Life
"""

from ipy_lib3 import LifeUserInterface

"""
    canvas file names must be renamed as followed:
    1: LifeInput1.txt = LifeInput1.txt
    2: LifeInput2.txt = LifeInput2.txt
    3: LifeInput3.txt = LifeInput3.txt
    4: LifeInput4.txt = Life_Stable.txt
    5: LifeInput5.txt = Life_Dies.txt
    6: LifeInput6.txt = Life_Period_02.txt
    7: LifeInput7.txt = Life_Period_14.txt
    
    after renaming, the seven files function as levels,
    they can be imported instead of starting random.
"""


class Cell:
    def __init__(self, x, y, life_state=1):
        self.life_state = life_state
        self.cell_x = x
        self.cell_y = y

    def count_alive_neighbors(self):
        counter = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbor_x = self.cell_x + i
                neighbor_y = self.cell_y + j
                if (neighbor_x in range(WINDOW_LENGTH)) and (neighbor_y in range(WINDOW_HEIGHT)):
                    if life.state.array[neighbor_y].row[neighbor_x].life_state == STATE_OF_ALIVE_CELL:
                        counter += 1
        if life.state.array[self.cell_y].row[self.cell_x].life_state == STATE_OF_ALIVE_CELL:
            counter -= 1
        return counter


class CellRow:
    def __init__(self, y, row):
        self.row = row
        self.row_y = y
        if len(self.row) == 0:
            x_value_counter = 0
            for i in range(WINDOW_LENGTH):
                self.row.append(Cell(x_value_counter, y))
                x_value_counter += 1


class State:
    def __init__(self):
        self.array = []
        y_value_counter = 0
        for i in range(WINDOW_HEIGHT):
            self.array.append(CellRow(y_value_counter, []))
            y_value_counter += 1


class LifeEngine:
    def __init__(self, ui):
        self.ui = ui
        self.state = State()
        self.past_states_binary_list = []
        self.generation_counter = 1

    def generate_next_life_state(self):
        self.past_states_binary_list.insert(0, self.current_state_to_binary())
        if len(self.past_states_binary_list) == PERIOD_FOR_OSCILLATION + 1:
            self.past_states_binary_list.pop()
        next_state = State()
        for y in range(WINDOW_HEIGHT):
            for x in range(WINDOW_LENGTH):
                old_cell = self.state.array[y].row[x]
                new_cell = next_state.array[y].row[x]
                amount_alive_neighbors = old_cell.count_alive_neighbors()
                if old_cell.life_state == STATE_OF_DEAD_CELL and amount_alive_neighbors == 3:
                    new_cell.life_state = STATE_OF_ALIVE_CELL
                elif old_cell.life_state == STATE_OF_ALIVE_CELL:
                    if 4 > amount_alive_neighbors > 1:
                        new_cell.life_state = STATE_OF_ALIVE_CELL
                    else:
                        new_cell.life_state = STATE_OF_DEAD_CELL
                else:
                    new_cell.life_state = old_cell.life_state
        self.state = next_state
        self.generation_counter += 1

    def current_state_to_binary(self):
        binary_string = ""
        for y in range(WINDOW_HEIGHT):
            for x in range(WINDOW_LENGTH):
                binary_string += str(self.state.array[y].row[x].life_state)
        return binary_string

    def check_oscillation(self):
        for binary_state in self.past_states_binary_list:
            if self.current_state_to_binary() == binary_state:
                oscillation_level = self.past_states_binary_list.index(binary_state) + 1
                return oscillation_level


# cell constants
STATE_OF_DEAD_CELL = 1
STATE_OF_ALIVE_CELL = 2

# game constants
WINDOW_LENGTH = 9
WINDOW_HEIGHT = 9
MAX_GENERATIONS = 100
PERIOD_FOR_OSCILLATION = 100
FPS = 2

life = LifeEngine(LifeUserInterface(WINDOW_LENGTH, WINDOW_HEIGHT))


def main():
    life.ui.print_(
        "You don't want to import a file? Press 0\nWhich level do you want to play? Press a number from 1 to 7"
    )

    while True:
        key_input = life.ui.get_event()
        if key_input.name == "number":
            level_number = int(key_input.data)

            if level_number in range(1, 8):
                create_level(level_number)
                break

            elif level_number == 0:
                life.ui.clear_text()
                for y in range(WINDOW_HEIGHT):
                    for x in range(WINDOW_LENGTH):
                        life.state.array[y].row[x].life_state = life.ui.random(2) + 1
                break

    life.ui.clear_text()
    life.ui.print_(
        f"Do you want to manually click or have {FPS} fps?\n0 for manual\n1 for auto"
    )

    while True:
        key_input = life.ui.get_event()
        if key_input.name == "number":
            if key_input.data == "1":
                life.ui.set_animation_speed(FPS)
                life.ui.clear_text()
                life.generation_counter = 0
                break
            elif key_input.data == "0":
                life.ui.set_animation_speed(0)
                life.ui.clear_text()
                life.ui.print_("#####GAME PREPARED######\nPress space bar to go to first generation")
                life.generation_counter = 0
                break

    while True:
        process_event(life.ui.get_event())
        life.ui.clear_text()
        life.ui.print_("Press space bar to go to next generation")


def draw_screen():
    for y in range(WINDOW_HEIGHT):
        for x in range(WINDOW_LENGTH):
            life_state_of_cell = life.state.array[y].row[x].life_state
            life.ui.place(x, y, life_state_of_cell)
    life.ui.show()


def process_event(event):
    if event.name == "alarm" or event.data == "space":
        life.ui.clear()
        oscillation_counter = life.check_oscillation()
        if life.generation_counter == MAX_GENERATIONS:
            end_game("limit of generations reached.")

        elif str(STATE_OF_ALIVE_CELL) not in life.current_state_to_binary():
            draw_screen()
            end_game("there are no more cells alive.")

        elif oscillation_counter is not None:
            if oscillation_counter == 1:
                end_game("still figure was detected.")
            else:
                draw_screen()
                end_game(f"oscillator with period {oscillation_counter} detected.")
        draw_screen()
        life.generate_next_life_state()


def create_level(desired_level):
    global MAX_GENERATIONS, PERIOD_FOR_OSCILLATION

    required_file_name = f"LifeInput{desired_level}.txt"
    with open(required_file_name) as file:
        all_lines = [line.rstrip("\n") for line in file.readlines()]

    MAX_GENERATIONS = int(all_lines.pop(0))
    PERIOD_FOR_OSCILLATION = int(all_lines.pop(0))

    life.state = State()
    for y in range(WINDOW_HEIGHT):
        for x in range(WINDOW_LENGTH):
            if all_lines[y][x] == "x":
                life.state.array[y].row[x].life_state = STATE_OF_ALIVE_CELL


def end_game(reason):
    life.ui.clear()
    life.ui.clear_text()
    life.ui.print_(f"game ended because {reason}\n")

    life.ui.print_("wanna have another go? \nIf yes, press 0\nelse: press 1")
    while True:
        if life.ui.get_event().data == "0":
            life.ui.clear()
            life.ui.clear_text()
            life.ui.show()
            main()
        elif life.ui.get_event().data == "1":
            life.ui.close()


if __name__ == "__main__":
    main()
