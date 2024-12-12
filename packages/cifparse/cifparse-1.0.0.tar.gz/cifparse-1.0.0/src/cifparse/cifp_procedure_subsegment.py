from .cifp_functions import clean_value
from .cifp_procedure_point import CIFPProcedurePoint

from sqlite3 import Cursor

# FOR SUBSEGMENTS OF PD/PE/PF AND HD/HE/HF


class CIFPProcedureSubsegment:
    def __init__(self) -> None:
        self.segment_id = None
        self.points: list[CIFPProcedurePoint] = []

    def from_lines(self, cifp_lines: list) -> None:
        initial = str(cifp_lines[0])
        segment_id = initial[20:25].strip()
        self.segment_id = segment_id

        for cifp_line in cifp_lines:
            cont_rec_no = int(cifp_line[38:39])
            if cont_rec_no == 0 or cont_rec_no == 1:
                self._cont0(cifp_line)

    def _cont0(self, cifp_line: str) -> None:
        point = CIFPProcedurePoint()
        point.from_line(cifp_line)
        self.points.append(point)

    def create_db_table(db_cursor: Cursor) -> None:
        CIFPProcedurePoint.create_db_table(db_cursor)

    def to_db(self, db_cursor: Cursor) -> None:
        for item in self.points:
            item.to_db(db_cursor)

    def to_dict(self) -> dict:
        points = []
        for item in self.points:
            points.append(item.to_dict())

        return {"segment_id": clean_value(self.segment_id), "points": points}
