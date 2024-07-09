# YouTube Sentiment Analyzer

### Overview 

This is a Python project that analyzes the sentiment of comments on YouTube videos. It uses the VADER sentiment analysis tool and TF-IDF to provide further information on what the comments think about the video. It also has a frontend powered by Flask.

![Screenshot of the website showing a review of the YouTube 2018 Rewind.](/static/example.png)

### ✨ Features
- Fetch comments from YouTube videos using the YouTube Data API.

- Analyze the sentiment of comments using VADER.
    
- Generate a wordcloud from the most important words.

### 📝 Prerequisites
- Python with PIP installed
- YouTube Data API key

> [!NOTE]
> Although this is a NodeJS project too, having node_modules installed is required only if editing TailwindCSS.

### 💽 Installation
1. Clone the repo:
    ```console
    $ git clone https://github.com/keanegrech/youtube-sentiment-analyzer.git
    $ cd youtube-sentiment-analyzer
    ```

2. Set up your API key:
    - Rename ```example.env``` to ```.env```
    - Add your API key to ```YSA_DATA_API_KEY="your key here"```

3. Run setup.py to install all required dependencies.

### 🎚️ Usage
1. Run the Flask app:

    Start the Flask web server to use the frontend
    ```console
    $ python main.py
    ```

2. Access the web interface

    Open your web browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000)
    > The default port is 5000, it can be changed from the .env file.

4. Fetch comments:

    Enter either a YouTube URL or video ID followed by the sample size of comments to begin processing.

5. Results:
    - You can see the videos title, like and comment count
    - See overall sentiment
    - See most positive and negative comment and their respective sentiment scores
    - Download comments as a txt file
    - Download word cloud of most important words