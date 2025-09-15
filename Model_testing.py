#%%
# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-generation", model="openbmb/MiniCPM4.1-8B", trust_remote_code=True)
messages = [
    {"role": "user", "content": "Who are you?"},
]
pipe(messages)

#%%

# import os
# import shutil

# # Define the path to the model directory for LLM360/K2-Think
# model_directory = r"C:\Users\ahmad\.cache\huggingface\hub\models--LLM360--K2-Think"

# # Check if the directory exists
# if os.path.exists(model_directory):
#     # Remove the directory and all its contents
#     shutil.rmtree(model_directory)
#     print(f"Successfully deleted the model directory: {model_directory}")
# else:
#     print(f"The directory does not exist: {model_directory}")

# # %%
