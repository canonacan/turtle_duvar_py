
import math

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist


class TurtleDuvar(Node):

    def __init__(self):
        super().__init__('turtle_duvar')

        # Parametreleri tanımla
        self.declare_parameter('speed', 2.0)
        self.declare_parameter('turn_speed', 1.5)

        self.declare_parameter('min_x', 1.0)
        self.declare_parameter('max_x', 10.0)
        self.declare_parameter('min_y', 1.0)
        self.declare_parameter('max_y', 10.0)

        # Parametre değerlerini oku
        self.speed = self.get_parameter('speed').value
        self.turn_speed = self.get_parameter('turn_speed').value

        self.min_x = self.get_parameter('min_x').value
        self.max_x = self.get_parameter('max_x').value
        self.min_y = self.get_parameter('min_y').value
        self.max_y = self.get_parameter('max_y').value

        # Kaplumbağanın konum bilgilerini dinle
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # Hareket komutlarını gönder
        self.publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        # Başlangıç konum ve yön bilgileri
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.pose_received = False

        # Dönüş kontrol değişkenleri
        self.turning = False
        self.target_theta = 0.0

        # Kontrol ve konum yazdırma zamanlayıcıları
        self.timer = self.create_timer(
            0.1,
            self.control_loop
        )

        self.log_timer = self.create_timer(
            1.0,
            self.log_position
        )

        self.get_logger().info(
            'Duvardan kacan kaplumbaga baslatildi.'
        )

        self.get_logger().info(
            f'Hiz: {self.speed}, Donus hizi: {self.turn_speed}'
        )

        self.get_logger().info(
            f'X siniri: {self.min_x}-{self.max_x}, '
            f'Y siniri: {self.min_y}-{self.max_y}'
        )

    def pose_callback(self, msg):
        """Kaplumbaganin konum ve yon bilgisini al."""
        self.x = msg.x
        self.y = msg.y
        self.theta = msg.theta
        self.pose_received = True

    def normalize_angle(self, angle):
        """Aciyi -pi ile pi araligina getir."""
        return math.atan2(
            math.sin(angle),
            math.cos(angle)
        )

    def control_loop(self):
        """Konumu kontrol et ve hareket komutu uret."""
        if not self.pose_received:
            return

        cmd = Twist()

        # Kaplumbaga belirlenen sinirlarin disinda mi?
        near_wall = (
            self.x < self.min_x
            or self.x > self.max_x
            or self.y < self.min_y
            or self.y > self.max_y
        )

        # Sinir disindaysa alanin merkezine dogru hedef aciyi hesapla
        if near_wall and not self.turning:
            center_x = (self.min_x + self.max_x) / 2.0
            center_y = (self.min_y + self.max_y) / 2.0

            self.target_theta = math.atan2(
                center_y - self.y,
                center_x - self.x
            )

            self.turning = True

        if self.turning:
            # Hedef yon ile mevcut yon arasindaki aci farki
            angle_error = self.normalize_angle(
                self.target_theta - self.theta
            )

            # Hedef yone yeterince yaklastiysa ileri git
            if abs(angle_error) < 0.15:
                self.turning = False
                cmd.linear.x = self.speed
                cmd.angular.z = 0.0

            else:
                # Yerinde don
                cmd.linear.x = 0.0

                if angle_error > 0.0:
                    cmd.angular.z = self.turn_speed
                else:
                    cmd.angular.z = -self.turn_speed

        else:
            # Sinir disinda degilse ileri git
            cmd.linear.x = self.speed
            cmd.angular.z = 0.0

        self.publisher.publish(cmd)

    def log_position(self):
        """Konumu saniyede bir terminale yazdir."""
        if self.pose_received:
            self.get_logger().info(
                f'Konum: x={self.x:.2f}, y={self.y:.2f}'
            )

    def stop_turtle(self):
        """Dugum kapanirken kaplumbagayi durdur."""
        self.publisher.publish(Twist())


def main(args=None):
    rclpy.init(args=args)
    node = TurtleDuvar()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.stop_turtle()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
