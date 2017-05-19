from sim.physics.utils.quaternion import Quaternion
import numpy as np
from sim.model.quad_copter import QuadStateDot
import scipy.integrate as integrate


class Simulation:

    def __init__(self, quadcopter, environment):
        self.quad = quadcopter
        self.env = environment

        kv = quadcopter.quad_config.k_voltage_omega # back EMF proportionality constant
        kt = quadcopter.quad_config.k_tau_current # torque proportionality constant
        k_tau = quadcopter.quad_config.k_tau_thrust  # tau is proportional to applied thrust
        rp  =  self.quad.quad_config.radius_propeller
        ap  =  self.quad.quad_config.area_propeller

        area_propeller = quadcopter.quad_config.area_propeller
        self.k_thrust_omega = (((kv * k_tau) / kt) ** 2) * 2 * self.env.rho * area_propeller
        self.k_drag = 0.5 * (rp ** 3) * self.quad.quad_config.k_tau_drag * ap



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

    def apply_thrust(self, thrust_pilot, dt):
        # convert the applied thrust into total Torque (Moments) and
        # compute its effect on linear and angular acceleration

        propeller_omega_vector  = self.pilot_thrust_to_propeller_omega(thrust_pilot, self.quad.quad_config.max_thrust)
        thrust = self.propeller_omega_to_thrust(propeller_omega_vector)
        acceleration = self.acceleration(thrust)

        torque_vector = self.propeller_omega_to_tau(propeller_omega_vector)
        omega_vector = self.quad.quad_state.omega()
        angular_acceleration = self.torque_to_omega_dot(omega_vector, torque_vector)

        # apply
        new_velocity = self.quad.quad_state.velocity + dt * acceleration;
        new_position = self.quad.quad_state.position + dt * new_velocity;
        new_omega = omega_vector + dt * angular_acceleration;

        self.quad.quad_state.angular_velocity = new_omega
        self.quad.quad_state.velocity = new_velocity
        self.quad.quad_state.position = new_position

    def propeller_omega_to_thrust(self, omega_vector):
        thrust = self.k_thrust_omega * np.array([0, 0, sum(omega_vector ** 2)])
        return thrust

    def pilot_thrust_to_propeller_omega(self, thrust, max_thrust):
        '''
        convert thrust applied to a motor into the induced angular velocity
        :param thrust: applied thrust
        :param max_thrust: maximum thrust possible
        :return: induced angular velocity
        '''

        T = np.array(thrust)
        return (T / max_thrust) * self.quad.quad_config.max_omega

    def propeller_omega_to_tau(self, omega_vector):
        '''
        given angular velocity vector of each motor, return the rotational torque vector on the
        quadcopter
        :param omega_vector:
        :return:
        '''

        L = self.quad.quad_config.arm_length
        tau_roll  = L * self.k_thrust_omega * (omega_vector[0] ** 2 - omega_vector[2] ** 2)
        tau_pitch = L * self.k_thrust_omega * (omega_vector[1] ** 2 - omega_vector[3] ** 2)
        tau_yaw = L * self.k_drag * ((omega_vector[0]**2 + omega_vector[2]**2) - (omega_vector[1]**2 + omega_vector[3]**2))

        return np.array([tau_roll, tau_pitch, tau_yaw])

    def torque_to_omega_dot(self, omega_vector, tau_vector):
        I_inverse = self.quad.quad_config.inv_inertia
        I = self.quad.quad_config.inertia
        omega_dot = I_inverse * (tau_vector - omega_vector * (I * omega_vector))
        return omega_dot

    def acceleration(self, thrust):
        gravity = np.array([0, 0, -self.env.g])

        R = self.quad.quad_state.quaternion().as_rotation_matrix(); #TODO must update quaternion in each timestep
        T = R * thrust;
        Fd = -self.quad.quad_config.k_friction_constant * self.quad.quad_state.velocity;
        a = gravity + 1 / self.quad.quad_config.mass * T + Fd;
        return a

    def omega_to_theta_dot(self, omega):
        pass
