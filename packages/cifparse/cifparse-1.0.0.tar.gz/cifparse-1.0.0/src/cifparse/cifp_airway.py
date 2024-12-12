from .cifp_airway_point import CIFPAirwayPoint
from .cifp_functions import clean_value

from sqlite3 import Cursor

TABLE_NAME = "airways"


class CIFPAirway:
    def __init__(self) -> None:
        self.area = None
        self.sec_code = None
        self.sub_code = None
        self.airway_id = None
        self.six_char = None
        self.application = None
        self.notes = None
        self.points: list[CIFPAirwayPoint] = []
        self._is_start_set = False

    def from_lines(self, cifp_lines: list) -> None:
        for cifp_line in cifp_lines:
            cont_rec_no = int(cifp_line[38:39])
            if cont_rec_no == 0:
                self._cont0(cifp_line)
            if cont_rec_no == 1:
                self._cont1(cifp_line)

    def _cont0(self, cifp_line: str) -> None:
        if self.airway_id == None:
            # PAD 1
            self.area = cifp_line[1:4].strip()
            self.sec_code = cifp_line[4:5].strip()
            self.sub_code = cifp_line[5:6].strip()
            # PAD 7
            self.airway_id = cifp_line[13:18].strip()
            self.six_char = cifp_line[18:19].strip()

        point = CIFPAirwayPoint()
        point.from_line(cifp_line)

        is_start = False
        if self._is_start_set == False:
            self._is_start_set = True
            is_start = True

        desc_code = cifp_line[39:43]
        is_end = False
        if desc_code[1:2] == "E":
            self._is_start_set = False
            is_end = True

        if is_start == True:
            sig_point = "S"
            point.set_sig_point(sig_point)
        if is_end == True:
            sig_point = "E"
            point.set_sig_point(sig_point)

        self.points.append(point)

    def _cont1(self, cifp_line: str) -> None:
        # PAD 38
        self.application = cifp_line[39:40]
        self.notes = cifp_line[40:109]

    def create_db_table(db_cursor: Cursor) -> None:
        CIFPAirwayPoint.create_db_table(db_cursor)

        drop_statement = f"DROP TABLE IF EXISTS `{TABLE_NAME}`;"
        db_cursor.execute(drop_statement)

        create_statement = f"""
            CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
                `area` TEXT,
                `sec_code` TEXT,
                `sub_code` TEXT,
                `airway_id` TEXT,
                `six_char` TEXT,
                `application` TEXT,
                `notes` TEXT
            );
        """
        db_cursor.execute(create_statement)

    def to_db(self, db_cursor: Cursor) -> None:
        for item in self.points:
            item.to_db(db_cursor)

        insert_statement = f"""
            INSERT INTO `{TABLE_NAME}` (
                `area`,
                `sec_code`,
                `sub_code`,
                `airway_id`,
                `six_char`,
                `application`,
                `notes`
            ) VALUES (
                ?,?,?,?,?,?,?
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
                clean_value(self.six_char),
                clean_value(self.application),
            ),
        )

    def to_dict(self) -> dict:
        points = []
        for item in self.points:
            points.append(item.to_dict())

        return {
            "area": clean_value(self.area),
            "sec_code": clean_value(self.sec_code),
            "sub_code": clean_value(self.sub_code),
            "airway_id": clean_value(self.airway_id),
            "six_char": clean_value(self.six_char),
            "application": clean_value(self.application),
            "notes": clean_value(self.notes),
            "points": points,
        }
