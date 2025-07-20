import kagglehub
import zipfile
import os
import shutil

def refresh_crop_data():
    try:
        print("Starting dataset refresh...")

        # Get absolute path to server/data/crop
        base_dir = os.path.dirname(os.path.abspath(__file__))  # utils/
        server_dir = os.path.abspath(os.path.join(base_dir, ".."))
        target_dir = os.path.join(server_dir, "data", "crop")

        # Step 1: Download dataset (downloads to ~/.kagglehub internally)
        path = kagglehub.dataset_download("atharvaingle/crop-recommendation-dataset")
        print(f" Dataset downloaded to: {path}", flush=True)
        print(f" Files in downloaded path: {os.listdir(path)}", flush=True)

        # Step 2: Remove existing data
        if os.path.exists(target_dir):
            print(f" Removing existing directory: {target_dir}", flush=True)
            shutil.rmtree(target_dir)

        os.makedirs(target_dir, exist_ok=True)
        print(f" Created fresh directory: {target_dir}", flush=True)

        # Step 3: Extract or copy files
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            if file.endswith('.zip'):
                print(f" Extracting: {file}")
                with zipfile.ZipFile(full_path, 'r') as zip_ref:
                    zip_ref.extractall(target_dir)
                print(f" Extracted {file}")
            else:
                print(f" Copying file: {file}", flush=True)
                shutil.copy(full_path, target_dir)
                print(f" Copied {file}",flush=True)

        print(" Dataset refresh completed successfully.", flush=True)
    
    except Exception as e:
        print(" Error during dataset refresh:", str(e))
        raise
