
# nlpchat

**nlpchat** is a Python package that simplifies the creation of chatbots using natural language processing (NLP) for intent identification. The package uses Sentence Transformers for embedding input text and supports easy management of intents with customizable responses. It employs Logistic Regression for enhanced performance in intent classification. It provides functionality for training, saving, and loading models, allowing you to avoid retraining the chatbot each time.

## Features
- **Simple intent management**: Easily add intents, patterns, and responses.
- **Logistic Regression for Intent Recognition**: Uses Logistic Regression for better intent classification.
- **NLP-powered**: Uses Sentence Transformers to embed and understand user inputs.
- **Train and Save**: Train the model once and save it for later use.
- **Load saved models**: Quickly load previously trained models for immediate use.
- **Intent prediction**: Predicts the user's intent based on input text.
- **Custom responses**: Generate responses based on detected intents.
- **Intent-only prediction**: Retrieve just the predicted intent without generating a response.


## Installation

You can install the package from the repository:

```bash
pip install nlpchat
```

### Dependencies
Make sure to install the following packages:

```bash
pip install sentence-transformers scikit-learn numpy pickle-mixin
```

## Usage

Here’s a simple example showing how to create a chatbot, train it using Logistic Regression, save the model, and make predictions.

### 1. Import and Initialize the Chatbot

```python
from nlpchat import NlpChat

# Create an instance of NlpChat
chatbot = NlpChat()
```

### 2. Add Intents

You can add intents using the `add_intent()` function in two ways:

#### Method 1: Detailed Syntax

```python
# Add a greeting intent
chatbot.add_intent(
    tag="greeting",
    patterns=["Hi", "Hello", "Good morning"],
    responses=["Hello!", "Hi there!", "Good to see you!"]
)

# Add a goodbye intent
chatbot.add_intent(
    tag="goodbye",
    patterns=["Bye", "See you later", "Goodbye"],
    responses=["Goodbye!", "See you later!", "Take care!"]
)
```

#### Method 2: Concise Syntax

```python
# Add intents using concise syntax
chatbot.add_intent("greeting", ["Hi", "Hello", "Good morning"], ["Hello!", "Hi there!", "Good to see you!"])
chatbot.add_intent("goodbye", ["Bye", "See you later", "Goodbye"], ["Goodbye!", "See you later!", "Take care!"])
```

### 3. Train the Model

Train the chatbot on the added intents. The model uses Logistic Regression for intent prediction.

```python
chatbot.train()
```

### 4. Save the Model

Once the model is trained, you can save it to a file for future use.

```python
# Save the trained model and intents to a file
chatbot.save_model("chatbot_model.pkl")
```

### 5. Load a Saved Model

To avoid retraining every time, load the saved model.

```python
# Load the saved model
chatbot.load_model("chatbot_model.pkl")
```

### 6. Predict Intent and Get Response

After the model is loaded, you can use it to predict user intents and get a response.

```python
user_input = "Hello"
response = chatbot.get_response(user_input)
print(response)  # Outputs: "Hello!" or another greeting response
```

### 7. Predict Intent Only

If you only need to predict the user's intent without generating a response, you can use the `get_intent()` method:

```python
# Get only the predicted intent (without response)
user_input = "Hello"
intent = chatbot.get_intent(user_input)
print(f"Predicted intent: {intent}")  # Outputs: "greeting"
```

## How It Works
- **Intent Management**: Users define intents using `add_intent()`. Each intent has a tag (such as "greeting"), a set of patterns (user inputs), and a set of responses.
- **Logistic Regression**: The chatbot uses Logistic Regression for intent prediction based on the Sentence Transformer embeddings of user inputs.
- **Prediction**: When user input is given, the chatbot encodes the input using the Sentence Transformer model, predicts the intent using Logistic Regression, and returns a random response from the associated intent (or just the intent if requested).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! If you’d like to contribute to the project, please fork the repository and submit a pull request.

## Contact
For any issues or suggestions, please open an issue on the [GitHub repository](https://github.com/IMApurbo/nlpchat).
