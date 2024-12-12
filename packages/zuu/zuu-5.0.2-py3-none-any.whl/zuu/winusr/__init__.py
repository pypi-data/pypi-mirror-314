
import os
home_path =  os.path.join(os.path.expanduser("~"), ".zwtil")
os.makedirs(home_path, exist_ok=True)

def app_lists():
    return os.listdir(home_path)

def app_path(app_name, create=False):
    app_path = os.path.join(home_path, app_name)
    if create:
        os.makedirs(app_path, exist_ok=True)
    return app_path


