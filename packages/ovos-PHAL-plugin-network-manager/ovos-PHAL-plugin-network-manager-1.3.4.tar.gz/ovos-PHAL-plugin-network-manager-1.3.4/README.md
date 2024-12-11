# PHAL plugin - Network Manager

Provides the network manager interface for NetworkManager based plugins.
This plugin utilizes nmcli for all communications with network manager.
The dbus interface for this plugin is a work in progress. [#15](https://github.com/OpenVoiceOS/ovos-PHAL-plugin-network-manager/pull/15)

# Requires
This plugin has the following requirements:
- nmcli

It also provides a GUI interface to setup wifi on screen, in this case you also need:
- Plasma Network Manager: https://invent.kde.org/plasma/plasma-nm

# Install

`pip install ovos-PHAL-plugin-network-manager`

# Config

This plugin is a Admin plugin, it needs to run as root and to be explicitly enabled in mycroft.conf

```javascript
{
"PHAL": {
    "admin": {
        "ovos-PHAL-plugin-network-manager": {"enabled": true}
    }
}
}
```
if not enabled (omit config above) it will be run as the regular user, you need to ensure [polkit policy](https://github.com/OpenVoiceOS/ovos-buildroot/blob/5c7af8b05892206846ae06adb3478f1df620bf6b/buildroot-external/rootfs-overlay/base/etc/polkit-1/rules.d/50-org.freedesktop.NetworkManager.rules) is set to allow usage of nmcli without sudo

# Event Details:

##### Scanning

This plugin provides scanning operations for Network Manager to scan for available nearby networks, the following event can be used to initialize the scan.

```python
# Scanning: 
# ovos.phal.nm.scan
# - type: Request
# - description: Allows client to request for a network scan
#
# ovos.phal.nm.scan.complete
# - type: Response
# - description: Emited when the requested scan is completed
# with a network list
```

##### Connecting

This plugin provides handling of connection operations for Network Manager, the following events can be used to connect a network, disconnect a network using the network manager interface.

```python

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
```

##### Forget Networks

The plugin also provides a interface to forget already connected networks, The following events can be used to forget a network

```python
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
```
