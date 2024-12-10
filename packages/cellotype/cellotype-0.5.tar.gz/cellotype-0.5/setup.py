from setuptools import setup,find_packages
import io
import re

with io.open('README.md', 'r', encoding='utf8') as f:
    long_description = f.read()

# with io.open("src/useful_decoration/__init__.py", "rt", encoding="utf8") as f:
#     version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)


setup(
    name="cellotype",
    license='Apache License 2.0',
    version='0.5',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    # package_dir={"": "src"},
    # long_description=long_description,
    url='https://github.com/maxpmx/CelloType',
    author='Minxing Pang',
    author_email='minxing@sas.upenn.edu',
    description='An end-to-end Transformer-based method for automated cell/nucleus segmentation and cell type classification',

    # project_urls={
    #     "Documentation": "https://useful-decoration.readthedocs.io/en/latest/",
    #     "Code": "https://github.com/changyubiao/useful_decoration",
    # },

    python_requires='==3.8.*',
    install_requires=[
        'cython',
        'scipy',
        'shapely',
        'timm',
        'h5py',
        'submitit',
        'scikit-image',
        'opencv-python',
        'pycocotools',
        'gdown',
        'sahi==0.11.16',
        'torch==1.9.0',
        'torchvision==0.10.0',
        # 'cudatoolkit==11.1',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Image Processing',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]

)