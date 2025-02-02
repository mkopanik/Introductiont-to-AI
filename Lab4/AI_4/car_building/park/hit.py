import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from skfuzzy.control import Antecedent, Consequent, Rule

from utils.control import Controller, Stage
from .model import FuzzyModel


class HitController(Controller):

    def __init__(self, tank):
        stages = [
            ForwardToFindSpace(),
            DriveCloserSecondTurn()
        ]
        super().__init__(tank, stages)


class ForwardToFindSpace(Stage):

    _model = FuzzyModel(
        max_vel=10,
        break_vel=3,
        stop_dist=1,
        break_dist=2,
        sharpness=0.3,
    )

    def control(self, tank, distances):
        velocity = self._model.get_velocity(distances.en2)
        tank.forward(velocity)
        if distances.en2 < 2:
            velocity ==0
            tank.forward(velocity)
        return velocity == 0

class DriveCloserSecondTurn(Stage):

    adj = 0.1

    diff = ctrl.Antecedent(np.linspace(0, 3, 10000), 'diff')
    vel = ctrl.Consequent(np.linspace(-1, 6, 200), 'vel')

    diff['l'] = fuzz.trapmf(diff.universe, [0, 0, 0.001, 0.01])
    diff['m'] = fuzz.trapmf(diff.universe, [0.001, 0.01, 0.09 + adj, 0.1 + adj])
    diff['h'] = fuzz.trapmf(diff.universe, [0.09 + adj, 0.1 + adj, 2, 2])

    vel['z'] = fuzz.trimf(vel.universe, [-1, 0, 1])
    vel['m'] = fuzz.trimf(vel.universe, [1, 2, 3])
    vel['h'] = fuzz.trimf(vel.universe, [4, 5, 6])

    rules = [
        ctrl.Rule(diff['l'], vel['z']),
        ctrl.Rule(diff['m'], vel['m']),
        ctrl.Rule(diff['h'], vel['h']),
    ]

    ctrl_system = ctrl.ControlSystem(rules)
    simulation = ctrl.ControlSystemSimulation(ctrl_system)

    @classmethod
    def get_velocity(cls, distance_n2):
        cls.simulation.input['diff'] = distance_n2
        cls.simulation.compute()
        velocity = cls.simulation.output['vel']
        if abs(velocity) < 0.1:
            return 0
        return velocity

    def control(self, tank, distances):
        velocity = self.get_velocity(distances.en2)
        if 6 - distances.en2 < 1:
            velocity = 0
            tank.forward(velocity)
        stop = velocity == 0
        return stop

