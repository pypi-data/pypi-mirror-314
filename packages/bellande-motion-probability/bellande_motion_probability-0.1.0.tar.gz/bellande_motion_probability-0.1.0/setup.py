from setuptools import setup, find_packages

with open("./README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bellande_motion_probability",
    version="0.1.0",
    description="The Bellande Motion Probability algorithm calculates particle movement probabilities using Bellande distributions for enhanced motion estimation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="RonaldsonBellande",
    author_email="ronaldsonbellande@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "numpy",
    ],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
    ],
    keywords=["package", "setuptools"],
    python_requires=">=3.0",
    extras_require={
        "dev": ["pytest", "pytest-cov[all]", "mypy", "black"],
    },
    entry_points={
        'console_scripts': [
            'bellande_motion_probability_api = bellande_motion_probability.bellande_motion_probability_api:main'
        ],
    },
    project_urls={
        "Home": "https://github.com/Robotics-Sensors/bellande_motion_probability",
        "Homepage": "https://github.com/Robotics-Sensors/bellande_motion_probability",
        "documentation": "https://github.com/Robotics-Sensors/bellande_motion_probability",
        "repository": "https://github.com/Robotics-Sensors/bellande_motion_probability",
    },
)
