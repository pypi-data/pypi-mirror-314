from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='burpy',
      version='0.1',
      description='Burp HTTP history parser',
      long_description=readme(),
      keywords='Burp Suite HTTP history parse',
      url='http://github.com/MatJosephs/burpy',
      author='Matei Josephs',
      author_email='majosephs@protonmail.com',
      license='MIT',
      packages=['burpy'],
      install_requires=['requests',
                        'bs4', 'pandas'],
      entry_points = {
            'console_scripts': ['burpy=burpy.command_line:main']},
      zip_safe=False)