"""
Robots sub-module of the Jacobi Library.
"""
from __future__ import annotations
import jacobi
import os
import pybind11_stubgen.typing_ext
import typing
import typing_extensions
__all__ = ['ABBGoFaCRB1500010', 'ABBIRB1200590', 'ABBIRB1200770', 'ABBIRB130010115', 'ABBIRB1300714', 'ABBIRB1600612', 'ABBIRB260012185', 'ABBIRB460060205', 'ABBIRB6700150320', 'ABBYuMiIRB14000', 'CustomRobot', 'DualArm', 'FanucCRX30iA', 'FanucLR10iA10', 'FanucLRMate200iD7L', 'FanucM20iB25', 'FanucM20iD25', 'FanucM710iC45M', 'FlexivRizon10', 'FlexivRizon10S', 'FlexivRizon4', 'FlexivRizon4S', 'FrankaPanda', 'KinovaGen37DoF', 'KukaIiwa7', 'KukaKR6R700sixx', 'KukaKR70R2100', 'MecademicMeca500', 'UfactoryXArm7', 'UniversalUR10', 'UniversalUR10e', 'UniversalUR20', 'UniversalUR5e', 'YaskawaGP12', 'YaskawaGP180', 'YaskawaGP180120', 'YaskawaGP50', 'YaskawaHC10', 'YaskawaHC20']
class ABBGoFaCRB1500010(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class ABBIRB1200590(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class ABBIRB1200770(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class ABBIRB130010115(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class ABBIRB1300714(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class ABBIRB1600612(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class ABBIRB260012185(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class ABBIRB460060205(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class ABBIRB6700150320(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class ABBYuMiIRB14000(DualArm):
    """
    """
    class Arm(jacobi.RobotArm):
        """
        """
        @staticmethod
        def _pybind11_conduit_v1_(*args, **kwargs):
            ...
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class CustomRobot(jacobi.RobotArm):
    """
    A custom robot arm that can be loaded from a URDF file.
    
    The `CustomRobot` class extends the `RobotArm` class and provides the
    functionality to load a robot's configuration from a URDF (Unified
    Robot Description Format) file. It also includes methods for handling
    inverse kinematics and filtering relevant configurations.
    """
    class JointType:
        """
        Types of joints that can be present in the robot.
        
        Members:
        
          Revolute : A revolute joint that allows rotation.
        
          Continuous : A continuous joint that allows unlimited rotation.
        
          Prismatic : A prismatic joint that allows linear motion.
        
          Fixed : A fixed joint that does not allow any motion.
        """
        Continuous: typing.ClassVar[CustomRobot.JointType]  # value = <JointType.Continuous: 1>
        Fixed: typing.ClassVar[CustomRobot.JointType]  # value = <JointType.Fixed: 3>
        Prismatic: typing.ClassVar[CustomRobot.JointType]  # value = <JointType.Prismatic: 2>
        Revolute: typing.ClassVar[CustomRobot.JointType]  # value = <JointType.Revolute: 0>
        __members__: typing.ClassVar[dict[str, CustomRobot.JointType]]  # value = {'Revolute': <JointType.Revolute: 0>, 'Continuous': <JointType.Continuous: 1>, 'Prismatic': <JointType.Prismatic: 2>, 'Fixed': <JointType.Fixed: 3>}
        @staticmethod
        def _pybind11_conduit_v1_(*args, **kwargs):
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    Continuous: typing.ClassVar[CustomRobot.JointType]  # value = <JointType.Continuous: 1>
    Fixed: typing.ClassVar[CustomRobot.JointType]  # value = <JointType.Fixed: 3>
    Prismatic: typing.ClassVar[CustomRobot.JointType]  # value = <JointType.Prismatic: 2>
    Revolute: typing.ClassVar[CustomRobot.JointType]  # value = <JointType.Revolute: 0>
    link_translations: list[jacobi.Frame]
    map_dofs_to_joints: list[int]
    map_joints_to_dofs: list[int]
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @staticmethod
    def load_from_urdf_file(file: os.PathLike, base_link: str = 'base_link', end_link: str = 'flange') -> CustomRobot:
        """
        Load the robot from a URDF file
        
        Loads a custom robot from a *.urdf file, and sets the robot arm to the
        kinematic chain between the given base_link and the end_link.
        
        Parameter ``file``:
            The path to the URDF file.
        
        Parameter ``base_link``:
            The name of the base link in the URDF.
        
        Parameter ``end_link``:
            The name of the end link in the URDF.
        
        Returns:
            A shared pointer to the loaded robot.
        """
    @typing.overload
    def __init__(self, degrees_of_freedom: int) -> None:
        ...
    @typing.overload
    def __init__(self, degrees_of_freedom: int, number_joints: int) -> None:
        ...
    @property
    def child(self) -> jacobi.RobotArm:
        """
        Possible child robot.
        """
    @child.setter
    def child(self, arg0: jacobi.RobotArm) -> None:
        ...
    @property
    def config_joint_names(self) -> list[str]:
        """
        Names of the joints corresponding to a specific joint configuration.
        """
    @config_joint_names.setter
    def config_joint_names(self, arg0: list[str]) -> None:
        ...
    @property
    def joint_axes(self) -> list[typing_extensions.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(3)]]:
        """
        Axes of the joints in the robot.
        """
    @joint_axes.setter
    def joint_axes(self, arg0: list[typing_extensions.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(3)]]) -> None:
        ...
    @property
    def joint_names(self) -> list[str]:
        """
        Names of the joints in the robot.
        """
    @joint_names.setter
    def joint_names(self, arg0: list[str]) -> None:
        ...
    @property
    def joint_types(self) -> list[...]:
        """
        The type of the joints: Currently revolute, continuous, prismatic, and
        fixed joints are supported.
        """
    @joint_types.setter
    def joint_types(self, arg0: list[...]) -> None:
        ...
class DualArm(jacobi.Robot):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, left: jacobi.RobotArm, right: jacobi.RobotArm) -> None:
        ...
    @property
    def left(self) -> jacobi.RobotArm:
        """
        The left arm of the robot
        """
    @property
    def right(self) -> jacobi.RobotArm:
        """
        The right arm of the robot
        """
class FanucCRX30iA(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class FanucLR10iA10(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class FanucLRMate200iD7L(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class FanucM20iB25(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class FanucM20iD25(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class FanucM710iC45M(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class FlexivRizon10(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class FlexivRizon10S(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class FlexivRizon4(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class FlexivRizon4S(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class FrankaPanda(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class KinovaGen37DoF(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class KukaIiwa7(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class KukaKR6R700sixx(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class KukaKR70R2100(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class MecademicMeca500(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class UfactoryXArm7(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class UniversalUR10(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class UniversalUR10e(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class UniversalUR20(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class UniversalUR5e(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class YaskawaGP12(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class YaskawaGP180(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class YaskawaGP180120(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class YaskawaGP50(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class YaskawaHC10(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class YaskawaHC20(jacobi.RobotArm):
    """
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
