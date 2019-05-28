from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='slecommon',
    version='0.0.1',
    author='VisionSpace Technologies GmbH',
    author_email="oss@visionspace.com",
    description='Python Space Link Extension Common Library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="www.visionspace.com",
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Framework :: Twisted"
    ],
    python_requires='>=3',
    keywords='sle common',
    packages=find_packages(exclude=['build', '*.build', 'build.*', '*.build.*',
                                    'dist', '*.dist', 'dist.*', '*.dist.*',
                                    'examples', '*.examples', 'examples.*', '*.examples.*',
                                    'tests', '*.tests', 'tests.*', '*.tests.*']),
    install_requires=['pyasn1', 'bitstring'],
)
