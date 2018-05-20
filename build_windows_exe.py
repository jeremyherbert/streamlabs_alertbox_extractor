import os
script_path = os.path.dirname(os.path.realpath(__file__))
os.system("pyinstaller --onefile %s" % os.path.join(script_path, "streamlabs_youtube_extractor_qt.py"))
