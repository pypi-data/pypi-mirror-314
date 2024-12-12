from .cifp_functions import chunk
from .cifp_airport import CIFPAirport
from .cifp_heliport import CIFPHeliport
from .cifp_ndb import CIFP_NDB
from .cifp_airway import CIFPAirway
from .cifp_vhf_dme import CIFP_VHF_DME
from .cifp_waypoint import CIFPWaypoint
from .cifp_controlled_airspace import CIFPControlledAirspace
from .cifp_restrictive_airspace import CIFPRestrictiveAirspace

import os
from datetime import datetime, timedelta
from sqlite3 import Cursor


class CIFP:
    CYCLE_LENGTH_DAYS = 28

    def __init__(self, path: str) -> None:
        self._exists = False
        self._file_path = ""
        self._cycle_id = None
        self._effective_from = None
        self._effective_to = None
        self._airport_lines: list[str] = []
        self._airport: list[CIFPAirport] = []
        self._waypoint_lines: list[str] = []
        self._waypoint: list[CIFPWaypoint] = []
        self._heliport_lines: list[str] = []
        self._heliport: list[CIFPHeliport] = []
        self._ndb_lines: list[str] = []
        self._ndb: list[CIFP_NDB] = []
        self._airway_lines: list[str] = []
        self._airway: list[CIFPAirway] = []
        self._vhf_dme_lines: list[str] = []
        self._vhf_dme: list[CIFP_VHF_DME] = []
        self._controlled_lines: list[str] = []
        self._controlled: list[CIFPControlledAirspace] = []
        self._restrictive_lines: list[str] = []
        self._restrictive: list[CIFPRestrictiveAirspace] = []

        self._set_path(path)
        if self._exists:
            self._split_sections()

    def _set_path(self, path: str) -> None:
        self._file_path = path
        if os.path.exists(self._file_path):
            print(f"CIFP Parser :: Found CIFP file at: {path}")
            self._exists = True
        else:
            print(
                f"CIFP Parser :: Unable to find CIFP file at: {path} :: Interpreted as {path}"
            )

    def _split_sections(self) -> None:
        with open(self._file_path) as cifpFile:
            for line in cifpFile:
                header_id = line[0:5]
                if header_id == "HDR04":
                    self._cycle_id = line[80:84]
                    effective_from = line[96:107]
                    effective_from_obj = datetime.strptime(effective_from, "%d %b %Y")
                    self._effective_from = effective_from_obj.strftime("%Y-%m-%d")
                    effective_to_obj = effective_from_obj + timedelta(
                        days=self.CYCLE_LENGTH_DAYS
                    )
                    self._effective_to = effective_to_obj.strftime("%Y-%m-%d")
                section_id = line[4:6]
                if section_id == "D ":
                    self._vhf_dme_lines.append(line)
                if section_id == "DB" or section_id == "PN":
                    self._ndb_lines.append(line)
                if section_id == "EA":
                    self._waypoint_lines.append(line)
                if section_id == "ER":
                    self._airway_lines.append(line)
                if section_id == "H ":
                    self._heliport_lines.append(line)
                if section_id == "P ":
                    subsection_id = line[12:13]
                    if subsection_id == "C":
                        self._waypoint_lines.append(line)
                    self._airport_lines.append(line)
                if section_id == "UC":
                    self._controlled_lines.append(line)
                if section_id == "UR":
                    self._restrictive_lines.append(line)

    def _airport_to_object(self) -> None:
        airport_chunked = chunk(self._airport_lines, 6, 10)
        del self._airport_lines
        for airport_chunk in airport_chunked:
            airport = CIFPAirport()
            airport.from_lines(airport_chunk)
            self._airport.append(airport)

    def _heliport_to_object(self) -> None:
        heliport_chunked = chunk(self._heliport_lines, 6, 10)
        del self._heliport_lines
        for heliport_chunk in heliport_chunked:
            heliport = CIFPHeliport()
            heliport.from_lines(heliport_chunk)
            self._heliport.append(heliport)

    def _ndb_to_object(self) -> None:
        ndb_chunked = chunk(self._ndb_lines, 6, 22)
        del self._ndb_lines
        for ndb_chunk in ndb_chunked:
            ndb = CIFP_NDB()
            ndb.from_lines(ndb_chunk)
            self._ndb.append(ndb)

    def _airway_to_object(self) -> None:
        airway_chunked = chunk(self._airway_lines, 6, 19)
        del self._airway_lines
        for airway_chunk in airway_chunked:
            airway = CIFPAirway()
            airway.from_lines(airway_chunk)
            self._airway.append(airway)

    def _vhf_dme_to_object(self) -> None:
        vhf_dme_chunked = chunk(self._vhf_dme_lines, 6, 22)
        del self._vhf_dme_lines
        for vhf_dme_chunk in vhf_dme_chunked:
            vhf_dme = CIFP_VHF_DME()
            vhf_dme.from_lines(vhf_dme_chunk)
            self._vhf_dme.append(vhf_dme)

    def _waypoint_to_object(self) -> None:
        waypoint_chunked = chunk(self._waypoint_lines, 6, 22)
        del self._waypoint_lines
        for waypoint_chunk in waypoint_chunked:
            waypoint = CIFPWaypoint()
            waypoint.from_lines(waypoint_chunk)
            self._waypoint.append(waypoint)

    def _controlled_to_object(self) -> None:
        controlled_chunked = chunk(self._controlled_lines, 9, 13)
        del self._controlled_lines
        for controlled_chunk in controlled_chunked:
            controlled = CIFPControlledAirspace()
            controlled.from_lines(controlled_chunk)
            self._controlled.append(controlled)

    def _restrictive_to_object(self) -> None:
        restrictive_chunked = chunk(self._restrictive_lines, 6, 19)
        del self._restrictive_lines
        for restrictive_chunk in restrictive_chunked:
            restrictive = CIFPRestrictiveAirspace()
            restrictive.from_lines(restrictive_chunk)
            self._restrictive.append(restrictive)

    def _create_validity_table(self, db_cursor: Cursor) -> None:
        table_name = "validity"
        drop_statement = f"DROP TABLE IF EXISTS `{table_name}`;"
        db_cursor.execute(drop_statement)

        create_statement = f"""
            CREATE TABLE IF NOT EXISTS `{table_name}` (
                `cycle_id` TEXT,
                `valid_from` TEXT,
                `valid_to` TEXT
            );
        """
        db_cursor.execute(create_statement)

    def _insert_validity(self, db_cursor: Cursor) -> None:
        table_name = "validity"
        insert_statement = f"""
            INSERT INTO `{table_name}` (
                `cycle_id`,
                `valid_from`,
                `valid_to`
            ) VALUES (
                ?,?,?
            );
        """
        db_cursor.execute(
            insert_statement, (self._cycle_id, self._effective_from, self._effective_to)
        )

    def initialize_database(self, db_cursor: Cursor) -> None:
        self._create_validity_table(db_cursor)
        CIFPAirport.create_db_table(db_cursor)
        CIFPWaypoint.create_db_table(db_cursor)
        CIFPHeliport.create_db_table(db_cursor)
        CIFP_NDB.create_db_table(db_cursor)
        CIFPAirway.create_db_table(db_cursor)
        CIFP_VHF_DME.create_db_table(db_cursor)
        CIFPControlledAirspace.create_db_table(db_cursor)
        CIFPRestrictiveAirspace.create_db_table(db_cursor)

    def to_db(self, db_cursor: Cursor) -> None:
        self._insert_validity(db_cursor)
        for airport in self._airport:
            airport.to_db(db_cursor)

        for waypoint in self._waypoint:
            waypoint.to_db(db_cursor)

        for heliport in self._heliport:
            heliport.to_db(db_cursor)

        for ndb in self._ndb:
            ndb.to_db(db_cursor)

        for airway in self._airway:
            airway.to_db(db_cursor)

        for vhf_dme in self._vhf_dme:
            vhf_dme.to_db(db_cursor)

        for controlled in self._controlled:
            controlled.to_db(db_cursor)

        for restrictive in self._restrictive:
            restrictive.to_db(db_cursor)

    def parse_airports(self) -> None:
        if self._exists:
            print("Processing Airports")
            self._airport_to_object()

    def parse_heliports(self) -> None:
        if self._exists:
            print("Processing Heliports")
            self._heliport_to_object()

    def parse_ndbs(self) -> None:
        if self._exists:
            print("Processing NDBs")
            self._ndb_to_object()

    def parse_airways(self) -> None:
        if self._exists:
            print("Processing Airways")
            self._airway_to_object()

    def parse_vhf_dmes(self) -> None:
        if self._exists:
            print("Processing VHF/DMEs")
            self._vhf_dme_to_object()

    def parse_waypoints(self) -> None:
        if self._exists:
            print("Processing Waypoints")
            self._waypoint_to_object()

    def parse_controlled(self) -> None:
        if self._exists:
            print("Processing Controlled Airspace")
            self._controlled_to_object()

    def parse_restrictive(self) -> None:
        if self._exists:
            print("Processing Restrictive Airspace")
            self._restrictive_to_object()

    def parse(self) -> None:
        self.parse_airports()
        self.parse_heliports()
        self.parse_ndbs()
        self.parse_airways()
        self.parse_vhf_dmes()
        self.parse_waypoints()
        self.parse_controlled()
        self.parse_restrictive()

    def get_airports(self) -> list:
        print(f"Fetching all airports.")
        return self._airport

    def find_airport(self, airport_id: str) -> CIFPAirport | None:
        print(f'Finding airport with ID "{airport_id}"')
        result = None
        for airport in self._airport:
            if airport.airport_id == airport_id:
                result = airport
        return result

    def get_heliports(self) -> list:
        print(f"Fetching all heliports.")
        return self._heliport

    def find_heliport(self, heliport_id: str) -> CIFPHeliport | None:
        print(f'Finding heliport with ID "{heliport_id}"')
        result = None
        for heliport in self._heliport:
            print(heliport.heliport_id)
            if heliport.heliport_id == heliport_id:
                result = heliport
        return result

    def get_airways(self) -> list:
        print(f"Fetching all airways.")
        return self._airway

    def find_airway(self, airway_id: str) -> CIFPAirway | None:
        print(f'Finding airway with ID "{airway_id}"')
        result = None
        for airway in self._airway:
            if airway.airway_id == airway_id:
                result = airway
        return result

    def get_ndbs(self) -> list:
        print(f"Fetching all NDBs.")
        return self._ndb

    def find_ndb(self, ndb_id: str) -> CIFP_NDB | None:
        print(f'Finding NDB with ID "{ndb_id}"')
        result = None
        for ndb in self._ndb:
            if ndb.ndb_id == ndb_id:
                result = ndb
        return result

    def get_vhf_dmes(self) -> list:
        print(f"Fetching all VHF/DMEs.")
        return self._vhf_dme

    def find_vhf_dme(self, vhf_dme_id: str) -> CIFP_VHF_DME | None:
        print(f'Finding VHF/DME navaid with ID "{vhf_dme_id}"')
        result = None
        for vhf_dme in self._vhf_dme:
            if vhf_dme.vhf_id == vhf_dme_id:
                result = vhf_dme
        return result

    def get_waypoints(self) -> list:
        print(f"Fetching all waypoints.")
        return self._waypoint

    def find_waypoint(self, waypoint_id: str) -> CIFPWaypoint | None:
        print(f'Finding waypoint with ID "{waypoint_id}"')
        result = None
        for waypoint in self._waypoint:
            if waypoint.waypoint_id == waypoint_id:
                result = waypoint
        return result

    def get_controlled(self) -> list:
        print(f"Fetching all controlled airspace.")
        return self._controlled

    def find_controlled(self, center_id: str) -> CIFPControlledAirspace | None:
        print(f'Finding controlled airspace with center point "{center_id}"')
        result = None
        for controlled in self._controlled:
            if controlled.center_id == center_id:
                result = controlled
        return result

    def get_restrictive(self) -> list:
        print(f"Fetching all restrictive airspace.")
        return self._restrictive

    def find_restrictive_match(self, restrictive_name: str) -> list:
        print(
            f'Finding all restrictive airspace with names containing "{restrictive_name}".'
        )
        result = []
        for restrictive in self._restrictive:
            if (
                restrictive.restrictive_name
                and restrictive_name in restrictive.restrictive_name
            ):
                result.append(restrictive.restrictive_name)
        return result

    def find_restrictive(self, restrictive_name: str) -> CIFPRestrictiveAirspace | None:
        print(f'Finding restrictive airspace with name "{restrictive_name}".')
        result = None
        for restrictive in self._restrictive:
            if restrictive.restrictive_name == restrictive_name:
                result = restrictive
        return result
