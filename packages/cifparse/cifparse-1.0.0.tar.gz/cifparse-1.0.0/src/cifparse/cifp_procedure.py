from .cifp_functions import chunk, clean_value
from .cifp_procedure_segment import CIFPProcedureSegment

from sqlite3 import Cursor

# FOR ENTIRE COLLECTION OF PD/PE/PF AND HD/HE/HF


class CIFPProcedure:
    def __init__(self) -> None:
        self.area = None
        self.sec_code = None
        self.procedure_id = None
        self.segments: list[CIFPProcedureSegment] = []

    def from_lines(self, cifp_lines: list) -> None:
        segment_chunked = chunk(cifp_lines, 13, 20)
        self._segment_to_object(segment_chunked)

        cifp_line = str(cifp_lines[0])
        self.area = cifp_line[1:4].strip()
        self.sec_code = cifp_line[4:5].strip()
        self.procedure_id = cifp_line[13:19].strip()

    def _segment_to_object(self, chunked_list: list) -> None:
        for segment_chunk in chunked_list:
            segment = CIFPProcedureSegment()
            segment.from_lines(segment_chunk)
            self.segments.append(segment)

    def create_db_table(db_cursor: Cursor) -> None:
        CIFPProcedureSegment.create_db_table(db_cursor)

    def to_db(self, db_cursor: Cursor) -> None:
        for item in self.segments:
            item.to_db(db_cursor)

    def to_dict(self) -> dict:
        segments = []
        for item in self.segments:
            segments.append(item.to_dict())

        return {
            "area": clean_value(self.area),
            "sec_code": clean_value(self.sec_code),
            "procedure_id": clean_value(self.procedure_id),
            "segments": segments,
        }
