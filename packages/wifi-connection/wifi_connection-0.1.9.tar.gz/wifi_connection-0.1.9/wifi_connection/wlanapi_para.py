from ctypes import *
from ctypes.wintypes import *


WLAN_INTERFACE_STATE = c_uint
(wlan_interface_state_not_ready,
wlan_interface_state_connected,
wlan_interface_state_ad_hoc_network_formed,
wlan_interface_state_disconnecting,
wlan_interface_state_disconnected,
wlan_interface_state_associating,
wlan_interface_state_discovering,
wlan_interface_state_authenticating) = map(WLAN_INTERFACE_STATE, range(0, 8))

WLAN_MAX_PHY_TYPE_NUMBER = 0x8
DOT11_SSID_MAX_LENGTH = 32
WLAN_REASON_CODE = DWORD

DOT11_BSS_TYPE = c_uint
(dot11_BSS_type_infrastructure,
dot11_BSS_type_independent,
dot11_BSS_type_any) = map(DOT11_BSS_TYPE, range(1, 4))

DOT11_PHY_TYPE = c_uint
DOT11_PHY_TYPE_DICT = {
    0: "dot11_phy_type_unknown",
    1: "dot11_phy_type_fhss",
    2: "dot11_phy_type_dsss",
    3: "dot11_phy_type_irbaseband",
    4: "dot11_phy_type_ofdm",
    5: "dot11_phy_type_hrdsss",
    6: "dot11_phy_type_erp",
    7: "dot11_phy_type_ht",
    8: "dot11_phy_type_vht",
    9: "dot11_phy_type_dmg",
    10: "dot11_phy_type_he",
    11: "dot11_phy_type_eht",
    0x80000000: "dot11_phy_type_IHV_start",
    0xffffffff: "dot11_phy_type_IHV_end"
}

DOT11_AUTH_ALGORITHM = c_uint
DOT11_CIPHER_ALGORITHM = c_uint

WLAN_AVAILABLE_NETWORK_CONNECTED = 1
WLAN_AVAILABLE_NETWORK_HAS_PROFILE = 2

WLAN_AVAILABLE_NETWORK_INCLUDE_ALL_ADHOC_PROFILES = 0x00000001
WLAN_AVAILABLE_NETWORK_INCLUDE_ALL_MANUAL_HIDDEN_PROFILES = 0x00000002

WLAN_SIGNAL_QUALITY = c_ulong
DOT11_MAC_ADDRESS = c_ubyte * 6

# WLAN Profile Flags
WLAN_PROFILE_GROUP_POLICY = 0x00000001
WLAN_PROFILE_USER = 0x00000002
WLAN_PROFILE_GET_PLAINTEXT_KEY = 0x00000004

WLAN_INTF_OPCODE = c_uint
WLAN_INTF_OPCODE_DICT = {
    0x000000000: "wlan_intf_opcode_autoconf_start",
    1: "wlan_intf_opcode_autoconf_enabled",
    2: "wlan_intf_opcode_background_scan_enabled",
    3: "wlan_intf_opcode_media_streaming_mode",
    4: "wlan_intf_opcode_radio_state",
    5: "wlan_intf_opcode_bss_type",
    6: "wlan_intf_opcode_interface_state",
    7: "wlan_intf_opcode_current_connection",
    8: "wlan_intf_opcode_channel_number",
    9: "wlan_intf_opcode_supported_infrastructure_auth_cipher_pairs",
    10: "wlan_intf_opcode_supported_adhoc_auth_cipher_pairs",
    11: "wlan_intf_opcode_supported_country_or_region_string_list",
    12: "wlan_intf_opcode_current_operation_mode",
    13: "wlan_intf_opcode_supported_safe_mode",
    14: "wlan_intf_opcode_certified_safe_mode",
    15: "wlan_intf_opcode_hosted_network_capable",
    16: "wlan_intf_opcode_management_frame_protection_capable",
    0x0fffffff: "wlan_intf_opcode_autoconf_end",
    0x10000100: "wlan_intf_opcode_msm_start",
    17: "wlan_intf_opcode_statistics",
    18: "wlan_intf_opcode_rssi",
    0x1fffffff: "wlan_intf_opcode_msm_end",
    0x20010000: "wlan_intf_opcode_security_start",
    0x2fffffff: "wlan_intf_opcode_security_end",
    0x30000000: "wlan_intf_opcode_ihv_start",
    0x3fffffff: "wlan_intf_opcode_ihv_end"
}

WLAN_OPCODE_VALUE_TYPE = c_uint
WLAN_OPCODE_VALUE_TYPE_DICT = {
    0: "wlan_opcode_value_type_query_only",
    1: "wlan_opcode_value_type_set_by_group_policy",
    2: "wlan_opcode_value_type_set_by_user",
    3: "wlan_opcode_value_type_invalid"
}

DOT11_RADIO_STATE = c_uint
DOT11_RADIO_STATE_DICT = {0: "dot11_radio_state_unknown",
                        1: "dot11_radio_state_on",
                        2: "dot11_radio_state_off"}

DOT11_AUTH_ALGORITHM_TYPE = c_uint
DOT11_AUTH_ALGORITHM_DICT = {1: "DOT11_AUTH_ALGO_80211_OPEN",
                            2: "DOT11_AUTH_ALGO_80211_SHARED_KEY",
                            3: "DOT11_AUTH_ALGO_WPA",
                            4: "DOT11_AUTH_ALGO_WPA_PSK",
                            5: "DOT11_AUTH_ALGO_WPA_NONE",
                            6: "DOT11_AUTH_ALGO_RSNA",
                            7: "DOT11_AUTH_ALGO_RSNA_PSK",
                            0x80000000: "DOT11_AUTH_ALGO_IHV_START",
                            0xffffffff: "DOT11_AUTH_ALGO_IHV_END"}


DOT11_CIPHER_ALGORITHM_TYPE = c_uint
DOT11_CIPHER_ALGORITHM_DICT = {0x00: "DOT11_CIPHER_ALGO_NONE",
                            0x01: "DOT11_CIPHER_ALGO_WEP40",
                            0x02: "DOT11_CIPHER_ALGO_TKIP",
                            0x04: "DOT11_CIPHER_ALGO_CCMP",
                            0x05: "DOT11_CIPHER_ALGO_WEP104",
                            0x100: "DOT11_CIPHER_ALGO_WPA_USE_GROUP",
                            0x100: "DOT11_CIPHER_ALGO_RSN_USE_GROUP",
                            0x101: "DOT11_CIPHER_ALGO_WEP",
                            0x80000000: "DOT11_CIPHER_ALGO_IHV_START",
                            0xffffffff: "DOT11_CIPHER_ALGO_IHV_END"}

WLAN_CONNECTION_MODE = c_uint
WLAN_CONNECTION_MODE_KV = {0: "wlan_connection_mode_profile",
                        1: "wlan_connection_mode_temporary_profile",
                        2: "wlan_connection_mode_discovery_secure",
                        3: "wlan_connection_mode_discovery_unsecure",
                        4: "wlan_connection_mode_auto",
                        5: "wlan_connection_mode_invalid"}

WLAN_CONNECTION_MODE_VK = {"wlan_connection_mode_profile": 0,
                        "wlan_connection_mode_temporary_profile": 1,
                        "wlan_connection_mode_discovery_secure": 2,
                        "wlan_connection_mode_discovery_unsecure": 3,
                        "wlan_connection_mode_auto": 4,
                        "wlan_connection_mode_invalid": 5}

class GUID(Structure):
    _fields_ = [
        ('Data1', c_ulong),
        ('Data2', c_ushort),
        ('Data3', c_ushort),
        ('Data4', c_ubyte*8),
        ]


class WLAN_INTERFACE_INFO(Structure):
    _fields_ = [
        ("InterfaceGuid", GUID),
        ("strInterfaceDescription", c_wchar * 256),
        ("isState", WLAN_INTERFACE_STATE)
        ]

class WLAN_INTERFACE_INFO_LIST(Structure):
    _fields_ = [
        ("NumberOfItems", DWORD),
        ("Index", DWORD),
        ("InterfaceInfo", WLAN_INTERFACE_INFO * 1)
        ]

class DOT11_SSID(Structure):
    _fields_ = [
        ("SSIDLength", c_ulong),
        ("SSID", c_char * DOT11_SSID_MAX_LENGTH)
        ]

class WLAN_AVAILABLE_NETWORK(Structure):
    _fields_ = [
        ("ProfileName", c_wchar * 256),
        ("dot11Ssid", DOT11_SSID),
        ("dot11BssType", DOT11_BSS_TYPE),
        ("NumberOfBssids", c_ulong),
        ("NetworkConnectable", c_bool),
        ("wlanNotConnectableReason", WLAN_REASON_CODE),
        ("NumberOfPhyTypes", c_ulong),
        ("dot11PhyTypes", DOT11_PHY_TYPE * WLAN_MAX_PHY_TYPE_NUMBER),
        ("MorePhyTypes", c_bool),
        ("wlanSignalQuality", c_ulong),
        ("SecurityEnabled", c_bool),
        ("dot11DefaultAuthAlgorithm", DOT11_AUTH_ALGORITHM),
        ("dot11DefaultCipherAlgorithm", DOT11_CIPHER_ALGORITHM),
        ("Flags", DWORD),
        ("Reserved", DWORD)
        ]

class WLAN_AVAILABLE_NETWORK_LIST(Structure):
    _fields_ = [
        ("NumberOfItems", DWORD),
        ("Index", DWORD),
        ("Network", WLAN_AVAILABLE_NETWORK * 1)
        ]



class WLAN_PHY_RADIO_STATE(Structure):
    _fields_ = [("dwPhyIndex", DWORD),
                ("dot11SoftwareRadioState", DOT11_RADIO_STATE),
                ("dot11HardwareRadioState", DOT11_RADIO_STATE)]


class WLAN_RADIO_STATE(Structure):
    """
        The WLAN_RADIO_STATE structure specifies the radio state on a list
        of physical layer (PHY) types.
        typedef struct _WLAN_RADIO_STATE {
            DWORD                dwNumberOfPhys;
            WLAN_PHY_RADIO_STATE PhyRadioState[64];
        } WLAN_RADIO_STATE, *PWLAN_RADIO_STATE
    """
    _fields_ = [("dwNumberOfPhys", DWORD),
                ("PhyRadioState", WLAN_PHY_RADIO_STATE * 64)]


class WLAN_ASSOCIATION_ATTRIBUTES(Structure):
    _fields_ = [("dot11Ssid", DOT11_SSID),
                ("dot11BssType", DOT11_BSS_TYPE),
                ("dot11Bssid", DOT11_MAC_ADDRESS),
                ("dot11PhyType", DOT11_PHY_TYPE),
                ("uDot11PhyIndex", c_ulong),
                ("wlanSignalQuality", WLAN_SIGNAL_QUALITY),
                ("ulRxRate", c_ulong),
                ("ulTxRate", c_ulong)]



class WLAN_SECURITY_ATTRIBUTES(Structure):
    _fields_ = [("bSecurityEnabled", BOOL),
                ("bOneXEnabled", BOOL),
                ("dot11AuthAlgorithm", DOT11_AUTH_ALGORITHM_TYPE),
                ("dot11CipherAlgorithm", DOT11_CIPHER_ALGORITHM_TYPE)]



class WLAN_CONNECTION_ATTRIBUTES(Structure):
    _fields_ = [("isState", WLAN_INTERFACE_STATE),
                ("wlanConnectionMode", WLAN_CONNECTION_MODE),
                ("strProfileName", c_wchar * 256),
                ("wlanAssociationAttributes", WLAN_ASSOCIATION_ATTRIBUTES),
                ("wlanSecurityAttributes", WLAN_SECURITY_ATTRIBUTES)]

WLAN_INTF_OPCODE_TYPE_DICT = {
    "wlan_intf_opcode_autoconf_enabled": c_bool,
    "wlan_intf_opcode_background_scan_enabled": c_bool,
    "wlan_intf_opcode_radio_state": WLAN_RADIO_STATE,
    "wlan_intf_opcode_bss_type": DOT11_BSS_TYPE,
    "wlan_intf_opcode_interface_state": WLAN_INTERFACE_STATE,
    "wlan_intf_opcode_current_connection": WLAN_CONNECTION_ATTRIBUTES,
    "wlan_intf_opcode_channel_number": c_ulong,
    "wlan_intf_opcode_media_streaming_mode": c_bool,
    "wlan_intf_opcode_rssi": c_long,
    "wlan_intf_opcode_current_operation_mode": c_ulong,
    "wlan_intf_opcode_supported_safe_mode": c_bool,
    "wlan_intf_opcode_certified_safe_mode": c_bool
}


class WLAN_PROFILE_INFO(Structure):
    _fields_ = [("ProfileName", c_wchar * 256),
                ("Flags", DWORD)]

class WLAN_PROFILE_INFO_LIST(Structure):
    _fields_ = [("NumberOfItems", DWORD),
                ("Index", DWORD),
                ("ProfileInfo", WLAN_PROFILE_INFO * 1)]
    
class NDIS_OBJECT_HEADER(Structure):
    _fields_ = [
        ("Type", c_ubyte),
        ("Revision", c_ubyte),
        ("Size", c_ushort)
    ]


class DOT11_BSSID_LIST(Structure):
    _fields_ = [
        ("Header", NDIS_OBJECT_HEADER),
        ("uNumOfEntries", c_ulong),
        ("uTotalNumOfEntries", c_ulong),
        ("BSSIDs", DOT11_MAC_ADDRESS * 1)
    ]


class WLAN_CONNECTION_PARAMETERS(Structure):
    _fields_ = [
        ("wlanConnectionMode", c_uint),
        ("strProfile", c_wchar_p),
        ("pDot11Ssid", POINTER(DOT11_SSID)),
        ("pDesiredBssidList", POINTER(DOT11_BSSID_LIST)),
        ("dot11BssType", c_uint),
        ("dwFlags", DWORD)
    ]


class WLAN_RAW_DATA(Structure):
    _fields_ = [
        ("dwDataSize", DWORD),
        ("DataBlob", c_byte * 1)
    ]

class WLAN_RATE_SET(Structure):
    _fields_ = [
     ("uRateSetLength", c_ulong),
     ("usRateSet", c_ushort * 126)
    ]

class WLAN_BSS_ENTRY(Structure):
    _fields_ = [
     ("dot11Ssid",DOT11_SSID),
     ("uPhyId",c_ulong),
     ("dot11Bssid", DOT11_MAC_ADDRESS),
     ("dot11BssType", DOT11_BSS_TYPE),
     ("dot11BssPhyType", DOT11_PHY_TYPE),
     ("lRssi", c_long),
     ("uLinkQuality", c_ulong),
     ("bInRegDomain", c_bool),
     ("usBeaconPeriod",c_ushort),
     ("ullTimestamp", c_ulonglong),
     ("ullHostTimestamp",c_ulonglong),
     ("usCapabilityInformation",c_ushort),
     ("ulChCenterFrequency", c_ulong),
     ("wlanRateSet",WLAN_RATE_SET),
     ("ulIeOffset", c_ulong),
     ("ulIeSize", c_ulong)]

class WLAN_BSS_LIST(Structure):
    _fields_ = [
     ("TotalSize", DWORD),
     ("NumberOfItems", DWORD),
     ("NetworkBSS", WLAN_BSS_ENTRY * 1)
    ]