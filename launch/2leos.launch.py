import os
from ament_index_python import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription, GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.launch_description import LaunchDescription
from launch_ros.actions import PushRosNamespace, Node


def generate_launch_description():
    pkg_ros_gazebo_sim = get_package_share_directory("ros_gz_sim")
    package_path = get_package_share_directory("ros2_gazebo_sandbox")

    sim_world = DeclareLaunchArgument(
        "sim_world",
        default_value=os.path.join(package_path, "worlds", "shackleton.sdf"),
        description="Path to the Gazebo world file",
    )

    robot1_ns = DeclareLaunchArgument(
        "robot1_ns",
        default_value="leo1",
        description="Namespace for the first robot",
    )

    robot2_ns = DeclareLaunchArgument(
        "robot2_ns",
        default_value="leo2",
        description="Namespace for the second robot",
    )

    robot1_x = DeclareLaunchArgument("robot1_x", default_value="0.0", description="X position of the first robot")
    robot1_y = DeclareLaunchArgument("robot1_y", default_value="0.0", description="Y position of the first robot")
    robot1_z = DeclareLaunchArgument("robot1_z", default_value="1.0", description="Z position of the first robot")

    robot2_x = DeclareLaunchArgument("robot2_x", default_value="0.0", description="X position of the second robot")
    robot2_y = DeclareLaunchArgument("robot2_y", default_value="1.0", description="Y position of the second robot")
    robot2_z = DeclareLaunchArgument("robot2_z", default_value="1.0", description="Z position of the second robot")

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gazebo_sim, "launch", "gz_sim.launch.py")
        ),
        launch_arguments={"gz_args": LaunchConfiguration("sim_world")}.items(),
    )

    robot1_group = GroupAction(
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(package_path, "launch", "spawn_leo.launch.py")
                ),
                launch_arguments={"robot_ns": LaunchConfiguration("robot1_ns"),
                                  "x": LaunchConfiguration("robot1_x"),
                                  "y": LaunchConfiguration("robot1_y"),
                                  "z": LaunchConfiguration("robot1_z"),
                                  }.items(),
            ),
        ]
    )

    robot2_group = GroupAction(
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(package_path, "launch", "spawn_leo.launch.py")
                ),
                launch_arguments={"robot_ns": LaunchConfiguration("robot2_ns"),
                                  "x": LaunchConfiguration("robot2_x"),
                                  "y": LaunchConfiguration("robot2_y"),
                                  "z": LaunchConfiguration("robot2_z"),
                                  }.items(),
            ),
        ]
    )

    # Bridge ROS topics and Gazebo messages for establishing communication
    topic_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="clock_bridge",
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
        ],
        parameters=[
            {
                "qos_overrides./tf_static.publisher.durability": "transient_local",
            }
        ],
        output="screen",
    )

    return LaunchDescription(
        [
            sim_world,
            robot1_ns,
            robot2_ns,
            robot1_x,
            robot1_y,
            robot1_z,
            robot2_x,
            robot2_y,
            robot2_z,
            gz_sim,
            robot1_group,
            robot2_group,
            topic_bridge,
        ]
    )
