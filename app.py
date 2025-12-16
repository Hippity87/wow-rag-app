import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

# Alustetaan FastAPI
app = FastAPI(
    title="WoW Classic RAG API",
    description="API for querying World of Warcraft Classic knowledge base.",
    version="1.0.0"
)

# Template-moottori HTML-sivua varten
templates = Jinja2Templates(directory="templates")

# --- KONFIGURAATIO (Ympäristömuuttujat) ---
AZURE_OPENAI_SERVICE = os.environ.get("AZURE_OPENAI_SERVICE")
AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")
AZURE_OPENAI_CHATGPT_DEPLOYMENT = os.environ.get("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "gpt-4o")
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-large")

AZURE_SEARCH_ENDPOINT = os.environ.get("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.environ.get("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX", "wow-classic-index")

# --- ASIAKKAIDEN ALUSTUS ---
openai_client = AzureOpenAI(
    azure_endpoint=f"https://{AZURE_OPENAI_SERVICE}.openai.azure.com",
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-02-01"
)

search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(AZURE_SEARCH_KEY)
)

# Pydantic-malli syötteelle (API-dokumentaatiota varten)
class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Palauttaa käyttöliittymän (UI)"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    RAG-endpoint: Ottaa kysymyksen, hakee tiedon Azuresta ja vastaa GPT:llä.
    """
    user_message = request.message
    
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        # 1. Luodaan vektorit (Embedding)
        embedding_response = openai_client.embeddings.create(
            model=AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
            input=user_message
        )
        query_vector = embedding_response.data[0].embedding

        # 2. Haku Azure AI Searchista
        vector_query = VectorizedQuery(vector=query_vector, k_nearest_neighbors=3, fields="vector")
        
        # Huom: select-kentät kannattaa tarkistaa indeksistä, jos nimet ovat muuttuneet
        results = search_client.search(
            search_text=user_message,
            vector_queries=[vector_query],
            select=["title", "chunk", "content", "data"], 
            top=5
        )

        # 3. Kontekstin rakentaminen
        context = ""
        for result in results:
            # Yritetään löytää oikea kenttä sisällölle (riippuu import wizardista)
            content = result.get("chunk") or result.get("content") or result.get("data") or ""
            source = result.get("title") or "Unknown Source"
            context += f"\n--- Source: {source} ---\n{content}\n"

        if not context:
            context = "No specific documents found. Answer based on general knowledge but mention that database was silent."

        # 4. GPT vastaus
        system_prompt = f"""
        You are a World of Warcraft Classic expert assistant.
        Use the retrieved context to answer the player's question.
        
        Context data:
        {context}
        
        Guidelines:
        - If the answer is in the context, use it.
        - If the info comes from 'wow_comments', mention it is community opinion.
        - If the info comes from 'wow_quest_items', mention drop locations or requirements.
        - Keep the tone helpful and slightly RPG-themed (e.g., 'Greetings hero').
        """

        completion = openai_client.chat.completions.create(
            model=AZURE_OPENAI_CHATGPT_DEPLOYMENT,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        response_text = completion.choices[0].message.content
        return {"response": response_text}

    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Paikallista testausta varten
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)