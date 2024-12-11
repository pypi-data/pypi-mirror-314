![Organization Logo](https://raw.githubusercontent.com/getflytrap/.github/main/profile/flytrap_logo.png)

# Flytrap Flask SDK

The Flytrap Flask SDK is a lightweight tool designed for Flask applications. It enables seamless error monitoring and reporting to the Flytrap system, capturing both global and manually handled errors with minimal setup.

This guide will walk you through setting up the Flytrap Flask SDK in your project and exploring its features. If you want to use Flytrap in a production environment, refer to the [Flytrap Installation Guide](https://github.com/getflytrap/flytrap_terraform) for complete setup instructions.

To learn more about Flytrap, check out our [case study](https://getflytrap.github.io/).

## 🚀 Getting Started

To start using Flytrap in your project:

1. Visit the Flytrap Dashboard and log in.
2. Click on **New Project** to create a project.
3. You’ll be provided with a **Project ID**, **API Key**, and **API Endpoint** specific to your project. These values are essential for configuring the SDK.

## 📦 Installation

Install the Flytrap Flask SDK via pip:

```bash
pip install flytrap_flask
```

## 🛠️ Usage
1. **Initialize Flytrap:** In your main application file (e.g., app.py), import the Flytrap module and initialize it with your project credentials:

    ```python
    import flytrap

    flytrap.init({
        "project_id": "YOUR_PROJECT_ID",  # Replace with your Project ID
        "api_endpoint": "YOUR_ENDPOINT",  # Replace with your API Endpoint
        "api_key": "YOUR_API_KEY",        # Replace with your API Key
    })
    ```

2. **Automatically Capture Global Errors:** The Flytrap Flask SDK sets up a `sys.excepthook` to automatically log uncaught exceptions globally, even outside Flask request cycles. This ensures all unhandled errors are captured and sent to Flytrap without additional configuration.

3. **Set Up Flask Middleware:** Add the Flytrap error handler to your Flask app to automatically capture unhandled errors:

    ```python
    from flask import Flask
    import flytrap

    app = Flask(__name__)

    flytrap.setup_flask_error_handler(app)
    ```

    This middleware intercepts any unhandled errors in your Flask routes and logs them to Flytrap, along with request metadata (e.g., HTTP method and path).

4. **Manually Capturing Exceptions:** For exceptions caught in a try/except block, use the capture_exception method to log the error to Flytrap manually:

    ```python
    try:
        # Your code here
        raise Exception("Something went wrong!")
    except Exception as e:
        flytrap.capture_exception(e)
    ```

## 🛠️ Example App Setup

Here’s a complete example of using Flytrap in a Flask application:

```python
from flask import Flask
import flytrap

app = Flask(__name__)

# Initialize the Flytrap SDK
flytrap.init({
    "project_id": "YOUR_PROJECT_ID",  
    "api_endpoint": "YOUR_ENDPOINT",  
    "api_key": "YOUR_API_KEY"        
})

# Set up Flytrap middleware
flytrap.setup_flask_error_handler(app)

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/unhandled-error")
def unhandled_error():
    raise Exception("Unhandled error in route")

@app.route("/handled-error")
def handled_error():
    try:
        raise Exception("Handled error in route")
    except Exception as e:
        flytrap.capture_exception(e)
        return "Handled error logged", 400

if __name__ == "__main__":
    app.run(debug=True, port=3003)
```

## 🖥️ Local End-to-End Testing with Flytrap Architecture

For full **local** integration with the Flytrap architecture:

1. **Install the Flytrap API:** Follow the [Flytrap API Repository setup guide](https://github.com/getflytrap/flytrap_api).
2. **Install the Flytrap Processor:** Refer to the [Flytrap Processor Repository](https://github.com/getflytrap/flytrap_processor) for instructions.
3. **View Errors in the Dashboard:** Set up the [Flytrap Dashboard](https://github.com/getflytrap/flytrap_ui) to view and manage reported errors.
4. **Integrate the Flytrap SDK in your project.**

### Testing the Complete Setup
1. Trigger errors in your application integrated with a Flytrap SDK.
2. Confirm that errors are logged by checking:
  - Flytrap Processor Logs: Ensure errors are processed correctly.
  - Flytrap Dashboard: View processed errors, including stack traces and context.

## 🚀 Production Setup
If you’re looking for detailed instructions to deploy Flytrap in a production environment, refer to:

- [Flytrap Installation Guide](https://github.com/getflytrap/flytrap_terraform)
- [How-To-Use Page](https://getflytrap.github.io/)

For questions or issues, feel free to open an issue in this repository or contact the Flytrap team. 🚀

---

<div align="center">
  🪰🪤🪲🌱🚦🛠️🪴
</div>