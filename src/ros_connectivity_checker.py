#!/usr/bin/env python
import rospy
from kobuki_msgs.msg import Sound
from multimaster_msgs_fkie.srv import DiscoverMasters


def init():
    rospy.init_node('radio_ros_connectivity_checker')
    desired_no_masters = rospy.get_param("~desired_no_masters", 2)
    sound_pub = rospy.Publisher('mobile_base/commands/sound', Sound, queue_size=1)
    print desired_no_masters
    duration = 10
    while not rospy.is_shutdown():
        try:
            rospy.wait_for_service('/master_discovery/list_masters', timeout = 10)
            service = rospy.ServiceProxy('/master_discovery/list_masters', DiscoverMasters)
            test = service()
            print len(test.masters)
            if len(test.masters) < desired_no_masters:
                sound_msg = Sound()
                sound_msg.value = 6
                sound_pub.publish(sound_msg)
                duration = 2
            else:
                duration = 10
        except (rospy.ServiceException, rospy.exceptions.ROSException) as e:
            print e
        rospy.sleep(duration)

if __name__ == '__main__':
    init() 