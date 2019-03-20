# coding:utf-8

import random
import setup
import qlearn
import config as cfg
#import json
from Queue import Queue
reload(setup)
reload(qlearn)


def pick_random_location():
    while 1:
        x = random.randrange(world.width)
        y = random.randrange(world.height)
        cell = world.get_cell(x, y)
        if not (cell.wall or len(cell.agents) > 0):
            return cell


def pick_precise_location(x, y):
    return world.get_cell(x, y)


class Cheese(setup.Agent):
    def __init__(self):
        self.color = cfg.cheese_color
        self.reward = cfg.EAT_CHEESE

    def update(self):
        pass


class Water(setup.Agent):
    def __init__(self):
        self.color = cfg.water_color
        self.reward = cfg.DRINK_WATER

    def update(self):
        pass


class Electricity(setup.Agent):
    def __init__(self):
        self.color = cfg.electricity_color
        self.reward = cfg.ELECTRICITY

    def update(self):
        pass


class Mouse(setup.Agent):
    def __init__(self):
        self.ai = None
        self.ai = qlearn.QLearn(actions=xrange(cfg.directions), alpha=0.1, gamma=0.9, epsilon=0.1)
        self.mouseWin = 0
        self.lastState = None
        self.lastAction = None
        self.color = cfg.mouse_color
        self.pathRewards = []
        self.pathReward = 0

        print('mouse init...')

    def update(self):
        print('mouse update begin...')
        print(water.reward)
        print(water2.reward)

        state = self.calculate_state()
        reward = cfg.MOVE_REWARD

        if self.cell == cheese.cell:
            self.mouseWin += 1
            reward = cheese.reward
            self.pathRewards.append(self.pathReward + reward)
            self.pathReward = 0
            water.reward = cfg.DRINK_WATER
            self.cell = pick_precise_location(1, 1)
        elif self.cell == water.cell:
            reward = water.reward
            water.reward = cfg.MOVE_REWARD + cfg.REGRETS
        elif self.cell == water2.cell:
            reward = water2.reward
            water2.reward = cfg.MOVE_REWARD + cfg.REGRETS
        elif self.cell == electricity.cell:
            reward = electricity.reward
        elif self.cell == electricity2.cell:
            reward = electricity2.reward

        self.pathReward += reward

        if self.lastState is not None:
            self.ai.learn(self.lastState, self.lastAction, state, reward)

        # choose a new action and execute it
        action = self.ai.choose_action(state)
        self.lastState = state
        self.lastAction = action
        self.go_direction(action)

    def calculate_state(self):
        def cell_value(cell):
            if cheese.cell is not None and (cell.x == cheese.cell.x and cell.y == cheese.cell.y):
                return 2
            elif water.cell is not None and (cell.x == water.cell.x and cell.y == water.cell.y):
                return 3
            elif water2.cell is not None and (cell.x == water2.cell.x and cell.y == water2.cell.y):
                return 4
            elif electricity.cell is not None and (cell.x == electricity.cell.x and cell.y == electricity.cell.y):
                return 5
            elif electricity2.cell is not None and (cell.x == electricity2.cell.x and cell.y == electricity2.cell.y):
                return 6
            else:
                return 1 if cell.wall else 0

        dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return tuple([cell_value(world.get_relative_cell(self.cell.x + dir[0], self.cell.y + dir[1])) for dir in dirs])


if __name__ == '__main__':
    mouse = Mouse()
    cheese = Cheese()
    water = Water()
    water2 = Water()
    electricity = Electricity()
    electricity2 = Electricity()
    world = setup.World(filename='resources/world.txt')

    world.add_agent(mouse, cell=pick_precise_location(1, 1))
   #world.add_agent(cheese, cell=pick_random_location())
    world.add_agent(cheese, cell=pick_precise_location(3, 3))

    world.add_agent(water, cell=pick_random_location())
    world.add_agent(water2, cell=pick_random_location())
    world.add_agent(electricity, cell=pick_random_location())
    world.add_agent(electricity2, cell=pick_random_location())

    world.display.activate()
    world.display.speed = cfg.speed

    while 1:
        break
    for _ in range(200):
        world.update(mouse.mouseWin)
    print(mouse.ai.q)
    print(mouse.pathRewards)
    """
    name = "strat"
    with open("jsonAI/" + name + ".json", 'w') as fp:
        json.dump(mouse.ai.q, fp)
    """
