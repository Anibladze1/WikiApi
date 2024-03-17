# Wikipedia Topic Insight Generator

## Objective

The Wikipedia Topic Insight Generator is a Python application designed to fetch data from Wikipedia on user-specified topics, analyze it using Large Language Models (LLMs) to generate insights, and store the outcomes in a MongoDB database. This tool is ideal for extracting summarized information and key insights from a wide range of topics available on Wikipedia.

## Core Features

- **Data Retrieval:** Fetch data from Wikipedia based on user-specified topics.
- **Data Analysis:** Use LLMs to analyze the retrieved data, summarizing articles, identifying key themes or trends, and generating novel insights.
- **Data Storage:** Store the analyzed data in MongoDB for easy retrieval and structured access.
- **API Development:** Utilize FastAPI to create endpoints for specifying topics, initiating data retrieval, and fetching analysis results.
- **Containerization:** The application is containerized with Docker for ease of deployment and scalability.
- **Scalability:** Designed to efficiently process requests and manage load, ensuring smooth operation even under high demand.

## Technology Stack

- **FastAPI:** For creating the web API.
- **Celery:** For managing background task processing.
- **MongoDB:** As the database for storing retrieved and analyzed data.
- **Docker:** For containerizing the application and ensuring consistent environments across different setups.
- **LangChain and OpenAI's GPT:** For processing and analyzing the text data.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup and Running

1. **Clone the repository:**
   ```bash
   git clone git@github.com:Anibladze1/WikiApi.git

2. **Navigate to Directory:**
   ```bash
      cd Wikipedia-Topic-Insight-Generator
3. **Set up the environment variables:**
Copy the `.env.example` file to a new file named `.env` and fill in the necessary details like database URI, API keys, etc.


4. **Build and run the application using Docker Compose:**
    ```bash
    docker-compose up --build

## Usage
### API Endpoints

- `GET /`: The root endpoint, which returns a welcome message.
- `POST /summarize_topic`: Endpoint to initiate the summarization of a specified Wikipedia topic.
- `GET /read_summary`: Endpoint to retrieve the summary of a topic by its title or ID.


### Example Requests
To summarize a topic:
```bash
curl -X POST http://localhost:8000/summarize_topic?topic_title="Madrid"
```
To read a summary:
```bash
curl http://localhost:8000/read_summary?topic_title_or_id="Madrid"
```

## Swagger Documentation
For more detailed information on the API endpoints and their usage, refer to the API documentation provided within the application, accessible at [http://localhost:8000/docs](http://localhost:8000/docs).
