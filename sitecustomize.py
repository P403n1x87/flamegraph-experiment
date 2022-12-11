import os
import time

if os.getenv("REGRESSION", False):
    time.sleep(0.1)
