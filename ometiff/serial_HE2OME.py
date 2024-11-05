import glob
import os
from im2ometiff import im2ometiff

if __name__=='__main__':
    src = r'\\10.99.68.54\Digital pathology image lib\SenNet JHU TDA Project\SN-JAX-PA-B1-SNP033'
    pth_ims = glob.glob(os.path.join(src,'WSI of direct HE stain\*.ndpi'))
    for idx,pth_im in enumerate(pth_ims):
        print('image #{}/{}'.format(idx, len(pth_ims)))
        pth_ometiff = os.path.join(*[src,'lab_processed\images','{}.ome.tiff'.format(os.path.basename(pth_im).replace('.ndpi',''))])
        # print(pth_im,pth_ometiff)
        if not os.path.exists(pth_ometiff): im2ometiff(pth_im,pth_ometiff)
        else: print('exists: ',pth_ometiff)

