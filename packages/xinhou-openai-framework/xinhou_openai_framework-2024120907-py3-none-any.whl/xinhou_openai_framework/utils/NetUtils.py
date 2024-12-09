import socket
import psutil  # This module requires installation via pip ('pip install psutil')


class NetUtils:
    """
    A helper class for network-related operations.
    """

    def __init__(self):
        self.name = 'NetUtil'

    @classmethod
    def get_host_ip(cls):
        """
        Get the IP address of the host machine.

        Returns:
            str: The IP address of the host machine.
        """
        try:
            st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            st.connect(('10.255.255.255', 1))
            IP = st.getsockname()[0]
        except socket.error as e:
            print(f"Socket error: {e}. Defaulting to localhost.")
            IP = '127.0.0.1'
        finally:
            st.close()
        return IP

    @classmethod
    def get_host_name(cls):
        """
        Get the hostname of the host machine.

        Returns:
            str: The hostname of the host machine.
        """
        return socket.gethostname()

    @classmethod
    def get_gateway_ip(cls):
        """
        Get the default gateway IP address.

        Returns:
            str: The default gateway IP address.
        """
        try:
            return psutil.net_if_addrs()['default'][2].address
        except (KeyError, IndexError):
            return "Gateway IP not found"

    @classmethod
    def get_network_interfaces(cls):
        """
        Get a list of network interfaces on the host machine.

        Returns:
            list: A list of network interface names.
        """
        return psutil.net_if_addrs().keys()


if __name__ == '__main__':
    net_helper = NetUtils()
    print("Host IP:", net_helper.get_host_ip())
    print("Host Name:", net_helper.get_host_name())
    print("Default Gateway IP:", net_helper.get_gateway_ip())
    print("Network Interfaces:", net_helper.get_network_interfaces())
