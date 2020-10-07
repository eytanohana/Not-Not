import random

simple_directions = {'UP', 'DOWN', 'LEFT', 'RIGHT'}
nots = ['', 'NOT', 'NOT NOT', 'NOT NOT NOT']

class Direction:

    def __init__(self, random_seed=42):
        self.random_seed = random_seed
        self.direction = None
        random.seed(random_seed)

    def pick_direction(self):
        num_nots = random.choice(nots)
        direction = random.choice(simple_directions)
        self.target_direction = num_nots + direction

    def correct_direction(self, input_dir, target_dir):
        components = target_dir.split(' ')

        *prefix_nots, dir = components
        print(prefix_nots, dir)

if __name__ == '__main__':
    direction = Direction()


    direction.correct_direction('RIGHT', 'RIGHT')
    direction.correct_direction('RIGHT', 'NOT RIGHT')
    direction.correct_direction('RIGHT', 'NOT NOT RIGHT')
    direction.correct_direction('RIGHT', 'NOT NOT NOT RIGHT')
