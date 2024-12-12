# Wi-Fi Connection 

This package provides commands to interact with Wi-Fi connections on Windows.

## Installation

Install the `wifi_connection` package using pip:

```bash
pip install wifi_connection
```

## Usage
1. Python code  
    ```python
    import wifi_connection
    ```
2. Command  
https://www.youtube.com/watch?v=20PbKNIRKfo

## Example
```python
import wifi_connection

# Get the list of available network interfaces
interfaces = wifi_connection.get_interfaces()
print("Available interfaces:", interfaces)

# Get the list of available networks for a specific interface
interface_name = "wlan0"  # Example interface name
networks = wifi_connection.get_network_list(interface_name)
print("Available networks for", interface_name + ":", networks)

# Set a network profile
ssid = "MyWiFiNetwork"  # Example SSID
password = "password123"  # Example password
band = "5"  # the ssid's band that you want to connect(2, 5 or 6)
success = wifi_connection.set_profile(interface_name, band, ssid, password)
print("Profile set successfully:", success)

# Connect to a network
success = wifi_connection.connect(interface_name, ssid)
print("Connection successful:", success)

# Get the SSID of the connected network
connected_ssid = wifi_connection.get_ssid(interface_name)
print("Connected SSID:", connected_ssid)

# Refresh the list of available networks
refresh_success = wifi_connection.refresh(interface_name)
print("Refresh successful:", refresh_success)

# Get the profile of a specific SSID network
profile_name = "MyWiFiNetwork"  # Example profile name
profile_content = wifi_connection.get_profile(interface_name, profile_name)
print("Profile content for", profile_name + ":", profile_content)

# Get connection information for a specified interface
connection_info = wifi_connection.get_connection_info(interface_name)
print("Connection information for", interface_name + ":", connection_info)
```

## Functions

### `settings`

Enable or disable printing of results.

- **Parameters:**
  - `set_print`: Flag to enable/disable printing. (Optional, Default: True)

### `get_interfaces`

Get the list of available network interfaces.

- **Return Value:**
  - List of available network interfaces.

### `get_network_list`

Get the dictionary of available networks for the specified interface.

- **Parameters:**
  - `iface_name`: Interface name. (Required)

- **Return Value:**
  - Dictionary of available networks. {SSID: RSSI}

### `set_profile`

Set a network profile for the specified interface.

- **Parameters:**
  - `iface_name`: Interface name. (Required)
  - `band`: Wireless band. (Required)
  - `ssid`: SSID of the network. (Required)
  - `pwd`: Password of the network. (Optional, ignore if the network does not require a password)
  - `auto`: Enable or disable automatic connection to the network. (Optional, Default: True)

- **Return Value:**
  - True if the profile is set successfully, False otherwise.

### `connect`

Connect to a network with the specified SSID using the specified interface.  
**If a profile for the network does not exist, make sure to first set the profile using `set_profile`.**

- **Parameters:**
  - `iface_name`: Interface name. (Required)
  - `ssid`: SSID of the network. (Required)

- **Return Value:**
  - True if the connection is successful, False otherwise.

### `refresh`

Refresh the list of available networks for the specified interface.

- **Parameters:**
  - `iface_name`: Interface name. (Required)

- **Return Value:**
  - True if the refresh is successful, False otherwise.

### `get_ssid`

Get the SSID of the connected network for the specified interface.

- **Parameters:**
  - `iface_name`: Interface name. (Required)

- **Return Value:**
  - SSID of the connected network, or an error if the interface is not connected to any network.

### `get_profile`

Get the Profile of the SSID network for the specified interface.

- **Parameters:**
  - `iface_name`: Interface name. (Required)
  - `profile_name`: Profile name. (Required)

- **Return Value:**
  - Profile content

### `get_connection_info`

Retrieve connection information for a specified network interface.

- **Parameters:**
  - `iface_name`: Interface name. (Required)

- **Return Value:**
  - JSON string containing connection information for the specified interface.  
    Example: 
    ```json
    {
      "RxSpeed": 574000,
      "TxSpeed": 117000,
      "Channel": 3,
      "Frequency": 2422000,
      "RSSI": -33,
      "Protocol": "dot11_phy_type_he"
    }
    ```

### `get_computer_info`

Retrieve information about the computer.

- **Parameters:**
  - `iface_name`: Interface name. (Required)

- **Return Value:**
  - JSON string containing information about the computer for the specified interface.  
    Example: 
    ```json
    {
      "WiFiDriverVersion": "22.220.0.4", 
      "WiFiDriverDate": "20230329", 
      "WiFiDriverProviderName": "Intel", 
      "OS": "Microsoft Windows 11 專業版", 
      "OSBuild": "22631", 
      "OSVersion": "23H2", 
      "CPU": "13th Gen Intel(R) Core(TM) i7-13700HX"
    }
    ```

### `get_tput_name`

Retrieves the name for the second argument (`tput_name`) of the `graph` function.

- **Parameters:**
  - None

- **Return Value:**
  - List of available throughput name.

### `graph` (only in version 0.1.7)

Generates a real-time graph showing throughput and RSSI (Received Signal Strength Indication).

- **Parameters:**
  - `iface_name` (str): Interface name. (Required)
  - `tput_name` (str): The name for getting throughput, obtained from the `get_tput_name` function. (Required)
  - `data` (str): Specifies the type of data to graph. Options are rx, tx, rssi, trx, txrssi, rxrssi. Default is rxrssi. (Optional)
  - **Note: First two arguments may be the same.**

- **Return Value:**
  - None
