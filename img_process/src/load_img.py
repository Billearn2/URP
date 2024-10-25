#!/usr/bin/env python3
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def image_callback(msg):
    bridge = CvBridge()
    try:
        # ROS 이미지를 OpenCV 이미지로 변환
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
    except CvBridgeError as e:
        rospy.logerr(f"CvBridge Error: {e}")
        return

    # OpenCV의 imshow를 사용해 이미지 표시
    cv2.imshow("Camera Feed", cv_image)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        rospy.signal_shutdown("User requested shutdown.")

def main():
    # ROS 노드 초기화
    rospy.init_node('image_subscriber_node', anonymous=True)
    
    # 이미지 구독자 생성
    rospy.Subscriber('/camera/image_raw', Image, image_callback)

    rospy.loginfo("Image subscriber node started.")
    
    # OpenCV 창이 닫힐 때까지 ROS 스핀 실행
    rospy.spin()

    # 자원 해제
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
