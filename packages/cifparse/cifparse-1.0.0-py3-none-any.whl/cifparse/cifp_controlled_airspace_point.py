from .cifp_functions import clean_value, convert_dms, translate_rnp

from sqlite3 import Cursor

TABLE_NAME = "controlled_airspace_points"


class CIFPControlledAirspacePoint:
    def __init__(self) -> None:
        self.area = None
        self.sec_code = None
        self.sub_code = None
        self.region = None
        self.airspace_type = None
        self.center_id = None
        self.center_sec_code = None
        self.center_sub_code = None
        self.airspace_class = None
        self.multiple_code = None
        self.sequence_number = None
        self.level = None
        self.time_zone = None
        self.notam = None
        self.boundary_via = None
        self.lat = None
        self.lon = None
        self.arc_lat = None
        self.arc_lon = None
        self.arc_dist = None
        self.arc_bearing = None
        self.rnp = None
        self.lower_limit = None
        self.lower_unit = None
        self.upper_limit = None
        self.upper_unit = None
        self.airspace_name = None
        self.record_number = None
        self.cycle_data = None

    def from_line(self, cifp_line: str) -> None:
        self.area = cifp_line[1:4].strip()
        self.sec_code = cifp_line[4:5].strip()
        self.sub_code = cifp_line[5:6].strip()
        self.region = cifp_line[6:8].strip()
        self.airspace_type = cifp_line[8:9].strip()
        self.center_id = cifp_line[9:14].strip()
        self.center_sec_code = cifp_line[14:15].strip()
        self.center_sub_code = cifp_line[15:16].strip()
        self.airspace_class = cifp_line[16:17].strip()
        # PAD 2
        self.multiple_code = cifp_line[19:20].strip()
        self.sequence_number = int(cifp_line[20:24].strip())
        # cont_rec_no = int(cifp_line[24:25].strip())
        self.level = cifp_line[25:26].strip()
        self.time_zone = cifp_line[26:27].strip()
        self.notam = cifp_line[27:28].strip()
        # PAD 2
        self.boundary_via = cifp_line[30:32].strip()
        lat_lon = cifp_line[32:51].strip()
        arc_lat_lon = cifp_line[51:70].strip()
        arc_dist = cifp_line[70:74].strip()
        arc_bearing = cifp_line[74:78].strip()
        self.rnp = cifp_line[78:81].strip()
        self.lower_limit = cifp_line[81:86].strip()
        self.lower_unit = cifp_line[86:87].strip()
        self.upper_limit = cifp_line[87:92].strip()
        self.upper_unit = cifp_line[92:93].strip()
        self.airspace_name = cifp_line[93:123].strip()
        self.record_number = int(cifp_line[123:128].strip())
        self.cycle_data = cifp_line[128:132].strip()

        if lat_lon != "":
            coordinates = convert_dms(lat_lon)
            self.lat = coordinates.lat
            self.lon = coordinates.lon

        if arc_lat_lon != "":
            arc_coordinates = convert_dms(arc_lat_lon)
            self.arc_lat = arc_coordinates.lat
            self.arc_lon = arc_coordinates.lon

        if arc_dist != "":
            self.arc_dist = int(arc_dist) / 10

        if arc_bearing != "":
            self.arc_bearing = int(arc_bearing) / 10

        if self.rnp != "":
            self.rnp = translate_rnp(self.rnp)

    def create_db_table(db_cursor: Cursor) -> None:
        drop_statement = f"DROP TABLE IF EXISTS `{TABLE_NAME}`;"
        db_cursor.execute(drop_statement)

        create_statement = f"""
            CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
                `area` TEXT,
                `sec_code` TEXT,
                `sub_code` TEXT,
                `region` TEXT,
                `airspace_type` TEXT,
                `center_id` TEXT,
                `center_sec_code` TEXT,
                `center_sub_code` TEXT,
                `airspace_class` TEXT,
                `multiple_code` TEXT,
                `sequence_number` INTEGER,
                `level` TEXT,
                `time_zone` TEXT,
                `notam` TEXT,
                `boundary_via` TEXT,
                `lat` REAL,
                `lon` REAL,
                `arc_lat` REAL,
                `arc_lon` REAL,
                `arc_dist` REAL,
                `arc_bearing` REAL,
                `rnp` REAL,
                `lower_limit` TEXT,
                `lower_unit` TEXT,
                `upper_limit` TEXT,
                `upper_unit` TEXT,
                `airspace_name` TEXT,
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
                `sub_code`,
                `region`,
                `airspace_type`,
                `center_id`,
                `center_sec_code`,
                `center_sub_code`,
                `airspace_class`,
                `multiple_code`,
                `sequence_number`,
                `level`,
                `time_zone`,
                `notam`,
                `boundary_via`,
                `lat`,
                `lon`,
                `arc_lat`,
                `arc_lon`,
                `arc_dist`,
                `arc_bearing`,
                `rnp`,
                `lower_limit`,
                `lower_unit`,
                `upper_limit`,
                `upper_unit`,
                `airspace_name`,
                `record_number`,
                `cycle_data`
            ) VALUES (
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
            );
        """
        db_cursor.execute(
            insert_statement,
            (
                clean_value(self.area),
                clean_value(self.sec_code),
                clean_value(self.sub_code),
                clean_value(self.region),
                clean_value(self.airspace_type),
                clean_value(self.center_id),
                clean_value(self.center_sec_code),
                clean_value(self.center_sub_code),
                clean_value(self.airspace_class),
                clean_value(self.multiple_code),
                clean_value(self.sequence_number),
                clean_value(self.level),
                clean_value(self.time_zone),
                clean_value(self.notam),
                clean_value(self.boundary_via),
                clean_value(self.lat),
                clean_value(self.lon),
                clean_value(self.arc_lat),
                clean_value(self.arc_lon),
                clean_value(self.arc_dist),
                clean_value(self.arc_bearing),
                clean_value(self.rnp),
                clean_value(self.lower_limit),
                clean_value(self.lower_unit),
                clean_value(self.upper_limit),
                clean_value(self.upper_unit),
                clean_value(self.airspace_name),
                clean_value(self.record_number),
                clean_value(self.cycle_data),
            ),
        )

    def to_dict(self) -> dict:
        return {
            "area": clean_value(self.area),
            "sec_code": clean_value(self.sec_code),
            "sub_code": clean_value(self.sub_code),
            "region": clean_value(self.region),
            "airspace_type": clean_value(self.airspace_type),
            "center_id": clean_value(self.center_id),
            "center_sec_code": clean_value(self.center_sec_code),
            "center_sub_code": clean_value(self.center_sub_code),
            "airspace_class": clean_value(self.airspace_class),
            "multiple_code": clean_value(self.multiple_code),
            "sequence_number": clean_value(self.sequence_number),
            "level": clean_value(self.level),
            "time_zone": clean_value(self.time_zone),
            "notam": clean_value(self.notam),
            "boundary_via": clean_value(self.boundary_via),
            "lat": clean_value(self.lat),
            "lon": clean_value(self.lon),
            "arc_lat": clean_value(self.arc_lat),
            "arc_lon": clean_value(self.arc_lon),
            "arc_dist": clean_value(self.arc_dist),
            "arc_bearing": clean_value(self.arc_bearing),
            "rnp": clean_value(self.rnp),
            "lower_limit": clean_value(self.lower_limit),
            "lower_unit": clean_value(self.lower_unit),
            "upper_limit": clean_value(self.upper_limit),
            "upper_unit": clean_value(self.upper_unit),
            "airspace_name": clean_value(self.airspace_name),
            "record_number": clean_value(self.record_number),
            "cycle_data": clean_value(self.cycle_data),
        }
