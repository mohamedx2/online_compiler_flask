# Online Compiler Flask

A web-based compiler that allows users to write and execute code directly in the browser. This project is built with Flask and provides a simple interface for code compilation and execution.

## Live Demo
Visit the live application at: [https://online-compiler-flask.onrender.com/](https://online-compiler-flask.onrender.com/)

## Features
- Web-based code editor
- Support for basic programming operations
- Real-time code compilation and execution
- Simple and intuitive user interface

## Technology Stack
- Python 3.x
- Flask (Web Framework)
- Flask-CORS (Cross-Origin Resource Sharing)
- HTML/CSS/JavaScript (Frontend)

## Prerequisites
- Python 3.x
- pip (Python package manager)
- A C compiler (for code execution)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mohamedx2/online_compiler_flask.git
cd online_compiler_flask
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Deployment
The application is currently deployed on Render. For deployment on your own server:

1. Ensure all requirements are installed
2. Set the `PORT` environment variable if needed
3. The application will automatically use the PORT environment variable or default to 5000

## Contributing
Feel free to fork the repository and submit pull requests for any improvements.

## License
This project is open source and available under the MIT License.
