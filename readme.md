To run the application on localhost, follow these steps: 
1. Clone the git repository and then go to the git location.
2. Run pip install -r requirements.txt
3. Install MoongoDB from https://www.mongodb.com/try/download/community and make sure the mongodb server is running on localhost:27017
4. Run uvicorn main:app --reload
5. Get your Gemini API Key from https://ai.google.dev/gemini-api/docs/api-key and enter in the terminal when prompted.
6. Go to 127.0.0.1:8000/docs to perform the requests.
