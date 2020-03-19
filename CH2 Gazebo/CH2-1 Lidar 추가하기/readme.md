# CH2.1 터틀봇에 Lidar 센서 추가하기

turtlebot_gazebo 패키지의 터틀봇은 기본적으로 Lidar센서가 없다 
 그 대신 asus xtion pro 3D 카메라가 설치되어 있지만, SLAM 등 많은 알고리즘에서 Lidar 센서는 굉장히 유용하기 때문에 이번 글어세 Lidar를 추가하는 방법에 대해 적는다
 
## .xacro
xacro는 xml+macro의 약어 정도로 이해하면 된다
xacro파일은 gazebo에서의 여러가지 동작을 정의해놓은 파일이다
로봇 모델을 정의만 해놓는다면 시뮬레이션을 해볼 수가 없기 때문에 xacro를 사용하는방법을 숙지해 놓는것이 좋다
그러나 xacro의 모든 기술방식을 이해하고 밑바닥에서부터 모델을 정의하는것은 오픈소스정신에 위배되므로, 
여기서는 중요한 포인트만을 적는다

## hokuyo urdf 파일 만들기
센서의 외형은 이미 모델링되어있는 파일을 쓰면 된다.
아래 명령어를 이용하여 센서의 urdf를 작성해주자.

> cd $ROS_ROOT/../turtlebot_description/urdf/sensors
sudo gedit hokuyo.urdf.xacro

그 다음, 이하의 내용을 적어준다

	<?xml version="1.0"?>
	<robot name="sensor_hokuyo" xmlns:xacro="http://ros.org/wiki/xacro">
		<xacro:include filename="$(find turtlebot_description)/urdf/turtlebot_gazebo.urdf.xacro"/>
  		<xacro:include filename="$(find turtlebot_description)/urdf/turtlebot_properties.urdf.xacro"/>

  		<xacro:macro name="sensor_hokuyo" params="parent">
			<link name="hokuyo_link">
      			<collision>
        			<origin xyz="0 0 0" rpy="0 0 0"/>
        			<geometry>
          				<box size="0.1 0.1 0.1"/>
        			</geometry>
      			</collision>
      			<visual>
        			<origin xyz="0 0 0" rpy="0 0 0"/>
        			<geometry>
          				<mesh filename="package://gazebo_plugins/test/multi_robot_scenario/meshes/laser/hokuyo.dae"/>
        			</geometry>
      			</visual>
      			<inertial>
        			<mass value="1e-5" />
        			<origin xyz="0 0 0" rpy="0 0 0"/>
        			<inertia ixx="1e-6" ixy="0" ixz="0" iyy="1e-6" iyz="0" izz="1e-6" />
      			</inertial>
    		</link>
    		<joint name="hokuyo_joint" type="fixed">
      		<!--<axis xyz="0 0 1" />-->
      			<origin xyz="0.08 0 0.430" rpy="0 0 0"/>
      			<parent link="${parent}"/>
      			<child link="hokuyo_link"/>
     		</joint>
     		<!-- Hokuyo sensor for simulation -->
     		<gazebo reference="hokuyo_link">
    			<sensor type="ray" name="head_hokuyo_sensor">
      				<pose>0 0 0 0 0 0</pose>
      				<visualize>true</visualize>
      				<update_rate>40</update_rate>
      				<ray>
        				<scan>
          					<horizontal>
            						<samples>360</samples>
            						<resolution>1</resolution>
            						<min_angle>0</min_angle>
            						<max_angle>6.28319</max_angle>
          					</horizontal>
        				</scan>
        				<range>
          					<min>0.10</min>
          					<max>30.0</max>
          					<resolution>0.01</resolution>
        				</range>
        				<noise>
          					<type>gaussian</type>
          					<!-- Noise parameters based on published spec for Hokuyo laser
               					achieving "+-30mm" accuracy at range < 10m.  A mean of 0.0m and
               					stddev of 0.01m will put 99.7% of samples within 0.03m of the true
               					reading. -->
          					<mean>0.0</mean>
          					<stddev>0.01</stddev>
        				</noise>
      				</ray>
      				<plugin name="gazebo_ros_head_hokuyo_controller" filename="libgazebo_ros_laser.so">
        				<topicName>scan</topicName>
        				<frameName>hokuyo_link</frameName>
      				</plugin>
    			</sensor>
  			</gazebo>
		</xacro:macro>
	</robot>
	
16~18행에서의 geometry 태그가 선세의 외형을 정의하고 있다.
태그 안의 .dae파일이 외형을 정의하고 있으므로, 불러왔을때 외형이 이상하다면 웹에서 직접 다운을 받아야 할 수도 있다.
turtlebot_gazebo를 설치할 때 대부분 설치가 될것이니 크게 걱정할 필요는 없다.

28행의 origin태그는 센서의 위치를 정의하고 있다.
여기서는 터틀봇의 상단에 위치하도록 설치되어있다.

36행의 visualize태그는 센서의 레이저의 가시화 여부를 말한다.
true 인 경우 레이져가 보이고, false인 경우 보이지 않는다.

41행의 samples 태그는 Lidar가 한바퀴 회전했을 때 몇변의 거리를 측정하는가를 말한다.
여기서는 360번을 측정하도록 되어있다.

43~44행은 처음(min_angle)과 마지막(max_angle)측정의 각도(rad)롤 말한다.
나는 180도 전방 전방위를 측정하고자 했으므로 0, 6.28319로 설정했다.

48~49행은 센서의 측정 한계 거리를 말한다.
min은 최소값, max는 최댓값을 말한다(단위 m).

63은 측정값을 발행하는 토픽의 이름을 정의한다.

다음은 우리가 정의한 센서를 xtion대신 사용하겠다는 설정이 필요하다.
다음의 명령어를 입력하자.

>cd ../../robots/
sudo cp kobuki_hexagons_asus_xtion_pro.urdf.xacro kobuki_hexagons_hokuyo.urdf.xacro
sudo gedit kobuki_hexagons_hokuyo.urdf.xacro 

다음 내용을 입력한다.

	<?xml version="1.0"?>
	<!--
		- Base      : kobuki
		- Stacks    : hexagons
    	- 3d Sensor : hokuyo
	-->
	<robot name="turtlebot" xmlns:xacro="http://ros.org/wiki/xacro">

  		<xacro:include filename="$(find turtlebot_description)/urdf/turtlebot_common_library.urdf.xacro" />
  		<xacro:include filename="$(find kobuki_description)/urdf/kobuki.urdf.xacro" />
  		<xacro:include filename="$(find turtlebot_description)/urdf/stacks/hexagons.urdf.xacro"/>
  		<xacro:include filename="$(find turtlebot_description)/urdf/sensors/hokuyo.urdf.xacro"/>

  		<kobuki/>
  		<stack_hexagons                 parent="base_link"/>
  		<sensor_hokuyo parent="base_link"/>
	</robot>
	
마지막으로 환경변수를 변경해주면 된다.

>export TURTLEBOT_3D_SENSOR="hokuyo"

아래 명령어로 설정이 잘 되었나 확인해 보자.

>echo $TURTLEBOT_3D_SENSOR

hokuyo라고 뜨면 성공적이다.

<iframe width="640" height="360" src="https://www.youtube.com/embed/6Az2cNU7gUw" frameborder="0" gesture="media" allowfullscreen=""></iframe>