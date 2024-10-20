This application is used to create a sample paper API using FastAPI, with the following requests:
GET /: Returns the JSON string "Welcome to PDF Extractor"
GET /papers/{paper_id}: To get the paper using paper_id.
POST /papers: Creates a paper using the provided data and returns a paper_id.
PUT /papers/{paper_id}: To edit the contents of paper, either fully or partially, provided the structure is valid.
DELETE /papers/{paper_id}: To delete the paper_id from MongoDB database.
POST /extract/pdf: To extract the contents of a test paper and then return the data in the pre-defined structure.

To run the application on localhost, follow these steps:
1. Clone the git repository and then go to the git location.
2. Run pip install -r requirements.txt
3. Install MongoDB from https://www.mongodb.com/try/download/community and make sure the mongodb server is running on default port.
4. Install Redis from https://github.com/microsoftarchive/redis/releases and make sure the redis server is running on default port.
5. Run uvicorn main:app --reload
6. Get your Gemini API Key from https://ai.google.dev/gemini-api/docs/api-key and enter in the terminal when prompted.
7. Go to 127.0.0.1:8000/docs to perform the requests.
