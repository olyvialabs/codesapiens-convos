from app import app
import dotenv


if __name__ == "__main__":
    # Load .env variables
    dotenv.load_dotenv()

    app.run()
    # debug=False, port=7091)
