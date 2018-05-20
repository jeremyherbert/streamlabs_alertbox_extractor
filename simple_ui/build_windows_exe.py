import os
script_path = os.path.dirname(os.path.realpath(__file__))
os.system("pyinstaller --onefile --noconsole %s" % os.path.join(script_path, "main.py"))
