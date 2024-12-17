import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import speech_recognition as sr
from textblob import TextBlob

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
        st.write("Please speak now...")
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

# Streamlit app UI
st.title("Speech Proficiency Tester")

# Allow user to record speech
if st.button("Start Speaking"):
    user_speech = recognize_speech()

    if user_speech:
        # Sentiment Analysis
        sentiment = analyze_sentiment(user_speech)
        st.write(f"Sentiment Analysis: {sentiment}")

        # Vocabulary Analysis
        vocabulary_analysis = analyze_vocabulary(user_speech)

        # Display the results of vocabulary analysis
        st.write(f"Total Words: {vocabulary_analysis['total_words']}")
        st.write(f"Nouns: {vocabulary_analysis['nouns']}")
        st.write(f"Verbs: {vocabulary_analysis['verbs']}")
        st.write(f"Adjectives: {vocabulary_analysis['adjectives']}")
        st.write(f"Adverbs: {vocabulary_analysis['adverbs']}")
        st.write(f"Pronouns: {vocabulary_analysis['pronouns']}")
        st.write(f"Prepositions: {vocabulary_analysis['prepositions']}")

        # Feedback based on vocabulary analysis
        if vocabulary_analysis["nouns"] > 8:
            st.write("Excellent vocabulary usage with a wide range of nouns!")
        elif 5 < vocabulary_analysis["nouns"] <= 8:
            st.write("Good vocabulary with a decent variety of nouns.")
        else:
            st.write("Try to use a wider variety of nouns.")

        if vocabulary_analysis["verbs"] > 8:
            st.write("Outstanding use of verbs! You effectively express action and movement.")
        elif 5 < vocabulary_analysis["verbs"] <= 8:
            st.write("Well done! Try adding more dynamic verbs.")
        else:
            st.write("Consider using more action verbs.")

        if vocabulary_analysis["adjectives"] > 5:
            st.write("Great job using adjectives!")
        elif 3 < vocabulary_analysis["adjectives"] <= 5:
            st.write("Good use of adjectives. Add more to enhance descriptions.")
        else:
            st.write("Try using more adjectives to describe things.")

        if vocabulary_analysis["adverbs"] > 5:
            st.write("Your use of adverbs is great!")
        elif 3 < vocabulary_analysis["adverbs"] <= 5:
            st.write("You're using adverbs well. Consider adding more.")
        else:
            st.write("Adverbs can add depth to your descriptions. Try incorporating more.")

        if vocabulary_analysis["pronouns"] > 3:
            st.write("You've used pronouns effectively.")
        else:
            st.write("Try using pronouns to avoid repetition.")

        if vocabulary_analysis["prepositions"] > 3:
            st.write("Your use of prepositions is good.")
        else:
            st.write("Consider using more prepositions to clarify relationships.")

        # Encourage overall language improvement
        if vocabulary_analysis["total_words"] > 50:
            st.write("You're using a rich vocabulary overall!")
        else:
            st.write("Keep working on expanding your vocabulary.")
