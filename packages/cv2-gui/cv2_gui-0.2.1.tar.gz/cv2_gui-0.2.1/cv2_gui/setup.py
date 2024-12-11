from setuptools import setup, find_packages

setup(
    name="cv2_gui",
    version="0.1.1",
    description="A library to create buttons using OpenCV (cv2)",
    author="Tarun Shenoy",
    author_email="tgshenoy1@gmail.com",
    url="https://github.com/Crystalazer/cv2_gui", 
    packages=find_packages(),
    install_requires=["opencv-contrib-python","numpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="Proprietary",
    python_requires=">=3.6",
)
