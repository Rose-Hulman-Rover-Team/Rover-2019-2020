import math

import rospy

from std_msgs.msg import Float32
from sensor_msgs.msg import NavSatFix, NavSatStatus, TimeReference
from geometry_msgs.msg import TwistStamped


class RosNMEADriver(object):
    def __init__(self):
        self.fix_pub = rospy.Publisher('fix', NavSatFix, queue_size=1)
        #self.vel_pub = rospy.Publisher('vel', TwistStamped, queue_size=1)
        #self.heading_pub = rospy.Publisher('heading', Float32, queue_size=1)
        #self.time_ref_pub = rospy.Publisher('time_reference', TimeReference, queue_size=1)

        #self.time_ref_source = rospy.get_param('~time_ref_source', None)
        #self.use_RMC = rospy.get_param('~useRMC', False)

    def add_sentence(self, nmea_string, frame_id, timestamp=None):
        if not check_nmea_checksum(nmea_string):
            rospy.logwarn("Received a sentence with an invalid checksum. " +
                          "Sentence was: %s" % repr(nmea_string))
            return False

        parsed_sentence = libnmea_navsat_driver.parser.parse_nmea_sentence(nmea_string)
        if not parsed_sentence:
            rospy.logdebug("Failed to parse NMEA sentence. Sentece was: %s" % nmea_string)
            return False

        #if timestamp:
        #    current_time = timestamp
        #else:
        #    current_time = rospy.get_rostime()
        
        current_fix = NavSatFix()
        
        # current_fix.header.stamp = current_time
        # current_fix.header.frame_id = frame_id
        # current_time_ref = TimeReference()
        # current_time_ref.header.stamp = current_time
        # current_time_ref.header.frame_id = frame_id
        #if self.time_ref_source:
        #    current_time_ref.source = self.time_ref_source
        #else:
        #    current_time_ref.source = frame_id

        if not self.use_RMC and 'GGA' in parsed_sentence:
            data = parsed_sentence['GGA']
            gps_qual = data['fix_type']
            if gps_qual == 0:
                current_fix.status.status = NavSatStatus.STATUS_NO_FIX
            elif gps_qual == 1:
                current_fix.status.status = NavSatStatus.STATUS_FIX
            elif gps_qual == 2:
                current_fix.status.status = NavSatStatus.STATUS_SBAS_FIX
            elif gps_qual in (4, 5):
                current_fix.status.status = NavSatStatus.STATUS_GBAS_FIX
            elif gps_qual == 9:
                current_fix.status.status = NavSatStatus.STATUS_SBAS_FIX
            else:
                current_fix.status.status = NavSatStatus.STATUS_NO_FIX

            current_fix.status.service = NavSatStatus.SERVICE_GPS

            current_fix.header.stamp = current_time

            latitude = data['latitude']
            if data['latitude_direction'] == 'S':
                latitude = -latitude
            current_fix.latitude = latitude

            longitude = data['longitude']
            if data['longitude_direction'] == 'W':
                longitude = -longitude
            current_fix.longitude = longitude

            hdop = data['hdop']
            current_fix.position_covariance[0] = hdop ** 2
            current_fix.position_covariance[4] = hdop ** 2
            current_fix.position_covariance[8] = (2 * hdop) ** 2  # FIXME
            current_fix.position_covariance_type = \
                NavSatFix.COVARIANCE_TYPE_APPROXIMATED

            # Altitude is above ellipsoid, so adjust for mean-sea-level
            altitude = data['altitude'] + data['mean_sea_level']
            current_fix.altitude = altitude

            self.fix_pub.publish(current_fix)

            if not math.isnan(data['utc_time']):
                current_time_ref.time_ref = rospy.Time.from_sec(data['utc_time'])
                self.time_ref_pub.publish(current_time_ref)

        elif 'RMC' in parsed_sentence:
            data = parsed_sentence['RMC']

            # Only publish a fix from RMC if the use_RMC flag is set.
            if self.use_RMC:
                if data['fix_valid']:
                    current_fix.status.status = NavSatStatus.STATUS_FIX
                else:
                    current_fix.status.status = NavSatStatus.STATUS_NO_FIX

                current_fix.status.service = NavSatStatus.SERVICE_GPS

                latitude = data['latitude']
                if data['latitude_direction'] == 'S':
                    latitude = -latitude
                current_fix.latitude = latitude

                longitude = data['longitude']
                if data['longitude_direction'] == 'W':
                    longitude = -longitude
                current_fix.longitude = longitude

                current_fix.altitude = float('NaN')
                current_fix.position_covariance_type = \
                    NavSatFix.COVARIANCE_TYPE_UNKNOWN

                self.fix_pub.publish(current_fix)

                if not math.isnan(data['utc_time']):
                    current_time_ref.time_ref = rospy.Time.from_sec(data['utc_time'])
                    self.time_ref_pub.publish(current_time_ref)

            # Publish velocity from RMC regardless, since GGA doesn't provide it.
            if data['fix_valid']:
                current_vel = TwistStamped()
                current_vel.header.stamp = current_time
                current_vel.header.frame_id = frame_id
                current_vel.twist.linear.x = data['speed'] * \
                    math.sin(data['true_course'])
                current_vel.twist.linear.y = data['speed'] * \
                    math.cos(data['true_course'])
                self.vel_pub.publish(current_vel)

        elif 'VTG' in parsed_sentence:
            data = parsed_sentence['VTG']
            if data['heading'] or data['heading'] == 0.0:
                self.heading_pub.publish(Float32(data['heading']))

        else:
            return False

    """Helper method for getting the frame_id with the correct TF prefix"""

    @staticmethod
    def get_frame_id():
        frame_id = rospy.get_param('~frame_id', 'gps')
        if frame_id[0] != "/":
            """Add the TF prefix"""
            prefix = ""
            prefix_param = rospy.search_param('tf_prefix')
            if prefix_param:
                prefix = rospy.get_param(prefix_param)
                if prefix[0] != "/":
                    prefix = "/%s" % prefix
            frame_id = "%s/%s" % (prefix, frame_id)
            return frame_id[1:]
        else:
            return frame_id[1:]