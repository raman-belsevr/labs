import numpy as np
from math import pi

class QuadConfig:

    def __init__(self, mass, arm_length, height, max_rpm, radius_propeller, max_thrust):
        self.mass = mass
        self.arm_length = arm_length
        self.inertia = np.array([(0.00025, 0, 2.55e-6), (0, 0.000232, 0), (2.55e-6, 0, 0.0003738)]);
        self.inv_inertia =  np.linalg.inv(self.inertia)
        self.height = height
        self.max_omega = (max_rpm / 60) * 2 * pi
        self.radius_propeller = radius_propeller
        self.max_thrust = max_thrust

        km = 1.5e-9
        kf = 6.11e-8
        r = km / kf
        L = self.arm_length
        H = self.height

        self.k_tau_current = 0.01  # torque proportionality constant
        self.k_voltage_omega = 0.01  # back EMF proportionality constant
        self.k_tau_thrust = 0.01 # tau is proportional to applied thrust
        self.k_tau_drag = 0.01 # a constant that relates torque from drag force
        self.area_propeller = 1 # area of propeller
        self.k_friction_constant = 1 # friction constant , drag force = constant * velocity

        #  [ F  ]         [ F1 ]
        #  | M1 |  = A *  | F2 |
        #  | M2 |         | F3 |
        #  [ M3 ]         [ F4 ]
        self.A = np.array([[1, 1, 1, 1],
                           [0, L, 0, -L],
                           [-L, 0, L, 0],
                           [r, -r, r, -r]])

        self.invA = np.linalg.inv(self.A)

        self.body_frame = np.array([(L, 0, 0, 1),
                                    (0, L, 0, 1),
                                    (-L, 0, 0, 1),
                                    (0, -L, 0, 1),
                                    (0, 0, 0, 1),
                                    (0, 0, H, 1)])

        self.minF = 0.0



class EnvironmentConfig:

    def __init__(self, g, rho):
        self.g = g     # acceleration due to gravity (m/s^2)
        self.rho = rho # air density (kg/m^3)
