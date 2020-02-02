#!/usr/bin/python
import rospy
import click
import math
import actionlib

from geographiclib.geodesic import Geodesic
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped, PointStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def do_gps_goal(lat, long, marker_only=False):
    rospy.init_node('gps_goal')

    goal_lat = float(lat)
    goal_long = float(long)
    rospy.loginfo('Given GPS goal: lat %s, long %s.' % (goal_lat, goal_long))

    # Get the lat long coordinates of our map frame's origin which must be publshed on topic /local_xy_origin. 
    # We use this to calculate our goal within the map frame.
    
    origin_topic = '/local_xy_origin'
    rospy.loginfo('Listening for origin location on topic %s' % origin_topic)
    origin_pose = rospy.wait_for_message(origin_topic, PoseStamped, timeout=10)
    origin_lat = origin_pose.pose.position.y
    origin_long = origin_pose.pose.position.x
    rospy.loginfo('Received origin: lat %s, long %s.' % (origin_lat, origin_long))

    # Calculate distance and azimuth between GPS points
    geod = Geodesic.WGS84  # define the WGS84 ellipsoid
    g = geod.Inverse(origin_lat, origin_long, goal_lat, goal_long) # Compute several geodesic calculations between two GPS points 
    hypotenuse = distance = g['s12'] # access distance
    rospy.loginfo("The distance from the origin to the goal is {:.3f} m.".format(distance))
    azimuth = g['azi1']
    rospy.loginfo("The azimuth from the origin to the goal is {:.3f} degrees.".format(azimuth))

    # Convert polar (distance and azimuth) to x,y translation in meters (needed for ROS) by finding side lenghs of a right-angle triangle
    x = adjacent = math.cos(azimuth) * hypotenuse
    y = opposite = math.sin(azimuth) * hypotenuse
    rospy.loginfo("The translation from the origin to the goal is (x,y) {:.3f}, {:.3f} m.".format(x, y))

    # TODO(Dan): Set target yaw pose
    # import tf_conversions
    # if yaw:
    #   euler_tuple = tf_conversions.transformations.euler_from_quaternion(quaternion)
    # else:
    #   # Use azimuth as yaw

    # Publish goal as point message for visualization purposes
    marker_topic = 'point_to_marker' # publish GPS point in ROS coordinates for visualization
    point_publisher = rospy.Publisher(marker_topic, PointStamped, queue_size=10)
    rospy.sleep(1) # allow time for subscribers to join
    gps_point = PointStamped()
    gps_point.point.x = x
    gps_point.point.y = y
    gps_point.point.z = 0
    point_publisher.publish(gps_point)
    rospy.loginfo("Published point {:.3f}, {:.3f} on topic {}.".format(x, y, marker_topic))

    if marker_only:
        return

    # Create move_base goal
    rospy.loginfo("Connecting to move_base...")
    move_base = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    move_base.wait_for_server()
    rospy.loginfo("Connected.")
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.position.z =  0.0
    goal.target_pose.pose.orientation.x = 0.0
    goal.target_pose.pose.orientation.y = 0.0
    goal.target_pose.pose.orientation.z = 0.0
    goal.target_pose.pose.orientation.w = 1
    rospy.loginfo('Executing move_base goal to position (x,y) %s, %s.' %
            (goal.target_pose.pose.position.x, goal.target_pose.pose.position.y))
    rospy.loginfo("To cancel the goal: 'rostopic pub -1 /move_base/cancel actionlib_msgs/GoalID -- {}'")

    # Send goal
    move_base.send_goal(goal)
    rospy.loginfo('Inital goal status: %s' % GoalStatus.to_string(move_base.get_state()))
    status = move_base.get_goal_status_text()
    if status:
        rospy.loginfo(status)

    # Wait for goal result
    move_base.wait_for_result()
    rospy.loginfo('Final goal status: %s' % GoalStatus.to_string(move_base.get_state()))
    status = move_base.get_goal_status_text()
    if status:
        rospy.loginfo(status)

@click.command()
@click.option('--lat', prompt='Latitude', help='Latitude')
@click.option('--long', prompt='Longitude', help='Longitude')
@click.option('--marker-only', help='Only publish a marker at the gps location, do not execute goal', is_flag=True)
# @click.option('--yaw', '-y', help='Set target direction robot should be facing after reaching the goal (ie. target yaw)')
def main_gps_goal(lat, long, marker_only):
    """Send goal to move_base given latitude and longitude
    \b
    Two usage formats:
    gps_goal.py --lat 43.658 --long -79.379 # decimal format
    gps_goal.py --lat 43,39,31 --long -79,22,45 # DMS format"""

    # Get click arguments then call do gps goal
    do_gps_goal(lat, long, marker_only)

if __name__ == '__main__':
    main_gps_goal()
    rospy.spin()