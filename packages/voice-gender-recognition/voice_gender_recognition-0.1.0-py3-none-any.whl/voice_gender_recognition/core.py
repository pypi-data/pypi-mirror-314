import os

def predict_gender(file=None, model_path="results/model.h5"):
    """
    Predict gender from audio file or live recording
    
    Args:
        file (str, optional): Path to audio file. If None, records from microphone
        model_path (str): Path to the trained model weights
        
    Returns:
        tuple: (predicted_gender, male_probability, female_probability)
    """
    from .utils import create_model  # relative import
    
    model = create_model()
    model.load_weights(model_path)
    
    if not file or not os.path.isfile(file):
        print("Please talk")
        file = "test.wav"
        record_to_file(file)
        
    features = extract_feature(file, mel=True).reshape(1, -1)
    male_prob = model.predict(features)[0][0]
    female_prob = 1 - male_prob
    gender = "male" if male_prob > female_prob else "female"
    
    return gender, male_prob, female_prob 