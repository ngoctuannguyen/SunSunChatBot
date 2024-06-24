<h1 align="center" id="title">Sun Sun Chatbot - Question Answering System</h1>

<h2>Project Description</h2>

<p id="description">This project is for
AI R&amp;D Challenge for Sun* Summer Internship</p>
<p> <b>Author:</b> Nguyen Tuan Ngoc, Sophomore from VNU-UET at this time </p>

This project is my Question-Answering System, you can ask anything. To improve the quality of the answer, you can add your data file into vector database to improve the quality with private data.

<h2>🚀 Demo</h2>

[link](https://drive.google.com/drive/folders/1Qus_YRHCnSC4V7tTHsTo2bLRvvLtI9mg?usp=sharing)

<h2>🖼️ Project Screenshots:</h2>

<img src="img\whoru.png" alt="project-screenshot" width="sdf" height="sdf/">
<img src="img\file_upload.png" alt="project-screenshot" width="sdf" height="sdf/">

  
<h2>🧐 Features</h2>

Here're some of the project's best features:

*   Chatting with Chatbot to help you address your problems.
*   You can add data with doc, docx(error), pdf format to enhance your database and improve the quality of the answer which based on RAG architecture.

<h2>🛠️ Installation Steps:</h2>

<p> <strong>1. Privileges</strong></p>

```
Python Version 3.10 
Conda Command Prompt
```

<p><strong>2. Conda Setup</strong></p>

```
conda create -n agent python=3.10 -y 
conda activate agent
#using pip to install all package from requirements.txt file 
pip install -r requirements.txt
```
  
<h2>💻 Built with</h2>

Technologies used in the project:

* <b>Frontend: </b>
    * Streamlit
* <b>Backend: </b>
    *   Langchain
    *   Zenguard for Prompt Injection Preserving (Not done)
    *   FastAPI
* <b>Vector database: </b>
    *   ChromaDB      
* <b>RAG Techniques: </b>
    *   Advanced RAG ReAct Agent
    *   Hybrid Search
    *   Agent External Tool: BingSearch Tool.
    *   Semantic Chunking
    *   Contextual Compression
    *   ReRanker (Demo Colab)
* <b>LLM API: </b> 
    *   OpenAI API Key

<h2>🔗 Pipeline </h2>

<img src="img\QA_pipeline.png" alt="project-screenshot" width="sdf" height="sdf/">
<img src="img\agent.png" alt="project-screenshot" width="sdf" height="sdf/">


<h2>📁 Project Structure</h2>

    * Tools:
        * AgentTools
            - BingSearch.py | Bing Search Tools
            - RAG.py | RAG Tools
            - Tools.py | Various Tools Powered By Agent
        * Retrieval:
            - Model.py | Model For Retrieval
            - Retrieval.py | Retrieval Tools
        * VectorDatabase:
            - API.py | API For Vector Database
            - Chroma.py | Vector Database Tools
    * Config_Model.yaml (use for higher performance configuration)
    * Config.py
    * RunBackend.py
    * requirements.txt
    * frontend:
        * app.py: Streamlit Server
        * client.py
    * RAG.py: Classical RAG with Vector Database

<h2>🗎 API docs </h2>

* In Tools\VectorDatabase\API.py: 
    * <b>add_data: </b> upload pdf file or doc file (still error) to chunk and store in Chroma database.
    * <b> delete_database: </b> delete database
* In RunBackend.py: 
    * <b> query_handler: </b> use for process questions and generate answers.
* In RAG.py: 
    * <b> query_handler: </b> use for process questions and generate answers.

<h2>👨🏻‍💻 How to run this project</h2>

<b>1. Clone this project from GitHub </b>
```
git clone https://github.com/ngoctuannguyen/SunSunChatBot.git
```
<b>2. Run Backend Server </b>
```
python RunBackend.py (Question Answering Server)
python Tools\VectorDatabase\API.py (File Upload Server)
```
<b>3. Run Frontend Server </b>
```
streamlit run frontend/app.py
``` 
<b>4. Run Classical RAG (due to lackage of data) </b>

Modify the <b>RAG.py</b>: change result of <b> def get_response() </b> to <b>response.json()["text"] </b>

<img src="img\image.png">

<h2>👨🏻 How to use this project </h2>
 
 Try some questions in <b>test.txt</b> or your own questions

<h2>📩 Contact </h2>
If you have questions, please issue this repository or contact me via email ngoctuannguyen198012@gmail.com.
