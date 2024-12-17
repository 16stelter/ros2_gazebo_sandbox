import os
from ament_index_python import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, TextSubstitution
from launch.launch_description import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    pkg_ros_gazebo_sim = get_package_share_directory("ros_gz_sim")
    package_path = get_package_share_directory("ros2_gazebo_sandbox")

    world_name = DeclareLaunchArgument("world_name", default_value="empty", description="Name of the world to load")

    robot_x = DeclareLaunchArgument("robot_x", default_value="0.0", description="X position of the first robot")
    robot_y = DeclareLaunchArgument("robot_y", default_value="0.0", description="Y position of the first robot")
    robot_z = DeclareLaunchArgument("robot_z", default_value="1.0", description="Z position of the first robot")

    sim_world = DeclareLaunchArgument(
        "sim_world",
        default_value=[package_path, "/worlds/", LaunchConfiguration("world_name"), ".sdf"],
        description="Path to the Gazebo world file",
    )

    robot_ns = DeclareLaunchArgument(
        "robot_ns",
        default_value="",
        description="Robot namespace",
    )

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gazebo_sim, "launch", "gz_sim.launch.py")
        ),
        launch_arguments={"gz_args": LaunchConfiguration("sim_world")}.items(),
    )

    spawn_robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(package_path, "launch", "spawn_leo.launch.py")
        ),
        launch_arguments={"robot_ns": LaunchConfiguration("robot_ns"),
                          "x": LaunchConfiguration("robot_x"),
                          "y": LaunchConfiguration("robot_y"),
                          "z": LaunchConfiguration("robot_z"),
                          }.items(),
    )

    # Bridge ROS topics and Gazebo messages for establishing communication
    topic_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="ros_bridge",
        arguments=[
            ["/world/", LaunchConfiguration("world_name"), "/control@ros_gz_interfaces/srv/ControlWorld"],
            ["/world/", LaunchConfiguration("world_name"), "/create@ros_gz_interfaces/srv/SpawnEntity"],
            ["/world/", LaunchConfiguration("world_name"), "/remove@ros_gz_interfaces/srv/DeleteEntity"],
            ["/world/", LaunchConfiguration("world_name"), "/set_pose@ros_gz_interfaces/srv/SetEntityPose"],
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
            world_name,
            sim_world,
            robot_ns,
            robot_x,
            robot_y,
            robot_z,
            gz_sim,
            spawn_robot,
            topic_bridge,
        ]
    )