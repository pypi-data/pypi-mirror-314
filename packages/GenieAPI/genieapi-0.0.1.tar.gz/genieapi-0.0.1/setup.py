from setuptools import setup, find_packages

setup(
    name='GenieAPI',
    version='0.0.1',
    description='Genie Music API',
    author='Pma10',
    author_email='pmavmak10@gmail.com',
    url='https://github.com/Pma10/GenieAPI',
    install_requires=["requests"],
    packages=find_packages(exclude=[]),
    keywords=['genie', 'korea', 'lyrics', 'api', 'music'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
)