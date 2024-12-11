from setuptools import setup, find_packages

setup(
    name='min-db',
    version='0.0.16',
    description='mybatis like minimum db utility',
    author='kyon',
    author_email='originky2@gmail.com',
    install_requires=['pydantic>=2.7', 'oracledb>=1.4.2', 'mysql-connector-python>=8.2.0',],
    packages=find_packages(exclude=[]),
    python_requires='>=3.10',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.11',
    ],
)

# python setup.py sdist bdist_wheel
# python -m twine upload dist/*