import os
from shutil import copy

csvfn = r"\\10.99.68.54\Digital pathology image lib\HubMap Skin TMC project\Data_upload\D009\lab_processed\images\z-0001.ome-tiff.channels.csv"
for i in range(99):
    n = i+2
    copy(csvfn,csvfn.replace('z-0001','z-{}'.format(str(n).zfill(4))))