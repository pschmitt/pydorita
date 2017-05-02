from setuptools import find_packages, setup


setup(
    name='pydorita',
    version='0.1',
    license='GPL3',
    description='Python client for controlling a iRobot Roomba 980 '
                '(via rest980)',
    long_description=open('README.rst').read(),
    author='Philipp Schmitt',
    author_email='philipp@schmitt.co',
    url='https://github.com/pschmitt/pydorita',
    packages=find_packages(),
    install_requires=['requests', 'paho-mqtt']
)
