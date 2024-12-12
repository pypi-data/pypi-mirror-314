from .cifp_functions import clean_value, translate_rnp

from sqlite3 import Cursor

TABLE_NAME = "airway_points"


class CIFPAirwayPoint:
    def __init__(self) -> None:
        self.area = None
        self.sec_code = None
        self.sub_code = None
        self.airway_id = None
        self.six_char = None
        self.sequence_number = None
        self.point_id = None
        self.point_region = None
        self.point_sec_code = None
        self.point_sub_code = None
        self.description_code = None
        self.bound_code = None
        self.route_type = None
        self.level = None
        self.direct = None
        self.tc_ind = None
        self.eu_ind = None
        self.rec_vhf = None
        self.rec_vhf_region = None
        self.rnp = None
        self.theta = None
        self.rho = None
        self.out_mag_crs = None
        self.from_dist = None
        self.in_mag_crs = None
        self.min_alt = None
        self.min_alt_2 = None
        self.max_alt = None
        self.fix_radius = None
        self.sig_point = None
        self.record_number = None
        self.cycle_data = None

    def from_line(self, cifp_line: str) -> None:
        # PAD 1
        self.area = cifp_line[1:4].strip()
        self.sec_code = cifp_line[4:5].strip()
        self.sub_code = cifp_line[5:6].strip()
        # PAD 7
        self.airway_id = cifp_line[13:18].strip()
        self.six_char = cifp_line[18:19].strip()
        # PAD 6
        self.sequence_number = int(cifp_line[26:29].strip())
        self.point_id = cifp_line[29:34].strip()
        self.point_region = cifp_line[34:36].strip()
        self.point_sec_code = cifp_line[36:37].strip()
        self.point_sub_code = cifp_line[37:38].strip()
        # cont_rec_no = int(cifp_line[38:39].strip())
        self.description_code = cifp_line[39:43]
        self.bound_code = cifp_line[43:44].strip()
        self.route_type = cifp_line[44:45].strip()
        self.level = cifp_line[45:46].strip()
        self.direct = cifp_line[46:47].strip()
        self.tc_ind = cifp_line[47:49].strip()
        self.eu_ind = cifp_line[49:50].strip()
        self.rec_vhf = cifp_line[50:54].strip()
        self.rec_vhf_region = cifp_line[54:56].strip()
        self.rnp = cifp_line[56:59].strip()
        # PAD 3
        self.theta = cifp_line[62:66].strip()
        self.rho = cifp_line[66:70].strip()
        out_crs = cifp_line[70:74].strip()
        dist = cifp_line[74:78].strip()
        in_crs = cifp_line[78:82].strip()
        # PAD 1
        minimum_alt = cifp_line[83:88].strip()
        minimum_alt_2 = cifp_line[88:93].strip()
        maximum_alt = cifp_line[93:98].strip()
        fix_rad = cifp_line[98:102].strip()
        # PAD 21
        self.record_number = int(cifp_line[123:128].strip())
        self.cycle_data = cifp_line[128:132].strip()

        if self.rnp != "":
            self.rnp = translate_rnp(self.rnp)

        if out_crs != "":
            self.out_mag_crs = int(out_crs) / 10

        if dist != "":
            self.from_dist = int(dist) / 10

        if in_crs != "":
            self.in_mag_crs = int(in_crs) / 10

        if minimum_alt == "UNKNN":
            minimum_alt = ""
        if minimum_alt != "":
            self.min_alt = int(minimum_alt)

        if minimum_alt_2 == "UNKNN":
            minimum_alt_2 = ""
        if minimum_alt_2 != "":
            self.min_alt_2 = int(minimum_alt_2)

        if maximum_alt == "UNKNN":
            maximum_alt = ""
        if maximum_alt != "":
            self.max_alt = int(maximum_alt)

        if fix_rad != "":
            self.fix_radius = int(fix_rad) / 10

    def set_sig_point(self, sig_point: str):
        self.sig_point = sig_point

    def create_db_table(db_cursor: Cursor) -> None:
        drop_statement = f"DROP TABLE IF EXISTS `{TABLE_NAME}`;"
        db_cursor.execute(drop_statement)

        create_statement = f"""
            CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
                `area` TEXT,
                `sec_code` TEXT,
                `sub_code` TEXT,
                `airway_id` TEXT,
                `six_char` TEXT,
                `sequence_number` INTEGER,
                `point_id` TEXT,
                `point_region` TEXT,
                `point_sec_code` TEXT,
                `point_sub_code` TEXT,
                `description_code` TEXT,
                `bound_code` TEXT,
                `route_type` TEXT,
                `level` TEXT,
                `direct` TEXT,
                `tc_ind` TEXT,
                `eu_ind` TEXT,
                `rec_vhf` TEXT,
                `rec_vhf_region` TEXT,
                `rnp` REAL,
                `theta` REAL,
                `rho` REAL,
                `out_mag_crs` REAL,
                `from_dist` REAL,
                `in_mag_crs` REAL,
                `min_alt` INTEGER,
                `min_alt_2` INTEGER,
                `max_alt` INTEGER,
                `fix_radius` REAL,
                `sig_point` TEXT,
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
                `airway_id`,
                `six_char`,
                `sequence_number`,
                `point_id`,
                `point_region`,
                `point_sec_code`,
                `point_sub_code`,
                `description_code`,
                `bound_code`,
                `route_type`,
                `level`,
                `direct`,
                `tc_ind`,
                `eu_ind`,
                `rec_vhf`,
                `rec_vhf_region`,
                `rnp`,
                `theta`,
                `rho`,
                `out_mag_crs`,
                `from_dist`,
                `in_mag_crs`,
                `min_alt`,
                `min_alt_2`,
                `max_alt`,
                `fix_radius`,
                `sig_point`,
                `record_number`,
                `cycle_data`
            ) VALUES (
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
            );
        """
        db_cursor.execute(
            insert_statement,
            (
                clean_value(self.area),
                clean_value(self.sec_code),
                clean_value(self.sub_code),
                clean_value(self.airway_id),
                clean_value(self.six_char),
                clean_value(self.sequence_number),
                clean_value(self.point_id),
                clean_value(self.point_region),
                clean_value(self.point_sec_code),
                clean_value(self.point_sub_code),
                clean_value(self.description_code),
                clean_value(self.bound_code),
                clean_value(self.route_type),
                clean_value(self.level),
                clean_value(self.direct),
                clean_value(self.tc_ind),
                clean_value(self.eu_ind),
                clean_value(self.rec_vhf),
                clean_value(self.rec_vhf_region),
                clean_value(self.rnp),
                clean_value(self.theta),
                clean_value(self.rho),
                clean_value(self.out_mag_crs),
                clean_value(self.from_dist),
                clean_value(self.in_mag_crs),
                clean_value(self.min_alt),
                clean_value(self.min_alt_2),
                clean_value(self.max_alt),
                clean_value(self.fix_radius),
                clean_value(self.sig_point),
                clean_value(self.record_number),
                clean_value(self.cycle_data),
            ),
        )

    def to_dict(self) -> dict:
        return {
            "area": clean_value(self.area),
            "sec_code": clean_value(self.sec_code),
            "sub_code": clean_value(self.sub_code),
            "airway_id": clean_value(self.airway_id),
            "six_char": clean_value(self.six_char),
            "sequence_number": clean_value(self.sequence_number),
            "point_id": clean_value(self.point_id),
            "point_region": clean_value(self.point_region),
            "point_sec_code": clean_value(self.point_sec_code),
            "point_sub_code": clean_value(self.point_sub_code),
            "description_code": clean_value(self.description_code),
            "bound_code": clean_value(self.bound_code),
            "route_type": clean_value(self.route_type),
            "level": clean_value(self.level),
            "direct": clean_value(self.direct),
            "tc_ind": clean_value(self.tc_ind),
            "eu_ind": clean_value(self.eu_ind),
            "rec_vhf": clean_value(self.rec_vhf),
            "rec_vhf_region": clean_value(self.rec_vhf_region),
            "rnp": clean_value(self.rnp),
            "theta": clean_value(self.theta),
            "rho": clean_value(self.rho),
            "out_mag_crs": clean_value(self.out_mag_crs),
            "from_dist": clean_value(self.from_dist),
            "in_mag_crs": clean_value(self.in_mag_crs),
            "min_alt": clean_value(self.min_alt),
            "min_alt_2": clean_value(self.min_alt_2),
            "max_alt": clean_value(self.max_alt),
            "fix_radius": clean_value(self.fix_radius),
            "sig_point": clean_value(self.sig_point),
            "record_number": clean_value(self.record_number),
            "cycle_data": clean_value(self.cycle_data),
        }
