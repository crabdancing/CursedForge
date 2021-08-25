from abc import abstractmethod, ABC
from typing import Optional


class AbstractDBWrapper(ABC):
    """ Crude database wrapper ADT, allowing us to easily swap out different DB implementations. """

    @abstractmethod
    def __init__(self, fname: str):
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

