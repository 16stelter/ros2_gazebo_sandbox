# ros2_gazebo_sandbox

A gazebo simulation environment with ros2 interface for simulating planetary exploration scenarios.

## Dependencies

The project currently requires a modified version of ```ros_gz_bridge``` and ```ros_gz_interfaces``` to allow spawning, moving and deleting entities through a ros service.
Until this is merged to the main ros2 repository, this modification can be found here: git@github.com:UoA-CARES/ros_gz.git

Clone the package into your workspace and build it using

```
git clone -b ros2 https://github.com/UoA-CARES/ros_gz.git
colcon build --packages-up-to ros_gz_bridge --parallel-workers 2 --allow-overriding ros_gz_bridge ros_gz_interfaces
```

Number of parallel workers can be adjusted if your PC is more powerful, but building this crashed my computer twice if I try to use more workers, so beware.

The project also expects some robot models:

* [LEO Rover](https://github.com/LeoRover/leo_common-ros2)
* [LEO Sim](https://github.com/LeoRover/leo_simulator-ros2)

## Known Issues

Currently deleting entities via service does not work