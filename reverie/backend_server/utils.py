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