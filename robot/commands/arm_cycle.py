import math
import commands2
from wpilib import SmartDashboard

from subsystems.upper_crank_trapezoid import UpperCrankArmTrapezoidal
from subsystems.lower_crank_trapezoid import LowerCrankArmTrapezoidal

class ArmCycle(commands2.Command):

    counter = 0

    def __init__(self, container, upper_crank: UpperCrankArmTrapezoidal, lower_crank: LowerCrankArmTrapezoidal) -> None:
        super().__init__()
        self.setName('ArmCycle')
        self.container = container
        self.upper_crank = upper_crank
        self.lower_crank = lower_crank
        self.addRequirements(self.upper_crank)
        self.addRequirements(self.lower_crank)

        self.crank_presets = {
            'intake': {'upper': math.radians(-80), 'lower': math.radians(70)},
            'shoot': {'upper': math.radians(-55), 'lower': math.radians(90)},
            'shoot2':{'upper':math.radians(-35), 'lower':math.radians(90)},
            'amp':{'upper': math.radians(50), 'lower':math.radians(100)},
            'trap':{'upper': math.radians(110), 'lower':math.radians(110)},
        }

    def initialize(self) -> None:
        """Called just before this Command runs the first time."""
        self.start_time = round(self.container.get_enabled_time(), 2)
        print("\n" + f"** Firing {self.getName()}  at {self.start_time} s **", flush=True)
        SmartDashboard.putString("alert",
                                 f"** Started {self.getName()} at {self.start_time - self.container.get_enabled_time():2.2f} s **")
        self.counter += 1
        active_mode = list(self.crank_presets.keys())[self.counter % len(self.crank_presets)]
        self.container.arm_mode = active_mode

        self.upper_crank.setGoal(self.crank_presets[active_mode]['upper'])
        self.lower_crank.setGoal(self.crank_presets[active_mode]['lower'])

    def execute(self) -> None:
        pass

    def isFinished(self) -> bool:
        return True

    def end(self, interrupted: bool) -> None:
        end_time = self.container.get_enabled_time()
        message = 'Interrupted' if interrupted else 'Ended'


