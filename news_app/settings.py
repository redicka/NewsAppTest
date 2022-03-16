import pathlib
import yaml

from news_app.utils import TRAFARET


BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = BASE_DIR / 'config' / 'news.yml'


def load_config() -> TRAFARET:
    with open(DEFAULT_CONFIG_PATH, 'rt') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return TRAFARET.check(data)
