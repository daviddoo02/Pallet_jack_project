# Pallet Jack Project

## Overview


## First Steps

### Setting up the environment
```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
```

```bash
# export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$PWD/models
export GAZEBO_RESOURCE_PATH=$GAZEBO_RESOURCE_PATH:$PWD/worlds
```

### Launching
```bash
ros2 launch pallet_jack_description pj_world.launch
```

## Troubleshooting

- Gzclient not opening [Fix](https://answers.ros.org/question/358847/cannot-launch-gzclient-on-a-launch-file-results-in-shared_ptr-assertion-error/):
```bash
 . /usr/share/gazebo/setup.sh 
```
