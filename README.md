# YouTube Video Search Dashboard

This project provides a robust dashboard for searching YouTube videos based on user queries. It utilizes the YouTube API to fetch video data and presents it in a user-friendly interface.

## Features

- **Search Videos:** Users can search for videos using keywords.
- **Display Top Results:** Shows the top videos based on the search query.
- **Background Task:** Starts a background task for asynchronous operations.

## Prerequisites

Before running the project, ensure you have the following:

- Python 3 installed
- Required Python packages installed (`flask`, `google-api-python-client`, `pandas`, `seaborn`, `matplotlib`)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repo.git
    ```

2. Navigate to the project directory:

    ```bash
    youtubesearch
    ```

3. Install the necessary dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Set your YouTube API key in the `new1.py` file:

    ```python
    api_key = 'AIzaSyAg_dqXlgYhCRbvbEVY7jjV8qyJbJl6mOM'
    ```

2. Run the Flask application:

    ```bash
    python new1.py
    ```

3. Access the dashboard in your browser at `http://localhost:5000`.

## File Structure

- `new1.py`: Flask application containing API handling and routing logic.
- `templates/dashboard.html`: HTML template for the dashboard interface.
- `static/style.css`: CSS file for styling the dashboard.
- `static/script.js`: JavaScript file for client-side functionality.

## Contributors

- List of contributors or maintainers involved in the project.

## License

This project is licensed under the [MIT License](LICENSE).
