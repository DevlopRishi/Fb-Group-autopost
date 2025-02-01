

# Fb-Group-autopost
Ever wanted to post in bulk in facebook groups... This will help to do it automatically

## Overview
The Facebook Group Poster is a GUI application designed to automate the process of posting content to multiple Facebook groups. It uses Selenium for web automation and Tkinter for the graphical user interface.

## Features
- **User-friendly GUI**: Easily input your Facebook credentials, group URLs, content, and optional images.
- **Headless Mode**: Option to run the browser in headless mode for background operation.
- **Proxy Support**: Use a proxy to mask your IP address.
- **Logging**: View and save logs of the posting process.

## Requirements
- Python 3.x
- Tkinter
- Selenium
- ChromeDriver (compatible with your Chrome browser version)

## Installation
1. **Clone the repository**:
    ```bash
    git clone https://github.com/Fb-Group-autopost
    cd Fb-Group-autopost
    ```

2. **Install the required Python packages**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Download ChromeDriver**:
    - Download the ChromeDriver from here.
    - Ensure the ChromeDriver executable is in your system's PATH or place it in the project directory.

## Usage
1. **Run the application**:
    ```bash
    python facebook_group_poster.py
    ```

2. **Fill in the required fields**:
    - **Email**: Your Facebook email.
    - **Password**: Your Facebook password.
    - **Group URLs File**: A text file containing the URLs of the Facebook groups (one URL per line).
    - **Content File**: A text file containing the content to be posted.
    - **Optional Image File**: An image file to be included in the post (optional).
    - **Headless Mode**: Check this box to run the browser in headless mode.
    - **Proxy**: Enter the proxy in the format `ip:port` (optional).


3. **Start Posting**:
    - Click the "Start Posting" button to begin the automated posting process.
    - View the log messages in the log display area.
    - Save the log to a file if needed.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.