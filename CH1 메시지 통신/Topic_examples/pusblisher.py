#! /usr/bin/python3

import rospy
from std_msgs.msg import String
import sys

def publisher():
    pub = rospy.Publisher('messenger', String, queue_size=10) #Publisher 클래스의 인스턴스 선언, 데이터 형식이 String 타입임에 주의
    rospy.init_node('publisher', anonymous=True) #노드 초기화

    while not rospy.is_shutdown(): #ROS 시스템이 꺼지기 전까지
        try:
            message = input() #터미널로 문자열을 입력받아
            pub.publish(message) # 메시지로 발행
        except KeyboardInterrupt:
            sys.exit(1)

if __name__ == "__main__":
    try:
        publisher()
    except rospy.ROSInternalException:
        pass