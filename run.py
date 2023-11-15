from app import app
import dotenv


if __name__ == "__main__":
    # Load .env variables
    dotenv.load_dotenv()

    app.run(debug=True)
    # debug=False, port=7091) 5w7LkPh6uU5mpj4t
