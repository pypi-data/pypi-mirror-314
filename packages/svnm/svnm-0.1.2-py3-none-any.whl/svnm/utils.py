from huggingface_hub import hf_hub_download
def download_model(repo_id,filename):
    # Download the file
    model_path = hf_hub_download(repo_id=repo_id, filename=filename)
    print("Model downloaded to:", model_path)
    return model_path