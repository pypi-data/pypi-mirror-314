from .cifp_functions import clean_value, convert_dms, convert_mag_var

from sqlite3 import Cursor

TABLE_NAME = "vhf_dmes"


class CIFP_VHF_DME:
    def __init__(self) -> None:
        self.area = None
        self.sec_code = None
        self.sub_code = None
        self.airport_id = None
        self.airport_region = None
        self.vhf_id = None
        self.vhf_region = None
        self.frequency = None
        self.nav_class = None
        self.lat = None
        self.lon = None
        self.dme_id = None
        self.dme_lat = None
        self.dme_lon = None
        self.mag_var = None
        self.dme_elevation = None
        self.figure_of_merit = None
        self.dme_bias = None
        self.frequency_protection = None
        self.datum_code = None
        self.name = None
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
        self.sub_code = cifp_line[5:6].strip()
        self.airport_id = cifp_line[6:10].strip()
        self.airport_region = cifp_line[10:12].strip()
        # PAD 1
        self.vhf_id = cifp_line[13:17].strip()
        # PAD 2
        self.vhf_region = cifp_line[19:21].strip()
        # self.cont_rec_no = int(cifp_line[21:22].strip())
        freq = cifp_line[22:27].strip()
        self.nav_class = cifp_line[27:32].strip()
        lat_lon = cifp_line[32:51].strip()
        self.dme_id = cifp_line[51:55].strip()
        dme_lat_lon = cifp_line[55:74].strip()
        variation = cifp_line[74:79].strip()
        dme_elev = cifp_line[79:84].strip()
        self.figMerit = cifp_line[84:85].strip()
        self.dme_bias = cifp_line[85:87].strip()
        self.frequency_protection = cifp_line[87:90].strip()
        self.datum_code = cifp_line[90:93].strip()
        self.name = cifp_line[93:123].strip()
        self.record_number = int(cifp_line[123:128].strip())
        self.cycle_data = cifp_line[128:132].strip()

        if freq != "":
            self.frequency = int(freq) / 100

        if lat_lon != "":
            coordinates = convert_dms(lat_lon)
            self.lat = coordinates.lat
            self.lon = coordinates.lon

        if dme_lat_lon != "":
            coordinates = convert_dms(dme_lat_lon)
            self.dme_lat = coordinates.lat
            self.dme_lon = coordinates.lon

        if variation != "":
            mag_var = convert_mag_var(variation)
            self.mag_var = mag_var

        if dme_elev != "":
            self.dme_elevation = int(dme_elev)

    def __cont1(self, cifp_line: str) -> None:
        # PAD 22
        self.application = cifp_line[22:23].strip()
        self.notes = cifp_line[23:91].strip()

    def create_db_table(db_cursor: Cursor) -> None:
        drop_statement = "DROP TABLE IF EXISTS `{TABLE_NAME}`;"
        db_cursor.execute(drop_statement)

        create_statement = f"""
            CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
                `area` TEXT,
                `sec_code` TEXT,
                `sub_code` TEXT,
                `airport_id` TEXT,
                `airport_region` TEXT,
                `vhf_id` TEXT,
                `vhf_region` TEXT,
                `frequency` REAL,
                `nav_class` TEXT,
                `lat` REAL,
                `lon` REAL,
                `dme_id` TEXT,
                `dme_lat` REAL,
                `dme_lon` REAL,
                `mag_var` REAL,
                `dme_elevation` INTEGER,
                `figure_of_merit` TEXT,
                `dme_bias` TEXT,
                `frequency_protection` TEXT,
                `datum_code` TEXT,
                `name` TEXT,
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
                `sub_code`,
                `airport_id`,
                `airport_region`,
                `vhf_id`,
                `vhf_region`,
                `frequency`,
                `nav_class`,
                `lat`,
                `lon`,
                `dme_id`,
                `dme_lat`,
                `dme_lon`,
                `mag_var`,
                `dme_elevation`,
                `figure_of_merit`,
                `dme_bias`,
                `frequency_protection`,
                `datum_code`,
                `name`,
                `application`,
                `notes`,
                `record_number`,
                `cycle_data`
            ) VALUES (
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
            );
        """
        db_cursor.execute(
            insert_statement,
            (
                clean_value(self.area),
                clean_value(self.sec_code),
                clean_value(self.sub_code),
                clean_value(self.airport_id),
                clean_value(self.airport_region),
                clean_value(self.vhf_id),
                clean_value(self.vhf_region),
                clean_value(self.frequency),
                clean_value(self.nav_class),
                clean_value(self.lat),
                clean_value(self.lon),
                clean_value(self.dme_id),
                clean_value(self.dme_lat),
                clean_value(self.dme_lon),
                clean_value(self.mag_var),
                clean_value(self.dme_elevation),
                clean_value(self.figure_of_merit),
                clean_value(self.dme_bias),
                clean_value(self.frequency_protection),
                clean_value(self.datum_code),
                clean_value(self.name),
                clean_value(self.application),
                clean_value(self.notes),
                clean_value(self.record_number),
                clean_value(self.cycle_data),
            ),
        )

    def to_dict(self) -> dict:
        return {
            "area": clean_value(self.area),
            "sec_code": clean_value(self.sec_code),
            "sub_code": clean_value(self.sub_code),
            "airport_id": clean_value(self.airport_id),
            "airport_region": clean_value(self.airport_region),
            "vhf_id": clean_value(self.vhf_id),
            "vhf_region": clean_value(self.vhf_region),
            "frequency": clean_value(self.frequency),
            "nav_class": clean_value(self.nav_class),
            "lat": clean_value(self.lat),
            "lon": clean_value(self.lon),
            "dme_id": clean_value(self.dme_id),
            "dme_lat": clean_value(self.dme_lat),
            "dme_lon": clean_value(self.dme_lon),
            "mag_var": clean_value(self.mag_var),
            "dme_elevation": clean_value(self.dme_elevation),
            "figure_of_merit": clean_value(self.figure_of_merit),
            "dme_bias": clean_value(self.dme_bias),
            "frequency_protection": clean_value(self.frequency_protection),
            "datum_code": clean_value(self.datum_code),
            "name": clean_value(self.name),
            "application": clean_value(self.application),
            "notes": clean_value(self.notes),
            "record_number": clean_value(self.record_number),
            "cycle_data": clean_value(self.cycle_data),
        }
