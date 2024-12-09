"""
This code defines a class which gives the equivalent Cyprian date for each day
in a given Gregorian year.
"""

# Standard imports.
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from sqlite3 import Connection

# Local imports.
from . import constants
from .cyprian_date import (
    CyprianDate,
    get_cyprian_year_beginning_with_greg_year,
    get_greg_year_ending_with_cyprian_year,
    get_vernal_equinox,
    get_cyprian_new_year
)

# Local constants.
DATETIME_EPHEMERALS = ("vernal_equinox", "cyprian_new_year")

##############
# MAIN CLASS #
##############

@dataclass
class Concordance:
    """ The class in question. """
    whole_greg_year: int|None = None
    whole_cyprian_year: int|None = None
    path_to_cache_db: str = constants.DEFAULT_PATH_TO_CACHE_DB
    last_vernal_equinox: datetime|None = field(init=False, default=None)
    this_vernal_equinox: datetime|None = field(init=False, default=None)
    last_cyprian_new_year: datetime|None = field(init=False, default=None)
    this_cyprian_new_year: datetime|None = field(init=False, default=None)
    db_connection: Connection|None = field(init=False, default=None)

    def __post_init__(self):
        if self.whole_greg_year is None:
            if self.whole_cyprian_year is None:
                self.whole_greg_year = datetime.now(timezone.utc).year
                self.auto_set_whole_cyprian_year()
            else:
                self.auto_set_whole_greg_year()
        else:
            self.auto_set_whole_cyprian_year()

    def auto_set_whole_cyprian_year(self):
        """ Given that the Gregorian year has already been set, set the Cyprian
        year automatically. """
        self.whole_cyprian_year = \
            get_cyprian_year_beginning_with_greg_year(self.whole_greg_year)

    def auto_set_whole_greg_year(self):
        """ Given that the Cyprian year has already been set, set the Gregorian
        year automatically. """
        self.whole_greg_year = \
            get_greg_year_ending_with_cyprian_year(self.whole_cyprian_year)

    def write(self, new_greg_year: int = None, new_cyprian_year: int = None):
        """ Create a concordance, and write it to the database. """
        if new_greg_year is not None:
            self.whole_greg_year = new_greg_year
            self.auto_set_whole_cyprian_year()
        if new_cyprian_year is not None:
            self.whole_cyprian_year = new_cyprian_year
            self.auto_set_whole_greg_year()
        self.establish_connection()
        self.create_database()
        self.set_equinoctes()
        self.set_cyprian_new_years()
        self.walk_through()
        self.write_ephemerals()
        self.commit_and_close()

    def establish_connection(self):
        """ Create the Connection object. """
        self.db_connection = sqlite3.connect(self.path_to_cache_db)

    def commit_and_close(self):
        """ Commit all transactions and close the connection. """
        self.db_connection.commit()
        self.db_connection.close()

    def create_database(self):
        """ Run the create-drop script. """
        path_to_script = str(Path(__file__).parent/"sql"/"create_drop.sql")
        with open(path_to_script, "r") as script_file:
            script = script_file.read()
        cursor = self.db_connection.cursor()
        cursor.executescript(script)

    def set_equinoctes(self):
        """ Ronseal. """
        self.last_vernal_equinox = get_vernal_equinox(self.whole_greg_year-1)
        self.this_vernal_equinox = get_vernal_equinox(self.whole_greg_year)

    def set_cyprian_new_years(self):
        """ Ronseal. """
        self.last_cyprian_new_year = \
            get_cyprian_new_year(self.whole_greg_year-1)
        self.this_cyprian_new_year = get_cyprian_new_year(self.whole_greg_year)

    def walk_through(self):
        """
        Go through each day of the Gregorian year, assigning an equivalent
        Cyprian date to each.
        """
        greg_date = self.last_cyprian_new_year
        cyprian_date = CyprianDate(self.whole_cyprian_year-1, 1, 1)
        while cyprian_date.year <= self.whole_cyprian_year:
            self.write_dates(greg_date, cyprian_date)
            cyprian_date.advance_one_day(greg_date)
            greg_date += timedelta(days=1)

    def write_dates(self, greg_date: datetime, cyprian_date: CyprianDate):
        """ Write the corresponding dates to the database. """
        cursor = self.db_connection.cursor()
        query = (
            "INSERT INTO Equivalence "+
            "(greg_year, greg_month, greg_day, "+
            "cyprian_year, cyprian_month, cyprian_day) "+
            "VALUES (?, ?, ?, ?, ?, ?);"
        )
        cursor.execute(
            query,
            (
                greg_date.year, greg_date.month, greg_date.day,
                cyprian_date.year, cyprian_date.month, cyprian_date.day,
            )
        )

    def write_ephemeral(self, key: str, val: int|str|None):
        """ Write a given ephemeral data point to the database. """
        cursor = self.db_connection.cursor()
        query = "INSERT INTO Ephemeral (key, val) VALUES (?, ?);"
        cursor.execute(query, (key, val))

    def write_ephemerals(self):
        """ Write all the ephemerals to the database. """
        ephemerals = (
            ("whole_greg_year", self.whole_greg_year),
            ("whole_cyprian_year", self.whole_cyprian_year),
            ("vernal_equinox", self.this_vernal_equinox.isoformat()),
            ("cyprian_new_year", self.this_cyprian_new_year.isoformat())
        )
        for pair in ephemerals:
            self.write_ephemeral(*pair)

    def convert_greg(
        self,
        greg: datetime = None,
        force_write_first: bool = False
    ) -> CyprianDate:
        """ Convert a given Gregorian date into its Cyprian equivalent. """
        if greg is None:
            greg = datetime.now(timezone.utc)
        if force_write_first or self.should_write_first(greg=greg):
            self.write(new_greg_year=greg.year)
        self.establish_connection()
        return self.read_equivalent_cyprian(greg)

    def should_write_first(
        self,
        greg: datetime = None,
        cyprian: CyprianDate = None
    ) -> bool:
        """ Decide whether we need to (re)write the cache first. """
        try:
            self.establish_connection()
            cache_greg_year = self.get_ephemeral("whole_greg_year")
            cache_cyprian_year = self.get_ephemeral("whole_cyprian_year")
        except (sqlite3.OperationalError, ConcordanceError):
            return True
        if greg and greg.year == cache_greg_year:
            return False
        if cyprian and cyprian.year == cache_cyprian_year:
            return False
        return True

    def get_ephemeral(self, key: str) -> int|str|datetime|None:
        """ Ronseal. """
        cursor = self.db_connection.cursor()
        query = "SELECT val FROM Ephemeral WHERE key = ?;"
        cursor.execute(query, (key,))
        extract = cursor.fetchall()
        if len(extract) != 1:
            raise ConcordanceError(
                f"Expected to fetch 1 item, but fetched {len(extract)}"
            )
        result = extract[0][0]
        if key in DATETIME_EPHEMERALS:
            result = datetime.fromisoformat(result)
        else:
            result = int(result)
        return result

    def read_equivalent_cyprian(self, greg: datetime) -> CyprianDate:
        """ Read the equivalent from the cache. """
        cursor = self.db_connection.cursor()
        query = (
            "SELECT cyprian_year, cyprian_month, cyprian_day "+
            "FROM Equivalence "+
            "WHERE greg_year = ? AND greg_month = ? AND greg_day = ?;"
        )
        cursor.execute(query, (greg.year, greg.month, greg.day))
        extract = cursor.fetchall()
        if len(extract) != 1:
            raise ConcordanceError(
                f"Expected to fetch 1 item, but fetched {len(extract)}"
            )
        constructor_args = extract[0]
        result = CyprianDate(*constructor_args)
        return result

    def convert_cyprian(
        self,
        cyprian: CyprianDate,
        force_write_first: bool = False
    ) -> datetime:
        """ Convert a given Cyprian date into its Gregorian equivalent. """
        if force_write_first or self.should_write_first(cyprian=cyprian):
            self.write(new_cyprian_year=cyprian.year)
        self.establish_connection()
        return self.read_equivalent_greg(cyprian)

    def read_equivalent_greg(self, cyprian: CyprianDate) -> datetime:
        """ Read the equivalent from the cache. """
        cursor = self.db_connection.cursor()
        query = (
            "SELECT greg_year, greg_month, greg_day "+
            "FROM Equivalence "+
            "WHERE cyprian_year = ? AND cyprian_month = ? AND cyprian_day = ?;"
        )
        cursor.execute(query, (cyprian.year, cyprian.month, cyprian.day))
        extract = cursor.fetchall()
        if len(extract) != 1:
            raise ConcordanceError(
                f"Expected to fetch 1 item, but fetched {len(extract)}"
            )
        constructor_args = extract[0]
        result = datetime(*constructor_args, tzinfo=timezone.utc)
        return result

##################
# HELPER CLASSES #
##################

class ConcordanceError(Exception):
    """ A custom exception. """
