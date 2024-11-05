import os
vipshome = r'\\10.99.68.51\Kyu\archive\openslide_vips\vips-dev-8.15\bin'
os.environ['PATH'] = vipshome + ';' + os.environ['PATH']
import pyvips  #must use conda to install
from time import time
from natsort import natsorted

def ims2omezstack(ims,pth_ometiff,q,compression):
    imobjs = []
    for idx,im in enumerate(ims):
        if im.endswith('ndpi'):
            imobj = pyvips.Image.openslideload(im,level=0)
        else:
            imobj = pyvips.Image.new_from_file(im)
        if imobj.hasalpha(): imobj = imobj[:-1]
        imobjs.append(pyvips.Image.arrayjoin(imobj.bandsplit(), across=1))
    numch = len(imobjs)
    print('number of channels:', numch)

    # determine image type with first image rather than the last in case there are mixture of image types
    imobj = pyvips.Image.new_from_file(ims[0])
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
                    SizeC="{numch}"
                    SizeT="1"
                    SizeX="{image_width}"
                    SizeY="{image_height}"
                    SizeZ="1"
                    Type="uint{bitdepth}"
                    PhysicalSizeX="1"
                    PhysicalSizeXUnit="µm"
                    PhysicalSizeY="1"
                    PhysicalSizeYUnit="µm"
                    PhysicalSizeZ="1"
                    PhysicalSizeZUnit="µm">
                <Channel ID="Channel:0:1" 
                         Name="80ArAr_80ArAr">
                </Channel>
                <Channel ID="Channel:0:2" 
                         Name="89Y_CD45">
                </Channel>
                <Channel ID="Channel:0:3" 
                         Name="100Ru_Ruthenium">
                </Channel>
                <Channel ID="Channel:0:4" 
                         Name="102Ru_Ruthenium">
                </Channel>
                <Channel ID="Channel:0:5" 
                         Name="113In_Collagen">
                </Channel>
                <Channel ID="Channel:0:6" 
                         Name="115In_Ecadherin">
                </Channel>
                <Channel ID="Channel:0:7" 
                         Name="120Sn_120Sn">
                </Channel>
                <Channel ID="Channel:0:8" 
                         Name="127I_127I">
                </Channel>
                <Channel ID="Channel:0:9" 
                         Name="131Xe_131Xe">
                </Channel>
                <Channel ID="Channel:0:10" 
                         Name="133Cs_133Cs">
                </Channel>
                <Channel ID="Channel:0:11" 
                         Name="138Ba_138Ba">
                </Channel>
                <Channel ID="Channel:0:12" 
                         Name="141Pr_SMA">
                </Channel>
                <Channel ID="Channel:0:13" 
                         Name="142Nd_Podoplanin">
                </Channel>
                <Channel ID="Channel:0:14" 
                         Name="143Nd_VIM">
                </Channel>
                <Channel ID="Channel:0:15" 
                         Name="144Nd_CD14">
                </Channel>
                <Channel ID="Channel:0:16" 
                         Name="145Nd_CD45RO">
                </Channel>
                <Channel ID="Channel:0:17" 
                         Name="146Nd_CD16">
                </Channel>
                <Channel ID="Channel:0:18" 
                         Name="147Sm_CD163">
                </Channel>
                <Channel ID="Channel:0:19" 
                         Name="148Nd_CK">
                </Channel>
                <Channel ID="Channel:0:20" 
                         Name="149Sm_CD137">
                </Channel>
                <Channel ID="Channel:0:21" 
                         Name="150Sm_PDL1">
                </Channel>
                <Channel ID="Channel:0:22" 
                         Name="151Eu_PD1">
                </Channel>
                <Channel ID="Channel:0:23" 
                         Name="152Sm_CD57">
                </Channel>
                <Channel ID="Channel:0:24" 
                         Name="153Eu_Tox-Tox2">
                </Channel>
                <Channel ID="Channel:0:25" 
                         Name="154Sm_DC-LAMP">
                </Channel>
                <Channel ID="Channel:0:26" 
                         Name="155Gd_FOXP3">
                </Channel>
                <Channel ID="Channel:0:27" 
                         Name="156Gd_CD4">
                </Channel>
                <Channel ID="Channel:0:28" 
                         Name="158Gd_pSTAT3">
                </Channel>
                <Channel ID="Channel:0:29" 
                         Name="159Tb_CD68">
                </Channel>
                <Channel ID="Channel:0:30" 
                         Name="160Gd_CD138">
                </Channel>
                <Channel ID="Channel:0:31" 
                         Name="161Dy_CD20">
                </Channel>
                <Channel ID="Channel:0:32" 
                         Name="162Dy_CD8">
                </Channel>
                <Channel ID="Channel:0:33" 
                         Name="163Dy_CD21">
                </Channel>
                <Channel ID="Channel:0:34" 
                         Name="164Dy_ARG1">
                </Channel>
                <Channel ID="Channel:0:35"
                         Name="165Ho_CD33">
                </Channel>
                <Channel ID="Channel:0:36" 
                         Name="166Er_CD45RA">
                </Channel>
                <Channel ID="Channel:0:37" 
                         Name="167Er_GZMB">
                </Channel>
                <Channel ID="Channel:0:38" 
                         Name="168Er_KI67">
                </Channel>
                <Channel ID="Channel:0:39" 
                         Name="170Er_CD3">
                </Channel>
                <Channel ID="Channel:0:40" 
                         Name="171Yb_LAG3">
                </Channel>
                <Channel ID="Channel:0:41" 
                         Name="172Yb_CD15">
                </Channel>
                <Channel ID="Channel:0:42" 
                         Name="173Yb_DC-SIGN">
                </Channel>
                <Channel ID="Channel:0:43" 
                         Name="174Yb_HLADR">
                </Channel>
                <Channel ID="Channel:0:44" 
                         Name="175Lu_CD86">
                </Channel>
                <Channel ID="Channel:0:45" 
                         Name="176Yb_CD206">
                </Channel>
                <Channel ID="Channel:0:46" 
                         Name="190BCKG_190BCKG">
                </Channel>
                <Channel ID="Channel:0:47" 
                         Name="190Os_190Os">
                </Channel>
                <Channel ID="Channel:0:48" 
                         Name="191Ir_DNA1">
                </Channel>
                <Channel ID="Channel:0:49" 
                         Name="193Ir_DNA2">
                </Channel>
                <Channel ID="Channel:0:50" 
                         Name="195Pt_PM2">
                </Channel>
                <Channel ID="Channel:0:51" 
                         Name="196Pt_PM3">
                </Channel>
                <Channel ID="Channel:0:52" 
                         Name="198Pt_PM4">
                </Channel>
                <Channel ID="Channel:0:53" 
                         Name="204Pb_204Pb">
                </Channel>
                <Channel ID="Channel:0:54" 
                         Name="208Pb_208Pb">
                </Channel>
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
                  tile_width=512, tile_height=512, Q=q,
                  pyramid=True, subifd=True, bigtiff=True)
    dt = round(time() - start)
    print('elapsed time: {}'.format(dt))
    print('ome-tiff saved here: ',pth_ometiff)

if __name__=='__main__':
    src = r'\\10.99.68.54\Digital pathology image lib\JHU\Won Jin Ho\240516 HE destain  IMC run1\20240501 HMP038-P07B1SB2\align2HE\roi1'
    dst = os.path.join(src,'cstack')
    pth_ims = natsorted([os.path.join(src,_) for _ in os.listdir(src) if _.endswith(('.jpg','.tif','.png'))])[0:-1]
    pth_ometiff = os.path.join(dst,'{}.ome.tiff'.format('P07B1SB2'))
    ims2omezstack(pth_ims, pth_ometiff, q=50, compression='jpeg')
    # if not os.path.exists(pth_ometiff): ims2omezstack(pth_ims,pth_ometiff,q=50,compression='jpeg')
    # else: print('exists: ',pth_ometiff)

