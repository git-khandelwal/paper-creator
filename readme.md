This application is used to create a sample paper API using FastAPI, with the following requests:

1. GET /: Returns the JSON string "Welcome to PDF Extractor"
2. GET /papers/{paper_id}: To get the paper using paper_id either from Redis cache or directly from database.
3. POST /papers: Creates a paper using the provided data and returns a paper_id.
4. PUT /papers/{paper_id}: To edit the contents of paper, either fully or partially, provided the structure is valid.
5. DELETE /papers/{paper_id}: To delete the paper_id from MongoDB database.
6. POST /extract/pdf: To extract the contents of a test paper and then return the data in the pre-defined structure using LangChain for prompt engineering and Gemini as the LLM for prompting.

To run the application on localhost, follow these steps:
1. Clone the git repository and then go to the git location.
2. Run pip install -r requirements.txt
3. Install MongoDB from https://www.mongodb.com/try/download/community and make sure the mongodb server is running on default port.
4. Install Redis from https://github.com/microsoftarchive/redis/releases and make sure the redis server is running on default port.
5. Run uvicorn main:app --reload
6. Get your Gemini API Key from https://ai.google.dev/gemini-api/docs/api-key and enter in the terminal when prompted.
7. Go to 127.0.0.1:8000/docs to perform the requests.
