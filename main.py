import os
from UIron.config import Config

path = os.path.dirname(__file__)
path = os.path.join(path, 'UIron/data/config.json')
config = Config(path)

print(config['countries'])