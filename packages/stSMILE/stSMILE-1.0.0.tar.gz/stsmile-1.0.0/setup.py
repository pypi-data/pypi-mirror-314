from setuptools import Command, find_packages, setup

__lib_name__ = "stSMILE"
__lib_version__ = "1.0.0"
__description__ = "Multiscale dissection of spatial heterogeneity by integrating multi-slice spatial and single-cell transcriptomics"
__url__ = "https://github.com/lhzhanglabtools/SMILE"
__author__ = "Lihua Zhang"
__author_email__ = "zhanglh@whu.edu.cn"
__license__ = "MIT"
__keywords__ = ["spatial transcriptomics", "data integration", "Graph nerual network", "scRNA-seq", "deconvolution"]
__requires__ = ["requests",]

setup(
    name = __lib_name__,
    version = __lib_version__,
    description = __description__,
    url = __url__,
    author = __author__,
    author_email = __author_email__,
    license = __license__,
    packages = ['stSMILE'],
    install_requires = __requires__,
    zip_safe = False,
    include_package_data = True,
)

