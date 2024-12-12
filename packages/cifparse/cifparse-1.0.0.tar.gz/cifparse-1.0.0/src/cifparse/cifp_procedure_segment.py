from .cifp_functions import chunk, clean_value
from .cifp_procedure_subsegment import CIFPProcedureSubsegment

from sqlite3 import Cursor

# FOR COLLECTION OF SUBSEGMENTS OF PD/PE/PF AND HD/HE/HF


class CIFPProcedureSegment:
    def __init__(self) -> None:
        self.type = None
        self.subsegments: list[CIFPProcedureSubsegment] = []

    def from_lines(self, cifp_lines: list) -> None:
        initial = str(cifp_lines[0])
        sub_code = initial[12:13].strip()
        route_type = initial[19:20].strip()
        self.type = self._translate_route_type(sub_code, route_type)

        sub_chunked = chunk(cifp_lines, 20, 25)
        for sub_chunk in sub_chunked:
            subsegment = CIFPProcedureSubsegment()
            subsegment.from_lines(sub_chunk)
            self.subsegments.append(subsegment)

    def _translate_route_type(self, sub_code: str, route_type: str) -> str | None:
        result = None
        if sub_code == "D":
            if route_type == "0":
                result = "eosid"
            if (
                route_type == "1"
                or route_type == "4"
                or route_type == "F"
                or route_type == "T"
            ):
                result = "runway_transition"
            if route_type == "2" or route_type == "5" or route_type == "M":
                result = "core"
            if (
                route_type == "3"
                or route_type == "6"
                or route_type == "S"
                or route_type == "V"
            ):
                result = "enroute_transition"
        if sub_code == "E":
            if (
                route_type == "1"
                or route_type == "4"
                or route_type == "7"
                or route_type == "F"
            ):
                result = "enroute_transition"
            if (
                route_type == "2"
                or route_type == "5"
                or route_type == "8"
                or route_type == "M"
            ):
                result = "core"
            if (
                route_type == "3"
                or route_type == "6"
                or route_type == "9"
                or route_type == "S"
            ):
                result = "runway_transition"
        if sub_code == "F":
            if route_type == "A":
                result = "transition"
            if route_type == "B":
                result = "LOC/BC"
            if route_type == "D":
                result = "VOR/DME"
            if route_type == "F":
                result = "FMS"
            if route_type == "G":
                result = "IGS"
            if route_type == "H":
                result = "RNP"
            if route_type == "I":
                result = "ILS"
            if route_type == "J":
                result = "GNSS"
            if route_type == "L":
                result = "LOC"
            if route_type == "M":
                result = "MLS"
            if route_type == "N":
                result = "NDB"
            if route_type == "P":
                result = "GPS"
            if route_type == "Q":
                result = "NDB/DME"
            if route_type == "R":
                result = "RNAV"
            if route_type == "S":
                result = "VORTAC"
            if route_type == "T":
                result = "TACAN"
            if route_type == "U":
                result = "SDF"
            if route_type == "V":
                result = "VOR"
            if route_type == "W":
                result = "MLS-A"
            if route_type == "X":
                result = "LDA"
            if route_type == "Y":
                result = "MLS-B/C"
            if route_type == "Z":
                result = "Missed"
        return result

    def create_db_table(db_cursor: Cursor) -> None:
        CIFPProcedureSubsegment.create_db_table(db_cursor)

    def to_db(self, db_cursor: Cursor) -> None:
        for item in self.subsegments:
            item.to_db(db_cursor)

    def to_dict(self) -> dict:
        subsegments = []
        for item in self.subsegments:
            subsegments.append(item.to_dict())

        return {"type": clean_value(self.type), "subsegments": subsegments}

    # No longer used, but kept just in case.
    def _determine_core(self, sub_code: str, route_type: str) -> bool:
        result = False
        if sub_code == "D":
            if (
                route_type == "0"
                or route_type == "2"
                or route_type == "5"
                or route_type == "M"
            ):
                result = True
        if sub_code == "E":
            if (
                route_type == "2"
                or route_type == "5"
                or route_type == "8"
                or route_type == "M"
            ):
                result = True
        if sub_code == "F":
            if route_type != "A" and route_type != "Z":
                result = True
        return result
