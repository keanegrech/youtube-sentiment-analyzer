from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np
import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as VSA

# nltk.download()

vectorizer = TfidfVectorizer(stop_words="english")


def processUserInput(request):
    """
    This function processes the user input to figure out if it is a video URL or a video ID, and returns the videoID

    Parameters:
    request (str): The user input

    Returns:
    str: The video ID
    """
    if "v=" in request:
        return request.split("v=")[1]
    else:
        return request


def cleanText(text):
    """
    Removes unecessary snippets from the text

    Parameters:
    text (str): The text to remove the snippets from

    Returns:
    str: The text with the snippets removed
    """

    # Remove hyperlinks, line breaks, and apostrophes ASCII (youtube API returns apostrophes as &#39;)
    # Remove text between <a> and </a> tags
    text = re.sub(r"<a.*?>.*?</a>", "", text, flags=re.DOTALL)

    # Remove <br> tags
    text = re.sub(r"<br>", "", text)

    # Remove apostrophes
    text = re.sub(r"&#39;", "'", text)

    # Remove emojis
    text = text.encode("ascii", "ignore").decode("ascii")

    return text


def tokenizeComments(comments):
    """
    Tokenizes the comments

    Parameters:
    comments (list): The comments to tokenize

    Returns:
    list: The tokenized comments
    """
    tokenized = []
    for comment in comments:
        word = word_tokenize(comment.lower())
        tokenized.append(word)
    return tokenized


def saveToFile(comments, filename):
    """
    Saves the comments to a file

    Parameters:
    comments (list): The comments to save
    filename (str): The name of the file to save the comments to

    Returns:
    None
    """
    with open(filename, "w", encoding="utf-8") as file:
        for comment in comments:
            file.write(comment + "\n")


def lemmatizeComments(tokenized):
    """
    Lemmatizes the comments

    Parameters:
    tokenized (list): The tokenized comments

    Returns:
    list: The lemmatized comments
    """
    wnl = WordNetLemmatizer()
    lemmatized = []
    for comment in tokenized:
        lemmatizedComment = " ".join([wnl.lemmatize(word) for word in comment])
        lemmatized.append(lemmatizedComment)
    return lemmatized


def getTFIDFVector(comments):
    """
    Gets the TF-IDF vector

    Parameters:
    comments (list): The comments to vectorize

    Returns:
    TF-IDF matrix
    """
    matrix = vectorizer.fit_transform(comments)
    return matrix


def getTFIDFFeatures():
    """
    Gets the TF-IDF features

    Returns:
    list: The TF-IDF features
    """
    return vectorizer.get_feature_names_out()


def getFeatureScores(feature_list, tfidf_matrix):
    """
    Gets the feature scores

    Parameters:
    feature_list (list): The list of features
    tfidf_matrix (matrix): The TF-IDF matrix

    Returns:
    list: The feature scores
    """
    scores = []
    tfidf_array = tfidf_matrix.toarray()
    for text in tfidf_array:
        text_scores = []
        for index, score in enumerate(text):
            if score > 0:
                print("\033[32m[PROCESS (FC)]\033[0m", score)
                text_scores.append(feature_list[index])
        scores.append(text_scores)
    return scores


def getMostImpactfulWords(tfidf_matrix, feature_list, n):
    """
    Gets the most impactful words

    Parameters:
    tfidf_matrix (matrix): The TF-IDF matrix
    feature_list (list): The list of features

    Returns:
    list: The most impactful words
    """
    word_scores = []
    tfidf_array = tfidf_matrix.toarray()

    for text_scores in tfidf_array:
        text_scores = [
            (feature_list[index], score)
            for index, score in enumerate(text_scores)
            if score > 0
        ]
        word_scores.extend(text_scores)

    word_scores.sort(key=lambda x: x[1], reverse=True)
    return [word for word, _ in word_scores[:n]]


def getSentimentScores(featureScores):
    """
    Gets the sentiment scores

    Parameters:
    featureScores (list): The feature scores

    Returns:
    list: The sentiment scores
    """
    analyzer = VSA()
    scores = []
    for features in featureScores:
        concatenated_features = " ".join(features)
        score = analyzer.polarity_scores(concatenated_features)
        scores.append(score)
    return scores


def getOverallAvgVSAScore(sentimentScores):
    """
    Gets the overall average VSA score

    Parameters:
    sentimentScores (list): The sentiment scores

    Returns:
    float: The overall average VSA score
    """
    total = 0
    for score in sentimentScores:
        total += score["compound"]
    return total / len(sentimentScores)


def getMostNegativeComment(sentimentScores, comments):
    """
    Gets the most negative comment
    
    Parameters:
    sentimentScores (list): The sentiment scores
    comments (list): The comments

    Returns:
    str: The most negative comment
    """
    mostNegative = 1
    for i in range(len(sentimentScores)):
        if sentimentScores[i]["compound"] < mostNegative:
            mostNegative = sentimentScores[i]["compound"]
            mostNegativeComment = comments[i]
    return mostNegativeComment, mostNegative


def getMostPositiveComment(sentimentScores, comments):
    """
    Gets the most positive comment

    Parameters:
    sentimentScores (list): The sentiment scores
    comments (list): The comments

    Returns:
    str: The most positive comment
    """
    mostPositive = -1
    for i in range(len(sentimentScores)):
        if sentimentScores[i]["compound"] > mostPositive:
            mostPositive = sentimentScores[i]["compound"]
            mostPositiveComment = comments[i]
    return mostPositiveComment, mostPositive

def htmlData(avg):
    """
    Processes the HTML data

    Parameters:
    avg (float): The average sentiment score

    Returns:
    str: The HTML data
    """
    if avg > 0.05:
        return '<div class="bg-gradient-to-r from-[#135541] to-[#0d3b18] flex gap-2 text-white font-bold text-xl py-2 px-3 rounded-[10px]"><i class="fa-solid fa-circle-check self-center text-green-500"></i><div class="">This videos comments seem to be<span class="text-green-500"> positive </span></div></div>'
    elif avg < -0.05:
        return '<div class="bg-gradient-to-r from-[#551313] to-[#3b0d0d] flex gap-2 text-white font-bold text-xl py-2 px-3 rounded-[10px]"><i class="fa-solid fa-circle-xmark self-center text-red-500"></i><div class="">This videos comments seem to be<span class="text-red-500"> negative </span></div></div>'
    else:
        return '<div class="bg-gradient-to-r from-[#194970] to-[#132a55] flex gap-2 text-white font-bold text-xl py-2 px-3 rounded-[10px]"><i class="fa-solid fa-circle-minus self-center text-blue-500"></i><div class="">This videos comments seem to be<span class="text-blue-500"> neutral </span></div></div>'
