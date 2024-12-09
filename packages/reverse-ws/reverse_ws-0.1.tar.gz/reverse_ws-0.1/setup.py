from setuptools import setup, find_packages
from setuptools.command.install import install
import os

class PostInstallCommand(install):
    """Custom installation script to run post-installation hooks."""
    def run(self):
        install.run(self)  # Exécute l'installation normale
        # Exécute le script post-installation
        os.system("python post_install.py")

setup(
    name="",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "websockets",  # Dépendance WebSocket
    ],
    cmdclass={
        'install': PostInstallCommand,  # Définir le hook d'installation personnalisé
    },
)
