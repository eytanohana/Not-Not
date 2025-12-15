import random

simple_directions = {'UP', 'DOWN', 'LEFT', 'RIGHT'}
set_ops = {'AND', 'OR', ''}


class Direction:
    def __init__(self, difficulty=0):
        self.difficulty = difficulty
        self.target_direction = None

    def pick_direction(self):
        if self.difficulty > 3:
            self.num_nots1 = random.randint(0, self.difficulty) % 3
            self.num_nots2 = random.randint(0, self.difficulty) % 3

        else:
            self.num_nots1 = random.randint(0, self.difficulty)
            self.num_nots2 = random.randint(0, self.difficulty)

        nots = 'NOT ' * self.num_nots1
        and_or = random.choice(list(set_ops))
        direction = nots + random.choice(list(simple_directions))
        self.target_direction = direction
        _, actual_directions = self.correct_direction(direction, return_dirs=True)

        if and_or == 'AND':
            pass

    def correct_direction(self, input_dir, return_dirs=False):
        components = self.target_direction.split(' ')
        *prefix_nots, direction = components

        if self.num_nots1 % 2 == 0:
            if return_dirs:
                return input_dir == direction, set(direction)
            return input_dir == direction
        else:
            if return_dirs:
                return input_dir in simple_directions - {direction}, simple_directions - {direction}
            return input_dir in simple_directions - {direction}

    def __str__(self):
        return f'{self.target_direction}'


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
