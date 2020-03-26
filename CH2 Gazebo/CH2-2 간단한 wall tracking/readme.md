# CH2.2 Wall Tracking


이번에는 Gazebo와 터틀봇을 이용해서 간단한 알고리즘을 연습해 보자.
본격적으로 알고리즘을 구현하기 전에, gazebo에 터틀봇을 올리고, 어떤 토픽이 있는지 확인해 보자.

> rostopic list

위 명령어를 입력해서 보면, /cmd_vel_mux/input/teleop토픽과 /scan 토픽을 확인할 수 있다.
/cmd_vel_mux/input/teleop은 터틀봇을 원격조종하기 위한 토픽이다.
우리가 터틀봇에게 내리는 이동명령은 /cmd_vel_mux/input/teleop토픽을 publish하면 된다.
/scan토픽은 터틀봇의 Lidar센서 정보를 담고있는 토픽이다.
Lidar센서의 정보를 읽어오려면 /scan토픽을 subscribe하면 된다.


이번에는 편의상 -135~135(deg)로 Lidar센서의 각도범위를 조절했으므로 바꿔주도록 하자. 기억이 안난다면 2.1절을 참조.

이제 wall tracking의 기본적인 아이디어를 살펴보자.
이번에는 터틀봇을 움직이는 것이 목적이므로 알고리즘은 매우 간단한 알고리즘을 사용한다.
벽을 마주칠때까지 -z방향으로 돌고, 벽을 마주치면 +z방향으로 돌아서 장애물을 오른쪽에 둔다.
오른쪽에 장애물이 있으면 직진, 전방과 오른쪽에 장애물을 감지하면 +z방향으로 회전하는 방식이다.

결과는 아래 동영상 링크에 첨부함.

[![wall tracking video](https://img.youtube.com/vi/RJQvuZxlY7Y/0.jpg)](https://www.youtube.com/watch?v=RJQvuZxlY7Y)