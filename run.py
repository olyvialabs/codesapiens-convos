from app import app
import dotenv


if __name__ == "__main__":
    # Load .env variables
    dotenv.load_dotenv()

    app.run(debug=True, port=7091)
