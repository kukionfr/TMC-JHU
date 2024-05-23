from im2ometiff import im2ometiff

if __name__=='__main__':
    pth_im = r"\\shelter.win.ad.jhu.edu\Kyu\skin_aging\HUBMAP\luciane_alignment\luciane_visium\HE_scans\Mar19_2024\HMP031_46.ndpi"
    pth_ometiff = r"\\shelter.win.ad.jhu.edu\Kyu\skin_aging\HUBMAP\luciane_alignment\luciane_visium\HE_scans\Mar19_2024\HMP031_46.ome.tiff"
    im2ometiff(pth_im,pth_ometiff)

