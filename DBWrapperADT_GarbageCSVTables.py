import csv
from pathlib import Path
from typing import Dict, List, Optional
import unicodedata
from DBWrapperADT import AbstractDBWrapper


class DBWrapper(AbstractDBWrapper):
    """ This implementation in particular is the most garbage thing I could possibly make.
    Instead of using a real db backend, we just muck about with a separate table storing everything in plaintext CSV"""

    fpath: Path = None
    # For whatever reason, DictWriter expects an Iterable[Mapping[str, Any]] instead of Dict[str, int]
    db_dict: Dict[str, int] = {}
    # most queries are going to be starting with name, seeking ID
    # So we're putting our fields backwards here :/
    fields: List[str] = ['name', 'id']

    def __init__(self, fname: str = 'id2name.csv'):
        self.fpath = Path(fname)
        if self.fpath.exists():
            # load all into memory as dict, then close
            with self.fpath.open('r', encoding='utf-8') as fhandle:
                # VERY IMPORTANT: you might be tempted to think you can simply typecast csv.DictReader() directly,
                # But you CANNOT. It will silently fail >.< You need .reader at the end.
                # It took me like an hour to figure this out, Fucking hell.
                reader = csv.DictReader(fhandle, fieldnames=self.fields).reader
                self.db_dict = dict(reader)
        else:
            # create file
            self.fpath.touch()

    def __del__(self):
        self.commit()

    def commit(self) -> None:
        # gets 'unknown encoder: ascii' error if I don't write specify encoding >.<
        with self.fpath.open('w', encoding='utf-8') as fhandle:
            writer = csv.DictWriter(fhandle, fieldnames=self.fields)
            for name in self.db_dict.keys():
                id_num = self.db_dict[name]
                writer.writerow({'name': name, 'id': id_num})

    def query_project_id(self, name: str) -> Optional[int]:  # Optional = Union[ur_type, None] ;)
        try:
            return int(self.db_dict[name])
        except KeyError:
            return None

    def query_project_name(self, id_num) -> Optional[str]:
        try:
            index: int = list(self.db_dict.keys()).index(id_num)
            return list(self.db_dict.keys())[index]
        except ValueError:
            return None

    def set_project_id(self, id_num: int, name: str) -> None:
        self.db_dict[name] = id_num
