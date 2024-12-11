from setuptools import setup, find_packages

with open('README.md', 'rb') as f:
    readme = f.read().decode('utf-8')


setup(
    name='autotasker',
    version='0.2.1',
    description='AutoTasker is a console application designed to simplify and automate repetitive tasks without the '
                'need for programming skills. With AutoTasker, you can easily set up a variety of automated tasks, '
                'saving you time and effort in your daily activities.',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='GPL-3.0',
    author='Mario Ramos',
    author_email='marioramos.cobisa@gmail.com',
    url='https://github.com/mramosg7/AutoTasker',
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.12',
    install_requires=[
        'Click',
        'InquirerPy',
    ],
    entry_points={
            'console_scripts': [
                'autotasker=autotasker:cli',
            ],
        },
)