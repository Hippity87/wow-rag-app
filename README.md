# ⚔️ Azeroth Archives - WoW Classic RAG Bot

Azeroth Archives is an AI-powered chatbot designed to assist World of Warcraft Classic players. It utilizes **Retrieval-Augmented Generation (RAG)** to provide accurate answers about quests, items, and community opinions based on custom datasets.

The bot is hosted on Azure and uses OpenAI's GPT-4o model to synthesize answers from indexed CSV data.

🔗 **Live Demo:** [https://wow.projectlexagon.fi](https://wow.projectlexagon.fi)

## 🏗 Architecture & Tech Stack

* **Frontend:** HTML5, CSS3, JavaScript (Clean & Responsive UI)
* **Backend:** Python FastAPI (Async REST API)
* **AI & Logic:**
    * **LLM:** Azure OpenAI (GPT-4o)
    * **Embeddings:** text-embedding-3-large
    * **Vector DB:** Azure AI Search (Vector Search)
* **Infrastructure:**
    * **Hosting:** Azure Web App (Linux B1 Plan)
    * **CI/CD:** GitHub Actions
    * **DNS:** Cloudflare

## 🚀 Key Features

* **RAG Pipeline:** Converts user queries into vectors, searches a custom index, and generates context-aware answers.
* **Rate Limiting:** Protects the API from spam (limit: 5 requests/min per IP).
* **Content Safety:** Custom Azure Content Filters configured to allow gaming context (e.g., "kill quest") while blocking harmful content.
* **Source Attribution:** The bot cites whether information comes from Quest Logs (Lore) or Community Comments (Opinions).

## 📂 Data Sources & Acknowledgments

This project is built using open datasets sourced from Kaggle. Huge thanks to the dataset creators for structuring this data.

1.  **World of Warcraft Quests** by Kacper Rawicki  
    [https://www.kaggle.com/datasets/kacperrawicki1/world-of-warcraft-quests](https://www.kaggle.com/datasets/kacperrawicki1/world-of-warcraft-quests)
    *Used for: Quest objectives, descriptions, and rewards.*

2.  **World of Warcraft Classic Quest Items Dataset** by Ammaruddin Qureshi  
    [https://www.kaggle.com/datasets/ammaruddinqureshi/world-of-warcraft-classic-quest-items-dataset](https://www.kaggle.com/datasets/ammaruddinqureshi/world-of-warcraft-classic-quest-items-dataset)
    *Used for: Item drop locations and drop rates.*

3.  **World of Warcraft YouTube Comments (2018-2025)** by Jesterhead  
    [https://www.kaggle.com/datasets/jesterhead/wow-classic-gamer-jargon-and-terms-dataset](https://www.kaggle.com/datasets/jesterhead/wow-classic-gamer-jargon-and-terms-dataset)
    *Used for: Simulating community discussions and extracting player sentiment/strategies.*

*Disclaimer: World of Warcraft is a registered trademark of Blizzard Entertainment. This project is a non-commercial educational demo.*

## 🛠 Local Development

1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/wow-rag-app.git](https://github.com/YOUR_USERNAME/wow-rag-app.git)
    cd wow-rag-app
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables:**
    Create a `.env` file and add your Azure keys:
    ```
    AZURE_OPENAI_KEY=your_key
    AZURE_OPENAI_SERVICE=your_service_name
    AZURE_SEARCH_ENDPOINT=your_endpoint
    ...
    ```

5.  **Run the App:**
    ```bash
    uvicorn app:app --reload
    ```