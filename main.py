import spacy
import subprocess
import sys

# Ensure the spaCy model is installed at runtime
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Predefined chatbot responses
responses = {
    "hello": ["Hi there!", "Hello!", "Hey! How can I help you?"],
    "how are you": ["I'm good! How about you?", "I'm doing great! What about you?"],
    "name": ["I'm a chatbot, and you can call me WordBot!", "I go by WordBot!"],
    "weather": ["I can't check the weather, but I hope it's nice!", "Weather depends on where you are!"],
    "bye": ["Goodbye! Have a nice day!", "See you later!", "Take care!"]
}

def analyze_input(user_input):
    """Decides whether to return chatbot response or grammar analysis."""
    user_input = user_input.strip()

    # Simple numeric/symbol check
    if user_input.isdigit():
        return "This is an integer."
    
    elif re.match(r'^\d+\.\d+$', user_input):
        return "This is a float."
    
    elif re.match(r'^[^a-zA-Z0-9]+$', user_input):
        return "This contains only special characters."

    # Decide based on sentence length
    words = user_input.split()
    if len(words) > 3:  # Longer input -> Grammar Analysis
        return analyze_grammar(user_input)
    
    else:  # Short input -> Chatbot response
        return predict_response(user_input)

def predict_response(user_input):
    """Finds the best chatbot response using NLP similarity."""
    user_input = user_input.lower()
    doc1 = nlp(user_input)

    best_match = None
    highest_similarity = 0

    for key in responses:
        doc2 = nlp(key)
        similarity = doc1.similarity(doc2)

        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = key

    if best_match and highest_similarity > 0.5:
        return random.choice(responses[best_match])
    else:
        return "I'm not sure how to respond to that."

def analyze_grammar(sentence):
    """Extracts key grammatical elements."""
    doc = nlp(sentence)
    
    nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    verbs = [token.text for token in doc if token.pos_ == "VERB"]
    adjectives = [token.text for token in doc if token.pos_ == "ADJ"]
    adverbs = [token.text for token in doc if token.pos_ == "ADV"]

    # Format the response
    grammar_output = "Here's the key grammatical structure:\n"

    if nouns:
        grammar_output += f"**Nouns:** {', '.join(nouns)}\n"
    if verbs:
        grammar_output += f"**Verbs:** {', '.join(verbs)}\n"
    if adjectives:
        grammar_output += f"**Adjectives:** {', '.join(adjectives)}\n"
    if adverbs:
        grammar_output += f"**Adverbs:** {', '.join(adverbs)}\n"

    return grammar_output.strip() if (nouns or verbs or adjectives or adverbs) else "No major grammatical elements found."

# Streamlit UI
st.title("🤖 WordBot - Intelligent NLP Chatbot")
st.write("This chatbot detects input types, responds smartly, and provides key grammatical analysis!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input field
user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        st.session_state.messages.append(("You", user_input))

        # Get chatbot response or grammar analysis
        bot_response = analyze_input(user_input)

        st.session_state.messages.append(("WordBot", bot_response))

# Display chat history
for sender, message in st.session_state.messages:
    st.write(f"**{sender}:** {message}")
