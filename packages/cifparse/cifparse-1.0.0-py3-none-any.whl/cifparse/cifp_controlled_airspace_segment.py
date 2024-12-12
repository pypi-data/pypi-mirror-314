from .cifp_controlled_airspace_point import CIFPControlledAirspacePoint
from .cifp_functions import clean_value

from sqlite3 import Cursor

TABLE_NAME = "controlled_airspace_segments"


class CIFPControlledAirspaceSegment:
    def __init__(self) -> None:
        self.center_id = None
        self.multiple_code = None
        self.lower_limit = None
        self.lower_unit = None
        self.upper_limit = None
        self.upper_unit = None
        self.airspace_name = None
        self.points: list[CIFPControlledAirspacePoint] = []

    def from_lines(self, cifp_lines: list) -> None:
        initial_line = str(cifp_lines[0])
        self.center_id = initial_line[9:14].strip()
        self.multiple_code = initial_line[19:20].strip()
        self.lower_limit = initial_line[81:86].strip()
        self.lower_unit = initial_line[86:87].strip()
        self.upper_limit = initial_line[87:92].strip()
        self.upper_unit = initial_line[92:93].strip()
        self.airspace_name = initial_line[93:123].strip()

        for cifp_line in cifp_lines:
            point = CIFPControlledAirspacePoint()
            point.from_line(cifp_line)
            self.points.append(point)

    def create_db_table(db_cursor: Cursor) -> None:
        CIFPControlledAirspacePoint.create_db_table(db_cursor)

        drop_statement = f"DROP TABLE IF EXISTS `{TABLE_NAME}`;"
        db_cursor.execute(drop_statement)

        create_statement = f"""
            CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
                `center_id` TEXT,
                `multiple_code` TEXT,
                `lower_limit` TEXT,
                `lower_unit` TEXT,
                `upper_limit` TEXT,
                `upper_unit` TEXT,
                `airspace_name` TEXT
            );
        """
        db_cursor.execute(create_statement)

    def to_db(self, db_cursor: Cursor) -> None:
        for item in self.points:
            item.to_db(db_cursor)

        insert_statement = f"""
            INSERT INTO `{TABLE_NAME}` (
                `center_id`,
                `multiple_code`,
                `lower_limit`,
                `lower_unit`,
                `upper_limit`,
                `upper_unit`,
                `airspace_name`
            ) VALUES (
                ?,?,?,?,?,?,?
            );
        """
        db_cursor.execute(
            insert_statement,
            (
                clean_value(self.center_id),
                clean_value(self.multiple_code),
                clean_value(self.lower_limit),
                clean_value(self.lower_unit),
                clean_value(self.upper_limit),
                clean_value(self.upper_unit),
                clean_value(self.airspace_name),
            ),
        )

    def to_dict(self) -> dict:
        points = []
        for item in self.points:
            points.append(item.to_dict())

        return {
            "multiple_code": clean_value(self.multiple_code),
            "airspace_name": clean_value(self.airspace_name),
            "points": points,
        }
