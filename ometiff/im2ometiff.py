import os
vipshome = r'\\10.99.68.51\Kyu\archive\openslide_vips\vips-dev-8.15\bin'
os.environ['PATH'] = vipshome + ';' + os.environ['PATH']
import pyvips  #must use conda to install
from time import time
from openslide import OpenSlide

def im2ometiff(impth,pth_ometiff):
    print('opening: {}'.format(impth))
    if impth.endswith('ndpi'):
        imobj = pyvips.Image.openslideload(impth, level=0)
        om = OpenSlide(impth)
        mppx = round(float(om.properties['openslide.mpp-x']), 4)
        mppy = round(float(om.properties['openslide.mpp-y']), 4)
        om.close()
        print('wsi found')
    else:
        imobj = pyvips.Image.new_from_file(impth)
        mppx = 7
        mppy = mppx
        print('image found')

    print('image type: {}'.format(imobj.interpretation))
    if imobj.interpretation == 'b-w':
        bitdepth = 8
    elif imobj.interpretation == 'grey16':
        bitdepth = 16
    else:
        bitdepth = 8

    if imobj.hasalpha(): imobj = imobj[:-1]
    comp = pyvips.Image.arrayjoin(imobj.bandsplit(), across=1)

    image_height = imobj.height
    image_width = imobj.width
    comp = comp.copy()
    # set minimal OME metadata
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
                    SizeZ="1"
                    Type="uint{bitdepth}"
                    PhysicalSizeX="{mppx}"
                    PhysicalSizeXUnit="µm"
                    PhysicalSizeY="{mppy}"
                    PhysicalSizeYUnit="µm"
                    PhysicalSizeZ="5"
                    PhysicalSizeZUnit="µm">
            </Pixels>
        </Image>
    </OME>""")
    #jpeg,jp2k,lzw,
    print('bit depth: {}'.format(bitdepth))
    print('saving image...')
    # jp2k breaks the format somehow
    start=time()
    comp.tiffsave(pth_ometiff, compression="none", tile=True, #hubmap requires none compression
                  tile_width=512, tile_height=512,
                  pyramid=True, subifd=True, bigtiff=True)
    dt = round(time() - start)
    print('elapsed time: {}'.format(dt))
    print('ome-tiff saved here: ',pth_ometiff)

if __name__=="__main__":
    impth = r"Z:\stephen_eric_3D_vis\data\2D\raw\images\z-024-p1b2sb3 - 2024-03-13 18.48.16.ndpi"
    pth_ometiff = impth.replace(".ndpi","_without_compression.ome.tiff")
    im2ometiff(impth,pth_ometiff)