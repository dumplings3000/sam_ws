import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os

class ImageSubscriberSaver(Node):
    def __init__(self):
        super().__init__('image_subscriber_saver')
        self.subscription = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.listener_callback,
            10
        )
        self.subscription  # prevent unused variable warning
        self.bridge = CvBridge()
        self.image_count = 0
        self.save_path = 'src/object_detection/object_detection/images'
        if not os.path.exists(self.save_path):
            self.get_logger().info('Creating directory for images')
            os.makedirs(self.save_path)

    def listener_callback(self, msg):
        self.get_logger().info('Receiving video frame')
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        
        # Display the image
        cv2.imshow("Camera Feed", cv_image)
        cv2.waitKey(1)

        # Save the image
        self.get_logger().info('saving image')
        save_file = os.path.join(self.save_path +"/", f"{self.image_count:04d}.jpg")
        cv2.imwrite(save_file, cv_image)
        self.image_count += 1

def main(args=None):
    rclpy.init(args=args)
    image_subscriber_saver = ImageSubscriberSaver()
    rclpy.spin(image_subscriber_saver)
    image_subscriber_saver.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()