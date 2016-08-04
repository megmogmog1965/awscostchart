import os
from tinydb import TinyDB
from server.util import root_dir

# open local tinydb.
dest = os.path.join(root_dir(), u'db.json')
_db = TinyDB(dest)
