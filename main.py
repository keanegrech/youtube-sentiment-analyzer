from flask import Flask, render_template, request
import fetch
import process
import visualisation
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print("\033[32m[INFO]\033[0m POST request received. Processing form data...")
        try:
            status = "No data yet"

            status = "\033[32m[INFO]\033[0m Retrieving form data..."
            print(status)
            userInput = request.form["ytId"]
            amount = request.form["amount"]

            status = "\033[32m[INFO]\033[0m Getting Video ID..."
            print(status)
            ytId = process.processUserInput(userInput)
            
            status = "\033[32m[INFO]\033[0m Fetching comments..."
            print(status)
            comments = fetch.getComments(ytId, amount)

            status = "\033[32m[INFO]\033[0m Tokenizing comments..."
            print(status)
            tokenized = process.tokenizeComments(comments)

            status = "\033[32m[INFO]\033[0m Lemmatizing comments..."
            print(status)
            lemmatized = process.lemmatizeComments(tokenized)

            status = "\033[32m[INFO]\033[0m Getting TF-IDF vector..."
            print(status)
            tfidf_matrix = process.getTFIDFVector(lemmatized)

            status = "\033[32m[INFO]\033[0m Getting TF-IDF features..."
            print(status)
            feature_list = process.getTFIDFFeatures()

            status = "\033[32m[INFO]\033[0m Getting feature scores..."
            print(status)
            featureScores = process.getFeatureScores(feature_list, tfidf_matrix)

            status = "\033[32m[INFO]\033[0m Getting sentiment scores..."
            print(status)
            sentimentScores = process.getSentimentScores(featureScores)

            status = "\033[32m[INFO]\033[0m Getting most impactful words..."
            print(status)
            mostImpactfulWords = process.getMostImpactfulWords(tfidf_matrix, feature_list, 5)

            status = "\033[32m[INFO]\033[0m Getting most negative and positive comments and their respective scores..."
            print(status)
            mostNegativeComment = process.getMostNegativeComment(sentimentScores, comments)[0]
            mostNegativeCommentScore = process.getMostNegativeComment(sentimentScores, comments)[1]

            mostPositiveComment = process.getMostPositiveComment(sentimentScores, comments)[0]
            mostPositiveCommentScore = process.getMostPositiveComment(sentimentScores, comments)[1]

            status = "\033[32m[INFO]\033[0m Saving comments to file..."
            print(status)
            process.saveToFile(comments, "static/comments.txt")

            #! Debug (not necessary)
            for i in range(len(featureScores)):
                print("\033[32m[PROCESS (CP)]\033[0m Processing comment ", i + 1)
                print("Comment: ", comments[i])
                print("Features: ", featureScores[i])
                print("Sentiment Score: ", sentimentScores[i])
                print("\n")

            status = "\033[32m[INFO]\033[0m Generating word cloud..."
            print(status)
            visualisation.generateWordCloud(mostImpactfulWords, 800, 800, "static/wordcloud.png")

            # Get the overall average VSA score.
            status = "\033[32m[INFO]\033[0m Getting overall average VSA score..."
            print(status)
            avgScore = process.getOverallAvgVSAScore(sentimentScores)

            # Process the HTML data.
            status = "\033[32m[INFO]\033[0m Processing HTML data..."
            print(status)
            htmlData = process.htmlData(avgScore)
        except Exception as e:
            print("\033[31m[ERROR]\033[0m An error occurred while processing the form data. Failed at: ", status)
            print("\033[31m[ERROR]\033[0m Error: ", e)
            return render_template("error.html", error=e, status=status)

        # Render a new page with the form data.
        return render_template(
            "results.html",
            ytId=ytId,
            amount=amount,
            title=fetch.getTitle(ytId),
            thumbnailURL=fetch.getThumbnailURL(ytId),
            channelTitle=fetch.getChannelTitle(ytId),
            datePublished=fetch.getDatePublished(ytId),
            likeCount=visualisation.formatNumber(fetch.getLikeCount(ytId)),
            commentCount=visualisation.formatNumber(fetch.getCommentCount(ytId)),
            htmlData=htmlData,
            mostImpactfulWords=mostImpactfulWords,
            mostNegativeComment=mostNegativeComment,
            mostNegativeCommentScore=mostNegativeCommentScore,
            mostPositiveComment=mostPositiveComment,
            mostPositiveCommentScore=mostPositiveCommentScore
        )

    # This is a GET request, so just render the index page.
    return render_template("index.html")


if __name__ == "__main__":
    debug_mode = os.getenv("YSA_FLASK_DEBUG_MODE")
    if debug_mode is not None:
        debug_mode = debug_mode.lower() == "true"
    else:
        debug_mode = False

    app.run(debug=debug_mode, port=os.getenv("YSA_FLASK_PORT"))