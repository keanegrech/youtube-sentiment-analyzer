from matplotlib import pyplot as plt
from wordcloud import WordCloud as WordCloudCreator

def generateWordCloud(input, width, height, path):
    """
    Generates a word cloud from the input text and saves it to the given path

    Parameters:
    input (list): The input text
    width (int): The width of the word cloud
    height (int): The height of the word cloud
    path (str): The path to save the word cloud

    Returns:
    None
    """
    # generate a single string from the input list
    text = (" ").join(input)
    # Generate a wordcloud with the given dimensions
    cloud = WordCloudCreator(width=width, height=height, collocations=False).generate(
        text
    )
    # Save the wordcloud to file
    cloud.to_file(path)

def formatNumber(num):
    """
    Formats a number with commas and no decimal places

    Parameters:
    num (str): The number to format

    Returns:
    str: The formatted number
    """
    return "{:,.0f}".format(float(num))