from flask import Flask, render_template, request
from pipeline.prediction_pipeline import hybrid_recommendation

# Initialize the Flask application
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    """
    Home route for the web application.
    Handles GET requests to show the form and POST requests to process the input user ID
    and return personalized anime recommendations using a hybrid recommendation pipeline.
    """
    recommendations = None  # Placeholder for anime recommendation results
    error_message = None  # Placeholder for error messages

    if request.method == "POST":
        try:
            # Try to convert user input to integer
            user_id = int(request.form["userID"])

            # Generate recommendations using the hybrid recommendation system
            recommendations = hybrid_recommendation(user_id)

        except ValueError:
            # Handle case when user input is not a valid integer
            error_message = "❌ Please enter a valid numeric User ID."

        except Exception as e:
            # Catch any unexpected errors and log them
            print("❌ Error occurred while generating recommendations:", e)
            error_message = "⚠️ Something went wrong while processing your request."

    # Render the index.html page with the results or error
    return render_template(
        "index.html", recommendations=recommendations, error=error_message
    )


# Main entry point of the application
if __name__ == "__main__":
    # Start the Flask development server on all interfaces, port 5000
    app.run(debug=True, host="0.0.0.0", port=5000)
