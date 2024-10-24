import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    description_package = LaunchConfiguration("description_package", default = 'urdf_viewer')

    rviz_config_filename = 'rviz/urdf_viewer_config.rviz'
    # Specify the path to the RViz configuration file
    rviz_config_file = os.path.join(
        get_package_share_directory('urdf_viewer'),
        rviz_config_filename
    )

    urdf_file_name = 'urdf/UR10/ur10.urdf'
    urdf = os.path.join(
        get_package_share_directory('urdf_viewer'),
        urdf_file_name)
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            namespace='ur10',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc, 'frame_prefix':'ur10/'}],
            arguments=[urdf]),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            namespace='ur10',
            output='screen',
            arguments=[urdf]),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            namespace='ur11',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc, 'frame_prefix':'ur11/'}],
            arguments=[urdf]),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            namespace='ur11',
            output='screen',
            arguments=[urdf]),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_transform_publisher',
            output='screen',
            arguments=['0', '0', '0', '0', '0', '0', 'world', 'ur10/base_link']
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_transform_publisher',
            output='screen',
            arguments=['0', '0', '0', '0', '0', '0', 'ur10/tool_link', 'ur11/base_link']
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            output='screen',
            arguments=['-d', rviz_config_file]),
    ])