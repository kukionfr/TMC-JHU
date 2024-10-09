import os
vipshome = r'C:\Users\kyu\Documents\vips-dev-8.15\bin'
os.environ['PATH'] = vipshome + ';' + os.environ['PATH']
import pyvips  #must use conda to install
from time import time

def ims2omezstack(ims,pth_ometiff,q,compression):
    imobjs = []
    for idx,im in enumerate(ims):
        if im.endswith('ndpi'):
            imobj = pyvips.Image.openslideload(im,level=0)
        else:
            imobj = pyvips.Image.new_from_file(im)
        if imobj.hasalpha(): imobj = imobj[:-1]
        imobjs.append(pyvips.Image.arrayjoin(imobj.bandsplit(), across=1))
    zlen = len(imobjs)
    print('Z stack height:', zlen)

    if imobj.interpretation == 'b-w':
        bitdepth = 8
    elif imobj.interpretation == 'grey16':
        bitdepth = 16
    else:
        bitdepth = 8

    comp = pyvips.Image.arrayjoin(imobjs, across=1)
    image_height = imobj.height
    image_width = imobj.width
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
                    SizeC="3"
                    SizeT="1"
                    SizeX="{image_width}"
                    SizeY="{image_height}"
                    SizeZ="{zlen}"
                    Type="uint{bitdepth}"
                    PhysicalSizeX="7.0656"
                    PhysicalSizeXUnit="µm"
                    PhysicalSizeY="7.0656"
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
    src = r'\\10.99.68.54\Digital pathology image lib\JHU\Won Jin Ho\240912 HCC 3D pilot sample\HESS\AlignIM\run1\Dalign_lbl__imdsf16__dsfout1_padsz200\imcrop_png\simple'
    pth_ims = [os.path.join(src,_) for _ in os.listdir(src) if _.endswith('.png')]
    pth_ometiff = os.path.join(src,'{}.ome.tiff'.format('deflate_zstack'))
    if not os.path.exists(pth_ometiff): ims2omezstack(pth_ims,pth_ometiff,q=50,compression='deflate')
    else: print('exists: ',pth_ometiff)

