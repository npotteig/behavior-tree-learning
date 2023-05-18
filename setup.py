## ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD

# from distutils.core import setup
from setuptools import setup, find_packages
# from catkin_pkg.python_setup import generate_distutils_setup

# setup_args = generate_distutils_setup(
#         packages=["behavior_tree_learning"],
#         package_dir={"": "src"})

setup(name="behavior_tree_learning",
      version='1.0',
      package_dir={"": "src"},
      packages=find_packages())

# setup(**setup_args)
