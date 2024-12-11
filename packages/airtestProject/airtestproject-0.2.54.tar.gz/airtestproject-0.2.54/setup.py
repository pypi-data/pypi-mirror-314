from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name='airtestProject',
    version='0.2.54',
    packages=find_packages(include=['airtestProject', 'airtestProject.*']),
    include_package_data=True,
    package_data={
        'android_deps': ["*.apk", "airtestProject/airtest/core/android/static"],
        'html_statics': ["airtestProject/airtest/report"],
        'ios_deps': ["airtestProject/airtest/core/ios/iproxy"],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "openpyxl==3.1.4",
        "qrcode==7.4.2",
        "watchdog==4.0.0",
        "easyocr==1.7.1",
        "paddleocr==2.7.3",
        "loguru==0.5.3",
        "paddlepaddle==2.6.1",
        "numpy==1.22.4",
        "torch==2.3.0",
        "hrpc>=1.0.9",
        "websocket-client==0.48.0",
        "ffmpeg==1.4",
        "xlwt==1.3.0",
        "logzero==1.7.0",
        "tidevice==0.12.9",
        "pyautogui",
        "pynput",
        "pywin32",
        "six"
        # 项目依赖项列表
    ],
    python_requires='>=3.9',
    author="mortal_sjh",                                     # 作者
    author_email="mortal_sjh@qq.com"
)
