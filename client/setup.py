
from setuptools import setup

setup(
        name = "gentoostats",
        version = "9999",
        author = "Vikraman Choudhury",
        author_email = "vikraman.choudhury@gmail.com",
        description = "Package statistics client",
        license = "GPLv3",
        url = "http://soc.dev.gentoo/org/gentoostats",
        packages = ['gentoostats'],
        scripts = ['gentoostats-send', 'gentoostats-cli']
        )
