
from ciocore import data as coredata

coredata.init("blender")
coredata.set_fixtures_dir("")

def connect():
    """
    Connect to the server to retrieve projects, packages, and machines.

    """
    print("Connect to the server to get projects, packages, machines.")
    coredata.data(force=True)
