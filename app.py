import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import speech_recognition as sr
from textblob import TextBlob
import random

# Ensure necessary NLTK resources are downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Vocabulary analysis function
def analyze_vocabulary(text):
    # Tokenize and POS tag the text
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    
    # Initialize counters for different parts of speech
    vocabulary_analysis = {
        "nouns": 0,
        "verbs": 0,
        "adjectives": 0,
        "adverbs": 0,
        "pronouns": 0,
        "prepositions": 0,
        "total_words": len(tokens)
    }
    
    # Loop through tagged tokens and count parts of speech
    for word, tag in tagged:
        if tag.startswith('NN'):  # Nouns (singular/plural)
            vocabulary_analysis["nouns"] += 1
        elif tag.startswith('VB'):  # Verbs (base form, past, gerund, etc.)
            vocabulary_analysis["verbs"] += 1
        elif tag.startswith('JJ'):  # Adjectives
            vocabulary_analysis["adjectives"] += 1
        elif tag.startswith('RB'):  # Adverbs (e.g., 'RB', 'RBR', 'RBS')
            vocabulary_analysis["adverbs"] += 1
        elif tag in ['PRP', 'PRP$']:  # Pronouns
            vocabulary_analysis["pronouns"] += 1
        elif tag in ['IN']:  # Prepositions
            vocabulary_analysis["prepositions"] += 1
    
    return vocabulary_analysis

# Sentiment analysis function using TextBlob
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    
    if sentiment_score > 0:
        return "Positive"
    elif sentiment_score < 0:
        return "Negative"
    else:
        return "Neutral"

# Function to perform speech recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Please speak now... (Ensure microphone access is allowed)")
        audio = recognizer.listen(source)
        try:
            # Recognize the speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            st.write(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.write("Sorry, I could not understand the audio.")
            return ""
        except sr.RequestError:
            st.write("Sorry, there was an issue with the speech recognition service.")
            return ""

# List of random questions
questions = [
    "What is your favorite hobby?",
    "Can you describe a memorable event from your life?",
    "What are your career aspirations?",
    "What motivates you to succeed?",
    "Describe a challenging experience you overcame."
]

# Select a random question
random_question = random.choice(questions)

# Streamlit app UI
st.title("Speech Proficiency Tester")
st.markdown("""
    This application allows you to record your speech, answer a random question, and get an analysis of your vocabulary and sentiment.
    Click the button below to start speaking and see the results.
""")

# Ask the random question
st.subheader("Random Question")
st.write(f"**Question**: {random_question}")

# Allow user to record speech and respond to the question
if st.button("Start Speaking", use_container_width=True):
    user_speech = recognize_speech()

    if user_speech:
        # Sentiment Analysis Section
        st.subheader("Sentiment Analysis")
        sentiment = analyze_sentiment(user_speech)
        st.write(f"Sentiment: **{sentiment}**")

        # Vocabulary Analysis Section
        st.subheader("Vocabulary Analysis")
        vocabulary_analysis = analyze_vocabulary(user_speech)
        
        with st.expander("View Vocabulary Details"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Total Words**: {vocabulary_analysis['total_words']}")
                st.write(f"**Nouns**: {vocabulary_analysis['nouns']}")
                st.write(f"**Pronouns**: {vocabulary_analysis['pronouns']}")
                st.write(f"**Prepositions**: {vocabulary_analysis['prepositions']}")
            with col2:
                st.write(f"**Verbs**: {vocabulary_analysis['verbs']}")
                st.write(f"**Adjectives**: {vocabulary_analysis['adjectives']}")
                st.write(f"**Adverbs**: {vocabulary_analysis['adverbs']}")

        # Feedback based on vocabulary analysis
        st.subheader("Feedback Based on Vocabulary Usage")
        feedback = []

        if vocabulary_analysis["nouns"] > 8:
            feedback.append("Excellent vocabulary usage with a wide range of nouns!")
        elif 5 < vocabulary_analysis["nouns"] <= 8:
            feedback.append("Good vocabulary with a decent variety of nouns.")
        else:
            feedback.append("Try to use a wider variety of nouns.")

        if vocabulary_analysis["verbs"] > 8:
            feedback.append("Outstanding use of verbs! You effectively express action and movement.")
        elif 5 < vocabulary_analysis["verbs"] <= 8:
            feedback.append("Well done! Try adding more dynamic verbs.")
        else:
            feedback.append("Consider using more action verbs.")

        if vocabulary_analysis["adjectives"] > 5:
            feedback.append("Great job using adjectives!")
        elif 3 < vocabulary_analysis["adjectives"] <= 5:
            feedback.append("Good use of adjectives. Add more to enhance descriptions.")
        else:
            feedback.append("Try using more adjectives to describe things.")

        if vocabulary_analysis["adverbs"] > 5:
            feedback.append("Your use of adverbs is great!")
        elif 3 < vocabulary_analysis["adverbs"] <= 5:
            feedback.append("You're using adverbs well. Consider adding more.")
        else:
            feedback.append("Adverbs can add depth to your descriptions. Try incorporating more.")

        if vocabulary_analysis["pronouns"] > 3:
            feedback.append("You've used pronouns effectively.")
        else:
            feedback.append("Try using pronouns to avoid repetition.")

        if vocabulary_analysis["prepositions"] > 3:
            feedback.append("Your use of prepositions is good.")
        else:
            feedback.append("Consider using more prepositions to clarify relationships.")

        # Display Feedback
        for item in feedback:
            st.write(f"- {item}")

        # Encourage overall language improvement
        if vocabulary_analysis["total_words"] > 50:
            st.write("You're using a rich vocabulary overall!")
        else:
            st.write("Keep working on expanding your vocabulary.")

        st.markdown("---")
        st.write("Thank you for using the Speech Proficiency Tester!")
