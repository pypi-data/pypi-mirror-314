from setuptools import setup, find_packages

setup(
    name="My-QR-COOLBOOY",
    version="1.1.0",
    author="coolbooy",
    author_email="coolbooy@gmail.com",
    description="A QR Code generator with customizable features",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=["My_QR_COOLBOOY"],
    install_requires=[
        "qrcode",
        "Pillow",
    ],
    entry_points={
        "console_scripts": [
            "My-QR-COOLBOOY=My_QR_COOLBOOY.main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",
    license="MIT",
)
