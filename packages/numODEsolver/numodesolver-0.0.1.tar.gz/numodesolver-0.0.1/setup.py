from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.12',
    'Topic :: Scientific/Engineering',
]

setup(
    name= 'numODEsolver',
    version= '0.0.1',
    description= 'A numerical ODE solver written in Python',
    long_description= open('README.md').read() + '\n\n'+open('CHANGELOG.txt').read(),
    long_description_content_type= 'text/markdown',
    url='https://github.com/lukasnf',
    author='Lukas Filipon',
    author_email='lukasfilipon7@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='math,physics,ode,differential equations,numerical',
    packages= find_packages(),
    install_requires= ['numpy', 'scipy', 'matplotlib','sympy']
)
