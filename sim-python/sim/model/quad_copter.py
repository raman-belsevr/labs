import numpy as np
from sim.physics.utils import utils as algebra_utils

class QuadCopter:

    def __init__(self, quad_config):
        self.quad_config = quad_config
        self.quad_state = QuadState(np.zeros(3), np.zeros(3))


class QuadStateDot:

    def __init__(self,  position_dot, velocity_dot, quat_dot, angular_velocity_dot):
        self.position_dot = position_dot
        self.velocity_dot = velocity_dot
        self.quat_dot  = quat_dot
        self.angular_velocity_dot = angular_velocity_dot


class QuadState:
    """ Quadcopter class

                state  - 1 dimensional vector but used as 13 x 1. [x, y, z, xd, yd, zd, qw, qx, qy, qz, p, q, r]
                         where [qw, qx, qy, qz] is quternion and [p, q, r] are angular velocity [roll_dot, pitch_dot, yaw_dot]
                F      - 1 x 1, thrust output from controller
                M      - 3 x 1, moments output from controller
                params - system parameters struct, arm_length, g, mass, etc.
                """

    def __init__(self, pos, attitude):
        """ pos      = [x,y,z]
            attitude = [rool,pitch,yaw]
        """

        # position vector of the quad copter in 3d space
        self.position = pos

        # orientation in 3d space, (roll, pitch, yaw) and equivalent representation in quaternion
        self.attitude = attitude
        roll, pitch, yaw = attitude
        self.quat = QuadState.rpy_to_quat(roll, pitch, yaw)

        # velocity vector components in the axis
        self.velocity = np.zeros(3)

        # angular velocity vector (omega)
        self.angular_velocity = np.zeros(3)

    def position(self):
        return self.position

    def velocity(self):
        return self.velocity

    def attitude(self):
        rot = self.quat.as_rotation_matrix()
        return algebra_utils.RotToRPY(rot)

    def omega(self):
        return self.angular_velocity

    def quaternion(self):
        return self.quat


    @staticmethod
    def rpy_to_quat(roll, pitch, yaw):
        rot = algebra_utils.RPYToRot(roll, pitch, yaw)
        quat = algebra_utils.RotToQuat(rot)
        return quat

    """
    def update(self, dt, F, M):
        # limit thrust and Moment
        L = params.arm_length
        r = params.r
        prop_thrusts = params.invA.dot(np.r_[np.array([[F]]), M])
        prop_thrusts_clamped = np.maximum(np.minimum(prop_thrusts, params.maxF / 4), params.minF / 4)
        F = np.sum(prop_thrusts_clamped)
        M = params.A[1:].dot(prop_thrusts_clamped)
        self.state = integrate.odeint(self.state_dot, self.state, [0, dt], args=(F, M))[1]
    """

