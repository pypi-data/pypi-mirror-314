import math
try:
    import utm
except:
    UTM = None
import re

X_PI = 3.14159265358979324 * 3000.0 / 180.0
PI = 3.1415926535897932384626
A = 6378245.0
EE = 0.00669342162296594323


def transformLat(x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * PI) + 40.0 * math.sin(y / 3.0 * PI)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * PI) + 320.0 * math.sin(y * PI / 30.0)) * 2.0 / 3.0
    return ret


def transformLon(x, y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * PI) + 40.0 * math.sin(x / 3.0 * PI)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * PI) + 300.0 * math.sin(x / 30.0 * PI)) * 2.0 / 3.0
    return ret


def WGS84_to_GCJ02(lat, lon):
    if out_of_china(lat, lon):
        return lat, lon
    dLat = transformLat(lon - 105.0, lat - 35.0)
    dLon = transformLon(lon - 105.0, lat - 35.0)
    radLat = lat / 180.0 * PI
    magic = math.sin(radLat)
    magic = 1 - EE * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((A * (1 - EE)) / (magic * sqrtMagic) * PI)
    dLon = (dLon * 180.0) / (A / sqrtMagic * math.cos(radLat) * PI)
    mgLat = lat + dLat
    mgLon = lon + dLon
    return mgLat, mgLon


def GCJ02_to_WGS84(lat, lon):
    GCJ02 = WGS84_to_GCJ02(lat, lon)
    dLat = GCJ02[0] - lat
    dLon = GCJ02[1] - lon
    return lat - dLat, lon - dLon


def GCJ02_to_BD09(lat, lon):
    z = math.sqrt(lon * lon + lat * lat) + 0.00002 * math.sin(lat * X_PI)
    theta = math.atan2(lat, lon) + 0.000003 * math.cos(lon * X_PI)
    bd_lon = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return bd_lat, bd_lon


def BD09_to_GCJ02(lat, lon):
    x = lon - 0.0065
    y = lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * X_PI)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * X_PI)
    gcj_lon = z * math.cos(theta)
    gcj_lat = z * math.sin(theta)
    return gcj_lat, gcj_lon


def WGS84_to_BD09(lat, lon):
    GCJ02 = WGS84_to_GCJ02(lat, lon)
    return GCJ02_to_BD09(GCJ02[0], GCJ02[1])


def BD09_to_WGS84(lat, lon):
    GCJ02 = BD09_to_GCJ02(lat, lon)
    return GCJ02_to_WGS84(GCJ02[0], GCJ02[1])


# def cgcs2000_to_WGS84(lat, lon):
#     return lat, lon  # Assume CGCS2000 is equivalent to WGS84 for simplicity
#
#
# def WGS84_to_cgcs2000(lat, lon):
#     return lat, lon  # Assume CGCS2000 is equivalent to WGS84 for simplicity


# def GCJ02_to_cgcs2000(lat, lon):
#     WGS84 = GCJ02_to_WGS84(lat, lon)
#     return WGS84_to_cgcs2000(WGS84[0], WGS84[1])
#
#
# def cgcs2000_to_GCJ02(lat, lon):
#     WGS84 = cgcs2000_to_WGS84(lat, lon)
#     return WGS84_to_GCJ02(WGS84[0], WGS84[1])


# WGS84 to UTM
def WGS84_to_UTM(lat, lon):
    u = utm.from_latlon(lat, lon)
    return u


# UTM to WGS84
def UTM_to_WGS84(easting, northing, zone_number, zone_letter):
    latlon = utm.to_latlon(easting, northing, zone_number, zone_letter)
    return latlon


def dms_to_decimal(dms_lat, dms_lon):
    lat = convert_dms_to_decimal(dms_lat)
    lon = convert_dms_to_decimal(dms_lon)
    return lat, lon


def convert_dms_to_decimal(dms):
    degrees, minutes, seconds, direction = re.split('[°\'"]', dms)
    decimal = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
    if direction in ['S', 'W']:
        decimal *= -1
    return decimal


def decimal_to_dms(decimal_lat, decimal_lon):
    lat_dms = convert_decimal_to_dms(decimal_lat, True)
    lon_dms = convert_decimal_to_dms(decimal_lon, False)
    return lat_dms, lon_dms


def convert_decimal_to_dms(decimal, is_latitude):
    direction = 'N' if is_latitude else 'E'
    if decimal < 0:
        direction = 'S' if is_latitude else 'W'
    decimal = abs(decimal)
    degrees = int(decimal)
    minutes = int((decimal - degrees) * 60)
    seconds = (decimal - degrees - minutes / 60) * 3600
    return f'{degrees}°{minutes}\'{seconds:.2f}"{direction}'


def out_of_china(lat, lon):
    return lon < 72.004 or lon > 137.8347 or lat < 0.8293 or lat > 55.8271