Processes

To get setup,

make a env file and paste in:***

"""
GROQ_API_KEY=Your API Key
PINECONE_API_KEY=Your API Key
"""

***You will have to make your own keys on the pinecone website and groq website too.

Create an index in pinecone and name it "ai-research-agent" with 384 Dimentions






1. An admin will input a link and set the number of recursive calls for anchor tags on a webstie to scrape.  The backend will extract the text from the anchor tags and input them into a csv document. The server will then make a series of embeddings that it will then store on pinecone API. Then, the embeddings will be used to give the llm some insights on the data it is mostly working with.


Directions:

    in the webscrape.py put in the number of sites you want to scrape into the calling of the "web_scrape_all" and the second argument must be how many recursive calls must be done There is still a bit of bugs here, so it will have to be fixed in future versions. run the webscrape.py

    run the store_pinecone.py file.







2. A user will talk with the AI chatbot, and it will input questions into a frontend. On the backend, the server will use a post request to take the prompt the user inputed. It will also use the embeddings to give the AI model an insight on what the model is supposted to be working with. Then, the backend will make a stream of the chatbot talking and loading chucks to the user. The post request will generate a response to the user.