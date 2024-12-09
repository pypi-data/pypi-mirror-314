from setuptools import setup, find_packages

setup(
    name='escanervuln',
    version='1.0.2',
    description='Librería Modular de Detección de Vulnerabilidades en Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ignacio',
    author_email='knjasu098@gmail.com',
    url='https://github.com/tuusuario/vulnscanner',  # Reemplázalo con tu repo
    packages=find_packages(),
    install_requires=[
        'flask',   # Dependencias necesarias
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'vulnscanner=vulnscanner.cli:main'  # Crear comando 'vulnscanner' en la CLI
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
