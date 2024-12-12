from wifi_connection.wlanapidll import *
import wmi
import winreg as wrg
import time, json

class Wlanapi:
    def __init__(self) -> None:
        self.dllclass = WlanapiDll()
        self.dll = self.dllclass.wlanapidll

        self.ClientHandle = HANDLE()
        self.pInterfaceList = pointer(WLAN_INTERFACE_INFO_LIST())   #free when finished 

    def customresize(self, array, new_size):
        return (array._type_*new_size).from_address(addressof(array))

    def openhandle(self):
        NegotiatedVersion = DWORD()

        result = self.dll.WlanOpenHandle(1, None, byref(NegotiatedVersion), byref(self.ClientHandle))
        if result != 0:
            print("openhandle failed.", FormatError(result))
            return

    def closshandle(self):
        if self.pInterfaceList:
            self.dll.WlanFreeMemory(self.pInterfaceList)
        
        self.dll.WlanCloseHandle(self.ClientHandle, None)


    def get_interfaces(self):
        # find all wireless network interfaces
        result = self.dll.WlanEnumInterfaces(self.ClientHandle, None, byref(self.pInterfaceList))
        if result != 0:
            print("get_interfaces failed.", FormatError(result))
            return

        ifaces = self.customresize(self.pInterfaceList.contents.InterfaceInfo,
                                   self.pInterfaceList.contents.NumberOfItems)

        return ifaces
    
    def get_available_network(self, InterfaceGuid):
        pAvailableNetworkList = pointer(WLAN_AVAILABLE_NETWORK_LIST())

        result = self.dll.WlanGetAvailableNetworkList(self.ClientHandle, byref(InterfaceGuid), 0, None, byref(pAvailableNetworkList))
        if result != 0:
            print("get_available_network failed.", FormatError(result))
            return
        
        available_network_list = pAvailableNetworkList.contents
        networks = self.customresize(available_network_list.Network, available_network_list.NumberOfItems)

        network_list = dict()
        for network in networks:
            ssid = network.dot11Ssid.SSID[:network.dot11Ssid.SSIDLength].decode()
            rssi = network.wlanSignalQuality
            
            if ssid and ssid not in network_list:
                network_list[ssid] = rssi
    
        return network_list
    
    def set_profile(self, InterfaceGuid, band, ssid, pwd = None, auto = True):
        if band == 6:
            authentication = "WPA3SAE"
        else:
            authentication = "WPA2PSK"

        if pwd:
            encrypt = "AES"
        else:
            authentication = "open"
            encrypt = "none"

        if auto:
            mode = "auto"
        else:
            mode = "manual"

        xmlBuffer = """<?xml version =\"1.0\"?>\
                        <WLANProfile xmlns =\"http://www.microsoft.com/networking/WLAN/profile/v1\">\
                        <name>{profile_name}</name>\
                        <SSIDConfig>\
                        <SSID>\
                        <name>{ssid}</name>\
                        </SSID>\
                        </SSIDConfig>\
                        <connectionType>ESS</connectionType>\
                        <connectionMode>{auto}</connectionMode>\
                        <autoSwitch>false</autoSwitch>\
                        <MSM>\
                        <security>\
                        <authEncryption>\
                        <authentication>{auth}</authentication>\
                        <encryption>{encrypt}</encryption>\
                        <useOneX>false</useOneX>\
                        </authEncryption>\
                    """
        if pwd:
            xmlBuffer += """<sharedKey>\
                        <keyType>passPhrase</keyType>\
                        <protected>false</protected>\
                        <keyMaterial>{pwd}</keyMaterial>\
                        </sharedKey>\
                        """

        xmlBuffer += """</security>\
                        </MSM>\
                        </WLANProfile>
                    """


        xmlBuffer = xmlBuffer.format(profile_name = ssid, ssid = ssid, auto = mode, auth = authentication, encrypt = encrypt, pwd = pwd)

        reasoncode = DWORD()
        result = self.dll.WlanSetProfile(self.ClientHandle, byref(InterfaceGuid), 0, xmlBuffer, None, True, None, byref(reasoncode))
        if result != 0:
            print("set_profile failed.", FormatError(result))
            return False
        
        return True

    
    def connect(self, InterfaceGuid, profile_name):
        connect_params = WLAN_CONNECTION_PARAMETERS()
        connect_params.wlanConnectionMode = 0  # CONNECT AP VIA THE PROFILE
        connect_params.dot11BssType = 1  # dot11_BSS_type_infrastructure
        connect_params.strProfile = create_unicode_buffer(profile_name).value

        result = self.dll.WlanConnect(self.ClientHandle, byref(InterfaceGuid), byref(connect_params), None)
        if result != 0:
            print("connect failed.", FormatError(result))
            return False
        
        return True

    def refresh_wifi_list(self, InterfaceGuid):
        result = self.dll.WlanScan(self.ClientHandle, byref(InterfaceGuid), None, None, None)
        if result != 0:
            print("refresh_wifi_list failed.", FormatError(result))
            return False
        
        return True


    def delete_profile(self, InterfaceGuid, profile_name):
        result = self.dll.WlanDeleteProfile(self.ClientHandle, byref(InterfaceGuid), profile_name, None)
        if result != 0:
            print("delete_profile failed.", FormatError(result))
            return False
        
        return True


    def get_ssid(self, InterfaceGuid):
        pdwDataSize = DWORD()
        ppData = pointer(self.dllclass.return_type())
        pWlanOpcodeValueType = WLAN_OPCODE_VALUE_TYPE()
        result = self.dll.WlanQueryInterface(self.ClientHandle,
                        byref(InterfaceGuid),
                        7,  #wlan_intf_opcode_current_connection
                        None,
                        pdwDataSize,
                        byref(ppData),
                        pWlanOpcodeValueType)
        
        if result != 0:
            print("getssid failed.", FormatError(result))
            return ""
        
        ssid = ppData.contents.wlanAssociationAttributes.dot11Ssid.SSID.decode() #no connection: ssid = ""

        return ssid

    def get_profile(self, InterfaceGuid, profile_name):
        pdw_granted_access = DWORD()
        xml = LPWSTR()
        flags = DWORD(WLAN_PROFILE_GET_PLAINTEXT_KEY)
        result = self.dll.WlanGetProfile(self.ClientHandle,
                        byref(InterfaceGuid),
                        profile_name,
                        None,
                        byref(xml),
                        byref(flags),
                        byref(pdw_granted_access))
        if result != 0:
            print("get_profile failed.", FormatError(result))
            return
        
        return xml


    def get_connection_info(self, InterfaceGuid):
        result = dict()

        pWlanOpcodeValueType = WLAN_OPCODE_VALUE_TYPE()
        pConnection = pointer(WLAN_CONNECTION_ATTRIBUTES())
        pConnectionSize = DWORD()
        self.dll.WlanQueryInterface(self.ClientHandle,
                                byref(InterfaceGuid),
                                7,  #wlan_intf_opcode_current_connection
                                None,
                                pConnectionSize,
                                byref(pConnection),
                                pWlanOpcodeValueType)
        
        result["RxSpeed"] = pConnection.contents.wlanAssociationAttributes.ulRxRate
        result["TxSpeed"] = pConnection.contents.wlanAssociationAttributes.ulTxRate

        channel = pointer(ULONG())
        channelSize = DWORD()
        self.dll.WlanQueryInterface(self.ClientHandle,
                                byref(InterfaceGuid),
                                8,  
                                None,
                                channelSize,
                                byref(channel),
                                pWlanOpcodeValueType)
        
        result["Channel"] = channel.contents.value

        wlan_bss_list = pointer(WLAN_BSS_LIST())
        self.dll.WlanGetNetworkBssList(self.ClientHandle, byref(InterfaceGuid), pConnection.contents.wlanAssociationAttributes.dot11Ssid, pConnection.contents.wlanAssociationAttributes.dot11BssType, True, None, byref(wlan_bss_list))

        result["Frequency"] = wlan_bss_list.contents.NetworkBSS[0].ulChCenterFrequency
        result["RSSI"] = wlan_bss_list.contents.NetworkBSS[0].lRssi
        result["Protocol"] = DOT11_PHY_TYPE_DICT.get(wlan_bss_list.contents.NetworkBSS[0].dot11BssPhyType)
        
        return result
    
    def get_computer_info(self, interface_name):
        result = {}
        wmiobj = wmi.WMI()

        driverinfo = wmiobj.Win32_PnPSignedDriver(Description = interface_name)
        result["WiFiDriverVersion"] = driverinfo[0].DriverVersion
        result["WiFiDriverDate"] = driverinfo[0].DriverDate[:8]
        result["WiFiDriverProviderName"] = driverinfo[0].DriverProviderName

        osinfo = wmiobj.Win32_OperatingSystem()
        result["OS"] = osinfo[0].Caption

        # Store location of HKEY_CURRENT_USER 
        location = wrg.HKEY_LOCAL_MACHINE 
        
        # Storing path in soft 
        soft = wrg.OpenKeyEx(location, r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion") 
        result["OSBuild"] = wrg.QueryValueEx(soft, "CurrentBuild")[0]
        result["OSVersion"] = wrg.QueryValueEx(soft, "DisplayVersion")[0]

        soft = wrg.OpenKeyEx(location, r"HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0") 
        result["CPU"] = wrg.QueryValueEx(soft, "ProcessorNameString")[0] 

        # Closing folder 
        if soft: 
            wrg.CloseKey(soft) 

        return result
    
    def get_tput_name(self):
        wmiobj = wmi.WMI()

        name_list = []
        for i in wmiobj.Win32_PerfFormattedData_Tcpip_NetworkInterface():
            name_list.append(i.Name)

        return name_list

    def graph(self, interface_name, tput_name):
        pass
