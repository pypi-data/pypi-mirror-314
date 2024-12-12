from muslimDeen.config import Config
from muslimDeen.service import Services
from muslimDeen.metasurahs import MetaSurahs
from muslimDeen.quran_reader_base import QuranReaderBase
from muslimDeen.meta_quran_reader import MetaQuranReader
from muslimDeen.handle_exception import ByError, SurahNotFound, VersetNotFound, FormatValueGet
from muslimDeen.model import Model
from typing import Union
from pathlib import Path


class MuslimDeen:
    def __init__(self, path_database: Union[str, Path, None] = None):
        if isinstance(path_database, str):
            path = Path(path_database).joinpath('database')
        elif isinstance(path_database, Path):
            path = path_database.joinpath('database')
        elif path_database is None:
            path = Path().cwd().joinpath('database')
        path.mkdir(parents=True, exist_ok=True)
        self.path_database = path.as_posix()
        self.setup_all()

    def config_url(self) -> Config:
        return Config()

    def meta_surahs(self) -> MetaSurahs:
        return MetaSurahs(self.path_database)

    def quran_reader(self) -> QuranReaderBase:
        return QuranReaderBase(self.path_database)

    def meta_quran_reader(self) -> MetaQuranReader:
        return MetaQuranReader(self.path_database)

    def model(self) -> Model:
        return Model(self.path_database)

    def setup_all(self) -> None:
        self.meta_surahs()
        self.quran_reader()
        self.model()
