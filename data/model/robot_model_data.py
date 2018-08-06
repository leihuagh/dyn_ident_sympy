from dynamics import Dynamics
from kinematics import Geometry
import robot_def


class RobotModel:
    def __init__(self, dyn):
        self.dof = dyn.rbt_def.dof
        self.coordinates = dyn.rbt_def.coordinates
        self.T_0n = dyn.geom.T_0n

        self.base_num = dyn.base_num
        self.base_param = dyn.base_param
        self.H_b_func = dyn.H_b_func

        self.bary_param = dyn.bary_params
        self.H_func = dyn.H_func

        self.std_param = dyn.std_params
