from sqlalchemy import create_engine
from model import BaseModel
from sqlalchemy.orm import sessionmaker
import importlib.util
from pathlib import Path
from service.configservice import load, get_connection_string


engine_name = get_connection_string('config.yaml')


db_engine = create_engine(engine_name, echo=True)
BaseModel.metadata.create_all(bind=db_engine)

db_session_maker = sessionmaker(bind=db_engine)
DBSession = db_session_maker()


def import_all_models():
    for full_module_name in _package_contents('model'):
        importlib.import_module(full_module_name)


def _package_contents(package_name):
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        return set()

    pathname = Path(spec.origin).parent
    ret = set()
    with os.scandir(pathname) as entries:
        for entry in entries:
            if entry.name.startswith('__'):
                continue
            current = '.'.join((package_name, entry.name.partition('.')[0]))
            if entry.is_file():
                if entry.name.endswith('.py'):
                    ret.add(current)
            elif entry.is_dir():
                ret.add(current)
                ret |= _package_contents(current)

    return ret

