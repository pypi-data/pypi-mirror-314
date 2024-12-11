from setuptools import setup, find_packages
setup(
    name="kivy_file_manager_package",
    version="0.5",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "kivy",
    ],
    entry_points={
        'console_scripts': [
            'kivy_file_manager = kivy_file_manager.__main__:main'
        ]
    },
    package_data={
        '': ['kivy_file_manager_package/*'],
    },
)
