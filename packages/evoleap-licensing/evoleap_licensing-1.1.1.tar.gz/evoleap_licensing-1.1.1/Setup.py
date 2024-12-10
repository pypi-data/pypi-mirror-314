import setuptools
import sys
# noinspection SpellCheckingInspection
with open("README.md", "r") as fh:
    long_description = fh.read()
major, minor, micro = sys.version_info[:3]
ir = ['pycryptodome', 'pytz']
if minor == 6:
    ir.append('dataclasses')

setuptools.setup(
    name="evoleap_licensing",
    version="1.1.1",
    author="evoleap",
    author_email="info@evoleap.com",
    packages=setuptools.find_packages(),
    url="https://github.com/evoleap/evoleap.licensing-python",
    license='https://evoleap.com/elm_client_api_net_eula.html',
    description='Software licensing client API for elm, a cloud-based, enterprise grade software licensing platform.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=True,
    install_requires=ir,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
)
