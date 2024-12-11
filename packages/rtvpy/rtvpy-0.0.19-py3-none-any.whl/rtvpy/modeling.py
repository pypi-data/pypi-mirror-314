import os
from joblib import dump

def saveModel(model, base_filename='model.joblib'):
    """
    Save the model to a file, ensuring no existing file is overwritten.
    If the file exists, increment the filename (e.g., model_1.joblib).
    """
    filename = base_filename
    if os.path.exists(filename):
        base_name, ext = os.path.splitext(base_filename)
        i = 1
        while os.path.exists(f"{base_name}_{i}{ext}"):
            i += 1
        filename = f"{base_name}_{i}{ext}"
    
    dump(model, filename)
    print(f"Model saved as: {filename}")

# Save the model
save_model(best_model)
