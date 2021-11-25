from abc import abstractmethod, ABC
from typing import Optional


class AbstractID2NameDB(ABC):
    """ Crude database wrapper ADT, allowing us to easily swap out different DB implementations.
    The purpose is to define the key database operations for storing/retrieving information about project IDs,
    and how they relate to slugs (the project name that shows up in CurseForge URL). """

    @abstractmethod
    def __init__(self, fname: str):
        """ Load the database if possible.
        Must be loaded first thing so that we can check against it when queries are made. """
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        """ Save database in memory to disk. """
        raise NotImplementedError

    @abstractmethod
    def __del__(self):
        """ Save changes if structure is about to be deleted. """
        raise NotImplementedError

    @abstractmethod
    def query_project_id(self, name: str) -> Optional[int]:  # Optional = Union[ur_type, None] ;)
        """ Query project ID from id2name table. """
        raise NotImplementedError

    @abstractmethod
    def query_project_name(self, id_num) -> Optional[str]:
        """ Query project name from id2name table. """
        raise NotImplementedError

    @abstractmethod
    def set_project_id(self, id_num: int, name: str) -> None:
        """ Set project ID in id2name table. """
        raise NotImplementedError

