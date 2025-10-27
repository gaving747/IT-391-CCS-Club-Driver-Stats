
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


class IAccountRepo(ABC):
    """Repository interface for the Account table.

    Table columns: act_username, act_drivername, act_email (PK), act_password
    """

    @abstractmethod
    def create_account(self, act_username: str, act_drivername: str, act_email: str, act_password: str) -> int:
        """Returns the new account ID"""
        raise NotImplementedError()

    @abstractmethod
    def update_account(self, act_email: str, updates: Dict[str, Any]) -> None:
        """updates is a mapping of column -> new value"""
        raise NotImplementedError()

    @abstractmethod
    def delete_account(self, act_email: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_account_by_email(self, act_email: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    @abstractmethod
    def get_accounts(self) -> List[Dict[str, Any]]:
        raise NotImplementedError()


class IEventChairRepo(ABC):
    """Repository interface for the Event_Chair table.

    Table columns: event_id (PK), chair_name
    """

    @abstractmethod
    def create_event_chair(self, event_id: int, chair_name: str) -> int:
        """Returns the new event chair ID"""
        raise NotImplementedError()

    @abstractmethod
    def update_event_chair(self, event_id: int, chair_name: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_event_chair(self, event_id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_event_chair(self, event_id: int) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    @abstractmethod
    def get_all_event_chairs(self) -> List[Dict[str, Any]]:
        raise NotImplementedError()


class ILocationRepo(ABC):
    """Repository interface for the Location table.

    Table columns: location_id (PK), lat, lon, surface_type, course_map_url
    """

    @abstractmethod
    def create_location(self, lat: float, lon: float, surface_type: Optional[str] = None, course_map_url: Optional[str] = None) -> int:
        """Returns the new location_id"""
        raise NotImplementedError()

    @abstractmethod
    def update_location(self, location_id: int, updates: Dict[str, Any]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_location(self, location_id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_location(self, location_id: int) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    @abstractmethod
    def get_locations(self) -> List[Dict[str, Any]]:
        raise NotImplementedError()


class IEventRepo(ABC):
    """Repository interface for the Event table.

    Table columns: event_id (PK), event_name, event_link, event_notes, location_id
    """

    @abstractmethod
    def create_event(self, event_name: str, event_link: str, event_notes: Optional[str] = None, location_id: Optional[int] = None) -> int:
        raise NotImplementedError()

    @abstractmethod
    def update_event(self, event_id: int, updates: Dict[str, Any]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_event(self, event_id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_event(self, event_id: int) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    @abstractmethod
    def get_events(self) -> List[Dict[str, Any]]:
        raise NotImplementedError()


class IEventSessionRepo(ABC):
    """Repository interface for the Event_Session table.

    Table columns: event_session_id (PK), evt_session_date (Date), event_id
    """

    @abstractmethod
    def create_event_session(self, evt_session_date, event_id: int) -> int:
        raise NotImplementedError()

    @abstractmethod
    def update_event_session(self, event_session_id: int, updates: Dict[str, Any]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_event_session(self, event_session_id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_event_session(self, event_session_id: int) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    @abstractmethod
    def get_event_sessions(self, event_id: Optional[int] = None) -> List[Dict[str, Any]]:
        raise NotImplementedError()


class IWeatherDataRepo(ABC):
    """Repository interface for the Weather_Data table.

    Table columns: weather_id (PK), cloud_cover, humidity, precip, high_temp, low_temp,
    pressure, wind_speed, wind_dir, event_session_id
    """

    @abstractmethod
    def create_weather(self, cloud_cover: int, humidity: int, precip: float, high_temp: float, low_temp: float, pressure: float, wind_speed: float, wind_dir: int, event_session_id: int) -> int:
        raise NotImplementedError()

    @abstractmethod
    def update_weather(self, weather_id: int, updates: Dict[str, Any]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_weather(self, weather_id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_weather(self, weather_id: int) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    @abstractmethod
    def get_weather_for_session(self, event_session_id: int) -> List[Dict[str, Any]]:
        raise NotImplementedError()


class ICarRepo(ABC):
    """Repository interface for the Car table.

    Table columns: car_id (PK), car_driver_name, car_year, car_make, car_model, wheelbase,
    mods, tire_description, weight
    """

    @abstractmethod
    def create_car(self, car_driver_name: str, car_year: int, car_make: str, car_model: str, wheelbase: Optional[float] = None, mods: Optional[str] = None, tire_description: Optional[str] = None, weight: Optional[int] = None) -> int:
        raise NotImplementedError()

    @abstractmethod
    def update_car(self, car_id: int, updates: Dict[str, Any]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_car(self, car_id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_car(self, car_id: int) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    @abstractmethod
    def get_cars(self) -> List[Dict[str, Any]]:
        raise NotImplementedError()


class ISessionRawRepo(ABC):
    """Repository interface for the Session_Raw_Data table.

    Table columns: session_data_id (PK), session_class_abrv, session_car_num, sr_raw_time, car_id, event_session_id
    """

    @abstractmethod
    def create_session_raw(self, session_class_abrv: str, session_car_num: int, sr_raw_time: float, car_id: int, event_session_id: int) -> int:
        raise NotImplementedError()

    @abstractmethod
    def update_session_raw(self, session_data_id: int, updates: Dict[str, Any]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_session_raw(self, session_data_id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_session_raw(self, session_data_id: int) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    @abstractmethod
    def get_session_raw_by_event(self, event_session_id: int) -> List[Dict[str, Any]]:
        raise NotImplementedError()


class ISessionPAXRepo(ABC):
    """Repository interface for the Session_PAX_Data table.

    Table columns: session_data_id (PK), session_class_abrv, session_car_num, sp_raw_time, sp_pax_factor, sp_pax_time, car_id, event_session_id
    """

    @abstractmethod
    def create_session_pax(self, session_class_abrv: str, session_car_num: int, sp_raw_time: float, sp_pax_factor: float, sp_pax_time: float, car_id: int, event_session_id: int) -> int:
        raise NotImplementedError()

    @abstractmethod
    def update_session_pax(self, session_data_id: int, updates: Dict[str, Any]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_session_pax(self, session_data_id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_session_pax(self, session_data_id: int) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    @abstractmethod
    def get_session_pax_by_event(self, event_session_id: int) -> List[Dict[str, Any]]:
        raise NotImplementedError()


class ISessionFinalRepo(ABC):
    """Repository interface for the Session_Final_Data table.

    Table columns: session_data_id (PK), session_class_abrv, session_car_num, sf_has_trophy, sf_car_color, car_id, event_session_id
    """

    @abstractmethod
    def create_session_final(self, session_class_abrv: str, session_car_num: int, sf_has_trophy: bool, sf_car_color: str, car_id: int, event_session_id: int) -> int:
        raise NotImplementedError()

    @abstractmethod
    def update_session_final(self, session_data_id: int, updates: Dict[str, Any]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_session_final(self, session_data_id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_session_final(self, session_data_id: int) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    @abstractmethod
    def get_session_final_by_event(self, event_session_id: int) -> List[Dict[str, Any]]:
        raise NotImplementedError()


class IRunRepo(ABC):
    """Repository interface for the Run table.

    Table columns: run_id (PK), run_time, is_dnf, num_penalties, fsession_id
    """

    @abstractmethod
    def create_run(self, run_time: float, is_dnf: bool, num_penalties: int, fsession_id: int) -> int:
        raise NotImplementedError()

    @abstractmethod
    def update_run(self, run_id: int, updates: Dict[str, Any]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_run(self, run_id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_run(self, run_id: int) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    @abstractmethod
    def get_runs_by_final_session(self, fsession_id: int) -> List[Dict[str, Any]]:
        raise NotImplementedError()







