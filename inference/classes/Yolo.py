import os
import pandas as pd
import ultralytics
from ultralytics import YOLO
ultralytics.checks()


class Yolo:
    def __init__(self, config):
        self.config = config
        self.model = YOLO(config.yolo_wights)




