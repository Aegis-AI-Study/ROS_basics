#토픽과 서비스

ROS의 메시지 통신 방법에는 크게 세가지 방식이 있다.
1. Topic : publisher와 subscriber로 나뉘어 publisher는 송신만, subscriber는 수신만 하는 단방향 비동기 통신
2. Service : server와 client로 나뉘어 client의 요청을 server가 처리후 반환하는 양방향 동기 통신
3. Action : client의 goal에 맞춰 server가 feedback과 result를 반환하는 양방향 비동기 통신
각각의 통신 방법에는 장단이 있어서 각자 필요에 맞는 통신방식을 사용하면된다

ROS 메시지 통신의 기본적인 구현의 순서는 아래와 같다

1. .msg .srv .action 파일로 데이터 형식 지정
2. CMakeLists.txt 에서 의존성 리스트 갱신
3. cmake를 통해 자동으로 필요한 함수 생성

먼저 .msg(.srv .action) 파일의 구조를 살펴보자
다음은 .msg파일의 예시이다

	float32 real
	float32 imaginary

위의 .msg파일은 복소수를 구현하기 위해 임의로 만든 메시지 파일이다
실수부(real)와 허수부(imaginary)를 float32 형식으로 지정했다는 의미다
ROS에서 기본적으로 제공해주는 메시지형식은 다음과 같다

	bool : 부울
	int8	: 8비트 정수
	uint8 : 부호없는 8비트 정수
	int16 : 16비트 정수
	uint16 : 부호없는 16비트 정수
	int32 : 32비트 정수
	uint32 : 부호없는 32비트 정수
	int64 : 64비트 정수
	uint64 : 부호없는 64비트 정수
	float32 : 32비트 부동 소수
	float64 : 64비트 부동 소수
	string : 아스키 문자열
	time : rospy.Time(duration을 나타냄)

>C++에서는 더 다양한 자료형을 제공한다. 
위의 정수형은 전부 python내부에서 int로 처리되는데
uint8로 작성된 프로그램은 c++에서는 정상적으로 동작하나, 파이썬에서는 음수 혹은 255보다 큰 숫자가 들어갈 수 있으므로 사용에 주의해야 한다.
이런 오류가 발생한다면 오류를 찾아내는것이 상당히 까다로우므로 부호없는 자료형을 파이썬에서 다룰 때에는 주의를 기율이자.

다음은 .srv(서비스 통신) 파일의 예시다

	string words
	---
	int count
	
위의 .srv 파일은 문자열(words)의 길이(count)를 측정하기위해 만들어진 서비스 파일이다
구분선을 기준으로 윗부분은 서버의 입력 데이터 형식, 아랫부분은 서버의 반환 데이터의 형식을 나타낸다

마지막으로 .action(액션 통신) 파일의 예시다

	duration time_to_wait
	---
	duration time_elapsed
	uint32 updates_sent
	---
	duration time_elapsed
	duration time_remaining

위 액션파일은 일정 시간을 대기하는 명령 중간에 남은시간과 소요된 시간을 알려주고,
최종적으로 걸린 시간과 업데이트 횟수를 결과로 나타내는 액션을 구현하기 위해 만들어진 파일이다
상단부의 time_to_wait은 해당 액션의 목표를 설정하는 부분이며
중단부는 액션이 종료됐을 시의 반환값,
하단부는 액션이 완료되기 전, 피드백에 해당되는 부분이다

다음으로 CMakeLists.txt 의존성 갱신을 해보자
CMakeLists.txt 안에는 ROS패키지의 의존성 정보를 담은 수많은 정보들이 존재한다
우리가 새롭게 정의한 메시지를 시스템에게 알려주기 위해 CMakeLists.txt 안에 다음을 추가한다

	<build_depend>message_generation</build_depend>
	<exec_depend>message_runtime</exec_depend>

message_generation 패키지를 추가해야 하므로 다음과 같이 추가한다

	find_package(catkin REQUIRED COMPONENTS
		roscpp
		rospy
		std_msgs
		message_generation
	)

런타임 의존성도 추가해 주자

	catkin_package(
	...
	CATKIN_DEPENDS message_runtime ...
	...)

우리가 작성한 메시지 파일도 추가해 주자

	add_message_files(
		FILES
		name_of_file.msg
	)

.msg(.srv .action)파일은 각각 패키지 최상위 디렉토리 msg(srv, action) 폴더에 넣어주어야 한다
>.srv .action도 마찬가지로 add_service_files, add_action_files 안에 파일이름을 추가해주면 된다

마지막으로 generate_messages 함수가 실행되도록 해주자

	generate_messages(
		DEPENDENCIES
		std_msgs
	)
	

다음은 노드를 작성하는 방법이다

## Topic
토픽은 publisher와 subscriber가 상호간에 메시지를 주고받는 방식이다
먼저 publisher를 구현해 보자
publisher는 rospy의 Publisher클래스를 이용한다
Publisher 클래스는 다음과 같이 인자를 받아들인다
>rospy.Publisher(name,data_class,queue_size)

순서대로 노드의 이름, 주고받는 메시지의 형식, 그리고 메시지 큐의 크기를 나타낸다
publisher의 선언이 완료되면 publish() 메소드로 메시지를 발행하면 된다

다음은 subscriber의 구현이다
subscriber는 publisher와 마찬가지로 Subscriber 클래스를 사용하면 되는데,
publisher가 메시지를 발행 할때까지 대기해야 한다

>rospy.Subscriber(name, data_class, callback)

subscriber는 publisher와 다르게 콜백 함수를 인자로 받아들인다
콜백 함수는 subscriber가 새로운 메시지를 읽어올 때마다 실행되는 함수를 말한다

## Service

서비스는 서버와 클라이언트가 메시지를 주고받는 방식이다
catkin_make를 실행하여 패키지를 빌드하면 시스템이 자동으로 서비스 클래스를 만들어 준다

>from YOUR_PACKAGE_NAME.srv import *

위 명령어로 생성된 파이썬 파일안의 클래스들을 불러올 수 있다
이렇게 불러온 클래스 안에는 서비스 클래스등이 정의되어 있다
서비스 클래스의 이름은 전부 서비스 파일명+Response 등으로 파일이름과 비슷하므로 필요한 클래스만을 따로 불러오는것도 가능하다

>rospy.Service(name, service_class, handler)

위의 명령어를 통해 통신에 필요한 서버를 생성할 수 있다

다음은 클라이언트의 구현 방법이다
클라이언트는 서버에 필요한 값들을 넘겨주고 결과를 기다린다

>rospy.ServiceProxy(name, service_class)

위 클래스를 선언하면 서버에 값을 넘겨줄 수 있다

서비스 통신에서는 서버와 클라이언트의 서비스 클래스가 일치해야 하며,
서비스 파일에 정의된 대로의 입출력 양식을 지켜야 한다(액션도 마찬가지)
## Action

액션은 잘 안 쓰이므로 생략