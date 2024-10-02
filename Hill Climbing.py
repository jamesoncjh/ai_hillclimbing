import random
import time

class State:
    def __init__(self):
        self.table = [[0, 0, 0] for _ in range(3)]

    def is_valid(self, x, y):
        return 0 <= x <= 2 and 0 <= y <= 2

    def swap(self, a, b):
        a, b = b, a

    def manhattan_distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


    def heuristic(self, final):
        misplaced_count = 0

        for i in range(3):
            for j in range(3):
                if self.table[i][j] != 0 and self.table[i][j] != final.table[i][j]:
                    misplaced_count += 1

        return misplaced_count


    def generate_neighbours(self):
        neighbours = []
        params = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        x, y = None, None

        for i in range(3):
            for j in range(3):
                if self.table[i][j] == 0:
                    x, y = i, j

        for param in params:
            newx, newy = x + param[0], y + param[1]
            if not self.is_valid(newx, newy):
                continue

            temp = State()
            temp.table = [row[:] for row in self.table]
            temp.table[newx][newy], temp.table[x][y] = temp.table[x][y], temp.table[newx][newy]
            neighbours.append(temp)

        return neighbours

    def display(self):
        print()
        for row in self.table:
            print(" ".join(map(str, row)))

def hill_climb(initial, final, path=[], move_counter=1, max_moves=100):
    start_time = time.perf_counter()

    initial.display()
    best = initial.heuristic(final)

    if best == 0:
        print("\nThe final state has been reached.")
        print("Path taken:")
        for state, move, heuristic_value in path:
            print(f"Move {move}")
            state.display()
            print(f"Heuristic Value: {heuristic_value}")

        end_time = time.perf_counter()
        print(f"\nTime taken: {end_time - start_time:.8f} seconds")

        return

    neighbours = initial.generate_neighbours()

    print("\nPossible moves:")
    for idx, neighbour in enumerate(neighbours, start=1):
        curr = neighbour.heuristic(final)
        print(f"Move {idx}")
        neighbour.display()
        print(f"Heuristic Value: {curr}")

    # Choose the move with the best heuristic value
    next_state = min(neighbours, key=lambda x: x.heuristic(final))
    best_move_index = neighbours.index(next_state) + 1

    if next_state.table == initial.table or move_counter >= max_moves:
        print("Stuck at a local minimum or reached maximum moves! Could not find any further path.")
        end_time = time.perf_counter()
        print(f"\nTime taken: {end_time - start_time:.8f} seconds")
        return

    print(f"\nStep {move_counter} (System Choose Move {best_move_index}):")
    next_state.display()
    print("Heuristic Value:", next_state.heuristic(final))

    path.append((next_state, move_counter, next_state.heuristic(final)))
    hill_climb(next_state, final, path, move_counter + 1, max_moves)






def is_valid_input(input_values):
    return len(input_values) == 9 and all(0 <= val <= 8 for val in input_values)

def main():
    print("------------------------------------------------------------------------------------------------------------------")
    print("Hill climbing is an optimization algorithm that starts at a random point and moves iteratively towards the")
    print("direction of increasing (or decreasing) function values. The method goes to the neighbour with the")
    print("greatest (or lowest) value at each step, after evaluating the current print solution and its neighbours.")
    print("------------------------------------------------------------------------------------------------------------------")

    is_retry = True

    while is_retry:
        input_values = []
        while True:
            input_line = input("Enter the initial state (use 0 for empty tile and separate each value with a space):\n")
            input_values = list(map(int, input_line.split()))

            if is_valid_input(input_values):
                break
            else:
                print("Invalid input. Please enter exactly 9 integers on a single line separated by space.")
                input_values = []

        initial = State()
        for i in range(3):
            for j in range(3):
                initial.table[i][j] = input_values[3 * i + j]

        is_correct = False
        while not is_correct:
            print("\nInitial state:")
            initial.display()
            select = input("Is this the correct initial state? (y/n): ").lower()

            if select == 'y':
                is_correct = True
            elif select == 'n':
                input_values.clear()
                while True:
                    input_line = input("Please enter the correct initial state:\n")
                    input_values = list(map(int, input_line.split()))
                    if is_valid_input(input_values):
                        break
                    else:
                        print("Invalid input. Please enter exactly 9 integers on a single line separated by space.")
                        input_values = []

                for i in range(3):
                    for j in range(3):
                        initial.table[i][j] = input_values[3 * i + j]
            else:
                print("Invalid input. Please enter either 'y' or 'n'.")

        input_values.clear()
        while True:
            input_line = input("Enter the goal state (use 0 for empty tile and separate each value with a space):\n")
            input_values = list(map(int, input_line.split()))

            if is_valid_input(input_values):
                break
            else:
                print("Invalid input. Please enter exactly 9 integers on a single line separated by space.")
                input_values = []

        final = State()
        for i in range(3):
            for j in range(3):
                final.table[i][j] = input_values[3 * i + j]

        is_correct_goal = False
        while not is_correct_goal:
            print("\nGoal state:")
            final.display()
            select = input("Is this the correct goal state? (y/n): ").lower()

            if select == 'y':
                is_correct_goal = True
            elif select == 'n':
                input_values.clear()
                while True:
                    input_line = input("Please enter the correct goal state:\n")
                    input_values = list(map(int, input_line.split()))
                    if is_valid_input(input_values):
                        break
                    else:
                        print("Invalid input. Please enter exactly 9 integers on a single line separated by space.")
                        input_values = []

                for i in range(3):
                    for j in range(3):
                        final.table[i][j] = input_values[3 * i + j]
            else:
                print("Invalid input. Please enter either 'y' or 'n'.")

        print("\nThe path is:")
        hill_climb(initial, final)

        choice = input("Do you want to run the program again? (y/n): ").lower()
        if choice == 'n':
            is_retry = False

if __name__ == "__main__":
    main()
