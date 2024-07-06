import pickle
from example_data import data as example_data

# Load the saved model
loaded_model = pickle.load(open("./models/pima.pickle.dat", "rb"))

# Make predictions
predictions = loaded_model.predict(example_data)

print("Predictions:", predictions)
