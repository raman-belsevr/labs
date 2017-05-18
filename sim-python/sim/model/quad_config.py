import numpy as np

class QuadConfig:

    def __init__(self, mass, arm_length, height):
        self.mass = mass
        self.arm_length = arm_length
        self.inertia = np.array([(0.00025, 0, 2.55e-6), (0, 0.000232, 0), (2.55e-6, 0, 0.0003738)]);
        self.inv_inertia =  np.linalg.inv(self.inertia)
        self.height = height

        km = 1.5e-9
        kf = 6.11e-8
        self.r = km / kf
        L = self.arm_length
        H = self.height

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
