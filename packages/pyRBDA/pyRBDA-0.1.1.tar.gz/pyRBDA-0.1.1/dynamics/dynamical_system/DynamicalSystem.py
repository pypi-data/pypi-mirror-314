import numpy as np
import casadi as ca

from spatial.jcalc import jcalc
from spatial.plnr import plnr
from spatial.rotz import rotz
from spatial.xlt import xlt
from spatial.pluho import pluho


class DynamicalSystem:
    def __init__(self, model):
        """
        Initialize the DynamicalSystem class.

        Parameters:
            model: A function handle that returns the robot structure.
        """
        robot_structure = model()

        self.Model = robot_structure
        self.Name = robot_structure['name']
        del self.Model['name']

        self.add_states()
        self.add_inputs()

        self.Gravity = robot_structure['gravity']
        del self.Model['gravity']

        self.InputMap = robot_structure['B']
        del self.Model['B']

        self.HTransforms = self.homogeneous_transforms()
        self.BodyPositions = self.get_body_positions()
        self.BodyVelocities = self.get_body_velocities()
        self.Dynamics = self.continuous_dynamics()

    def add_states(self):
        # Implementation for adding states
        """
        Add states to the DynamicalSystem object.
        """
        states = {}

        states['q'] = self.Model['q']
        states['dq'] = self.Model['qd']
        states['ddq'] = self.Model['qdd']

        states['q'].ID = 'pos'
        states['dq'].ID = 'vel'
        states['ddq'].ID = 'acc'

        self.States = states

        del self.Model['q']
        del self.Model['qd']
        del self.Model['qdd']

    def add_inputs(self):
        # Implementation for adding inputs
        """
        Add inputs to the DynamicalSystem object.
        """
        control = {}

        control['u'] = self.Model['u']
        control['u'].ID = 'input'

        self.Inputs = control

        del self.Model['u']

    def homogeneous_transforms(self):
        """
        Calculate homogeneous transforms.

        Parameters:
            self: Instance of DynamicalSystem

        Returns:
            T: List of homogeneous transforms
        """
        model = self.Model
        q = self.States['q'].sym
        Xtree = model['Xtree']

        Xa = {}
        T = []

        for i in range(model['nd']):
            XJ, _ = jcalc(model['jtype'][i], q[i])
            Xa[i] = XJ @ Xtree[i]
            if model['parent'][i] != 0:
                Xa[i] = Xa[i] @ Xa[model['parent'][i]]

            if Xa[i].shape[0] == 3:  # Xa[i] is a planar coordinate transform
                theta, r = plnr(Xa[i])
                X = rotz(theta) @ xlt(np.append(r, 0))
                T.append(pluho(X))
            else:
                T.append(pluho(Xa[i]))

        return T

    def get_body_positions(self):
        """
        Calculate the body positions.

        Parameters:
            self: Instance of DynamicalSystem

        Returns:
            pos_body: List of body positions
        """
        model = self.Model
        nd = model['nd']

        T = self.HTransforms
        pos_body = []

        for i in range(nd):
            T_i = T[i]
            R_i = T_i[:3, :3].T
            p_i = -R_i @ T_i[:3, 3]

            T_next = np.vstack(
                (np.hstack((R_i, p_i.reshape(-1, 1))), [0, 0, 0, 1]))
            p_next = T_next @ np.append(model['body_length']
                                        [i] * model['body_axis'][i], 1)

            pos_body.append((p_i, p_next[:3]))

        return pos_body

    def get_body_velocities(self):
        """
        Calculate the body velocities.

        Parameters:
            self: Instance of DynamicalSystem

        Returns:
            vel_body: List of body velocities
        """
        model = self.Model
        nd = model['nd']

        vel_body = []

        for i in range(nd):
            Jac_1 = ca.jacobian(self.BodyPositions[i][0], self.States.q.sym)
            Jac_2 = ca.jacobian(self.BodyPositions[i][1], self.States.q.sym)

            vel_1 = Jac_1 @ self.States.dq.sym
            vel_2 = Jac_2 @ self.States.dq.sym

            vel_body.append((vel_1, vel_2))

        return vel_body

    def continuous_dynamics(self):
        # Implementation for continuous dynamics
        pass
