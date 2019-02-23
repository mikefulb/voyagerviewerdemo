# -*- mode: python -*-

block_cipher = None

# from https://github.com/astropy/astropy/issues/7052
import astropy
astropy_path, = astropy.__path__

a = Analysis(['voyagerviewerdemo_main.py'],
             pathex=['..', 'C:\\Users\\msf\\Documents\\Astronomy\\Projects\\Utilities\\voyagerviewerdemo\\scripts'],
             binaries=[],
             datas=[(astropy_path, 'astropy')],
             hiddenimports=['shelve', 'csv'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['astropy'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

# get rid of mkl stuff taking up so much room!
# from https://github.com/pyinstaller/pyinstaller/issues/2270
#Key = ['mkl','libopenblas']
#
#def remove_from_list(input, keys):
#    print(a.binaries)
#    print(keys)
#    outlist = []
#    for item in input:
#        name, _, _ = item
#        flag = 0
#        for key_word in keys:
#            if name.find(key_word) > -1:
#                flag = 1
#        if flag != 1:
#            outlist.append(item)
#    print(outlist)
#    return outlist
#
#print('Modifying a.binaries')
#a.binaries = remove_from_list(a.binaries, Key)
# end mkl cleanup

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='voyagerviewerdemo_main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
