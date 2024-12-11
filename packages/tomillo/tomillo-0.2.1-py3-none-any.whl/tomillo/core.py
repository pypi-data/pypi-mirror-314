from tomillo.log_prep import config as logconf

from bshlib.utils import super_touch
from pathlib import Path
from loguru import logger
import tomlkit
import os

logconf()

class Configuration(object):
    """For accesing and modifying config, use the `map` attribute.
    """

    _stgfile: Path
    project: str
    map: tomlkit.TOMLDocument

    def __new__(cls, project: str):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Configuration, cls).__new__(cls)
        return cls.instance

    def __init__(self, project: str):
        self._stgfile = Path(os.environ["HOME"]) / '.config' / project / 'settings.toml'
        self.project = project
        # TODO: dont debug log anything unless initialized with a option `debug=True`
        logger.debug('parsing settings file..')
        self.map = self.__parse()
        self.save()

    def __parse(self):
        try:
            with open(self._stgfile, 'rt') as f:
                stg = tomlkit.load(f)
            logger.success('settings applied')
        except FileNotFoundError:
            super_touch(self._stgfile)
            stg = tomlkit.document()
            stg.add(tomlkit.comment(f'{self.project} configuration'))
            stg.add(tomlkit.nl())
            logger.success('settings initialized')
        return stg

    def save(self):
        with open(self._stgfile, 'wt') as f:
            tomlkit.dump(self.map, f)
        logger.success('settings saved')
