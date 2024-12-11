import subprocess
from distutils.spawn import find_executable

from ovos_bus_client.message import Message
from ovos_config import Configuration
from ovos_plugin_manager.templates.phal import AdminPlugin, AdminValidator, PHALPlugin, PHALValidator
from ovos_utils.log import LOG
from ovos_PHAL_plugin_network_manager.gui import GUISetup

# Event Documentation
# ===================
# Scanning: 
# ovos.phal.nm.scan
# - type: Request
# - description: Allows client to request for a network scan
#
# ovos.phal.nm.scan.complete
# - type: Response
# - description: Emited when the requested scan is completed
# with a network list
#
# Connecting:
# ovos.phal.nm.connect
# - type: Request
# - description: Allows clients to connect to a given network
#
# ovos.phal.nm.connection.successful
# - type: Response
# - description: Emitted when a connection is successfully established
#
# ovos.phal.nm.connection.failure
# - type: Response
# - description: Emitted when a connection fails to establish
#
# Disconnecting:
# ovos.phal.nm.disconnect
# - type: Request
# - description: Allows clients to disconnect from a network
#
# ovos.phal.nm.disconnection.successful
# - type: Response
# - description: Emitted when a connection successfully disconnects
#
# ovos.phal.nm.disconnection.failure
# - type: Response
# - description: Emitted when a connection fails to disconnect
#
# Forgetting:
# ovos.phal.nm.forget
# - type: Request
# - description: Allows a client to forget a network
#
# ovos.phal.nm.forget.successful
# - type: Response
# - description: Emitted when a connection successfully is forgetten
#
# ovos.phal.nm.forget.failure
# - type: Response
# - description: Emitted when a connection fails to forget


class NetworkManagerValidator(PHALValidator):
    @staticmethod
    def validate(config=None):
        # check if admin plugin is not enabled
        cfg = Configuration().get("PHAL", {}).get("admin", {})
        if cfg.get("ovos-PHAL-plugin-network-manager", {}).get("enabled"):
            # run this plugin in admin mode (as root)
            return False

        # check if nmcli is installed, assume polkit allows non-root usage
        LOG.info("ovos-PHAL-plugin-network-manager running as user")
        return find_executable("nmcli")


class NetworkManagerPlugin(PHALPlugin):
    validator = NetworkManagerValidator

    def __init__(self, bus=None, config=None):
        super().__init__(bus=bus, name="ovos-PHAL-plugin-network-manager", config=config)
        # Register Network Manager Events
        self.bus.on("ovos.phal.nm.scan", self.handle_network_scan_request)
        self.bus.on("ovos.phal.nm.connect", self.handle_network_connect_request)
        self.bus.on("ovos.phal.nm.connect.open.network", self.handle_open_network_connect_request)
        self.bus.on("ovos.phal.nm.reconnect", self.handle_network_reconnect_request)
        self.bus.on("ovos.phal.nm.disconnect", self.handle_network_disconnect_request)
        self.bus.on("ovos.phal.nm.forget", self.handle_network_forget_request)
        self.bus.on("ovos.phal.nm.get.connected", self.handle_network_connected_query)
        self.gui_setup = GUISetup(bus=bus)  # extra GUI events

    # Network Manager Events
    def handle_network_scan_request(self, message):
        # Scan for networks using Network Manager and build a list of networks found and their security types
        LOG.info("Scanning for networks using nmcli backend")
        subprocess.Popen(
            ['nmcli', 'dev', 'wifi', 'rescan']
        )
        scan_process = subprocess.Popen(
            ["nmcli", "--terse", "--fields", "SSID,SECURITY", "device", "wifi", "list"], stdout=subprocess.PIPE)
        scan_output = scan_process.communicate()[0].decode("utf-8").split("\n")

        # We will use the output to build a list of networks and their security types
        networks_list = []
        for line in scan_output:
            if line != "":
                line_split = line.split(":")
                networks_list.append({"ssid": line_split[0], "security": line_split[1]})
        # Emit the list of networks and their security types
        self.bus.emit(Message("ovos.phal.nm.scan.complete",
                              {"networks": networks_list}))

    def handle_network_connect_request(self, message):
        network_name = message.data.get("connection_name", "")
        secret_phrase = message.data.get("password", "")
        security_type = message.data.get("security_type", "")

        # First check we have a valid network name
        if network_name is None or network_name == "":
            LOG.error("No network name provided")
            return

        # Check if the password is provided if the security type is not open
        if security_type != "open" and secret_phrase is None:
            LOG.error("No password provided")
            self.bus.emit(Message("ovos.phal.nm.connection.failure",
                                  {"errorCode": 0, "errorMessage": "Password Required"}))
            return

        # Handle different backends
        connection_process = subprocess.Popen(
            ["nmcli", "device", "wifi", "connect", network_name, "password", secret_phrase], stdout=subprocess.PIPE)
        connection_output = connection_process.communicate()[0].decode("utf-8").split("\n")
        if "successfully activated" in connection_output[0]:
            self.bus.emit(Message("ovos.phal.nm.connection.successful",
                                  {"connection_name": network_name}))
        else:
            if "(7)" in connection_output[0] or "(10)" in connection_output[0]:
                self.handle_network_forget_request(Message("ovos.phal.nm.forget",
                                                           {"connection_name": network_name}))

            self.bus.emit(Message("ovos.phal.nm.connection.failure",
                                  {"errorCode": 1, "errorMessage": "Connection Failed"}))

    def handle_open_network_connect_request(self, message):
        network_name = message.data.get("connection_name", "")

        # First check we have a valid network name
        if network_name is None or network_name == "":
            LOG.error("No network name provided")
            return

        connection_process = subprocess.Popen(
            ["nmcli", "device", "wifi", "connect", network_name], stdout=subprocess.PIPE)
        connection_output = connection_process.communicate()[0].decode("utf-8").split("\n")
        if "successfully activated" in connection_output[0]:
            self.bus.emit(Message("ovos.phal.nm.connection.successful",
                                  {"connection_name": network_name}))
        else:
            self.bus.emit(Message("ovos.phal.nm.connection.failure",
                                  {"errorCode": 1, "errorMessage": "Connection Failed"}))

    def handle_network_reconnect_request(self, message):
        network_name = message.data.get("connection_name", "")
        connection_process = subprocess.Popen(
            ["nmcli", "connection", "up", network_name], stdout=subprocess.PIPE)
        connection_output = connection_process.communicate()[0].decode("utf-8").split("\n")
        if "successfully activated" in connection_output[0]:
            self.bus.emit(Message("ovos.phal.nm.connection.successful",
                                  {"connection_name": network_name}))
        else:
            self.bus.emit(Message("ovos.phal.nm.connection.failure",
                                  {"errorCode": 1, "errorMessage": "Connection Failed"}))

    def handle_network_disconnect_request(self, message):
        network_name = message.data.get("connection_name", "")

        # First check we have a valid network name
        if network_name is None or network_name == "":
            LOG.error("No network name provided")
            return

        # Handle different backends
        disconnection_process = subprocess.Popen(
            ["nmcli", "connection", "down", network_name], stdout=subprocess.PIPE)
        disconnection_output = disconnection_process.communicate()[0].decode("utf-8").split("\n")
        # if disconnection output contains the words "Connection" and "successfully deactivated"
        if "successfully deactivated" in disconnection_output[0]:
            self.bus.emit(Message("ovos.phal.nm.disconnection.successful",
                                  {"connection_name": network_name}))
        else:
            self.bus.emit(Message("ovos.phal.nm.disconnection.failure"))

    def handle_network_forget_request(self, message):
        network_name = message.data.get("connection_name", "")

        # First check we have a valid network name
        if network_name is None or network_name == "":
            LOG.error("No network name provided")
            return

        forget_process = subprocess.Popen(
            ["nmcli", "connection", "delete", network_name], stdout=subprocess.PIPE)
        forget_output = forget_process.communicate()[0].decode("utf-8").split("\n")
        if "successfully deleted" in forget_output[0]:
            self.bus.emit(Message("ovos.phal.nm.forget.successful",
                                  {"connection_name": network_name}))
        else:
            self.bus.emit(Message("ovos.phal.nm.forget.failure"))

    def handle_network_connected_query(self, message):
        connected_process = subprocess.Popen(
            ["nmcli", "connection", "show", "--active"], stdout=subprocess.PIPE)
        connected_output = connected_process.communicate()[0].decode("utf-8").split("\n")

        for entry in connected_output:
            if entry == connected_output[0]:
                continue
            if "wifi" or "ethernet" or "wimax" in connected_output[1]:
                self.bus.emit(Message("ovos.phal.nm.is.connected",
                                      {"connection_name": connected_output[1].split(" ")[0]}))
                break
        else:
            self.bus.emit(Message("ovos.phal.nm.is.not.connected"))


class NetworkManagerAdminValidator(AdminValidator, NetworkManagerValidator):
    @staticmethod
    def validate(config=None):
        LOG.info("ovos-PHAL-plugin-network-manager running as root")
        # check if nmcli is installed
        return find_executable("nmcli")


class NetworkManagerAdminPlugin(AdminPlugin, NetworkManagerPlugin):
    validator = NetworkManagerAdminValidator
