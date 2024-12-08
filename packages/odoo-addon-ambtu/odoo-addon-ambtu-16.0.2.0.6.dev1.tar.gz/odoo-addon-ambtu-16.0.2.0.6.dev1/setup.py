import setuptools

with open("odoo/addons/ambtu/README.md") as f:
    long_description = f.read()

setuptools.setup(
    setup_requires=['setuptools-odoo'],
    long_description=long_description,
    odoo_addon=True,
)
