from .cifp_functions import chunk, convert_dms, convert_mag_var, clean_value, yn_to_bool
from .cifp_procedure import CIFPProcedure
from .cifp_waypoint import CIFPWaypoint

from sqlite3 import Cursor

TABLE_NAME = "heliports"


class CIFPHeliport:
    def __init__(self) -> None:
        self.area = None
        self.sec_code = None
        self.heliport_id = None
        self.region = None
        self.sub_code = None
        self.iata = None
        self.pad_id = None
        self.cont_rec_no = None
        self.limit_alt = None
        self.datum_code = None
        self.is_ifr = None
        self.lat = None
        self.lon = None
        self.mag_var = None
        self.elevation = None
        self.limit = None
        self.rec_vhf = None
        self.rec_vhf_region = None
        self.transition_alt = None
        self.transition_level = None
        self.usage = None
        self.time_zone = None
        self.daylight_ind = None
        self.pad_dimensions = None
        self.mag_true = None
        self.heliport_name = None
        self.record_number = None
        self.cycle_data = None
        self.points: list[CIFPWaypoint] = []
        self.departures: list[CIFPProcedure] = []
        self.arrivals: list[CIFPProcedure] = []
        self.approaches: list[CIFPProcedure] = []
        self._departure_lines = []
        self._departure_chunked = []
        self._arrival_lines = []
        self._arrival_chunked = []
        self._approach_lines = []
        self._approach_chunked = []

    def from_lines(self, cifp_lines: list) -> None:
        for cifp_line in cifp_lines:
            sub_code = cifp_line[12:13]
            if sub_code == "A":
                self._sec_A(cifp_line)
            if sub_code == "C":
                self._sec_C(cifp_line)
            if sub_code == "D":
                self._departure_lines.append(cifp_line)
            if sub_code == "E":
                self._arrival_lines.append(cifp_line)
            if sub_code == "F":
                self._approach_lines.append(cifp_line)

        # Process Departures
        self._departure_chunked = chunk(self._departure_lines, 6, 19)
        self._departure_to_object()
        del self._departure_lines
        del self._departure_chunked
        # Process Arrivals
        self._arrival_chunked = chunk(self._arrival_lines, 6, 19)
        self._arrival_to_object()
        del self._arrival_lines
        del self._arrival_chunked
        # Process Approaches
        self._approach_chunked = chunk(self._approach_lines, 6, 19)
        self._approach_to_object()
        del self._approach_lines
        del self._approach_chunked

    def _departure_to_object(self) -> None:
        for departure_chunk in self._departure_chunked:
            departure = CIFPProcedure()
            departure.from_lines(departure_chunk)
            self.departures.append(departure)

    def _arrival_to_object(self) -> None:
        for arrival_chunk in self._arrival_chunked:
            arrival = CIFPProcedure()
            arrival.from_lines(arrival_chunk)
            self.arrivals.append(arrival)

    def _approach_to_object(self) -> None:
        for approach_chunk in self._approach_chunked:
            approach = CIFPProcedure()
            approach.from_lines(approach_chunk)
            self.approaches.append(approach)

    def _sec_A(self, cifp_line: str) -> None:
        # PAD 1
        self.area = cifp_line[1:4].strip()
        self.sec_code = cifp_line[4:5].strip()
        # PAD 1
        self.heliport_id = cifp_line[6:10].strip()
        self.region = cifp_line[10:12].strip()
        self.sub_code = cifp_line[12:13].strip()
        self.iata = cifp_line[13:16].strip()
        self.pad_id = cifp_line[16:21].strip()
        self.cont_rec_no = int(cifp_line[21:22].strip())
        speed_limit_alt = cifp_line[22:27].strip()
        self.datum_code = cifp_line[27:30].strip()
        is_ifr = cifp_line[30:31].strip()
        # PAD 1
        lat_lon = cifp_line[32:51].strip()
        variation = cifp_line[51:56].strip()
        elev = cifp_line[56:61].strip()
        speed_limit = cifp_line[61:64].strip()
        self.rec_vhf = cifp_line[64:68].strip()
        self.rec_vhf_region = cifp_line[68:70].strip()
        tr_alt = cifp_line[70:75].strip()
        tr_level = cifp_line[75:80].strip()
        self.usage = cifp_line[80:81].strip()
        self.time_zone = cifp_line[81:84].strip()
        self.daylight_ind = cifp_line[84:85].strip()
        self.pad_dimensions = cifp_line[85:91].strip()
        self.mag_true = cifp_line[91:92].strip()
        # RESERVED 1
        self.heliport_name = cifp_line[93:123].strip()
        self.record_number = int(cifp_line[123:128].strip())
        self.cycle_data = cifp_line[128:132].strip()

        if is_ifr != "":
            self.is_ifr = yn_to_bool(is_ifr)

        if speed_limit_alt != "":
            self.limit_alt = int(speed_limit_alt)

        if lat_lon != "":
            coordinates = convert_dms(lat_lon)
            self.lat = coordinates.lat
            self.lon = coordinates.lon

        if variation != "":
            mag_var = convert_mag_var(variation)
            self.mag_var = mag_var

        if elev != "":
            self.elevation = int(elev)

        if speed_limit != "":
            self.limit = int(speed_limit)

        if tr_alt != "":
            self.transition_alt = int(tr_alt)

        if tr_level != "":
            self.transition_level = int(tr_level)

    def _sec_C(self, cifp_line: str) -> None:
        point = CIFPWaypoint()
        point.from_lines([cifp_line])
        self.points.append(point)

    def create_db_table(db_cursor: Cursor) -> None:
        drop_statement = "DROP TABLE IF EXISTS `{TABLE_NAME}`;"
        db_cursor.execute(drop_statement)

        create_statement = f"""
            CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
                `area` TEXT,
                `sec_code` TEXT,
                `heliport_id` TEXT,
                `region` TEXT,
                `sub_code` TEXT,
                `iata` TEXT,
                `pad_id` TEXT,
                `cont_rec_no` INTEGER,
                `limit_alt` TEXT,
                `datum_code` TEXT,
                `is_ifr` INTEGER,
                `lat` REAL,
                `lon` REAL,
                `mag_var` REAL,
                `elevation` INTEGER,
                `limit` INTEGER,
                `rec_vhf` TEXT,
                `rec_vhf_region` TEXT,
                `transition_alt` INTEGER,
                `transition_level` INTEGER,
                `usage` TEXT,
                `time_zone` TEXT,
                `daylight_ind` TEXT,
                `pad_dimensions` TEXT,
                `mag_true` TEXT,
                `heliport_name` TEXT,
                `record_number` INTEGER,
                `cycle_data` TEXT
            );
        """
        db_cursor.execute(create_statement)

    def to_db(self, db_cursor: Cursor) -> None:
        insert_statement = f"""
            INSERT INTO `{TABLE_NAME}` (
                `area`,
                `sec_code`,
                `heliport_id`,
                `region`,
                `sub_code`,
                `iata`,
                `pad_id`,
                `cont_rec_no`,
                `limit_alt`,
                `datum_code`,
                `is_ifr`,
                `lat`,
                `lon`,
                `mag_var`,
                `elevation`,
                `limit`,
                `rec_vhf`,
                `rec_vhf_region`,
                `transition_alt`,
                `transition_level`,
                `usage`,
                `time_zone`,
                `daylight_ind`,
                `pad_dimensions`,
                `mag_true`,
                `heliport_name`,
                `record_number`,
                `cycle_data`
            ) VALUES (
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
            );
        """
        db_cursor.execute(
            insert_statement,
            (
                clean_value(self.area),
                clean_value(self.sec_code),
                clean_value(self.heliport_id),
                clean_value(self.region),
                clean_value(self.sub_code),
                clean_value(self.iata),
                clean_value(self.pad_id),
                clean_value(self.cont_rec_no),
                clean_value(self.limit_alt),
                clean_value(self.datum_code),
                clean_value(self.is_ifr),
                clean_value(self.lat),
                clean_value(self.lon),
                clean_value(self.mag_var),
                clean_value(self.elevation),
                clean_value(self.limit),
                clean_value(self.rec_vhf),
                clean_value(self.rec_vhf_region),
                clean_value(self.transition_alt),
                clean_value(self.transition_level),
                clean_value(self.usage),
                clean_value(self.time_zone),
                clean_value(self.daylight_ind),
                clean_value(self.pad_dimensions),
                clean_value(self.mag_true),
                clean_value(self.heliport_name),
                clean_value(self.record_number),
                clean_value(self.cycle_data),
            ),
        )

    def to_dict(self) -> dict:
        points = []
        for item in self.points:
            points.append(item.to_dict())

        departures = []
        for item in self.departures:
            departures.append(item.to_dict())

        arrivals = []
        for item in self.arrivals:
            arrivals.append(item.to_dict())

        approaches = []
        for item in self.approaches:
            approaches.append(item.to_dict())

        return {
            "area": clean_value(self.area),
            "sec_code": clean_value(self.sec_code),
            "heliport_id": clean_value(self.heliport_id),
            "region": clean_value(self.region),
            "sub_code": clean_value(self.sub_code),
            "iata": clean_value(self.iata),
            "pad_id": clean_value(self.pad_id),
            "cont_rec_no": clean_value(self.cont_rec_no),
            "limit_alt": clean_value(self.limit_alt),
            "datum_code": clean_value(self.datum_code),
            "is_ifr": clean_value(self.is_ifr),
            "lat": clean_value(self.lat),
            "lon": clean_value(self.lon),
            "mag_var": clean_value(self.mag_var),
            "elevation": clean_value(self.elevation),
            "limit": clean_value(self.limit),
            "rec_vhf": clean_value(self.rec_vhf),
            "rec_vhf_region": clean_value(self.rec_vhf_region),
            "transition_alt": clean_value(self.transition_alt),
            "transition_level": clean_value(self.transition_level),
            "usage": clean_value(self.usage),
            "time_zone": clean_value(self.time_zone),
            "daylight_ind": clean_value(self.daylight_ind),
            "pad_dimensions": clean_value(self.pad_dimensions),
            "mag_true": clean_value(self.mag_true),
            "heliport_name": clean_value(self.heliport_name),
            "record_number": clean_value(self.record_number),
            "cycle_data": clean_value(self.cycle_data),
            "points": points,
            "departures": departures,
            "arrivals": arrivals,
            "approaches": approaches,
        }
