from setuptools import setup, find_packages

setup(
    name='yelp-batchaaaaa',  # Nombre del paquete
    version='0.27.1',   # Versión
    description='Descripción de tu paquete',
    author='Tu nombre o tu empresa',
    author_email='poc@asd.com',
    packages=find_packages(),  # Encuentra todos los paquetes automáticamente
    install_requires=[         # Aquí puedes añadir las dependencias si las tienes
        # Por ejemplo: 'requests>=2.0.0',
    ],
    license='MIT',  # Puedes cambiar esto si usas otra licencia
)
