from .cifp_functions import clean_value, convert_dms, convert_mag_var

from sqlite3 import Cursor

TABLE_NAME = "loc_gs"


class CIFP_LOC_GS:
    def __init__(self) -> None:
        self.area = None
        self.sec_code = None
        self.airport_id = None
        self.airport_region = None
        self.sub_code = None
        self.loc_id = None
        self.cat = None
        self.frequency = None
        self.runway_id = None
        self.loc_lat = None
        self.loc_lon = None
        self.loc_bearing = None
        self.gs_lat = None
        self.gs_lon = None
        self.loc_dist = None
        self.plus_minus = None
        self.gs_thr_dist = None
        self.loc_width = None
        self.gs_angle = None
        self.mag_var = None
        self.tch = None
        self.gs_elevation = None
        self.support_fac = None
        self.support_region = None
        self.support_sec_code = None
        self.support_sub_code = None
        self.application = None
        self.notes = None
        self.record_number = None
        self.cycle_data = None

    def from_lines(self, cifp_lines: list) -> None:
        for cifp_line in cifp_lines:
            cont_rec_no = int(cifp_line[21:22])
            if cont_rec_no == 0:
                self.__cont0(cifp_line)
            if cont_rec_no == 1:
                self.__cont1(cifp_line)

    def __cont0(self, cifp_line: str) -> None:
        # PAD 1
        self.area = cifp_line[1:4].strip()
        self.sec_code = cifp_line[4:5].strip()
        # PAD 1
        self.airport_id = cifp_line[6:10].strip()
        self.airport_region = cifp_line[10:12].strip()
        self.sub_code = cifp_line[12:13].strip()
        self.loc_id = cifp_line[13:17].strip()
        self.cat = cifp_line[17:18].strip()
        # PAD 3
        # self.cont_rec_no = int(cifp_line[21:22].strip())
        freq = cifp_line[22:27].strip()
        self.runway_id = cifp_line[27:32].strip()
        loc_lat_lon = cifp_line[32:51].strip()
        loc_brg = cifp_line[51:55].strip()
        gs_lat_lon = cifp_line[55:74].strip()
        loc_from_end = cifp_line[74:78].strip()
        self.plus_minus = cifp_line[78:79].strip()
        gs_from_thr = cifp_line[79:83].strip()
        loc_deg_width = cifp_line[83:87].strip()
        gs_deg_angle = cifp_line[87:90].strip()
        variation = cifp_line[90:95].strip()
        thr_cross_height = cifp_line[95:97].strip()
        gs_elev = cifp_line[97:102].strip()
        self.support_fac = cifp_line[102:106].strip()
        self.support_region = cifp_line[106:108].strip()
        self.support_sec_code = cifp_line[108:109].strip()
        self.support_sub_code = cifp_line[109:110].strip()
        # PAD 13
        self.record_number = int(cifp_line[123:128].strip())
        self.cycle_data = cifp_line[128:132].strip()

        if freq != "":
            self.frequency = int(freq) / 100

        if loc_lat_lon != "":
            coordinates = convert_dms(loc_lat_lon)
            self.loc_lat = coordinates.lat
            self.loc_lon = coordinates.lon

        if loc_brg != "":
            self.loc_bearing = int(loc_brg) / 10

        if gs_lat_lon != "":
            coordinates = convert_dms(gs_lat_lon)
            self.gs_lat = coordinates.lat
            self.gs_lon = coordinates.lon

        if loc_from_end != "":
            self.loc_dist = int(loc_from_end)

        if gs_from_thr != "":
            self.gs_thr_dist = int(gs_from_thr)

        if loc_deg_width != "":
            self.loc_width = int(loc_deg_width) / 100

        if gs_deg_angle != "":
            self.gs_angle = int(gs_deg_angle) / 100

        if thr_cross_height != "":
            self.tch = int(thr_cross_height)

        if gs_elev != "":
            self.gs_elevation = int(gs_elev)

        if variation != "":
            mag_var = convert_mag_var(variation)
            self.mag_var = mag_var

    def __cont1(self, cifp_line: str) -> None:
        # PAD 22
        self.application = cifp_line[22:23].strip()
        self.notes = cifp_line[23:92].strip()

    def create_db_table(db_cursor: Cursor) -> None:
        drop_statement = "DROP TABLE IF EXISTS `{TABLE_NAME}`;"
        db_cursor.execute(drop_statement)

        create_statement = f"""
            CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
                `area` TEXT,
                `sec_code` TEXT,
                `airport_id` TEXT,
                `airport_region` TEXT,
                `sub_code` TEXT,
                `loc_id` TEXT,
                `cat` TEXT,
                `frequency` REAL,
                `runway_id` TEXT,
                `loc_lat` REAL,
                `loc_lon` REAL,
                `loc_bearing` REAL,
                `gs_lat` REAL,
                `gs_lon` REAL,
                `loc_dist` INTEGER,
                `plus_minus` TEXT,
                `gs_thr_dist` INTEGER,
                `loc_width` REAL,
                `gs_angle` REAL,
                `mag_var` INTEGER,
                `tch` INTEGER,
                `gs_elevation` INTEGER,
                `support_fac` TEXT,
                `support_region` TEXT,
                `support_sec_code` TEXT,
                `support_sub_code` TEXT,
                `application` TEXT,
                `notes` TEXT,
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
                `airport_id`,
                `airport_region`,
                `sub_code`,
                `loc_id`,
                `cat`,
                `frequency`,
                `runway_id`,
                `loc_lat`,
                `loc_lon`,
                `loc_bearing`,
                `gs_lat`,
                `gs_lon`,
                `loc_dist`,
                `plus_minus`,
                `gs_thr_dist`,
                `loc_width`,
                `gs_angle`,
                `mag_var`,
                `tch`,
                `gs_elevation`,
                `support_fac`,
                `support_region`,
                `support_sec_code`,
                `support_sub_code`,
                `application`,
                `notes`,
                `record_number`,
                `cycle_data`
            ) VALUES (
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
            );
        """
        db_cursor.execute(
            insert_statement,
            (
                self.area,
                self.sec_code,
                self.airport_id,
                self.airport_region,
                self.sub_code,
                self.loc_id,
                self.cat,
                self.frequency,
                self.runway_id,
                self.loc_lat,
                self.loc_lon,
                self.loc_bearing,
                self.gs_lat,
                self.gs_lon,
                self.loc_dist,
                self.plus_minus,
                self.gs_thr_dist,
                self.loc_width,
                self.gs_angle,
                self.mag_var,
                self.tch,
                self.gs_elevation,
                self.support_fac,
                self.support_region,
                self.support_sec_code,
                self.support_sub_code,
                self.application,
                self.notes,
                self.record_number,
                self.cycle_data,
            ),
        )

    def to_dict(self) -> dict:
        return {
            "area": clean_value(self.area),
            "sec_code": clean_value(self.sec_code),
            "airport_id": clean_value(self.airport_id),
            "airport_region": clean_value(self.airport_region),
            "sub_code": clean_value(self.sub_code),
            "loc_id": clean_value(self.loc_id),
            "cat": clean_value(self.cat),
            "frequency": clean_value(self.frequency),
            "runway_id": clean_value(self.runway_id),
            "loc_lat": clean_value(self.loc_lat),
            "loc_lon": clean_value(self.loc_lon),
            "loc_bearing": clean_value(self.loc_bearing),
            "gs_lat": clean_value(self.gs_lat),
            "gs_lon": clean_value(self.gs_lon),
            "loc_dist": clean_value(self.loc_dist),
            "plus_minus": clean_value(self.plus_minus),
            "gs_thr_dist": clean_value(self.gs_thr_dist),
            "loc_width": clean_value(self.loc_width),
            "gs_angle": clean_value(self.gs_angle),
            "mag_var": clean_value(self.mag_var),
            "tch": clean_value(self.tch),
            "gs_elevation": clean_value(self.gs_elevation),
            "support_fac": clean_value(self.support_fac),
            "support_region": clean_value(self.support_region),
            "support_sec_code": clean_value(self.support_sec_code),
            "support_sub_code": clean_value(self.support_sub_code),
            "application": clean_value(self.application),
            "notes": clean_value(self.notes),
            "record_number": clean_value(self.record_number),
            "cycle_data": clean_value(self.cycle_data),
        }
