import os
import pandas as pd
from hubmapID_lookup import hubmapID_lookup
from bid2did import bid2did
def ims2tsv(src,blockID):
    dst = r'\\10.99.68.54\Digital pathology image lib\HubMap Skin TMC project\bulk_slide_registration'
    lab_id = [os.path.splitext(_)[0] for _ in os.listdir(src) if _.endswith('.ndpi')]
    sample_category = 'section'
    organ_type = ''
    sample_protocol = 'https://dx.doi.org/10.17504/protocols.io.kqdg3242qv25/v3'
    description = 'None'
    rui_location = ''
    lenim = len(lab_id)
    df = pd.DataFrame({'source_id':[blockID]*lenim,
                       'lab_id':lab_id,
                       'sample_category':[sample_category]*lenim,
                       'organ_type':[organ_type]*lenim,
                       'sample_protocol':[sample_protocol]*lenim,
                       'description':[description]*lenim,
                       'rui_location':[rui_location]*lenim
                       })

    df.to_csv(os.path.join(dst,csvname),index=False)
    if lenim>80: df[80:].to_csv(os.path.join(dst,csvname.replace('csv','80toend.tsv')), sep="\t", index=False)
    if lenim>40: df[40:80].to_csv(os.path.join(dst,csvname.replace('csv','40to80.tsv')), sep="\t", index=False)
    if lenim>1:  df[0:40].to_csv(os.path.join(dst,csvname.replace('csv','0to40.tsv')), sep="\t", index=False)

if __name__=='__main__':
    # src = r'\\10.99.68.54\Digital pathology image lib\HubMap Skin TMC project\Data_upload\D001B002\raw\images'
    # csvname = 'D001B002.csv'

    bid = 2

    did = bid2did(bid)
    bid = 'B' + str(bid).zfill(3)
    src = r'\\10.99.68.54\Digital pathology image lib\HubMap Skin TMC project\Data_upload\{}{}'.format(did,bid)
    blockID = hubmapID_lookup(bid,'block')


    csvname = os.path.basename(src)+'.csv'
    src = os.path.join(*[src,'raw','images'])
    ims2tsv(src, blockID)