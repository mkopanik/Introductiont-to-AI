import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from skfuzzy.control import Antecedent, Consequent, Rule

from utils.control import Controller, Stage
from .model import FuzzyModel


class ParaParkController(Controller):

    def __init__(self, tank):
        stages = [
            ForwardToFindSpace(),
            DriveCloserFirstTurn(),
            DriveCloserSecondTurn(),
            ParkFirstTurn(),
            ParkSecondTurn(),
            LastAdjustment(),
        ]
        super().__init__(tank, stages)


class ForwardToFindSpace(Stage):

    _model = FuzzyModel(
        max_vel=10,
        break_vel=3,
        stop_dist=3.7,
        break_dist=4.2,
        sharpness=0.2,
    )

    def control(self, tank, distances):
        distance = 6 - (0 if distances.se2 == 6 else distances.se2)
        velocity = self._model.get_velocity(distance)
        tank.forward(velocity)
        stop = velocity == 0
        return stop


class DriveCloserFirstTurn(Stage):

    _model = FuzzyModel(
        max_vel=5,
        break_vel=1,
        stop_dist=0.7,
        break_dist=1,
        sharpness=0.1,
    )

    #fuzz.trapmf(dist.universe, [self._stop_dist - s, self._stop_dist + s, self._break_dist - s, self._break_dist + s]) assert a <= b and b <= c and c <= d

    def control(self, tank, distances):
        distance = distances.ne2
        velocity = self._model.get_velocity(distance)
        tank.turn_left_circle(velocity)
        stop = velocity == 0
        return stop


class DriveCloserSecondTurn(Stage):

    diff = Antecedent(np.linspace(0, 2, 10000), 'diff')
    vel = Consequent(np.linspace(-1, 6, 200), 'vel')

    adj = 0.1

    diff['l'] = fuzz.trapmf(diff.universe, [0, 0, 0.001, 0.01])
    diff['m'] = fuzz.trapmf(diff.universe, [0.001, 0.01, 0.09+adj, 0.1+adj])
    diff['h'] = fuzz.trapmf(diff.universe, [0.09+adj, 0.1+adj, 2, 2])

    vel['z'] = fuzz.trimf(vel.universe, [-1, 0, 1])
    vel['m'] = fuzz.trimf(vel.universe, [1, 2, 3])
    vel['h'] = fuzz.trimf(vel.universe, [4, 5, 6])

    rules = [
        Rule(diff['l'], vel['z']),
        Rule(diff['m'], vel['m']),
        Rule(diff['h'], vel['h']),
    ]

    ctrl_system = ctrl.ControlSystem(rules)
    simulation = ctrl.ControlSystemSimulation(ctrl_system)

    @classmethod
    def get_velocity(cls, distances):
        diff = abs(distances.es2 - distances.en2)
        cls.simulation.input['diff'] = diff
        cls.simulation.compute()
        velocity = cls.simulation.output['vel']
        if abs(velocity) < 0.1:
            return 0
        return velocity

    def control(self, tank, distances):
        velocity = self.get_velocity(distances)
        tank.turn_right_circle(velocity)
        stop = velocity == 0
        return stop


class ParkFirstTurn(Stage):

    _model = FuzzyModel(
        max_vel=5,
        break_vel=3,
        stop_dist=6-4.2,
        break_dist=6-3.05,
        sharpness=0.2,
    )

    def control(self, tank, distances):
        velocity = -self._model.get_velocity(6 - distances.se2)
        tank.turn_left_circle(velocity)
        return velocity == 0


class ParkSecondTurn(Stage):

    _model = FuzzyModel(
        max_vel=20,
        break_vel=1,
        stop_dist=0.5,
        break_dist=1.3,
        sharpness=0.4,
    )

    def control(self, tank, distances):
        distance = min(distances.sw2, distances.se2)
        velocity = -self._model.get_velocity(distance-0.12)
        tank.turn_left_circle(velocity)
        if 3 - distance > 0.8:
            tank.turn_right_circle(velocity+0.3)
        return velocity == 0


class LastAdjustment(Stage):

    diff = Antecedent(np.linspace(-2, 3, 200), 'diff')
    # The division of the diff variable's universe into 200 discrete points allows the fuzzy logic system to
    # accurately and efficiently process input data, balance computational demands, and perform precise fuzzy inference and defuzzification.
    vel = Consequent(np.linspace(-4, 5, 200), 'vel')

    best = -0.7
    slope = 0.5
    speed = 1.5

    diff['l'] = fuzz.trapmf(diff.universe, [-2, -2, best - slope, best])
    diff['m'] = fuzz.trimf(diff.universe, [best - slope, best, best + slope]) # This set represents states close to the ideal condition.
    diff['h'] = fuzz.trapmf(diff.universe, [best, best + slope, 2, 2])

    vel['zero'] = fuzz.trimf(vel.universe, [-1, 0, 1])
    vel['forward'] = fuzz.trimf(vel.universe, [speed-1, speed, speed+1])
    vel['backward'] = fuzz.trimf(vel.universe, [-speed-1, -speed, -speed+1])

    rules = [
        Rule(diff['h'], vel['forward']),
        Rule(diff['l'], vel['backward']),
        Rule(diff['m'], vel['zero']),
    ]

    ctrl_system = ctrl.ControlSystem(rules)
    simulation = ctrl.ControlSystemSimulation(ctrl_system)

    @classmethod
    def get_velocity(cls, distances):
        front = min(distances.nw2, distances.ne2)
        back = min(distances.sw2, distances.se2)
        diff = front - back
        cls.simulation.input['diff'] = diff
        cls.simulation.compute()
        velocity = cls.simulation.output['vel']
        if abs(velocity) < 0.1:
            return 0
        return velocity

    def control(self, tank, distances):
        velocity = self.get_velocity(distances)

        if distances.ws2 < 3 and distances.es2 < 3:
            tank.backward(velocity)
            return False

        tank.forward(velocity)
        return velocity == 0