#! /usr/bin/python3

import rospy
from std_msgs.msg import String

def callback(message): #값이 들어오게 되면 실행 된
    print(message.data) #받아들인 메시지의 data 만을 테미널에 출력

def subscriber():

    rospy.init_node('subscriber', anonymous=True) #노드 초기화
    rospy.Subscriber('messenger', String, callback=callback) #Subscriber 인스턴스 생성

    rospy.spin() #토픽이 갱신될때까지 대기

if __name__ == "__main__":
    subscriber()