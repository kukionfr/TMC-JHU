import os
from shutil import copy

csvfn = r"\\10.99.68.54\Digital pathology image lib\HubMap Skin TMC project\bulk_slide_registration\imname.ome-tiff.channels.csv"
dst = r'\\10.99.68.54\Digital pathology image lib\HubMap Skin TMC project\Data_upload\D006B008\lab_processed\images'
ims = [_ for _ in os.listdir(dst) if _.endswith('ome.tiff')]

for im in ims:
    imnm, ext = os.path.splitext(im)
    imnm, ext = os.path.splitext(imnm)
    copy(csvfn,os.path.join(dst,imnm+'.ome-tiff.channels.csv'))
