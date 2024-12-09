from setuptools import setup, find_packages

setup(
    name='mrjpacking',
    version='0.4.24',
    description='Theo dõi đóng gói sản phẩm sàn thương mại điện tử',
    long_description=open('README.md', encoding='utf-8').read(),
    author='Justin Nguyễn',
    author_email='duchuy_1997@hotmail.com',
    packages=find_packages(),
    package_data={
        'mrjpacking': ['sound/*.mp3'], 
    },
    install_requires=[  
        'pyfiglet',
        'colorama',
        'keyboard',
        'numpy',
        'opencv-python',
        'pygame',
        'pyzbar',
        'pygrabber',
        'packaging',
        'timedelta'
    ],
    python_requires='>=3.6', 
    entry_points={
        'console_scripts': [
            'mrjpacking=mrjpacking.main:main',  
        ],
    },
)