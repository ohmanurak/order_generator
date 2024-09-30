# Chachacha order generator
A brief description of your project and its functionality.

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)

## Table of Contents
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Troubleshoot](#troubleshoot)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation
Clone the repo and install the tools
```bash
git clone https://github.com/natchapol2347/order_generator/
pip install virtualenv
pip install pyinstaller
```
## Setup
1. create a virtual environment for project dependencies(requirements.txt) so that pyinstaller can to include it to path
```bash
mkdir 3chaGenerator
cd 3chaGenerator
virtualenv venv 
source venv/bin/activate 
pip install -r requirements.txt
```
2. Use pyinstaller to create an exe with the already built main.spec
 ```bash
 pyinstaller main.spec
 ```
## Usage
1. Once setup, there should be a folder called dist in the project. Navigate to /dist/main/main.exe and run it
2. If exe runs successfully, there will be a generated folder named Week_N containing the order stickers for packaging.

## Troubleshoot
If there's a change in configuration to how you want the pyinstaller to generate the exe OR the .spec file is lost; here's how you can generate it 
```bash
pyinstaller.exe --onefile --paths 3chaGenerator/lib/python3.12/site-packages --add-data "./fonts;fonts" --add-data "./misc;misc" main.py
or
path\to\pyinstaller.exe --onefile --paths path\to\venv\Lib\site-packages --add-data "./resources/folders;folder_name_in_dist" file.py
```
### If there's an unknown bug in the code and you want details on what it is: change the log level to DEBUG
Change from 
```python
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d')
```
to
```python
ogging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d')
```
in main.py 

## Features
### Only features right now is for images and pdf creation

## Contributing
1. Fork the project
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License

This project is currently a private repo.
