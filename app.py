import sys
import os
import runpy

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

runpy.run_path(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/agenticchatbot/ui/app.py")
)
