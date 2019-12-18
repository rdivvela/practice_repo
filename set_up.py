from setuptools import setup, find_packages

setup(
    name="map_plot",
    version="0.1.1",
    packages=find_packages(
        exclude=[
            "data/",
            "query_templates/",
            "scripts/",
        ]
    ),
    author="Ravi Divvela",
    install_requires=[
        "scikit-learn",
        "numpy",
        "click"
    ],
    entry_points = {
        "console_scripts": \
        ["map_plot=map_practice.bokeh_mapping:map_plot"]
    }
)
