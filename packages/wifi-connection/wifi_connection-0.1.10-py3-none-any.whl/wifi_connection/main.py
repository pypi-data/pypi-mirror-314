import typer
from typing_extensions import Annotated, Optional
from wifi_connection.wlanapi import *
from enum import Enum
import json

app = typer.Typer()
isprint = True

wlan = Wlanapi()

class DataName(str, Enum):
    rx = "rx"
    tx = "tx"
    rssi = "rssi"
    trx = "trx"
    txrssi = "txrssi"
    rxrssi = "rxrssi"

def get_guid(iface_name):
    interfaces = wlan.get_interfaces()

    guid = None
    if interfaces:
        for iface in interfaces:
            if iface.strInterfaceDescription == iface_name:
                guid = iface.InterfaceGuid
    
    if not guid:
        print("Can't find {}".format(iface_name))

    return guid

@app.command()
def get_interfaces():
    """
    Get the list of available network interfaces.
    """
    global isprint
    wlan.openhandle()

    interfaces = wlan.get_interfaces()

    interface_list = []
    if interfaces:
        for i in range(len(interfaces)):
            interface_list.append(interfaces[i].strInterfaceDescription)

    if isprint:
        print(interface_list)

    wlan.closshandle()

    return interface_list

@app.command()
def get_network_list(iface_name: Annotated[str, typer.Argument(help = "Interface name")]):
    """
    Get the list of available networks for the specified interface
    """
    wlan.openhandle()

    networks = None
    guid = get_guid(iface_name)
    if guid:
        networks = wlan.get_available_network(guid)

        if isprint:
            print(networks)
    
    wlan.closshandle()

    return networks

@app.command()
def set_profile(iface_name: Annotated[str, typer.Argument(help = "Interface name")],
                band: Annotated[int, typer.Option(help = "Wireless band")],
                ssid: Annotated[str, typer.Option(help = "SSID of the network")],
                pwd: Annotated[Optional[str], typer.Option(help = "Password of the network")] = None,
                auto: Annotated[Optional[bool], typer.Option(help = "Automatically connect to the network or not")] = True):
    
    """
    Set a network profile for the specified interface.
    """

    result = False
    wlan.openhandle()

    guid = get_guid(iface_name)
    if guid:
        result = wlan.set_profile(guid, band, ssid, pwd, auto)

    wlan.closshandle()

    return result

@app.command()
def connect(iface_name: Annotated[str, typer.Argument(help = "Interface name")], ssid: Annotated[str, typer.Option(help = "SSID of the network")]):
    """
    Connect to a network with the specified SSID using the specified interface.
    *Please make sure the network profile is already set.
    """

    result = False
    wlan.openhandle()

    guid = get_guid(iface_name)
    if guid:
        result = wlan.connect(guid, ssid)

    wlan.closshandle()

    return result

@app.command()
def refresh(iface_name: Annotated[str, typer.Argument(help = "Interface name")]):
    """
    Refresh the list of available networks for the specified interface.
    """

    result = False
    wlan.openhandle()

    guid = get_guid(iface_name)
    if guid:
        result = wlan.refresh_wifi_list(guid)

    wlan.closshandle()    

    return result

@app.command()
def get_ssid(iface_name: Annotated[str, typer.Argument(help = "Interface name")]):
    """
    Get the SSID of the connected network for the specified interface.
    """

    result = False
    wlan.openhandle()

    guid = get_guid(iface_name)
    if guid:
        result = wlan.get_ssid(guid)

        if isprint:
            print(result)

    wlan.closshandle()   

    return result

@app.command()
def get_profile(iface_name: Annotated[str, typer.Argument(help = "Interface name")], profile_name: Annotated[str, typer.Option(help = "Profile name")]):
    """
    Get the Profile of the SSID network for the specified interface.
    """
    result = ""
    wlan.openhandle()

    guid = get_guid(iface_name)

    if guid:
        result = wlan.get_profile(guid, profile_name)

        if isprint:
            print(result.value)

    wlan.closshandle()

    return result.value

@app.command()
def get_connection_info(iface_name: Annotated[str, typer.Argument(help = "Interface name")]):
    """
    Retrieve connection information for a specified network interface.
    """
    result = {}
    wlan.openhandle()

    guid = get_guid(iface_name)

    if guid:
        result = wlan.get_connection_info(guid)

        if isprint:
            print(result)

    wlan.closshandle()

    return json.dumps(result)

@app.command()
def get_computer_info(iface_name: Annotated[str, typer.Argument(help = "Interface name")]):
    """
    Get information about the computer.
    """
    result = wlan.get_computer_info(iface_name)

    if isprint:
        print(result)

    return json.dumps(result)

@app.command()
def get_tput_name():
    """
    Get the name for the second argument (tput_name) of the graph function.
    """
    result = wlan.get_tput_name()

    if isprint:
        print(result)

    return json.dumps(result)

@app.callback()
def settings(set_print: Annotated[Optional[bool], typer.Option(help = "Flag to enable/disable printing.")] = True):
    """
    Enable or disable printing of results.
    """
    global isprint

    if not set_print:
        isprint = False


if __name__ == "__main__":
    app()
