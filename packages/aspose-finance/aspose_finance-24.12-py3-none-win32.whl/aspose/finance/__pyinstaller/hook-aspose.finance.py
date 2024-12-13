from PyInstaller.utils.hooks import get_package_paths
import os.path

(_, root) = get_package_paths('aspose')

datas = [(os.path.join(root, 'assemblies', 'finance'), os.path.join('aspose', 'assemblies', 'finance'))]

hiddenimports = [ 'aspose', 'aspose.pyreflection', 'aspose.pygc', 'aspose.pycore' ]

