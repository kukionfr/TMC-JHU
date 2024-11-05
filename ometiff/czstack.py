import os
vipshome = r'\\10.99.68.51\Kyu\archive\openslide_vips\vips-dev-8.15\bin'
os.environ['PATH'] = vipshome + ';' + os.environ['PATH']
import pyvips  #must use conda to install
from time import time
from natsort import natsorted
def ims2omezstack(ims,pth_ometiff,q,compression):
    zs = []
    clen = 2
    for c1,c2,c3 in ims:
        c1 = pyvips.Image.new_from_file(c1)
        # if c1.hasalpha(): c1 = c1[:-1]
        c2 = pyvips.Image.new_from_file(c2)
        # if c2.hasalpha(): c2 = c2[:-1]
        # c3 = pyvips.Image.new_from_file(c3)
        # if c3.hasalpha(): c3 = c3[:-1]
        z= c2.bandjoin(c1)
        zs.append(z)

    zlen = len(zs)
    print('Z stack height:', zlen)


    bitdepth = 8
    comp = pyvips.Image.arrayjoin(zs, across=1)
    image_height = c1.height
    image_width = c1.width
    comp = comp.copy()

    # set minimal OME metadata
    # before we can modify an image (set metadata in this case), we must take a
    # private copy
    comp.set_type(pyvips.GValue.gint_type, "page-height", image_height)
    comp.set_type(pyvips.GValue.gstr_type, "image-description",
                  f"""<?xml version="1.0" encoding="UTF-8"?>
    <OME xmlns="http://www.openmicroscopy.org/Schemas/OME/2016-06"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.openmicroscopy.org/Schemas/OME/2016-06 http://www.openmicroscopy.org/Schemas/OME/2016-06/ome.xsd">
        <Image ID="Image:0">
            <!-- Minimum required fields about image dimensions -->
            <Pixels DimensionOrder="XYCZT"
                    ID="Pixels:0"
                    SizeC="{clen}"
                    SizeT="1"
                    SizeX="{image_width}"
                    SizeY="{image_height}"
                    SizeZ="{zlen}"
                    Type="uint{bitdepth}"
                    PhysicalSizeX="0.4416"
                    PhysicalSizeXUnit="µm"
                    PhysicalSizeY="0.4416"
                    PhysicalSizeYUnit="µm"
                    PhysicalSizeZ="4"
                    PhysicalSizeZUnit="µm">
            </Pixels>
        </Image>
    </OME>""")
    #20X - 0.4416
    #dsf16 - 7.0656
    #dsf

    #jpeg,jp2k,lzw,
    print('bit depth: {}'.format(bitdepth))
    print('saving image in {} format ...'.format(compression))
    # jp2k breaks the format somehow
    start=time()
    comp.tiffsave(pth_ometiff, compression=compression, tile=True, #hubmap requires none compression
                  tile_width=512, tile_height=512,Q=q,
                  pyramid=True, subifd=True, bigtiff=True)
    dt = round(time() - start)
    print('elapsed time: {}'.format(dt))
    print('ome-tiff saved here: ',pth_ometiff)

if __name__=='__main__':
    # src =  r'\\10.99.68.54\Digital pathology image lib\JHU\Won Jin Ho\240912 HCC 3D pilot sample\HESS\AlignIM\run1\Dalign_lbl__imdsf4__dsfout1_padsz200'
    # src = r'\\10.99.68.54\Digital pathology image lib\JHU\Won Jin Ho\240912 HCC 3D pilot sample\HESS\AlignIM\run1\Dalign_lbl__imdsf16__dsfout4_padsz200'
    # src = r'\\10.99.68.54\Digital pathology image lib\JHU\Won Jin Ho\240912 HCC 3D pilot sample\HESS\AlignIM\run1\Dalign_lbl__imdsf4__dsfout4_padsz200'
    src = r'\\10.99.68.54\Digital pathology image lib\JHU\Won Jin Ho\240912 HCC 3D pilot sample\HESS\AlignIM\run1\Dalign_lbl__imdsf16__dsfout1_padsz200'


    c1src = os.path.join(src,'5')
    c1s = [os.path.join(c1src,_) for _ in os.listdir(c1src) if _.endswith('.png')][0:3]
    c1s = natsorted(c1s)

    c2src = os.path.join(src, '7')
    c2s = [os.path.join(c2src,_) for _ in os.listdir(c2src) if _.endswith('.png')][0:3]
    c2s = natsorted(c2s)

    c3src = os.path.join(src, '8')
    c3s = [os.path.join(c3src,_) for _ in os.listdir(c3src) if _.endswith('.png')][0:3]
    c3s = natsorted(c3s)

    pth_ims = zip(c1s,c2s,c3s)

    pth_ometiff = os.path.join(src,'{}.ome.tiff'.format('czstack_75_noalpha'))
    # print(pth_im,pth_ometiff)
    if not os.path.exists(pth_ometiff): ims2omezstack(pth_ims,pth_ometiff,q=50,compression='none')
    else: print('exists: ',pth_ometiff)

