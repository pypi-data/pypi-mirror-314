from .coordinate import Coordinate


def convert_dms(cifp_dms_substring: str) -> Coordinate:
    lat_string = cifp_dms_substring[0:9]
    lon_string = cifp_dms_substring[9:19]
    north_south = lat_string[0:1]
    lat_d = int(lat_string[1:3])
    lat_m = int(lat_string[3:5])
    lat_s = int(lat_string[5:]) / 100
    east_west = lon_string[0:1]
    lon_d = int(lon_string[1:4])
    lon_m = int(lon_string[4:6])
    lon_s = int(lon_string[6:]) / 100
    coord = Coordinate()
    coord.fromDMS(north_south, lat_d, lat_m, lat_s, east_west, lon_d, lon_m, lon_s)
    return coord


def convert_mag_var(cifp_mag_var_substring: str) -> float:
    mag_var_value = int(cifp_mag_var_substring[1:]) / 10
    if cifp_mag_var_substring[0:1] == "W":
        mag_var_value = -mag_var_value
    return mag_var_value


def translate_rnp(rnp_string: str) -> float:
    if len(rnp_string) != 3:
        return rnp_string
    leading_digit_string = rnp_string[0:1]
    if leading_digit_string == "0":
        value = int(rnp_string[1:2])
        exponent = -int(rnp_string[2:3])
        result = round(value * (10**exponent), 1)
        return result
    return int(rnp_string) / 10


def chunk(
    line_array: list,
    id_start: int,
    id_stop: int,
) -> list[list[str]]:
    last_id = ""
    chunk = []
    result = []
    for line in line_array:
        current_id = line[id_start:id_stop]
        if current_id != last_id and last_id != "":
            result.append(chunk)
            chunk = []
        chunk.append(line)
        last_id = current_id
    if len(chunk) > 0:
        result.append(chunk)
    return result


def clean_value(value: any) -> any:
    if isinstance(value, str) and value == "":
        return None
    return value


def yn_to_bool(text_val: str) -> bool:
    result = False
    if text_val.upper() == "Y":
        result = True
    return result
