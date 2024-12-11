import codecs
import os.path
from pathlib import Path
from setuptools import setup, Extension, find_packages
from distutils.command.build import build as build_orig

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

here = Path(__file__).parent
readme_file = (here / "README.md").read_text()

exts = [
    Extension(name="tactigon_gear.middleware.Tactigon_Gesture", sources=["tactigon_gear/middleware/Tactigon_Gesture.c"]),
    Extension(name="tactigon_gear.middleware.Tactigon_Recorder", sources=["tactigon_gear/middleware/Tactigon_Recorder.c"]),
    Extension(name="tactigon_gear.middleware.Tactigon_Audio", sources=["tactigon_gear/middleware/Tactigon_Audio.c"]),
    Extension(name="tactigon_gear.middleware.utilities.Data_Preprocessor", sources=["tactigon_gear/middleware/utilities/Data_Preprocessor.c"]),
    Extension(name="tactigon_gear.middleware.utilities.Tactigon_RT_Computing", sources=["tactigon_gear/middleware/utilities/Tactigon_RT_Computing.c"]),
]

class build(build_orig):

    def finalize_options(self):
        super().finalize_options()
        __builtins__.__NUMPY_SETUP__ = False

        from Cython.Build import cythonize
        self.distribution.ext_modules = cythonize(self.distribution.ext_modules,
                                                  language_level=3)

setup(
    name="tactigon_gear",
    version=get_version("tactigon_gear/__init__.py"),
    maintainer="Next Industries s.r.l.",
    maintainer_email="info@thetactigon.com",
    url="https://www.thetactigon.com",
    description="Tactigon Gear to connect to Tactigon Skin wereable platform",
    long_description=readme_file,
    long_description_content_type='text/markdown',
    keywords="tactigon,wereable,gestures controller,human interface",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8.0",
    setup_requires=["cython"],
    install_requires=[
        "requests==2.31.0",
        "scipy==1.10.1",
        "numpy==1.24.4",
        "bleak==0.22.0",
        "scikit-learn==1.3.1",
        "pandas==2.0.3"
    ],
    ext_modules=exts  
)