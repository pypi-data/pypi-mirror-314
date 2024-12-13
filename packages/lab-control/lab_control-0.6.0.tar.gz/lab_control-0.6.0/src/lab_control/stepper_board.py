import rpc

LARGE_FLOAT = 1e10  # large "effectively infinite" float because json doesn't support inf

Number = int | float


class StepperBoard(rpc.RpcProxy):
    # control functions
    def move_to(self, index: int, target: int, speed: Number = LARGE_FLOAT) -> None:
        """Move a stepper with given index to a target position at a given speed, blocking until the move is complete

        Args:
            index (int): The index of the stepper to move
            target (int): The target position to move to
            speed (Number, optional): The speed to move at. Defaults to LARGE_FLOAT.
        """
        pass

    def wait(self, index: int) -> None:
        """Wait for a stepper with given index to finish moving

        Args:
            index (int): The index of the stepper to wait for
        """
        pass

    def set_target(self, index: int, target: int, speed: Number = LARGE_FLOAT) -> None:
        """Set the target position of a stepper with given index, non-blocking version of move_to

        Args:
            index (int): The index of the stepper to set the target of
            target (int): The target position to set
            speed (Number, optional): The speed to move at. Defaults to LARGE_FLOAT.
        """
        pass

    def stop(self, index: int) -> None:
        """Stop a stepper with given index

        Args:
            index (int): The index of the stepper to stop
        """
        pass

    def set_home(self, index: int) -> None:
        """Set the current position of a stepper with given index as the home (zero) position

        Args:
            index (int): The index of the stepper to set the home of
        """
        pass

    # status functions
    def position(self, index: int) -> int:
        """Get the current position of a stepper with given index

        Args:
            index (int): The index of the stepper to get the position of

        Returns:
            int: The current position of the stepper
        """
        pass

    def target(self, index: int) -> int:
        """Get the target position of a stepper with given index

        Args:
            index (int): The index of the stepper to get the target of

        Returns:
            int: The target position of the stepper
        """
        pass

    def steps_remaining(self, index: int) -> int:
        """Get the number of steps remaining for a stepper with given index to reach its target

        Args:
            index (int): The index of the stepper to get the steps remaining of

        Returns:
            int: The number of steps remaining for the stepper to reach its target
        """
        pass

    def time_remaining(self, index: int) -> float:
        """Get the approximate time remaining for a stepper with given index to reach its target

        Args:
            index (int): The index of the stepper to get the time remaining of

        Returns:
            float: The approximate time remaining for the stepper to reach its target, the time will sometimes be slightly overestimated
        """

        pass

    # configuration functions
    def max_speed(self, index: int) -> float:
        """Get the maximum speed of a stepper with given index

        Args:
            index (int): The index of the stepper to get the maximum speed of

        Returns:
            float: The maximum speed of the stepper
        """
        pass

    def set_max_speed(self, index: int, speed: Number) -> None:
        """Set the maximum speed of a stepper with given index

        Args:
            index (int): The index of the stepper to set the maximum speed of
            speed (Number): The maximum speed to set
        """
        pass

    def max_accel(self, index: int) -> float:
        """Get the maximum acceleration of a stepper with given index

        Args:
            index (int): The index of the stepper to get the maximum acceleration of

        Returns:
            float: The maximum acceleration of the stepper
        """
        pass

    def set_max_accel(self, index: int, speed: Number) -> None:
        """Set the maximum acceleration of a stepper with given index

        Args:
            index (int): The index of the stepper to set the maximum acceleration of
            speed (Number): The maximum acceleration to set
        """
        pass

    # vector functions
    def move_to_vec(self, targets: list[int], mode: str, speed: Number = LARGE_FLOAT) -> None:
        """Move all steppers to the given target positions at the given speed, blocking until all steppers have reached their targets

        Args:
            targets (list[int]): The target positions to move to. If the list is shorter than the number of steppers the list will be padded with zeros
            mode (str): Joint movement mode:
                - "individual_max": Each stepper moves to its target at its maximum speed, the stepper generally finish at different times
                - "joint_max": The steppers speeds are adjusted so that the path is linearly interpolated and they all finish at the same time. The speed is determined by the max speed of the stepper that takes the longest time to reach its target.
                - "joint_euclid": The steppers speeds are adjusted so that the path is linearly interpolated and they all finish at the same time. The euclidean norm of the speeds must be specified.
                - "joint_cheby": The steppers speeds are adjusted so that the path is linearly interpolated and they all finish at the same time. The chebyshev norm (max of the absolute values) of the speeds must be specified.
            speed (Number, optional): Speed for "joint_euclid" and "joint_cheby" modes. Defaults to LARGE_FLOAT.
        """
        pass

    def wait_vec(self) -> None:
        """Wait for all steppers to finish moving"""
        pass

    def set_target_vec(self, targets: list[int], mode: str, speed: Number = LARGE_FLOAT) -> None:
        """Set the target positions of all steppers, non-blocking version of move_to_vec

        Args:
            targets (list[int]): The target positions to set. If the list is shorter than the number of steppers the list will be padded with zeros
            mode (str): Joint movement mode:
                - "individual_max": Each stepper moves to its target at its maximum speed, the stepper generally finish at different times
                - "joint_max": The steppers speeds are adjusted so that the path is linearly interpolated and they all finish at the same time. The speed is determined by the max speed of the stepper that takes the longest time to reach its target.
                - "joint_euclid": The steppers speeds are adjusted so that the path is linearly interpolated and they all finish at the same time. The euclidean norm of the speeds must be specified.
                - "joint_cheby": The steppers speeds are adjusted so that the path is linearly interpolated and they all finish at the same time. The chebyshev norm (max of the absolute values) of the speeds must be specified.
            speed (Number, optional): Speed for "joint_euclid" and "joint_cheby" modes. Defaults to LARGE_FLOAT.
        """
        pass

    def stop_vec(self) -> None:
        """Stop all steppers"""
        pass

    def set_home_vec(self) -> None:
        """Set the current positions of all steppers as the home (zero) positions"""
        pass

    # vector status functions
    def position_vec(self) -> list[int]:
        """Get the current positions of all steppers

        Returns:
            list[int]: The current positions of all steppers
        """
        pass

    def target_vec(self) -> list[int]:
        """Get the target positions of all steppers

        Returns:
            list[int]: The target positions of all steppers
        """
        pass

    def steps_remaining_vec(self) -> list[int]:
        """Get the number of steps remaining for all steppers to reach their targets

        Returns:
            list[int]: The number of steps remaining for all steppers to reach their targets
        """
        pass

    def time_remaining_vec(self) -> float:
        """Get the approximate time remaining until all steppers reach their targets

        Returns:
            float: The approximate time remaining until all steppers reach their targets, the time will sometimes be slightly overestimated
        """
        pass

    # vector configuration functions
    def max_speed_vec(self) -> list[float]:
        """Get the maximum speeds of all steppers

        Returns:
            list[float]: The maximum speeds of all steppers
        """
        pass

    def max_accel_vec(self) -> list[float]:
        """Get the maximum accelerations of all steppers

        Returns:
            list[float]: The maximum accelerations of all steppers
        """
        pass

    # control functions
    def enabled(self) -> bool:
        """Query wether the physical stepper drivers (stepsticks) are enabled

        If the drivers are disabled they will no longer drive any (holding) current. The stepper board will refuse to move the stepper until the drivers are enabled again.

        Returns:
            bool: True if the drivers are enabled, False if they are disabled
        """
        pass

    def set_enabled(self, enable: bool) -> None:
        """Enable or disable the physical stepper drivers (stepsticks)

        If the drivers are disabled they will no longer drive any (holding) current. The stepper board will refuse to move the stepper until the drivers are enabled again.

        Args:
            enable (bool): True to enable the drivers, False to disable them
        """
        pass

    def microsteps(self) -> int:
        """Get the number of microsteps per full step (step pulses required per full step) that the stepper drivers are currently configured for

        Returns:
            int: The number of microsteps per full step
        """
        pass

    def set_microsteps(self, microsteps: int) -> None:
        """Set the number of microsteps per full step (step pulses required per full step) that the stepper drivers should be configured for

        Args:
            microsteps (int): The number of microsteps per full step. Must be one of [2, 4, 8, 16]
        """
        pass

    # compensation functions
    def compensation(self) -> str:
        """Get the current compensation type

        The available compensation types are:
            - "none": No compensation is applied
            - "backlash": Backlash compensation is applied. When the stepper changes direction the stepper will add an additional number of steps to the target position according to the specified backlash value
            - "hysteresis": Hysteresis compensation is applied. The driver will always approach the target position from a given offset determined by the specified hysteresis value

        Returns:
            str: The current compensation type
        """
        pass

    def set_compensation(self, compensation_type: str) -> None:
        """Set the compensation type

        The available compensation types are:
            - "none": No compensation is applied
            - "backlash": Backlash compensation is applied. When the stepper changes direction the stepper will add an additional number of steps to the target position according to the specified backlash value
            - "hysteresis": Hysteresis compensation is applied. The driver will always approach the target position from a given offset determined by the specified hysteresis value

        Args:
            compensation_type (str): The compensation type to set
        """
        pass

    def backlash(self, index: int) -> int:
        """Get the backlash compensation value for a stepper with given index

        Args:
            index (int): The index of the stepper to get the backlash compensation value of

        Returns:
            int: The backlash compensation value
        """
        pass

    def set_backlash(self, index: int, value: int) -> None:
        """Set the backlash compensation value for a stepper with given index

        Args:
            index (int): The index of the stepper to set the backlash compensation value of
            value (int): The backlash compensation value to set
        """
        pass

    def hysteresis(self, index: int) -> int:
        """Get the hysteresis compensation value for a stepper with given index

        Args:
            index (int): The index of the stepper to get the hysteresis compensation value of

        Returns:
            int: The hysteresis compensation value
        """
        pass

    def set_hysteresis(self, index: int, value: int) -> None:
        """Set the hysteresis compensation value for a stepper with given index

        Args:
            index (int): The index of the stepper to set the hysteresis compensation value of
            value (int): The hysteresis compensation value to set
        """
        pass

    # misc
    def reset_config(self) -> None:
        """Reset the configuration of the stepper board to default values"""
        pass
