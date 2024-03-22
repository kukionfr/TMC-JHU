import os
vipshome = r'C:\Users\kyu\Documents\vips-dev-8.15\bin'
os.environ['PATH'] = vipshome + ';' + os.environ['PATH']
import pyvips  #must use conda to install
from time import time
import glob
from openslide import OpenSlide

def im2ometiff(src):
    impth = glob.glob(os.path.join(src,'raw\images\*.ndpi'))
    impth = impth[0]
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

    image_height = imobj.height
    image_width = imobj.width

    if imobj.interpretation == 'b-w':
        comp = imobj
    else:
        if imobj.hasalpha(): imobj = imobj[:-1]
        comp = pyvips.Image.arrayjoin(imobj.bandsplit(), across=1)

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
                    SizeC="1"
                    SizeT="1"
                    SizeX="{image_width}"
                    SizeY="{image_height}"
                    SizeZ="1"
                    Type="uint8"
                    PhysicalSizeX="{mppx}"
                    PhysicalSizeXUnit="µm"
                    PhysicalSizeY="{mppy}"
                    PhysicalSizeYUnit="µm"
                    PhysicalSizeZ="4"
                    PhysicalSizeZUnit="µm">
            </Pixels>
        </Image>
    </OME>""")
    #jpeg,jp2k,lzw,
    print('saving image...')
    # jp2k breaks the format somehow
    start=time()
    outputfilepath = os.path.join(src,'lab_processed\images\{}.ome.tiff'.format(os.path.basename(src)))
    comp.tiffsave(outputfilepath, compression="none", tile=True, #hubmap requires none compression
                  tile_width=512, tile_height=512,
                  pyramid=True, subifd=True, bigtiff=True)
    print('elapsed time: {}'.format(round(time()-start)))
    print('ome-tiff saved here: ',outputfilepath)

    fn,ext = os.path.splitext(os.path.basename(impth))
    impthrn = impth.replace(fn,os.path.basename(src))
    os.rename(impth,impthrn) #close openslide object
    print('wsi is renamed to: ', impthrn)

if __name__=='__main__':
    src = r"\\10.99.68.54\Digital pathology image lib\HubMap Skin TMC project\HBM296.SPWJ.878-D003"
    im2ometiff(src)
