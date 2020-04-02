# CH3.1 OpenCV 창에서 카메라 영상 띄우기

카메라가 찍고있는 영상은 OpenCV이미지 영상이다.  
ROS시스템에서 OpenCV이미지를 직접 주고받는 것은 불가능하므로 우리는 카메라가 담고있는 이미지를 OpenCV이미지로 변환한 후, CvBridge를 이용하여 ROS 이미지 메시지로 변환해야 한다.  
발행된 이미지 메시지를 수신할 때도 마찬가지로 CvBridge를 이용하여 OpenCV메시지로 변환하여 발행된 이미지를 직접 확인 해볼 수 있다.  
이미지 메시지의 발행은 Gazebo플러그인이 해주고 있으므로 이번에는 수신받아 확인해 보는 작업을 해보자.  

## 토픽 이름 확인하기
저번 챕터에서 카메라를 추가해 봤다. 터틀봇 환경을 구축하고 다른 터미널에서 아래 명령어로 토픽이름을 확인해 보자.

	rostopic list
	
그 중에서 /webcam_camera/image_raw 토픽을 확인할 수 있을 것이다.  
이 토픽이 gazebo의 카메라 영상을 이미지 메시지로 발행하는 토픽이다.  
따라서 우리는 Subscriber를 만들어 이 이미지 메시지를 수신해 볼 것이다.

## 코드 설명
이번 코드에는 이미지 핸들러 클래스를 만들어 봤다.  
주로 봐야할 곳은 callback함수 쪽인데, CvBridge.imgmsg_to_cv2 메소드로 이미지 메시지를 OpenCV 이미지로 바꿔준다.  
gazebo에서 토픽을 갱신할 때 마다 OpenCV 창에 변환된 이미지를 띄우고 waitkey 메소드로 ctrl+C 키가 입력되길 기다린다.  
마찬가지로 main 함수에서 키보드 인터럽트가 발생하면 모든 창을 닫는 함수가 실행된다. 이 구조로 해놓지 않으면 창을 닫는데 매우 수고스러울 수 있으므로 OpenCV 코드를 짤때는 destroyAllWindows 부분을 주의깊게 살펴보아야 한다.

## 결과
영상으로 확인해 보자.(구좋알 팍팍)
[![opencv video](https://img.youtube.com/vi/VMaZyb9xJM8/0.jpg)](https://www.youtube.com/watch?v=VMaZyb9xJM8)