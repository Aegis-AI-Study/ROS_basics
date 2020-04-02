#! /usr/bin/python3

import rospy
import sys
import cv2
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

class imageHandler():
    def __init__(self):
        self.image_pub=rospy.Publisher("publish_image_name",Image)
        self.image_sub=rospy.Subscriber("/webcam_camera/image_raw",Image,self.callback)
        self.bridge=CvBridge()
        
    def callback(self, data):
        cv_image=self.bridge.imgmsg_to_cv2(data, "bgr8")
        
        (rows, cols, channels)=cv_image.shape
        
        cv2.imshow("image window", cv_image)
        cv2.waitKey(3)
        
def main(args):
    handler=imageHandler()
    rospy.init_node("image_handle", anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shutting down")
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
    main(sys.argv)