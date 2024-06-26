# give ourselves three possible actions for the shooter - stop, set, and cycle through a list (for testing)
import math
import commands2
import constants
import wpilib
from wpilib import SmartDashboard, DriverStation
from wpimath.geometry import Translation2d


from subsystems.upper_crank_trapezoid import UpperCrankArmTrapezoidal
from subsystems.lower_crank_trapezoid import LowerCrankArmTrapezoidal

class ShooterToggle(commands2.Command):

    def __init__(self, container, shooter, rpm=3500, amp_rpm=2000, auto_amp_slowdown=False, wait_for_spinup=False, force=None, timeout=3) -> None:
        super().__init__()
        self.setName('ShooterToggle')
        self.container = container
        self.shooter = shooter
        self.shooter_arm: UpperCrankArmTrapezoidal = self.container.shooter_arm
        self.crank_arm: LowerCrankArmTrapezoidal = self.container.crank_arm
        self.rpm = rpm
        self.amp_rpm = amp_rpm
        self.auto_amp_slowdown = auto_amp_slowdown
        self.wait_for_spinup = wait_for_spinup
        self.force = force
        self.addRequirements(shooter)  # commandsv2 version of requirements
        self.timer = wpilib.Timer()
        self.timeout = timeout

    def initialize(self) -> None:

        self.timer.restart()

        if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
            self.speaker_translation = Translation2d(constants.k_speaker_tags_poses["red"][0], constants.k_speaker_tags_poses["red"][1])
        elif DriverStation.getAlliance() == DriverStation.Alliance.kBlue:
            self.speaker_translation = Translation2d(constants.k_speaker_tags_poses["blue"][0], constants.k_speaker_tags_poses["blue"][1])

        #figuring out how far we are from the speaker
        robot_pose = self.container.drive.get_pose()
        x = robot_pose.X()
        y = robot_pose.Y()
        self.distance_to_speaker = math.sqrt(math.pow((x - self.speaker_translation[0]), 2) + math.pow((y - self.speaker_translation[1]), 2))

        # try to set the shot based on the last arm configuration set  - CJH update 20240319
        arm_configuration:str = self.container.get_arm_configuration()
        if 'amp' in arm_configuration.lower():
            rpm = self.amp_rpm
        elif 'trap' in arm_configuration.lower():
            rpm = 1100  # 1050 previous to match 37 @ Houston
        elif self.distance_to_speaker > 3:
            rpm = 4500
            print(f'ATTEMPTED TO DO {rpm} FAST SHOT FROM ({x},{y}) AT DISTANCE {self.distance_to_speaker}')
        else:
            rpm = self.rpm

        # determine rpm based on shooter arm position - deprecated 20240319 CJH
        # if self.auto_amp_slowdown and (self.shooter_arm.get_angle() > 0 or self.crank_arm.get_angle() > math.pi / 2 + .05):
        #     rpm = self.amp_rpm
        # else:
        #     rpm = self.rpm

        # give ourselves three possible actions
        if self.force == 'on':
            self.shooter.set_flywheel(rpm)
        elif self.force == 'off':
            self.shooter.stop_shooter()
        else:
            self.shooter.toggle_shooter(rpm)
        
        """Called just before this Command runs the first time."""
        self.start_time = round(self.container.get_enabled_time(), 2)
        print(f"  ** Firing {self.getName()} with force={self.force} and rpm {rpm} at {self.start_time} s **", flush=True)
        # SmartDashboard.putString("alert", f"** Started {self.getName()} at {self.start_time - self.container.get_enabled_time():2.2f} s **")

    def execute(self) -> None:
        pass

    def isFinished(self) -> bool:
        if self.wait_for_spinup:
            return self.shooter.get_at_velocity() or self.timer.get() > self.timeout  # do not let this get stuck!
        if not self.wait_for_spinup:
            return True

    def end(self, interrupted: bool) -> None:
        end_time = self.container.get_enabled_time()
        message = 'Interrupted' if interrupted else 'Ended'
        print(f"  ** {message} {self.getName()} at {end_time:.1f} s after {end_time - self.start_time:.1f} s **", flush=True)
        SmartDashboard.putString(f"alert", f"** {message} {self.getName()} at {end_time:.1f} s after {end_time - self.start_time:.1f} s **")

        
