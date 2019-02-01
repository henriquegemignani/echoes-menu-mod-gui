from pyqt_distutils.build_ui import build_ui
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py

from echoes_menu_mod_gui import VERSION


class custom_build_py(build_py):
    def run(self):
        self.run_command('build_ui')
        super().run()


with open("README.md") as readme_file:
    long_description = readme_file.read()

setup(
    name='echoes-menu-mod-gui',
    version=VERSION,
    author='Henrique Gemignani',
    url='https://github.com/henriquegemignani/echoes-menu-mod-gui',
    description='A GUI for applying Menu Mod to a Metroid Prime 2 ISO.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    cmdclass={
        "build_ui": build_ui,
        "build_py": custom_build_py
    },
    scripts=[
    ],
    package_data={
        "randovania": [
            "data/*",
            "data/ClarisPrimeRandomizer/*",
        ]
    },
    license='License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Games/Entertainment',
    ],
    python_requires=">=3.7",
    install_requires=[
        'PySide2>=5.12',
        'appdirs',
        'nod>=1.1',
        'requests',
        'pytest',
        'pytest-cov',
        'pytest-qt',
    ],
    entry_points={
        'console_scripts': [
            "randovania = randovania.__main__:main"
        ]
    },
)
