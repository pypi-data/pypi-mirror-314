import platform
import sys
from setuptools import setup, find_packages

def get_platform_dependencies():
    """Get platform-specific dependencies"""
    system = platform.system().lower()
    if system == 'windows':
        return [
            'comtypes>=1.2.0',
            'pywin32>=305'
        ]
    elif system == 'linux':
        return [
            'python-xlib>=0.31',
            'pyatspi>=2.38.1'
        ]
    elif system == 'darwin':
        return [
            'pyobjc-framework-Cocoa>=9.0',
            'pyobjc-framework-Quartz>=9.0'
        ]
    return []

def get_install_requires():
    """Get all required packages"""
    requirements = [
        'numpy>=1.24.0',
        'opencv-python>=4.7.0',
        'Pillow>=9.5.0',
        'paddlepaddle>=2.5.1',
        'paddleocr>=2.7.0',
        'psutil>=5.9.0',
        'matplotlib>=3.7.1',
        'colour>=0.1.5',
        'torch>=1.7.0',
        'torchvision>=0.8.0'
    ]
    
    # Add platform-specific dependencies
    requirements.extend(get_platform_dependencies())
    
    return requirements

setup(
    name="pyui_automation",
    version="0.1.0",
    packages=find_packages(exclude=["tests*", "docs*"]),
    install_requires=get_install_requires(),
    python_requires='>=3.8',
    
    # Metadata
    author="Ravil Shakerov",
    author_email="your.email@example.com",
    description="A powerful, cross-platform Python library for desktop UI testing and automation",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DaymaNKinG990/pyui_automation",
    project_urls={
        "Bug Tracker": "https://github.com/DaymaNKinG990/pyui_automation/issues",
        "Documentation": "https://github.com/DaymaNKinG990/pyui_automation#readme",
        "Source Code": "https://github.com/DaymaNKinG990/pyui_automation",
    },
    
    # Classifiers help users find your project
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
    ],
    
    # Keywords for PyPI
    keywords=[
        "ui automation",
        "testing",
        "gui testing",
        "automation",
        "accessibility testing",
        "visual testing",
        "performance testing",
        "ocr",
        "cross-platform"
    ],
    
    # Additional data files
    package_data={
        "pyui_automation": ["py.typed", "*.pyi", "**/*.pyi"],
    },
    
    # Entry points for command-line scripts
    entry_points={
        "console_scripts": [
            "pyui-automation=pyui_automation.cli:main",
        ],
    },
)
