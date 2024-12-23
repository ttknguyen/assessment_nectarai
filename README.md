

# Generative Agents: Dating Show (Love Island)

<p align="center" width="100%">
<img src="cover.png" alt="Smallville" style="width: 80%; min-width: 300px; display: block; margin: auto;">
</p>

This project based on  "[Generative Agents: Interactive Simulacra of Human Behavior](https://github.com/joonspk-research/generative_agents/tree/main)." It is a simulation of a dating show where generative agents can interact and flirt with each other. The agents are designed to emulate human-like behaviors, enabling dynamic and engaging interactions that mirror real-life dating scenarios. Through this project, we aim to explore the capabilities of generative agents in creating lifelike social experiences and delve into the nuances of AI-driven human behavior simulation.

### Significant Achievements of This Project:
- Designed a simulation environment that enables agents to communicate, flirt, and even fall in love, much like participants in a Dating Show.  
- Replaced all OpenAI APIs with open-source alternatives, providing a framework that allows for flexible deployment and easy modification of models.  
- Achieved a **ZERO-COST** implementation by supporting the deployment of an LLM model on Colab via ngrok.  

The following is a detailed guide for this project: 

# Setting Up the Environment 

Here’s the revised version with more explanation and introductory context:  

## Step 1: Deploy Model LLMs  

This step involves setting up a server to host two models for the project:  
1. **Text-generation task**: This model generates responses based on input text.  
2. **Embedding task**: This model is used for encoding text into vector representations for efficient semantic understanding.  

In this implementation, the following models are used:  
- **Text-generation task**: `LLAMA3.1-8B-Instruct` – a robust model for generating coherent and context-aware text.  
- **Embedding task**: `intfloat/e5-mistral-7b-instruct` – a compact and efficient model optimized for embedding tasks.  

You can **substitute these models with any open-source model available on HuggingFace** that fits your use case.  

### Deployment Options  

#### 1. Deploy with a Local Server  

This approach is ideal if you have adequate computational resources to run the models locally.  

   Running the models locally allows for greater control, faster access, and enhanced privacy. However, it requires a GPU with sufficient memory and processing power.  

- **Steps to Run with `docker compose`:**  
    1. Open your terminal and navigate to the directory containing the `docker-compose.yml` file:  
       ```bash
       cd /path/to/your/project
       ```  
    2. Start the services by executing the following command:  
       ```bash
       docker compose up
       ```  

#### 2. Deploy Using Google Colab  

To minimize costs, you can use Google Colab as a server. This is an efficient solution for hosting:  
- A Large Language Model (LLM) for text generation.  
- A smaller model for embedding.  

- Google Colab provides free GPU resources, making it a cost-effective solution for projects with limited budgets. Using ngrok, we can expose the server running on Colab to the internet for external access.  

- **Setup Instructions:**  
   1. **Register with ngrok:**  
      - Sign up at [ngrok.com](https://ngrok.com/) and retrieve your Authtoken. Use the following commands to set up ngrok:  
        ```bash
        !pip install pyngrok
        !wget -q -O ngrok.zip https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
        !unzip -q ngrok.zip
        !./ngrok authtoken <your_authtoken>
        !./ngrok http 8000
        ```  

   2. **Install Required Packages:**  
      Use the following commands to install the necessary dependencies:  
      ```bash
      # Installation
      !pip install -qU \
          transformers \
          accelerate==0.21.0 \
          einops==0.6.1 \
          langchain==0.0.240 \
          xformers==0.0.20 \
          bitsandbytes==0.41.0 \
          accelerate>=0.26.0 \
          huggingface-hub \
          fastapi \
          uvicorn \
          vllm

      !pip install torch -U
      ```  

   3. **Start the Server for the Text-Generation Model:**  
      Launch the LLM model for text generation using the following command:  
      ```bash
      # Should run through terminal
      !export HF_HOME=/content/
      !export HF_TOKEN=<hf_token>

      !python3 -m vllm.entrypoints.openai.api_server \
          --model=meta-llama/Meta-Llama-3.1-8B-Instruct \
          --dtype=half \
          --max-model-len=20000 \
          --gpu-memory-utilization=1 \
          --port 8001
      ```  

   4. **Repeat the Steps for the Embedding Model:**  
      Follow similar steps to set up and run the embedding model.  

---

By following these instructions, you can deploy the necessary LLMs either locally or using Google Colab. This flexible setup ensures that you can adapt the deployment to fit your resources and requirements.  


- These models were chosen for their balance of performance and efficiency. `LLAMA3.1-8B-Instruct` is highly capable of generating coherent and context-aware text, making it ideal for text-generation tasks. The `intfloat/e5-mistral-7b-instruct` is optimized for embedding, offering speed and accuracy in encoding text into vectors, which is essential for semantic tasks.  

- Limitations include limited session duration, reliance on stable internet, and restricted GPU availability. These can be mitigated by regularly saving model checkpoints, using premium Colab plans for extended session time, and ensuring scripts auto-restart when interrupted.  

- Open-source models from HuggingFace allow customization and fine-tuning to meet specific project requirements. They provide a broad library of pre-trained models, enabling easy substitution based on task complexity and resource availability. Additionally, community support ensures updates and troubleshooting resources are readily available.  

## Step 2: Flow as set up the orignal repo
To set up your environment, you will need to generate a `utils.py` file that contains your OpenAI API key and download the necessary packages.

### Step 2.1. 
In the `reverie/backend_server` folder (where `reverie.py` is located), create a new file titled `utils.py` and copy and paste the content below into the file:
```
# Copy and paste your OpenAI API Key
url = "http://localhost:8001/v1/"
url_emb = "http://localhost:8002/v1/"

model_name = 'meta-llama/Llama-3.2-3B-Instruct'
model_emb = 'intfloat/e5-mistral-7b-instruct'

maze_assets_loc = "../../environment/frontend_server/static_dirs/assets"
env_matrix = f"{maze_assets_loc}/the_ville/matrix"
env_visuals = f"{maze_assets_loc}/the_ville/visuals"

fs_storage = "../../environment/frontend_server/storage"
fs_temp_storage = "../../environment/frontend_server/temp_storage"

collision_block_id = "32125"

# Verbose 
debug = True
```
Replace `<url>`, `<url_emb>` with your url, and `<model_name>`, `model_emb`.
 
### Step 2.2. Install requirements.txt
Install everything listed in the `requirements.txt` file (I strongly recommend first setting up a virtualenv as usual). A note on Python version: we tested our environment on Python 3.9.12. 

# Running a Simulation 
To run a new simulation, you will need to concurrently start two servers: the environment server and the agent simulation server.

### Step 1. Starting the Environment Server


    python manage.py runserver

Then, on your favorite browser, go to [http://localhost:8000/](http://localhost:8000/).

### Step 2. Starting the Simulation Server
Navigate to `reverie/backend_server` and run `reverie.py`.

    python reverie.py
"Enter the name of the forked simulation: ". Type the following:
    
    love_island
"Enter the name of the new simulation: ". Type any name to denote your current simulation (e.g., just "test-simulation" will do for now).

    test-simulation
Keep the simulator server running. At this stage, it will display the following prompt: "Enter option: "

### Step 3. Running and Saving the Simulation
To run the simulation, type the following command in your simulation server in response to the prompt, "Enter option":

    run <step-count>



# Detailed Experimental Plan: Open-Source Model Integration for AI Dating Simulation

## Project Overview

This project aims to replace the OpenAI API calls with open-source large language models (LLMs) and self-host them to simulate a dating environment. The main goal is to create a simulation of a dating show (similar to Love Island) with at least six characters. These characters will interact, flirt, and form relationships within a fictional world, all powered by self-hosted AI models.

The experiment will involve the following steps:
1. Replacing OpenAI API calls with open-source LLMs.
2. Hosting and serving these models for use within the simulation.
3. Creating and refining a custom simulation environment for a dating show.
4. Optimizing prompts and interactions to ensure high-quality, realistic simulations.

---

## Goals and Objectives

- **Replace OpenAI API**: Remove all dependencies on the OpenAI API and replace them with open-source models such as LLaMA 3.1-8B-Instruct, Mistral, etc. Host these models locally to save on costs.
  
- **Zero-Cost Hosting**: The goal is to self-host these models in a way that avoids high costs and is sustainable. We will use pre-trained models from HuggingFace and set up local infrastructure for serving them.

- **Custom Environment**: Create a custom environment for the dating simulation where characters can interact naturally, engage in romantic dialogues, and evolve through the course of the simulation.

- **Prompt Optimization**: Refine and optimize prompts to ensure the characters behave realistically and have coherent, engaging conversations.

- **Documentation**: Provide a working simulation with detailed instructions on running it and a clear explanation of how different open-source models can be tested and swapped in the code.

---

## Experimental Plan

### 1. **Setting Up the Environment**

- **Self-Hosting the Models**: 
    - Use HuggingFace's `transformers` library to load open-source models like LLaMA 3.1-8B-Instruct and Mistral locally.
    - Setup a Python server (using FastAPI or Flask) to serve these models via REST APIs.
    - Utilize GPU or multi-core CPU setups to efficiently run the models locally.
    - Install necessary dependencies: `transformers`, `torch`, `fastapi`, etc.
    
    **Steps**:
    - Install necessary libraries using `pip install transformers torch fastapi`.
    - Download pre-trained models from HuggingFace (or other repositories) and set up local hosting.
    - Build a REST API server for easy interaction between the simulation and the models.

    **Expected Outcome**: 
    - The system will be able to serve AI responses from open-source models instead of the OpenAI API, significantly reducing costs.

---

### 2. **Creating the Custom Simulation Environment**

- **Character Design**: 
    - Design at least 6 characters with unique personalities, preferences, and behavior patterns.
    - Characters will engage in daily interactions, such as flirting, having conversations, and forming relationships.
    
- **Daily Planning**:
    - Create a "daily plan" that simulates typical interactions in a dating show environment.
    - Each day, characters will engage in various activities: group conversations, private dates, challenges, etc.

    **Expected Outcome**: 
    - A robust environment where characters are aware they are in a dating show and interact with each other accordingly.

---

### 3. **Developing the AI Agents and Interaction Mechanism**

- **Agent Actions**:
    - The agents will take actions like greeting, complimenting, flirting, and breaking up based on the context of the day.
    - Use the self-hosted LLMs to generate responses to these actions in a conversational manner.

- **Model Integration**:
    - Replace the OpenAI API calls in the original code with calls to the self-hosted models.
    - Test different models (LLaMA, Mistral) and evaluate their performance in the simulation.

    **Expected Outcome**: 
    - The AI agents will respond to interactions in a natural, fluid way based on the simulation's context and character traits.

---

### 4. **Optimizing Prompts for Realistic Interactions**

- **Prompt Refinement**:
    - Develop and optimize prompts that guide the models to simulate realistic interactions. These prompts will be stored in a directory called `love_island_prompt`.
    - Focus on creating varied, rich prompts for:
      - **Flirting**: Ask models to generate flirtatious, playful responses.
      - **Conflict Resolution**: Create prompts that encourage agents to handle relationship drama.
      - **Daily Activities**: Prompts to guide agents through daily activities like date planning, group interactions, etc.

    **Expected Outcome**: 
    - The agents will engage in realistic and diverse conversations that simulate the complexities of a dating show environment.

---

### 5. **Model Evaluation and Comparison**

- **Model Comparison**: 
    - Experiment with different models (LLaMA 3.1-8B-Instruct, Mistral, etc.) to evaluate their effectiveness in generating natural and engaging dialogues.
    - Analyze the performance of each model in terms of:
        - Conversation flow
        - Character consistency
        - Appropriateness of responses

    **Expected Outcome**:
    - Identify the best-performing model for the simulation, based on factors like naturalness, coherence, and relevance to the simulation's goals.

---

### 6. **Zero-Cost Hosting Setup**

- **Cost-Efficiency**:
    - Use free-tier cloud services or on-premise hardware (if available) to host models.
    - Ensure that all hosting and API usage is cost-effective and adheres to a zero-cost goal for the duration of the project.

    **Steps**:
    - Optimize the model's inference efficiency to reduce computational costs (e.g., batch processing, model quantization).
    - Consider using local resources like personal GPUs, or free cloud compute options (Google Colab, HuggingFace Spaces, etc.).

    **Expected Outcome**: 
    - Achieve zero-cost hosting while ensuring the AI models are responsive and able to handle the simulation load.

---

### 7. **Documentation and Final Reporting**

- **README**:
    - Provide a detailed README that explains how to run the simulation, set up the environment, and replace models as needed.
    - Include instructions on how to test different models (e.g., LLaMA, Mistral, etc.) by changing model names and tokens.
    - Document the folder structure, including `llama-structure` for model API management and `love_island_prompt` for prompt storage.
    
- **Logbook**:
    - Maintain a log of experiments, including what worked, what didn’t, and lessons learned during the process of replacing OpenAI with open-source models and setting up the dating simulation.

---

## Conclusion

This experimental plan outlines the steps to replace OpenAI API calls with open-source models, host them locally, and create a simulation of a dating show where characters interact naturally. The project will focus on cost efficiency, using self-hosted LLMs, and optimizing the dialogue and character behaviors for the best experience possible. By the end, the goal is to have a fully functional simulation with detailed documentation, offering flexibility to test various open-source models.

