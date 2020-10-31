import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import markdown

from echoes_menu_mod_gui import VERSION

zip_folder = "echoes-menu-mod-gui-{}".format(VERSION)

package_folder = Path("dist", "echoes_menu_mod_gui")
shutil.rmtree(package_folder, ignore_errors=True)

subprocess.run([sys.executable, "-m", "PyInstaller", "echoes_menu_mod_gui.spec"], check=True)

with zipfile.ZipFile("dist/{}.zip".format(zip_folder), "w", compression=zipfile.ZIP_DEFLATED) as release_zip:
    for f in package_folder.glob("**/*"):
        print("Adding", f)
        release_zip.write(f, "{}/{}".format(zip_folder, f.relative_to(package_folder)))

    with open("README.md") as readme_file:
        readme_html = markdown.markdown(readme_file.read())
        release_zip.writestr(zip_folder + "/README.html", readme_html)

    for subdir, _, files in os.walk("echoes-menu-mod-gui-readme"):
        for file in files:
            path = os.path.join(subdir, file)
            release_zip.write(path, "{}/{}".format(zip_folder, path))
