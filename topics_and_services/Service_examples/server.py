#! /usr/bin/python3

import rospy
from beginner_tutorials.srv import message, messageResponse

def check_even_odd(req):
    print("returning {}".format(req.num))
    if req.num%2 == 0:
        return messageResponse('even')
    else:
        return messageResponse('odd')

def server():
    rospy.init_node('server')
    msg = rospy.Service('check_even_odd', message, check_even_odd)
    rospy.spin()

if __name__ == "__main__":
    
    server()