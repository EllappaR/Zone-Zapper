# ZONE ZAPPER: Anticipatory No-Parking Vehicle Owner Identification System

ZONE ZAPPER is an innovative system developed using machine learning algorithms such as YOLOv8 and Tesseract OCR recognition. This system identifies vehicles parked in no-parking zones, recognizes their license plates, and sends alert notifications to the respective vehicle owners.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features
- **Vehicle Detection**: Identifies vehicles parked in no-parking zones using YOLOv8.
- **License Plate Recognition**: Extracts and recognizes license plate numbers using Tesseract OCR.
- **Owner Identification**: Matches license plates with vehicle owner information from the database.
- **Alert Notifications**: Sends alert notifications to vehicle owners regarding no-parking violations.
- **Real-time Processing**: Performs detection and recognition in real-time for immediate alerts.

## Installation
To set up the ZONE ZAPPER system locally, follow these steps:

### Prerequisites
- Python 3.7 or later: [Install Python](https://www.python.org/downloads/)
- Virtual Environment: Recommended for managing dependencies

### Steps
1. Clone the repository
   ```sh
   git clone https://github.com/your-username/zone-zapper.git
   ```
2. Navigate to the project directory
   ```sh
   cd zone-zapper
   ```
3. Create and activate a virtual environment
   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```
4. Install required dependencies
   ```sh
   pip install -r requirements.txt
   ```
5. Download YOLOv8 weights and place them in the designated directory
6. Configure database and notification settings as per your setup

## Usage
1. **Start the System**: Run the main script to start the vehicle detection and owner identification system.
   ```sh
   python main.py
   ```
2. **Monitor No-Parking Zones**: The system will monitor designated no-parking zones using connected cameras.
3. **Receive Notifications**: Vehicle owners will receive alert notifications if their vehicle is detected in a no-parking zone.

## Technologies Used
- **YOLOv8**: Object detection algorithm for identifying vehicles
- **Tesseract OCR**: Optical character recognition for license plate recognition
- **OpenCV**: Image processing library
- **Python**: Programming language for implementation
- **SQLite / MySQL**: Database for storing vehicle owner information
- **Twilio / SMTP**: Services for sending notifications

## Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
Your Name - [consoleyash@gmail.com]

Project Link: [https://github.com/EllappaR/zone-zapper]

---

Thank you for using ZONE ZAPPER! We hope this system helps in maintaining proper parking regulations and assists in efficient traffic management. If you have any feedback or suggestions, please feel free to reach out.
