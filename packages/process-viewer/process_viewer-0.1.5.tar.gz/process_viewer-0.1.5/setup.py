from setuptools import setup, find_packages

setup(
    name="process-viewer",
    version="0.1.5",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "psutil>=6.1.0",
        "curses-menu>=0.7.0",
        "twine>=6.0.1",
        "wheel>=0.45.1",
        "build>=1.2.2.post1",
    ],
    entry_points={
        'console_scripts': [
            'process-viewer=process_viewer.main:run',
        ],
    },
    python_requires=">=3.11",
)
