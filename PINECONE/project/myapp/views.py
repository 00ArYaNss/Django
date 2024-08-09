from pinecone import Pinecone
import openai
from django.http import JsonResponse
from django.views import View

# Set the API keys and other configurations
PINECONE_API_KEY = ""
OPENAI_API_KEY = ""
INDEX_NAME = "index123"
DIMENSION = 1536

# Text to be processed
text = """
My name is Aryan Sahu. I am currently living in Bhopal, MP. 
I am pursuing BTech CSE from Amity University in Gwalior, MP.
I have completed my second year. My age is 20 years old. I am currently working as an intern at triosoft technologies.
My job post is AI engineer. Your creator is triosoft.
"""

# Initialize Pinecone using the Pinecone class
pc = Pinecone(api_key=PINECONE_API_KEY)
openai.api_key = OPENAI_API_KEY

class PineconeHandler(View):
    def get(self, request, *args, **kwargs):
        # Access the existing Pinecone index
        index = pc.Index(INDEX_NAME)

        # Split text into chunks
        sentences = text.split('. ')
        embeddings = []

        # Generate embeddings for each chunk
        for sentence in sentences:
            response = openai.Embedding.create(input=sentence, model="text-embedding-ada-002")
            embeddings.append((sentence, response['data'][0]['embedding']))

        # Store embeddings in Pinecone
        vectors = [(str(i), embedding, {}) for i, (sentence, embedding) in enumerate(embeddings)]
        index.upsert(vectors=vectors)  # Store the vectors in the existing index

        print("Text chunks have been stored in Pinecone.")

        # Function to query the model
        def query_model(query):
            # Generate embedding for the query
            query_response = openai.Embedding.create(input=query, model="text-embedding-ada-002")
            query_embedding = query_response['data'][0]['embedding']

            # Query Pinecone to get the closest match
            query_results = index.query(vector=query_embedding, top_k=1, include_metadata=True)

            if query_results['matches']:
                top_match = query_results['matches'][0]
                relevant_sentence = sentences[int(top_match['id'])]

                # Use GPT-4 to generate the final answer based on the relevant chunk
                gpt_response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": 'Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text below, say that you are unable to answer the question based on the information provided.'},
                        {"role": "user", "content": f"Context: {text}\n\nQuestion: {query}"}
                    ],
                    max_tokens=150,
                    temperature=0.5
                )
                return gpt_response.choices[0].message['content'].strip()
            else:
                return "I don't have information."

        # Define your question here
        query = "What technology is used to build you?"

        # Get the answer for the defined question
        answer = query_model(query)

        print(f"Question: {query}")
        print(f"Answer: {answer}")

        return JsonResponse({"question": query, "answer": answer})

