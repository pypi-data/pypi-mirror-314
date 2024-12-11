import random
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

class NlpChat:
    def __init__(self):
        self.intents = {}
        self.model = None
        self.embeddings_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    def add_intent(self, tag, patterns, responses):
        """Add a new intent with patterns and responses."""
        self.intents[tag] = {
            'patterns': patterns,
            'responses': responses
        }

    def train(self):
        """Train the intent recognition model using Logistic Regression."""
        all_patterns = []
        all_labels = []

        for tag, data in self.intents.items():
            for pattern in data['patterns']:
                all_patterns.append(pattern)
                all_labels.append(tag)

        # Encode patterns using Sentence Transformers
        X = self.embeddings_model.encode(all_patterns)

        # Train Logistic Regression model
        self.model = LogisticRegression()
        self.model.fit(X, all_labels)

    def save_model(self, filename):
        """Save the trained model and intents to a file."""
        with open(filename, 'wb') as f:
            pickle.dump((self.model, self.intents), f)

    def load_model(self, filename):
        """Load the saved model and intents from a file."""
        with open(filename, 'rb') as f:
            self.model, self.intents = pickle.load(f)

    def get_response(self, user_input):
        """Get a response for the given user input."""
        if self.model is None:
            raise Exception("Model not trained. Please train the model before making predictions.")

        # Predict intent
        input_embedding = self.embeddings_model.encode([user_input])
        predicted_intent = self.model.predict(input_embedding)[0]

        # Get a random response from the predicted intent
        return random.choice(self.intents[predicted_intent]['responses'])

    def get_intent(self, user_input):
        """Get only the predicted intent without generating a response."""
        if self.model is None:
            raise Exception("Model not trained. Please train the model before making predictions.")

        input_embedding = self.embeddings_model.encode([user_input])
        return self.model.predict(input_embedding)[0]
