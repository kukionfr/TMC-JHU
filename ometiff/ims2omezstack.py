import os
vipshome = r'C:\Users\kyu\Documents\vips-dev-8.15\bin'
os.environ['PATH'] = vipshome + ';' + os.environ['PATH']
import pyvips  #must use conda to install
from time import time

def ims2omezstack(ims,output_dir,q,compression):
    imobjs = []
    for idx,im in enumerate(ims):
        impth = os.path.join(input_dir, im)
        if im.endswith('ndpi'):
            imobj = pyvips.Image.openslideload(impth,level=0)
        else:
            imobj = pyvips.Image.new_from_file(impth)
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

    outputfilepath = os.path.join(output_dir, 'Z{}_Q{}_B{}_{}_kyu.ome.tiff'.format(zlen, q, bitdepth, compression))

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

    # 75% compression by default
    comp.tiffsave(outputfilepath, compression=compression, tile=True,
                  tile_width=512, tile_height=512, Q=q,
                  pyramid=True, subifd=True, bigtiff=True)
    dt = round(time()-start)
    print('elapsed time: {}'.format(dt))
    os.rename(outputfilepath,outputfilepath.replace('kyu','T'+str(dt)))
    print('ome-tiff saved here: ',outputfilepath)