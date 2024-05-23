import pandas as pd

def hubmapID_lookup(blockID,sampletype):
    df = pd.read_excel(r"\\babyserverdw3.acasmart.jh.edu\PW Cloud Exp Documents\Research Projects\PRJ-23-02-01 Skin Tissue mapping HubMAP TMC project\sample cohort\Cohort_List_JHU-TMC_240429.xlsx",'Block')
    if sampletype.lower() == 'block': return df[df['Block_ID']==blockID]['HuBMAP ID'].values[0]

if __name__=='__main__':
    blockID = 'B002'
    sampletype = 'block'
    hubmapID = hubmapID_lookup(blockID,sampletype)
    print(blockID, hubmapID)
