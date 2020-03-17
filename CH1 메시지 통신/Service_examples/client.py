#! /usr/bin/python3

import rospy
from beginner_tutorials.srv import *
import sys

def check(num): #들어온 숫자의 홀짝을 구분
    rospy.wait_for_service('check_even_odd') #check_even_odd 서비스가 활성화 될때까지 대기, 즉 서버의 활성화를 기다림

    try:
        odd_even = rospy.ServiceProxy('check_even_odd', message) #서비스 통신을 위해 핸들을 생성
        result = odd_even(num) #메시지 형식에 맞게 값을 입력
        return result
    except rospy.ServiceException as e:
        print("service call failed : {}".format(e))

if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        num = int(sys.argv[1])
    else:
        print("wrong format")
        sys.exit(1)

    print("requesting {}".format(num))
    print("{} is a {} number".format(num, check(num).msg))