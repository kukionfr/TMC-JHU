%% add python executor and python script path
pyExec = 'C:\ProgramData\anaconda3\envs\histo_ome_tiff\python.exe';
hoverRoot = '\\10.99.68.31\PW Cloud Exp Documents\Lab work documenting\W-24-01-01 PW Output omeTiff with libvip KH\multichannel2ometiff_matlab.py';
%% add python script to matlab path
pyRoot = fileparts(pyExec);
p = getenv('PATH');
p = strsplit(p, ';');
addToPath = {
    pyRoot
    hoverRoot
    fullfile(pyRoot, 'Library', 'mingw-w64', 'bin')
    fullfile(pyRoot, 'Library', 'usr', 'bin')
    fullfile(pyRoot, 'Library', 'bin')
    fullfile(pyRoot, 'Scripts')
    fullfile(pyRoot, 'bin')
    };
p = [addToPath(:); p(:)];
p = unique(p, 'stable');
p = strjoin(p, ';');
setenv('PATH', p);


%% set up variables - User Input
% image folder to be analyzed..% work with PNG, TIF, JPEG
src = "\\10.99.68.54\Digital pathology image lib\MxIF SFC\Musle samples from Buck\204\align_wsi\ReadDsf1_OutDsf1_8bit";
dst = fullfile(src,'cstack');
q='70';
compression='jpeg';





%% run command line for TILE
system(sprintf(['python "\\\\10.99.68.31\\PW Cloud Exp Documents\\Lab work documenting\\W-24-01-01 PW Output omeTiff with libvip KH\\multichannel2ometiff_matlab.py" ',...
        '--input_dir="%s" ',...
        '--output_dir="%s" ',...
        '--quality="%s" ',...
        '--compression=%s'],...
        src,...
        dst,...
        q,...
        compression))