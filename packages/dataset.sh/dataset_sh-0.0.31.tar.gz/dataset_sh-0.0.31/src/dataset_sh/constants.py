import os.path

CONFIG_JSON = os.path.expanduser('~/.dataset_sh_config.json')
STORAGE_BASE = os.path.expanduser('~/dataset_sh/storage')
ALIAS_FILE = os.path.expanduser('~/.dataset.sh.host-alias.json')
DSH_DEFAULT_HOST = os.getenv('DSH_DEFAULT_HOST', 'https://base.dataset.sh')

SAMPLE_CHAR_COUNT = 1000 * 10

DEFAULT_COLLECTION_NAME = 'main'
