from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hiddenimports = collect_submodules('win32api')
datas = collect_data_files('win32api')
