#!/bin/bash


USER_ID=$(id -u)
GRP=$(id -g -n)
GRP_ID=$(id -g)
LOCAL_HOST=`hostname`
DOCKER_HOME="/home/$USER"
SERVER_IP=`ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|grep -v 172.17.0.1|sed -n '1p'`

if [ ! -n "$SERVER_IP" ];then
	SERVER_IP=`127.0.0.1`
fi

if [ "$USER" == "root" ];then
    DOCKER_HOME="/root"
fi
if [ ! -d "$HOME/.cache" ];then
    mkdir "$HOME/.cache"
fi

IMG=$1
CONTAINER_NAME=$2


docker run -it \
	-d \
	--gpus all \
	--privileged \
	--name $CONTAINER_NAME \
	-e DOCKER_USER=$USER \
	-e USER=$USER \
	-e DOCKER_USER_ID=$USER_ID \
	-e DOCKER_GRP=$GRP \
	-e DOCKER_GRP_ID=$GRP_ID \
	-e HOST_IP=$SERVER_IP   \
	--env ROS_DOMAIN_ID=$(date +%N) \
	-v /tmp/.X11-unix:/tmp/.X11-unix:rw \
	-e DISPLAY=unix$DISPLAY \
	-v /media:/media \
	-v $HOME/.cache:${DOCKER_HOME}/.cache \
	-v /home/$USER/code:/home/$USER/code \
	-v /home/$USER/package:/home/$USER/package \
	-v /home/$USER/Desktop:/home/$USER/Desktop \
	-v /home/$USER/Downloads:/home/$USER/Downloads \
	-v /home/$USER/APPS:/home/$USER/APPS \
	-v /home/$USER/workspace:/home/$USER/workspace \
	-v /etc/localtime:/etc/localtime:ro \
	--net host \
	--shm-size 2048M \
	-w /home/$USER \
	$IMG \
	/bin/bash



xhost +local:root 1>/dev/null 2>&1
docker exec -it $CONTAINER_NAME /bin/bash
xhost -local:root 1>/dev/null 2>&1
