Processes

1. An admin will input a link and set the number of recursive calls for anchor tags on a webstie to scrape.  The backend will extract the text from the anchor tags and input them into a csv document. The server will then make a series of embeddings that it will then store on pinecone API. Then, the embeddings will be used to give the llm some insights on the data it is mostly working with.


2. A user will talk with the AI chatbot, and it will input questions into a frontend. On the backend, the server will use a post request to take the prompt the user inputed. It will also use the embeddings to give the AI model an insight on what the model is supposted to be working with. Then, the backend will make a stream of the chatbot talking and loading chucks to the user. The post request will generate a response to the user.