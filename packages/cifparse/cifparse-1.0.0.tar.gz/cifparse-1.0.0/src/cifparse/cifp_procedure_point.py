from .cifp_functions import clean_value, translate_rnp

from sqlite3 import Cursor

TABLE_NAME = "procedure_points"

# FOR PD/PE/PF AND HD/HE/HF


class CIFPProcedurePoint:
    def __init__(self) -> None:
        self.area = None
        self.sec_code = None
        self.fac_id = None
        self.fac_region = None
        self.fac_sub_code = None
        self.procedure_id = None
        self.route_type = None
        self.transition_id = None
        self.sequence_number = None
        self.fix_id = None
        self.fix_region = None
        self.fix_sec_code = None
        self.fix_sub_code = None
        self.description_code = None
        self.turn_direction = None
        self.rnp = None
        self.path_term = None
        self.tdv = None
        self.rec_vhf = None
        self.rec_vhf_region = None
        self.arc_radius = None
        self.theta = None
        self.rho = None
        self.course = None
        self.dist = None
        self.time = None
        self.rec_vhf_sec_code = None
        self.rec_vhf_sub_code = None
        self.alt_desc = None
        self.atc = None
        self.altitude = None
        self.flight_level = None
        self.altitude_2 = None
        self.flight_level_2 = None
        self.trans_alt = None
        self.speed_limit = None
        self.vert_angle = None
        self.center_fix = None
        self.multiple_code = None
        self.center_fix_region = None
        self.center_fix_sec_code = None
        self.center_fix_sub_code = None
        self.gns_fms_id = None
        self.speed_limit_2 = None
        self.rte_qual_1 = None
        self.rte_qual_2 = None
        self.record_number = None
        self.cycle_data = None

    def from_line(self, cifp_line: str) -> None:
        # PAD 1
        self.area = cifp_line[1:4].strip()
        self.sec_code = cifp_line[4:5].strip()
        # PAD 1
        self.fac_id = cifp_line[6:10].strip()
        self.fac_region = cifp_line[10:12].strip()
        self.fac_sub_code = cifp_line[12:13].strip()
        self.procedure_id = cifp_line[13:19].strip()
        self.route_type = cifp_line[19:20].strip()
        self.transition_id = cifp_line[20:25].strip()
        # PAD 1
        self.sequence_number = int(cifp_line[26:29].strip())
        self.fix_id = cifp_line[29:34].strip()
        self.fix_region = cifp_line[34:36].strip()
        self.fix_sec_code = cifp_line[36:37].strip()
        self.fix_sub_code = cifp_line[37:38].strip()
        self.cont_rec_no = int(cifp_line[38:39])
        self.description_code = cifp_line[39:43]
        self.turn_direction = cifp_line[43:44].strip()
        self.rnp = cifp_line[44:47].strip()
        self.path_term = cifp_line[47:49].strip()
        self.tdv = cifp_line[49:50].strip()
        self.rec_vhf = cifp_line[50:54].strip()
        self.rec_vhf_region = cifp_line[54:56].strip()
        arc_rad = cifp_line[56:62].strip()
        theta_s = cifp_line[62:66].strip()
        rho_s = cifp_line[66:70].strip()
        crs = cifp_line[70:74].strip()
        dist_time = cifp_line[74:78].strip()
        self.rec_vhf_sec_code = cifp_line[78:79].strip()
        self.rec_vhf_sub_code = cifp_line[79:80].strip()
        # RESERVED 2
        self.alt_desc = cifp_line[82:83].strip()
        self.atc = cifp_line[83:84].strip()
        alt = cifp_line[84:89].strip()
        alt_2 = cifp_line[89:94].strip()
        trans_alt = cifp_line[94:99].strip()
        speed = cifp_line[99:102].strip()
        vert_angle = cifp_line[102:106].strip()
        self.center_fix = cifp_line[106:111].strip()
        self.multiple_code = cifp_line[111:112].strip()
        self.center_fix_region = cifp_line[112:114].strip()
        self.center_fix_sec_code = cifp_line[114:115].strip()
        self.center_fix_sub_code = cifp_line[115:116].strip()
        self.gns_fms_id = cifp_line[116:117].strip()
        self.speed_limit_2 = cifp_line[117:118].strip()
        self.rte_qual_1 = cifp_line[118:119].strip()
        self.rte_qual_2 = cifp_line[119:120].strip()
        # PAD 3
        self.record_number = int(cifp_line[123:128].strip())
        self.cycle_data = cifp_line[128:132].strip()

        if self.rnp != "":
            self.rnp = translate_rnp(self.rnp)

        if arc_rad != "":
            self.arc_radius = int(arc_rad) / 1000

        if theta_s != "":
            self.theta = int(theta_s) / 10

        if rho_s != "":
            self.rho = int(rho_s) / 10

        if crs != "":
            self.course = int(crs) / 10

        if dist_time != "":
            if dist_time.startswith("T"):
                self.time = int(dist_time[1:]) / 10
            else:
                self.distance = int(dist_time) / 10

        if alt != "":
            if alt.startswith("FL"):
                self.flight_level = int(alt[2:])
            else:
                self.altitude = int(alt)

        if alt_2 != "":
            if alt_2.startswith("FL"):
                self.flight_level_2 = int(alt_2[2:])
            else:
                self.altitude_2 = int(alt_2)

        if trans_alt != "":
            self.transition_alt = int(trans_alt)

        if speed != "":
            self.speed_limit = int(speed)

        if vert_angle != "":
            self.vertical_angle = int(vert_angle)

    def create_db_table(db_cursor: Cursor) -> None:
        drop_statement = f"DROP TABLE IF EXISTS `{TABLE_NAME}`;"
        db_cursor.execute(drop_statement)

        create_statement = f"""
            CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
                `area` TEXT,
                `sec_code` TEXT,
                `fac_id` TEXT,
                `fac_region` TEXT,
                `fac_sub_code` TEXT,
                `procedure_id` TEXT,
                `route_type` TEXT,
                `transition_id` TEXT,
                `sequence_number` INTEGER,
                `fix_id` TEXT,
                `fix_region` TEXT,
                `fix_sec_code` TEXT,
                `fix_sub_code` TEXT,
                `description_code` TEXT,
                `turn_direction` TEXT,
                `rnp` REAL,
                `path_term` TEXT,
                `tdv` TEXT,
                `rec_vhf` TEXT,
                `rec_vhf_region` TEXT,
                `arc_radius` REAL,
                `theta` REAL,
                `rho` REAL,
                `course` EARL,
                `dist` REAL,
                `time` REAL,
                `rec_vhf_sec_code` TEXT,
                `rec_vhf_sub_code` TEXT,
                `alt_desc` TEXT,
                `atc` TEXT,
                `altitude` INTEGER,
                `flight_level` INTEGER,
                `altitude_2` INTEGER,
                `flight_level_2` INTEGER,
                `trans_alt` INTEGER,
                `speed_limit` INTEGER,
                `vert_angle` INTEGER,
                `center_fix` TEXT,
                `multiple_code` TEXT,
                `center_fix_region` TEXT,
                `center_fix_sec_code` TEXT,
                `center_fix_sub_code` TEXT,
                `gns_fms_id` TEXT,
                `speed_limit_2` TEXT,
                `rte_qual_1` TEXT,
                `rte_qual_2` TEXT,
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
                `fac_id`,
                `fac_region`,
                `fac_sub_code`,
                `procedure_id`,
                `route_type`,
                `transition_id`,
                `sequence_number`,
                `fix_id`,
                `fix_region`,
                `fix_sec_code`,
                `fix_sub_code`,
                `description_code`,
                `turn_direction`,
                `rnp`,
                `path_term`,
                `tdv`,
                `rec_vhf`,
                `rec_vhf_region`,
                `arc_radius`,
                `theta`,
                `rho`,
                `course`,
                `dist`,
                `time`,
                `rec_vhf_sec_code`,
                `rec_vhf_sub_code`,
                `alt_desc`,
                `atc`,
                `altitude`,
                `flight_level`,
                `altitude_2`,
                `flight_level_2`,
                `trans_alt`,
                `speed_limit`,
                `vert_angle`,
                `center_fix`,
                `multiple_code`,
                `center_fix_region`,
                `center_fix_sec_code`,
                `center_fix_sub_code`,
                `gns_fms_id`,
                `speed_limit_2`,
                `rte_qual_1`,
                `rte_qual_2`,
                `record_number`,
                `cycle_data`
            ) VALUES (
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
            );
        """
        db_cursor.execute(
            insert_statement,
            (
                clean_value(self.area),
                clean_value(self.sec_code),
                clean_value(self.fac_id),
                clean_value(self.fac_region),
                clean_value(self.fac_sub_code),
                clean_value(self.procedure_id),
                clean_value(self.route_type),
                clean_value(self.transition_id),
                clean_value(self.sequence_number),
                clean_value(self.fix_id),
                clean_value(self.fix_region),
                clean_value(self.fix_sec_code),
                clean_value(self.fix_sub_code),
                clean_value(self.description_code),
                clean_value(self.turn_direction),
                clean_value(self.rnp),
                clean_value(self.path_term),
                clean_value(self.tdv),
                clean_value(self.rec_vhf),
                clean_value(self.rec_vhf_region),
                clean_value(self.arc_radius),
                clean_value(self.theta),
                clean_value(self.rho),
                clean_value(self.course),
                clean_value(self.dist),
                clean_value(self.time),
                clean_value(self.rec_vhf_sec_code),
                clean_value(self.rec_vhf_sub_code),
                clean_value(self.alt_desc),
                clean_value(self.atc),
                clean_value(self.altitude),
                clean_value(self.flight_level),
                clean_value(self.altitude_2),
                clean_value(self.flight_level_2),
                clean_value(self.trans_alt),
                clean_value(self.speed_limit),
                clean_value(self.vert_angle),
                clean_value(self.center_fix),
                clean_value(self.multiple_code),
                clean_value(self.center_fix_region),
                clean_value(self.center_fix_sec_code),
                clean_value(self.center_fix_sub_code),
                clean_value(self.gns_fms_id),
                clean_value(self.speed_limit_2),
                clean_value(self.rte_qual_1),
                clean_value(self.rte_qual_2),
                clean_value(self.record_number),
                clean_value(self.cycle_data),
            ),
        )

    def to_dict(self) -> dict:
        return {
            "area": clean_value(self.area),
            "sec_code": clean_value(self.sec_code),
            "fac_id": clean_value(self.fac_id),
            "fac_region": clean_value(self.fac_region),
            "fac_sub_code": clean_value(self.fac_sub_code),
            "procedure_id": clean_value(self.procedure_id),
            "route_type": clean_value(self.route_type),
            "transition_id": clean_value(self.transition_id),
            "sequence_number": clean_value(self.sequence_number),
            "fix_id": clean_value(self.fix_id),
            "fix_region": clean_value(self.fix_region),
            "fix_sec_code": clean_value(self.fix_sec_code),
            "fix_sub_code": clean_value(self.fix_sub_code),
            "description_code": clean_value(self.description_code),
            "turn_direction": clean_value(self.turn_direction),
            "rnp": clean_value(self.rnp),
            "path_term": clean_value(self.path_term),
            "tdv": clean_value(self.tdv),
            "rec_vhf": clean_value(self.rec_vhf),
            "rec_vhf_region": clean_value(self.rec_vhf_region),
            "arc_radius": clean_value(self.arc_radius),
            "theta": clean_value(self.theta),
            "rho": clean_value(self.rho),
            "course": clean_value(self.course),
            "dist": clean_value(self.dist),
            "time": clean_value(self.time),
            "rec_vhf_sec_code": clean_value(self.rec_vhf_sec_code),
            "rec_vhf_sub_code": clean_value(self.rec_vhf_sub_code),
            "alt_desc": clean_value(self.alt_desc),
            "atc": clean_value(self.atc),
            "altitude": clean_value(self.altitude),
            "flight_level": clean_value(self.flight_level),
            "altitude_2": clean_value(self.altitude_2),
            "flight_level_2": clean_value(self.flight_level_2),
            "trans_alt": clean_value(self.trans_alt),
            "speed_limit": clean_value(self.speed_limit),
            "vert_angle": clean_value(self.vert_angle),
            "center_fix": clean_value(self.center_fix),
            "multiple_code": clean_value(self.multiple_code),
            "center_fix_region": clean_value(self.center_fix_region),
            "center_fix_sec_code": clean_value(self.center_fix_sec_code),
            "center_fix_sub_code": clean_value(self.center_fix_sub_code),
            "gns_fms_id": clean_value(self.gns_fms_id),
            "speed_limit_2": clean_value(self.speed_limit_2),
            "rte_qual_1": clean_value(self.rte_qual_1),
            "rte_qual_2": clean_value(self.rte_qual_2),
            "record_number": clean_value(self.record_number),
            "cycle_data": clean_value(self.cycle_data),
        }
