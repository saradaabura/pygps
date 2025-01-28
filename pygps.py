import re
patterns = {
    'GGA': re.compile(r'\$GNGGA,.*?\*..'),
    'GLL': re.compile(r'\$GNGLL,.*?\*..'),
    'GSA': re.compile(r'\$GNGSA,.*?\*..'),
    'GSV': re.compile(r'\$GNGSV,.*?\*..|\$BDGSV,.*?\*..|\$GLGSV,.*?\*..|\$GPGSV,.*?\*..'),
    'RMC': re.compile(r'\$GNRMC,.*?\*..'),
    'VTG': re.compile(r'\$GNVTG,.*?\*..')
}
def parse_nmea_sentences(nmea_data):
    parsed_data = {key: [] for key in patterns.keys()}
    for sentence in nmea_data:
        for key, pattern in patterns.items():
            if pattern.match(sentence):
                parsed_data[key].append(sentence)
    return parsed_data
def parse_lat_lon(lat, lon, lat_dir, lon_dir):
    lat_deg = int(lat[:2])
    lat_min = float(lat[2:])
    lon_deg = int(lon[:3])
    lon_min = float(lon[3:])
    latitude = lat_deg + lat_min / 60.0
    longitude = lon_deg + lon_min / 60.0
    if lat_dir == 'S':
        latitude = -latitude
    if lon_dir == 'W':
        longitude = -longitude
    return latitude, longitude
def parse_speed_knots_to_kmh(speed_knots):
    return float(speed_knots) * 1.852
def parse_gga(data):
    for sentence in data:
        parts = sentence.split(',')
        print(len(parts))
        latitude, longitude = parse_lat_lon(parts[2], parts[4], parts[3], parts[5])
        altitude = float(parts[9])
        satellites_used = int(parts[7])
        return {"Lat" : latitude, "Lon" : longitude, "Alt" : altitude, "SatellitesUsed" : satellites_used}
def parse_rmc(data):
    for sentence in data:
        parts = sentence.split(',')
        time = parts[1]
        hours, minutes, seconds, millisecond = int(time[0:2]), int(time[2:4]), int(time[4:6]), int(time[7:10])
        latitude, longitude = parse_lat_lon(parts[3], parts[5], parts[4], parts[6])
        speed_knots = parts[7]
        speed_kmh = parse_speed_knots_to_kmh(speed_knots)
        date = parts[9]
        day, month, year = int(date[0:2]), int(date[2:4]), int(date[4:]) + 2000
        return {"Lat" : latitude, "Lon" : longitude, "Speed" : speed_kmh, "year" : year, "month" : month, "day" : day, "hour" : hours, "minutes" : minutes, "seconds" : seconds, "millisecond" : millisecond}
def parse_gsv(data):
    satellite_info_list = []
    satellites = 0
    for sentence in data:
        parts = sentence.split(',')
        try:
            num_satellites = int(parts[3])
            for i in range(4, len(parts) - 4, 4):
                satellite_id = int(parts[i])
                elevation = int(parts[i+1])
                azimuth = int(parts[i+2])
                snr = int(parts[i+3]) if parts[i+3] else 0
                satellite_info_list.append({
                    'SV': satellite_id,
                    'EL': elevation,
                    'AZ': azimuth,
                    'SNR': snr
                })
                satellites += 1
        except (ValueError, IndexError):
            pass
    return satellites, satellite_info_list
def parse_vtg(data):
    for sentence in data:
        parts = sentence.split(',')
        course_true = float(parts[1])
        speed_knots = float(parts[5])
        speed_kmh = float(parts[7])
        return {"course" : course_true, "speed" : speed_kmh}
def parse_gsa(data):
    for sentence in data:
        parts = sentence.split(',')
        mode = parts[1]
        fix_type = int(parts[2])
        pdop = float(parts[15])
        hdop = float(parts[16])
        vdop = float(parts[17].split('*')[0])
        satellites_used = [int(parts[i]) for i in range(3, 15) if parts[i].isdigit()]
        return {"fixmode" : mode, "fixtype" : fix_type, "PDOP" : pdop, "HDOP" : hdop, "VDOP" : vdop, "SVUsed" : satellites_used}
def parse_gll(data):
    for sentence in data:
        parts = sentence.split(',')
        latitude, longitude = parse_lat_lon(parts[1], parts[3], parts[2], parts[4])
        time = parts[5]
        hours, minutes, seconds = int(time[0:2]), int(time[2:4]), float(time[4:])
        status = parts[6]
        return {"Time" : [hours, minutes, seconds], "Lat" : latitude, "Lon" : longitude, "Status" : status}
