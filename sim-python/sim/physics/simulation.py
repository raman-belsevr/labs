from sim.physics.utils.quaternion import Quaternion
import numpy as np
from sim.model.quad_copter import QuadStateDot
import scipy.integrate as integrate


class Simulation:

    def __init__(self, quadcopter, environment):
        self.quad = quadcopter
        self.env = environment


    def state_dot(self, t, F, M):
        quat = self.quad.quad_state.quat
        (qw, qx, qy, qz) = quat

        (omega_x, omega_y, omega_z) = self.quad.quad_state.angular_velocity

        bRw = Quaternion(quat).as_rotation_matrix()  # world to body rotation matrix
        wRb = bRw.T  # orthogonal matrix inverse = transpose

        # acceleration - Newton's second law of motion
        accel = 1.0 / self.quad_config.mass * (wRb.dot(np.array([[0, 0, F]]).T)
                                     - np.array([[0, 0, self.quad.quad_config.mass * self.env.g]]).T)
        # angular velocity - using quternion
        # http://www.euclideanspace.com/physics/kinematics/angularvelocity/
        K_quat = 2.0;  # this enforces the magnitude 1 constraint for the quaternion
        quaterror = 1.0 - (qw ** 2 + qx ** 2 + qy ** 2 + qz ** 2)
        qdot = (-1.0 / 2) * np.array([[0, -omega_x, -omega_y, -omega_z],
                                      [omega_x, 0, -omega_z, omega_y],
                                      [omega_y, omega_z, 0, -omega_x],
                                      [omega_z, -omega_y, omega_x, 0]]).dot(quat) + K_quat * quaterror * quat;

        # angular acceleration - Euler's equation of motion
        # https://en.wikipedia.org/wiki/Euler%27s_equations_(rigid_body_dynamics)
        omega = np.array([omega_x, omega_y, omega_z])
        I = self.quad.quad_config.inertia
        I_inverse = self.quad.quad_config.inv_inertia
        angular_acceration = I_inverse.dot(M.flatten() - np.cross(omega, I.dot(omega)))

        position_dot = self.quad.quad_state.velocity()
        velocity_dot = (accel[0], accel[1], accel[2])
        angular_velocity_dot = (angular_acceration[0], angular_acceration[1], angular_acceration[2])
        quad_state_dot = QuadStateDot(position_dot, velocity_dot, qdot, angular_velocity_dot)

        return quad_state_dot

    def update(self, dt, F, M):
        # limit thrust and Moment
        quad_config = self.quad.quad_config
        L = quad_config.arm_length
        r = quad_config.r
        prop_thrusts = quad_config.invA.dot(np.r_[np.array([[F]]), M])
        prop_thrusts_clamped = np.maximum(np.minimum(prop_thrusts, 2 * quad_config.mass * self.env.g/ 4), quad_config.minF / 4)
        F = np.sum(prop_thrusts_clamped)
        M = quad_config.A[1:].dot(prop_thrusts_clamped)
        self.quad.quad_state = integrate.odeint(self.state_dot, self.state, [0, dt], args=(F, M))[1]

    def apply_thrust(self, T):
        # convert the applied thrust into total Torque (Moments) and
        # compute its effect on linear and angular acceleration
        pass
