from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name='PySide6-PahoMqtt',
    version='0.1.0',
    description='This is a wrapping class for using paho-mqtt(V2.x) in pyside6.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='chanmin.park',
    author_email='devcamp@gmail.com',
    packages=find_packages(exclude=[]),
    package_dir={'PySide6-PahoMqtt': 'src'},
    install_requires=[
        'paho-mqtt',
        'PySide6'
    ],
    keywords=['PySide6', 'paho-mqtt'],
    python_requires='>=3.8',
    zip_safe=False,
    data_files=[
        ('Lib/site-packages/PySide6', ['src/PahoMqtt.py'])
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]    
)