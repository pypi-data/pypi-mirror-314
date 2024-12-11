from setuptools import setup
from setuptools.command.install import install


class CustomInstallCommand(install):
    def initialize_options(self):
        install.initialize_options(self)

    def finalize_options(self):
        install.finalize_options(self)

    def run(self):
        install.run(self)


setup(cmdclass={'install': CustomInstallCommand})
