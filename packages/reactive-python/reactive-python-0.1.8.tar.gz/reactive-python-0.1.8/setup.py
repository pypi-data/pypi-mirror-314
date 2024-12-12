from setuptools import setup

setup(
    name='reactive-python',  # package name
    version="0.1.8",  # package version
    description='A simple reactive programming library',  # package description
    packages=['reactive', 
              'reactive.observable',
              'reactive.observer'],
    # package_dir={"": "src"},
    zip_safe=False,
    author="yunfan, jiahao",
    author_email="bi1lqy.y@gmail.com",
    license="MIT",
    install_requires=[]
)
