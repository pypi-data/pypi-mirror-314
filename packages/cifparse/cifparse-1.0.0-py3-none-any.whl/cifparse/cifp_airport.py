from .cifp_functions import chunk, convert_dms, convert_mag_var, clean_value, yn_to_bool
from .cifp_loc_gs import CIFP_LOC_GS
from .cifp_procedure import CIFPProcedure
from .cifp_runway import CIFPRunway
from .cifp_waypoint import CIFPWaypoint

from sqlite3 import Cursor

TABLE_NAME = "airports"


class CIFPAirport:
    def __init__(self) -> None:
        self.area = None
        self.sec_code = None
        self.airport_id = None
        self.region = None
        self.sub_code = None
        self.iata = None
        self.cont_rec_no = None
        self.limit_alt = None
        self.longest = None
        self.is_ifr = None
        self.longest_surface = None
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
        self.mag_true = None
        self.datum_code = None
        self.airport_name = None
        self.record_number = None
        self.cycle_data = None
        self.points: list[CIFPWaypoint] = []
        self.loc_gs: list[CIFP_LOC_GS] = []
        self.departures: list[CIFPProcedure] = []
        self.arrivals: list[CIFPProcedure] = []
        self.approaches: list[CIFPProcedure] = []
        self.runways: list[CIFPRunway] = []
        self._departure_lines = []
        self._departure_chunked = []
        self._arrival_lines = []
        self._arrival_chunked = []
        self._approach_lines = []
        self._approach_chunked = []

    def from_lines(self, cifp_lines: list) -> None:
        for cifp_line in cifp_lines:
            sub_code = cifp_line[12:13]
            # cont_rec_no = int(cifp_line[38:39])
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
            if sub_code == "G":
                self._sec_G(cifp_line)
            if sub_code == "I":
                self._sec_I(cifp_line)

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
        self._sec_code = cifp_line[4:5].strip()
        # PAD 1
        self.airport_id = cifp_line[6:10].strip()
        self.region = cifp_line[10:12].strip()
        self.sub_code = cifp_line[12:13].strip()
        self.iata = cifp_line[13:16].strip()
        # PAD 5
        self.cont_rec_no = int(cifp_line[21:22].strip())
        speed_limit_alt = cifp_line[22:27].strip()
        longest_runway = cifp_line[27:30].strip()
        is_ifr = cifp_line[30:31].strip()
        self.longest_surface = cifp_line[31:32].strip()
        lat_lon = cifp_line[32:51].strip()
        variation = cifp_line[51:56].strip()
        elev = cifp_line[56:61].strip()
        speed_limit = cifp_line[61:64].strip()
        self.rec_vhf = cifp_line[64:68].strip()
        self.rec_vhf_region = cifp_line[68:70].strip()
        tr_alt = cifp_line[70:75].strip()
        self.transition_alt = None
        tr_level = cifp_line[75:80].strip()
        self.transition_level = None
        self.usage = cifp_line[80:81].strip()
        self.time_zone = cifp_line[81:84].strip()
        self.daylight_ind = cifp_line[84:85].strip()
        self.mag_true = cifp_line[85:86].strip()
        self.datum_code = cifp_line[86:89].strip()
        # PAD 4
        self.airport_name = cifp_line[93:123].strip()
        self.record_number = int(cifp_line[123:128].strip())
        self.cycle_data = cifp_line[128:132].strip()

        if speed_limit_alt != "":
            self.limit_alt = int(speed_limit_alt)

        if longest_runway != "":
            self.longest = int(longest_runway) * 100

        if is_ifr != "":
            self.is_ifr = yn_to_bool(is_ifr)

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

    def _sec_G(self, cifp_line: str) -> None:
        runway = CIFPRunway()
        runway.from_line(cifp_line)
        self.runways.append(runway)

    def _sec_I(self, cifp_line: str) -> None:
        loc_gs = CIFP_LOC_GS()
        loc_gs.from_lines([cifp_line])
        self.loc_gs.append(loc_gs)

    def create_db_table(db_cursor: Cursor) -> None:
        CIFP_LOC_GS.create_db_table(db_cursor)
        CIFPProcedure.create_db_table(db_cursor)
        CIFPRunway.create_db_table(db_cursor)

        drop_statement = f"DROP TABLE IF EXISTS `{TABLE_NAME}`;"
        db_cursor.execute(drop_statement)

        create_statement = f"""
            CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
                `area` TEXT,
                `sec_code` TEXT,
                `airport_id` TEXT,
                `region` TEXT,
                `sub_code` TEXT,
                `iata` TEXT,
                `cont_rec_no` INTEGER,
                `limit_alt` TEXT,
                `longest` INTEGER,
                `is_ifr` INTEGER,
                `longest_surface` TEXT,
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
                `mag_true` TEXT,
                `datum_code` TEXT,
                `airport_name` TEXT,
                `record_number` INTEGER,
                `cycle_data` TEXT
            );
        """
        db_cursor.execute(create_statement)

    def to_db(self, db_cursor: Cursor) -> None:
        for item in self.loc_gs:
            item.to_db(db_cursor)

        for item in self.departures:
            item.to_db(db_cursor)

        for item in self.arrivals:
            item.to_db(db_cursor)

        for item in self.approaches:
            item.to_db(db_cursor)

        for item in self.runways:
            item.to_db(db_cursor)

        insert_statement = f"""
            INSERT INTO `{TABLE_NAME}` (
                `area`,
                `sec_code`,
                `airport_id`,
                `region`,
                `sub_code`,
                `iata`,
                `cont_rec_no`,
                `limit_alt`,
                `longest`,
                `is_ifr`,
                `longest_surface`,
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
                `mag_true`,
                `datum_code`,
                `airport_name`,
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
                clean_value(self.airport_id),
                clean_value(self.region),
                clean_value(self.sub_code),
                clean_value(self.iata),
                clean_value(self.cont_rec_no),
                clean_value(self.limit_alt),
                clean_value(self.longest),
                clean_value(self.is_ifr),
                clean_value(self.longest_surface),
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
                clean_value(self.mag_true),
                clean_value(self.datum_code),
                clean_value(self.airport_name),
                clean_value(self.record_number),
                clean_value(self.cycle_data),
            ),
        )

    def to_dict(self) -> dict:
        points = []
        for item in self.points:
            points.append(item.to_dict())

        loc_gs = []
        for item in self.loc_gs:
            loc_gs.append(item.to_dict())

        departures = []
        for item in self.departures:
            departures.append(item.to_dict())

        arrivals = []
        for item in self.arrivals:
            arrivals.append(item.to_dict())

        approaches = []
        for item in self.approaches:
            approaches.append(item.to_dict())

        runways = []
        for item in self.runways:
            runways.append(item.to_dict())

        return {
            "area": clean_value(self.area),
            "sec_code": clean_value(self.sec_code),
            "airport_id": clean_value(self.airport_id),
            "region": clean_value(self.region),
            "sub_code": clean_value(self.sub_code),
            "iata": clean_value(self.iata),
            "cont_rec_no": clean_value(self.cont_rec_no),
            "limit_alt": clean_value(self.limit_alt),
            "longest": clean_value(self.longest),
            "is_ifr": clean_value(self.is_ifr),
            "longest_surface": clean_value(self.longest_surface),
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
            "mag_true": clean_value(self.mag_true),
            "datum_code": clean_value(self.datum_code),
            "airport_name": clean_value(self.airport_name),
            "record_number": clean_value(self.record_number),
            "cycle_data": clean_value(self.cycle_data),
            "points": points,
            "loc_gs": loc_gs,
            "departures": departures,
            "arrivals": arrivals,
            "approaches": approaches,
            "runways": runways,
        }
