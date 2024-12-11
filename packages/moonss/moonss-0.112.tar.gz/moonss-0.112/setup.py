import setuptools

setuptools.setup(
    name='moonss',
    version='0.112',
    author="Thanh Hoa",
    author_email="thanhhoakhmt1@gmail.com",
    description="A Des of moonss",
    long_description="Des",
    long_description_content_type="text/markdown",
    url="https://github.com/vtandroid/dokr",
    packages=setuptools.find_packages(),
    py_modules=['moonss','DownloadHelper','SourceDataHelper'],
    install_requires=[
        'requests==2.25.1', 'moviepy==1.0.3', 'Pillow==9.5.0', 'coolbg', 'gbak', 'yt_dlp'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )