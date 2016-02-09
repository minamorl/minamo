from setuptools import setup, find_packages

setup(
    name="minamo",
    description="",
    author="minamorl",
    author_email="minamorl@minamorl.com",
    version="0.0.1",
    entry_points={
        'console_scripts': ['minamo = minamo.__main__:main']
    },
    packages=find_packages(),
    tests_require=['tox'],
    install_requires=[
        "redis-orm",
        "requests",
        "beautifulsoup4",
    ]
)
