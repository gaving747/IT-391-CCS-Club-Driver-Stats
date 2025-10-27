"""
Simple MySQL-backed repository implementations for the repository interfaces defined in
`classes/Repository.py`.

This file provides a minimal, straightforward implementation using `mysql.connector`.
It expects the caller to provide a `db_config` dictionary with keys suitable for
`mysql.connector.connect(**db_config)` (for example: host, user, password, database).

This is intentionally lightweight: methods return primitive types (int for inserted id,
None for update/delete) or dict/list-of-dict for selects. It uses parameterized queries
to avoid SQL injection.

Note: Install mysql-connector-python (or update `requirements.txt`) if not already present.
"""
from __future__ import annotations

import mysql.connector
from mysql.connector import Error
from typing import Dict, Any, List, Optional, cast
from datetime import date

from classes.Repository import (
    IAccountRepo,
    IEventChairRepo,
    ILocationRepo,
    IEventRepo,
    IEventSessionRepo,
    IWeatherDataRepo,
    ICarRepo,
    ISessionRawRepo,
    ISessionPAXRepo,
    ISessionFinalRepo,
    IRunRepo,
)


class MySQLConnection:
    def __init__(self, db_config: Dict[str, Any]):
        self._db_config = db_config

    def get_conn(self):
        return mysql.connector.connect(**self._db_config)


class MySQLAccountRepo(IAccountRepo):
    def __init__(self, conn: MySQLConnection):
        self._conn = conn

    def create_account(self, act_username: str, act_drivername: str, act_email: str, act_password: str) -> int:
        q = """INSERT INTO Account (act_username, act_drivername, act_email, act_password)
               VALUES (%s, %s, %s, %s)"""
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (act_username, act_drivername, act_email, act_password))
            c.commit()
            return int(cur.lastrowid or 0)

    def update_account(self, act_email: str, updates: Dict[str, Any]) -> None:
        if not updates:
            return
        cols = ", ".join(f"{k}=%s" for k in updates.keys())
        q = f"UPDATE Account SET {cols} WHERE act_email = %s"
        params = list(updates.values()) + [act_email]
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, params)
            c.commit()

    def delete_account(self, act_email: str) -> None:
        q = "DELETE FROM Account WHERE act_email = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (act_email,))
            c.commit()

    def get_account_by_email(self, act_email: str) -> Optional[Dict[str, Any]]:
        q = "SELECT act_username, act_drivername, act_email, act_password FROM Account WHERE act_email = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q, (act_email,))
            return cast(Optional[Dict[str, Any]], cur.fetchone())

    def get_accounts(self) -> List[Dict[str, Any]]:
        q = "SELECT act_username, act_drivername, act_email, act_password FROM Account"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q)
            return cast(List[Dict[str, Any]], cur.fetchall())


class MySQLEventChairRepo(IEventChairRepo):
    def __init__(self, conn: MySQLConnection):
        self._conn = conn

    def create_event_chair(self, event_id: int, chair_name: str) -> int:
        q = "INSERT INTO Event_Chair (event_id, chair_name) VALUES (%s, %s)"
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (event_id, chair_name))
            c.commit()
            return int(cur.lastrowid or 0)

    def update_event_chair(self, event_id: int, chair_name: str) -> None:
        q = "UPDATE Event_Chair SET chair_name = %s WHERE event_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (chair_name, event_id))
            c.commit()

    def delete_event_chair(self, event_id: int) -> None:
        q = "DELETE FROM Event_Chair WHERE event_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (event_id,))
            c.commit()

    def get_event_chair(self, event_id: int) -> Optional[Dict[str, Any]]:
        q = "SELECT event_id, chair_name FROM Event_Chair WHERE event_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q, (event_id,))
            return cast(Optional[Dict[str, Any]], cur.fetchone())

    def get_all_event_chairs(self) -> List[Dict[str, Any]]:
        q = "SELECT event_id, chair_name FROM Event_Chair"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q)
            return cast(List[Dict[str, Any]], cur.fetchall())


class MySQLLocationRepo(ILocationRepo):
    def __init__(self, conn: MySQLConnection):
        self._conn = conn

    def create_location(self, lat: float, lon: float, surface_type: Optional[str] = None, course_map_url: Optional[str] = None) -> int:
        q = "INSERT INTO Location (lat, lon, surface_type, course_map_url) VALUES (%s, %s, %s, %s)"
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (lat, lon, surface_type, course_map_url))
            c.commit()
            return int(cur.lastrowid or 0)

    def update_location(self, location_id: int, updates: Dict[str, Any]) -> None:
        if not updates:
            return
        cols = ", ".join(f"{k}=%s" for k in updates.keys())
        q = f"UPDATE Location SET {cols} WHERE location_id = %s"
        params = list(updates.values()) + [location_id]
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, params)
            c.commit()

    def delete_location(self, location_id: int) -> None:
        q = "DELETE FROM Location WHERE location_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (location_id,))
            c.commit()

    def get_location(self, location_id: int) -> Optional[Dict[str, Any]]:
        q = "SELECT location_id, lat, lon, surface_type, course_map_url FROM Location WHERE location_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q, (location_id,))
            return cast(Optional[Dict[str, Any]], cur.fetchone())

    def get_locations(self) -> List[Dict[str, Any]]:
        q = "SELECT location_id, lat, lon, surface_type, course_map_url FROM Location"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q)
            return cast(List[Dict[str, Any]], cur.fetchall())


class MySQLEventRepo(IEventRepo):
    def __init__(self, conn: MySQLConnection):
        self._conn = conn

    def create_event(self, event_name: str, event_link: str, event_notes: Optional[str] = None, location_id: Optional[int] = None) -> int:
        q = "INSERT INTO Event (event_name, event_link, event_notes, location_id) VALUES (%s, %s, %s, %s)"
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (event_name, event_link, event_notes, location_id))
            c.commit()
            return int(cur.lastrowid or 0)

    def update_event(self, event_id: int, updates: Dict[str, Any]) -> None:
        if not updates:
            return
        cols = ", ".join(f"{k}=%s" for k in updates.keys())
        q = f"UPDATE Event SET {cols} WHERE event_id = %s"
        params = list(updates.values()) + [event_id]
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, params)
            c.commit()

    def delete_event(self, event_id: int) -> None:
        q = "DELETE FROM Event WHERE event_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (event_id,))
            c.commit()

    def get_event(self, event_id: int) -> Optional[Dict[str, Any]]:
        q = "SELECT event_id, event_name, event_link, event_notes, location_id FROM Event WHERE event_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q, (event_id,))
            return cast(Optional[Dict[str, Any]], cur.fetchone())

    def get_events(self) -> List[Dict[str, Any]]:
        q = "SELECT event_id, event_name, event_link, event_notes, location_id FROM Event"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q)
            return cast(List[Dict[str, Any]], cur.fetchall())


class MySQLEventSessionRepo(IEventSessionRepo):
    def __init__(self, conn: MySQLConnection):
        self._conn = conn

    def create_event_session(self, evt_session_date: date, event_id: int) -> int:
        q = "INSERT INTO Event_Session (evt_session_date, event_id) VALUES (%s, %s)"
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (evt_session_date, event_id))
            c.commit()
            return int(cur.lastrowid or 0)

    def update_event_session(self, event_session_id: int, updates: Dict[str, Any]) -> None:
        if not updates:
            return
        cols = ", ".join(f"{k}=%s" for k in updates.keys())
        q = f"UPDATE Event_Session SET {cols} WHERE event_session_id = %s"
        params = list(updates.values()) + [event_session_id]
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, params)
            c.commit()

    def delete_event_session(self, event_session_id: int) -> None:
        q = "DELETE FROM Event_Session WHERE event_session_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (event_session_id,))
            c.commit()

    def get_event_session(self, event_session_id: int) -> Optional[Dict[str, Any]]:
        q = "SELECT event_session_id, evt_session_date, event_id FROM Event_Session WHERE event_session_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q, (event_session_id,))
            return cast(Optional[Dict[str, Any]], cur.fetchone())

    def get_event_sessions(self, event_id: Optional[int] = None) -> List[Dict[str, Any]]:
        if event_id is None:
            q = "SELECT event_session_id, evt_session_date, event_id FROM Event_Session"
            params = ()
        else:
            q = "SELECT event_session_id, evt_session_date, event_id FROM Event_Session WHERE event_id = %s"
            params = (event_id,)
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q, params)
            return cast(List[Dict[str, Any]], cur.fetchall())


class MySQLWeatherDataRepo(IWeatherDataRepo):
    def __init__(self, conn: MySQLConnection):
        self._conn = conn

    def create_weather(self, cloud_cover: int, humidity: int, precip: float, high_temp: float, low_temp: float, pressure: float, wind_speed: float, wind_dir: int, event_session_id: int) -> int:
        q = ("INSERT INTO Weather_Data (cloud_cover, humidity, precip, high_temp, low_temp, pressure, wind_speed, wind_dir, event_session_id)"
             " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (cloud_cover, humidity, precip, high_temp, low_temp, pressure, wind_speed, wind_dir, event_session_id))
            c.commit()
            return int(cur.lastrowid or 0)

    def update_weather(self, weather_id: int, updates: Dict[str, Any]) -> None:
        if not updates:
            return
        cols = ", ".join(f"{k}=%s" for k in updates.keys())
        q = f"UPDATE Weather_Data SET {cols} WHERE weather_id = %s"
        params = list(updates.values()) + [weather_id]
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, params)
            c.commit()

    def delete_weather(self, weather_id: int) -> None:
        q = "DELETE FROM Weather_Data WHERE weather_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (weather_id,))
            c.commit()

    def get_weather(self, weather_id: int) -> Optional[Dict[str, Any]]:
        q = "SELECT * FROM Weather_Data WHERE weather_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q, (weather_id,))
            return cast(Optional[Dict[str, Any]], cur.fetchone())

    def get_weather_for_session(self, event_session_id: int) -> List[Dict[str, Any]]:
        q = "SELECT * FROM Weather_Data WHERE event_session_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q, (event_session_id,))
            return cast(List[Dict[str, Any]], cur.fetchall())


class MySQLCarRepo(ICarRepo):
    def __init__(self, conn: MySQLConnection):
        self._conn = conn

    def create_car(self, car_driver_name: str, car_year: int, car_make: str, car_model: str, wheelbase: Optional[float] = None, mods: Optional[str] = None, tire_description: Optional[str] = None, weight: Optional[int] = None) -> int:
        q = ("INSERT INTO Car (car_driver_name, car_year, car_make, car_model, wheelbase, mods, tire_description, weight)"
             " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (car_driver_name, car_year, car_make, car_model, wheelbase, mods, tire_description, weight))
            c.commit()
            return int(cur.lastrowid or 0)

    def update_car(self, car_id: int, updates: Dict[str, Any]) -> None:
        if not updates:
            return
        cols = ", ".join(f"{k}=%s" for k in updates.keys())
        q = f"UPDATE Car SET {cols} WHERE car_id = %s"
        params = list(updates.values()) + [car_id]
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, params)
            c.commit()

    def delete_car(self, car_id: int) -> None:
        q = "DELETE FROM Car WHERE car_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (car_id,))
            c.commit()

    def get_car(self, car_id: int) -> Optional[Dict[str, Any]]:
        q = "SELECT * FROM Car WHERE car_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q, (car_id,))
            return cast(Optional[Dict[str, Any]], cur.fetchone())

    def get_cars(self) -> List[Dict[str, Any]]:
        q = "SELECT * FROM Car"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q)
            return cast(List[Dict[str, Any]], cur.fetchall())


class MySQLSessionRawRepo(ISessionRawRepo):
    def __init__(self, conn: MySQLConnection):
        self._conn = conn

    def create_session_raw(self, session_class_abrv: str, session_car_num: int, sr_raw_time: float, car_id: int, event_session_id: int) -> int:
        q = ("INSERT INTO Session_Raw_Data (session_class_abrv, session_car_num, sr_raw_time, car_id, event_session_id)"
             " VALUES (%s, %s, %s, %s, %s)")
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (session_class_abrv, session_car_num, sr_raw_time, car_id, event_session_id))
            c.commit()
            return int(cur.lastrowid or 0)

    def update_session_raw(self, session_data_id: int, updates: Dict[str, Any]) -> None:
        if not updates:
            return
        cols = ", ".join(f"{k}=%s" for k in updates.keys())
        q = f"UPDATE Session_Raw_Data SET {cols} WHERE session_data_id = %s"
        params = list(updates.values()) + [session_data_id]
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, params)
            c.commit()

    def delete_session_raw(self, session_data_id: int) -> None:
        q = "DELETE FROM Session_Raw_Data WHERE session_data_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (session_data_id,))
            c.commit()

    def get_session_raw(self, session_data_id: int) -> Optional[Dict[str, Any]]:
        q = "SELECT * FROM Session_Raw_Data WHERE session_data_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q, (session_data_id,))
            return cast(Optional[Dict[str, Any]], cur.fetchone())

    def get_session_raw_by_event(self, event_session_id: int) -> List[Dict[str, Any]]:
        q = "SELECT * FROM Session_Raw_Data WHERE event_session_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q, (event_session_id,))
            return cast(List[Dict[str, Any]], cur.fetchall())


class MySQLSessionPAXRepo(ISessionPAXRepo):
    def __init__(self, conn: MySQLConnection):
        self._conn = conn

    def create_session_pax(self, session_class_abrv: str, session_car_num: int, sp_raw_time: float, sp_pax_factor: float, sp_pax_time: float, car_id: int, event_session_id: int) -> int:
        q = ("INSERT INTO Session_PAX_Data (session_class_abrv, session_car_num, sp_raw_time, sp_pax_factor, sp_pax_time, car_id, event_session_id)"
             " VALUES (%s, %s, %s, %s, %s, %s, %s)")
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (session_class_abrv, session_car_num, sp_raw_time, sp_pax_factor, sp_pax_time, car_id, event_session_id))
            c.commit()
            return int(cur.lastrowid or 0)

    def update_session_pax(self, session_data_id: int, updates: Dict[str, Any]) -> None:
        if not updates:
            return
        cols = ", ".join(f"{k}=%s" for k in updates.keys())
        q = f"UPDATE Session_PAX_Data SET {cols} WHERE session_data_id = %s"
        params = list(updates.values()) + [session_data_id]
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, params)
            c.commit()

    def delete_session_pax(self, session_data_id: int) -> None:
        q = "DELETE FROM Session_PAX_Data WHERE session_data_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (session_data_id,))
            c.commit()

    def get_session_pax(self, session_data_id: int) -> Optional[Dict[str, Any]]:
        q = "SELECT * FROM Session_PAX_Data WHERE session_data_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q, (session_data_id,))
            return cast(Optional[Dict[str, Any]], cur.fetchone())

    def get_session_pax_by_event(self, event_session_id: int) -> List[Dict[str, Any]]:
        q = "SELECT * FROM Session_PAX_Data WHERE event_session_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q, (event_session_id,))
            return cast(List[Dict[str, Any]], cur.fetchall())


class MySQLSessionFinalRepo(ISessionFinalRepo):
    def __init__(self, conn: MySQLConnection):
        self._conn = conn

    def create_session_final(self, session_class_abrv: str, session_car_num: int, sf_has_trophy: bool, sf_car_color: str, car_id: int, event_session_id: int) -> int:
        q = ("INSERT INTO Session_Final_Data (session_class_abrv, session_car_num, sf_has_trophy, sf_car_color, car_id, event_session_id)"
             " VALUES (%s, %s, %s, %s, %s, %s)")
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (session_class_abrv, session_car_num, sf_has_trophy, sf_car_color, car_id, event_session_id))
            c.commit()
            return int(cur.lastrowid or 0)

    def update_session_final(self, session_data_id: int, updates: Dict[str, Any]) -> None:
        if not updates:
            return
        cols = ", ".join(f"{k}=%s" for k in updates.keys())
        q = f"UPDATE Session_Final_Data SET {cols} WHERE session_data_id = %s"
        params = list(updates.values()) + [session_data_id]
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, params)
            c.commit()

    def delete_session_final(self, session_data_id: int) -> None:
        q = "DELETE FROM Session_Final_Data WHERE session_data_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (session_data_id,))
            c.commit()

    def get_session_final(self, session_data_id: int) -> Optional[Dict[str, Any]]:
        q = "SELECT * FROM Session_Final_Data WHERE session_data_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q, (session_data_id,))
            return cast(Optional[Dict[str, Any]], cur.fetchone())

    def get_session_final_by_event(self, event_session_id: int) -> List[Dict[str, Any]]:
        q = "SELECT * FROM Session_Final_Data WHERE event_session_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q, (event_session_id,))
            return cast(List[Dict[str, Any]], cur.fetchall())


class MySQLRunRepo(IRunRepo):
    def __init__(self, conn: MySQLConnection):
        self._conn = conn

    def create_run(self, run_time: float, is_dnf: bool, num_penalties: int, fsession_id: int) -> int:
        q = "INSERT INTO Run (run_time, is_dnf, num_penalties, fsession_id) VALUES (%s, %s, %s, %s)"
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (run_time, is_dnf, num_penalties, fsession_id))
            c.commit()
            return int(cur.lastrowid or 0)

    def update_run(self, run_id: int, updates: Dict[str, Any]) -> None:
        if not updates:
            return
        cols = ", ".join(f"{k}=%s" for k in updates.keys())
        q = f"UPDATE Run SET {cols} WHERE run_id = %s"
        params = list(updates.values()) + [run_id]
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, params)
            c.commit()

    def delete_run(self, run_id: int) -> None:
        q = "DELETE FROM Run WHERE run_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor()
            cur.execute(q, (run_id,))
            c.commit()

    def get_run(self, run_id: int) -> Optional[Dict[str, Any]]:
        q = "SELECT * FROM Run WHERE run_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q, (run_id,))
            return cast(Optional[Dict[str, Any]], cur.fetchone())

    def get_runs_by_final_session(self, fsession_id: int) -> List[Dict[str, Any]]:
        q = "SELECT * FROM Run WHERE fsession_id = %s"
        with self._conn.get_conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(q, (fsession_id,))
            return cast(List[Dict[str, Any]], cur.fetchall())

