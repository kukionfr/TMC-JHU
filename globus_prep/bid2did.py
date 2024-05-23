import pandas as pd

def bid2did(blockID):
    df = pd.read_excel(r"\\babyserverdw3.acasmart.jh.edu\PW Cloud Exp Documents\Research Projects\PRJ-23-02-01 Skin Tissue mapping HubMAP TMC project\sample cohort\Cohort_List_JHU-TMC_240429.xlsx",'Block')
    return df[df['Block_ID']=='B{}'.format(str(blockID).zfill(3))]['Donor_ID'].values[0]

if __name__=='__main__':
    blockID = 3
    donorID = bid2did(blockID)
    print(blockID, donorID)