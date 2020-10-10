import random

simple_directions = {'UP', 'DOWN', 'LEFT', 'RIGHT'}
# nots = ['', 'NOT', 'NOT NOT', 'NOT NOT NOT']

class Direction:

    def __init__(self, difficulty=0):
        self.difficulty = difficulty
        self.target_direction = None

    def pick_direction(self):
        self.num_nots = random.randint(0, self.difficulty) % 4
        nots = 'NOT ' * self.num_nots
        direction = random.choice(list(simple_directions))
        self.target_direction = nots + direction

    def correct_direction(self, input_dir):
        components = self.target_direction.split(' ')
        *prefix_nots, direction = components

        if self.num_nots % 2 == 0:
            return input_dir == direction
        else:
            return input_dir in simple_directions - {direction}

    def __str__(self):
        return f'Target Direction: {self.target_direction}'


if __name__ == '__main__':
    direction = Direction(difficulty=3)

    for i in range(20):
        direction.pick_direction()
        print(direction.target_direction)
        print('-' * len(direction.target_direction))

        print('UP:', direction.correct_direction('UP'))
        print('DOWN:', direction.correct_direction('DOWN'))
        print('LEFT:', direction.correct_direction('LEFT'))
        print('RIGHT:', direction.correct_direction('RIGHT'))

        print()
