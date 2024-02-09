import launch
from launch.substitutions import LaunchConfiguration, Command
import launch_ros
import os
from ament_index_python import get_package_prefix

pkg_share_path = os.pathsep + os.path.join(get_package_prefix(package_name='pallet_jack_description'), 'share')
if 'GAZEBO_MODEL_PATH' in os.environ:
    os.environ['GAZEBO_MODEL_PATH'] += pkg_share_path
else:
    os.environ['GAZEBO_MODEL_PATH'] =  pkg_share_path

def generate_launch_description():
    pkg_share = launch_ros.substitutions.FindPackageShare(package='pallet_jack_description').find('pallet_jack_description')
    default_model_path = os.path.join(pkg_share, 'src/description/pallet_jack_description.urdf')
    # default_mesh_path = os.path.join(pkg_share, 'src/meshes/')
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/urdf_config.rviz')

    with open(default_model_path, 'r') as infp:
        robot_desc = infp.read()

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_desc}]
        # parameters=[{'robot_description': Command(['xacro ', LaunchConfiguration('model')])}]
    )
    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        arguments=[default_model_path],
        # condition=launch.conditions.UnlessCondition(LaunchConfiguration('gui'))
    )
    # joint_state_publisher_gui_node = launch_ros.actions.Node(
    #     package='joint_state_publisher_gui',
    #     executable='joint_state_publisher_gui',
    #     name='joint_state_publisher_gui',
    #     condition=launch.conditions.IfCondition(LaunchConfiguration('gui'))
    # )
    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
    )

    spawn_entity = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'pallet_jack', '-topic', 'robot_description', '-x', '0.0', '-y', '0.45', '-z', '0.895', '-Y', '0', '-R', '0', '-P', '0'],
        output='screen'
    )

    return launch.LaunchDescription([
        # launch.actions.DeclareLaunchArgument(name='gui', default_value='True',
        #                                     description='Flag to enable joint_state_publisher_gui'),
        launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
                                            description='Absolute path to robot urdf file and meshes'),
        launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                            description='Absolute path to rviz config file'),
        
        launch.actions.ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so'], output='screen'),
        
        joint_state_publisher_node,
        # joint_state_publisher_gui_node,
        robot_state_publisher_node,
        spawn_entity,
        rviz_node
    ])