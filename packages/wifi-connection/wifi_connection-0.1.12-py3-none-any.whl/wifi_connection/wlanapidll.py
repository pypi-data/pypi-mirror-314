from ctypes import *
from ctypes.wintypes import *
from wifi_connection.wlanapi_para import *

class WlanapiDll:
    
    def __init__(self):
        self.wlanapidll = windll.LoadLibrary('wlanapi.dll')

        WlanOpenHandle = self.wlanapidll.WlanOpenHandle
        WlanOpenHandle.argtypes = [DWORD, c_void_p, POINTER(DWORD), POINTER(HANDLE)]
        WlanOpenHandle.restype = DWORD

        WlanEnumInterfaces = self.wlanapidll.WlanEnumInterfaces
        WlanEnumInterfaces.argtypes = [HANDLE, c_void_p, 
                                    POINTER(POINTER(WLAN_INTERFACE_INFO_LIST))]
        WlanEnumInterfaces.restype = DWORD

        WlanGetAvailableNetworkList = self.wlanapidll.WlanGetAvailableNetworkList
        WlanGetAvailableNetworkList.argtypes = [HANDLE, POINTER(GUID), DWORD, c_void_p, 
                                                POINTER(POINTER(WLAN_AVAILABLE_NETWORK_LIST))]
        WlanGetAvailableNetworkList.restype = DWORD

        WlanFreeMemory = self.wlanapidll.WlanFreeMemory
        WlanFreeMemory.argtypes = [c_void_p]

        WlanQueryInterface = self.wlanapidll.WlanQueryInterface
        opcode_name = WLAN_INTF_OPCODE_DICT[7]
        self.return_type = WLAN_INTF_OPCODE_TYPE_DICT[opcode_name]
        WlanQueryInterface.argtypes = [HANDLE, POINTER(GUID), DWORD, c_void_p, POINTER(DWORD), c_void_p, POINTER(DWORD)]
        WlanQueryInterface.restype = DWORD

        WlanGetProfileList = self.wlanapidll.WlanGetProfileList
        WlanGetProfileList.argtypes = [HANDLE, POINTER(GUID), c_void_p, POINTER(POINTER(WLAN_PROFILE_INFO_LIST))]
        WlanGetProfileList.restype = DWORD

        WlanSetProfile = self.wlanapidll.WlanSetProfile
        WlanSetProfile.argtypes = [HANDLE, POINTER(GUID), DWORD, c_wchar_p, c_wchar_p, c_bool, c_void_p, POINTER(DWORD)]
        WlanSetProfile.restype = DWORD

        WlanDeleteProfile = self.wlanapidll.WlanDeleteProfile
        WlanDeleteProfile.argtypes = [HANDLE, POINTER(GUID), c_wchar_p, c_void_p]
        WlanDeleteProfile.restype = DWORD

        WlanConnect = self.wlanapidll.WlanConnect
        WlanConnect.argtypes = [HANDLE, POINTER(GUID), POINTER(WLAN_CONNECTION_PARAMETERS), c_void_p]
        WlanConnect.restype = DWORD

        WlanScan = self.wlanapidll.WlanScan
        WlanScan.argtypes = [HANDLE, POINTER(GUID), POINTER(DOT11_SSID), POINTER(WLAN_RAW_DATA), c_void_p]
        WlanScan.restype = DWORD

        WlanCloseHandle = self.wlanapidll.WlanCloseHandle
        WlanCloseHandle.argtypes = [HANDLE, c_void_p]
        WlanCloseHandle.restype = DWORD

        WlanGetProfile = self.wlanapidll.WlanGetProfile
        WlanGetProfile.argtypes = [HANDLE, POINTER(GUID), LPCWSTR, c_void_p, POINTER(LPWSTR), POINTER(DWORD), POINTER(DWORD)]
        WlanGetProfile.restype = DWORD

        WlanGetNetworkBssList = self.wlanapidll.WlanGetNetworkBssList
        WlanGetNetworkBssList.argtypes = [HANDLE, POINTER(GUID), POINTER(DOT11_SSID), c_uint, c_bool, c_void_p, POINTER(POINTER(WLAN_BSS_LIST))]
        WlanGetNetworkBssList.restype = DWORD
