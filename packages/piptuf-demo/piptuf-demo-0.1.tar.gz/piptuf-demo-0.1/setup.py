from setuptools import setup

# Read the signature
with open("piptuf_demo/package_name.sig", "rb") as sig_file:
    package_signature = sig_file.read().hex()

setup(
    name="piptuf-demo",
    version="0.1",
    description=f"Demo project with a signed package name.",
    author="LV",
    author_email="lv@example.com",
    packages=["piptuf_demo"],
    include_package_data=True,
    package_data={
        "piptuf_demo": [],
    },
    long_description=f"This package includes a TUF signature for verification.",
    long_description_content_type="text/plain",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
