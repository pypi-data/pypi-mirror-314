from .cifp_restrictive_airspace_point import CIFPRestrictiveAirspacePoint
from .cifp_functions import clean_value

from sqlite3 import Cursor

TABLE_NAME = "restrictive_airspace_segments"


class CIFPRestrictiveAirspaceSegment:
    def __init__(self) -> None:
        self.restrictive_designation = None
        self.multiple_code = None
        self.lower_limit = None
        self.lower_unit = None
        self.upper_limit = None
        self.upper_unit = None
        self.restrictive_name = None
        self.points: list[CIFPRestrictiveAirspacePoint] = []

    def from_lines(self, cifp_lines: list) -> None:
        initial_line = str(cifp_lines[0])
        self.restrictive_designation = initial_line[9:19].strip()
        self.multiple_code = initial_line[19:20].strip()
        self.lower_limit = initial_line[81:86].strip()
        self.lower_unit = initial_line[86:87].strip()
        self.upper_limit = initial_line[87:92].strip()
        self.upper_unit = initial_line[92:93].strip()
        self.restrictive_name = initial_line[93:123].strip()

        ignored_terms = ["GND", "UNKNN", "UNLTD"]

        if self.lower_limit != "" and self.lower_limit not in ignored_terms:
            if self.lower_limit.startswith("FL"):
                self.lower_limit = f"{self.lower_limit[2:]}00"
            self.lower_limit = int(self.lower_limit)

        if self.upper_limit != "" and self.upper_limit not in ignored_terms:
            if self.upper_limit.startswith("FL"):
                self.upper_limit = f"{self.upper_limit[2:]}00"
            self.upper_limit = int(self.upper_limit)

        for cifp_line in cifp_lines:
            point = CIFPRestrictiveAirspacePoint()
            point.from_line(cifp_line)
            self.points.append(point)

    def create_db_table(db_cursor: Cursor) -> None:
        CIFPRestrictiveAirspacePoint.create_db_table(db_cursor)

        drop_statement = f"DROP TABLE IF EXISTS `{TABLE_NAME}`;"
        db_cursor.execute(drop_statement)

        create_statement = f"""
            CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
                `restrictive_designation` TEXT,
                `multiple_code` TEXT,
                `lower_limit` TEXT,
                `lower_unit` TEXT,
                `upper_limit` TEXT,
                `upper_unit` TEXT,
                `restrictive_name` TEXT
            );
        """
        db_cursor.execute(create_statement)

    def to_db(self, db_cursor: Cursor) -> None:
        for item in self.points:
            item.to_db(db_cursor)

        insert_statement = f"""
            INSERT INTO `{TABLE_NAME}` (
                `restrictive_designation`,
                `multiple_code`,
                `lower_limit`,
                `lower_unit`,
                `upper_limit`,
                `upper_unit`,
                `restrictive_name`
            ) VALUES (
                ?,?,?,?,?,?,?
            );
        """
        db_cursor.execute(
            insert_statement,
            (
                clean_value(self.restrictive_designation),
                clean_value(self.multiple_code),
                clean_value(self.lower_limit),
                clean_value(self.lower_unit),
                clean_value(self.upper_limit),
                clean_value(self.upper_unit),
                clean_value(self.restrictive_name),
            ),
        )

    def to_dict(self) -> dict:
        points = []
        for item in self.points:
            points.append(item.to_dict())

        return {
            "restrictive_designation": clean_value(self.restrictive_designation),
            "multiple_code": clean_value(self.multiple_code),
            "lower_limit": clean_value(self.lower_limit),
            "lower_unit": clean_value(self.lower_unit),
            "upper_limit": clean_value(self.upper_limit),
            "upper_unit": clean_value(self.upper_unit),
            "restrictive_name": clean_value(self.restrictive_name),
            "points": points,
        }
