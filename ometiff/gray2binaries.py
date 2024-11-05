import glob, os
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
import numpy as np
from tqdm import tqdm
src = r'\\10.99.68.54\Digital pathology image lib\JHU\Won Jin Ho\240912 HCC 3D pilot sample\HESS\AlignIM\run1\Dalign_lbl__imdsf16__dsfout4_padsz200'
ims = glob.glob(os.path.join(src,'*.png'))
for im in tqdm(ims):
    fol, fn = os.path.split(im)
    im = Image.open(im)
    imarr = np.array(im)
    # 5,7,8
    # imtmps = range(1,px+1)
    imtmps = [5,7,8]
    px = np.max(imarr)
    for imtmp in imtmps:
        dst = os.path.join(src,str(imtmp+100))
        if not os.path.exists(dst): os.makedirs(dst)
    for imtmp in imtmps:
        Image.fromarray(imarr==imtmp).save(os.path.join(*[fol,str(imtmp+100),fn]))