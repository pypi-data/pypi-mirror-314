# Brewify

![Brew](https://images-ext-1.discordapp.net/external/qG41hZHbsmNVc9WSE6aX3oVWi_LP39dQZjxZgdIdFLI/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1076140187471593492/bfea312390b3b52773f1358457d7261b.png?format=webp&quality=lossless&width=427&height=427)

Brewify is a Python library that provides a simple interface to interact
with various APIs, including Google Search, IMDb, Discord, and more. It
is designed to be easy to use while allowing you to extend its
functionality.

## Features

-   **API Requests**: Make GET requests to various endpoints.
-   **Error Handling**: Custom exceptions for better error management.
-   **Multiple Services**: Access Google Images, IMDb, Discord, and
    more.
-   **Sentiment Analysis**: Analyze the sentiment of text.
-   **Chatbot Functionality**: Engage in simple conversations.
-   **Joke Generator**: Get a random joke.

## Installation

You can install Brewify via pip:

``` bash
pip install brewify
```

## Usage

**Initialize the Brewify Class**

To get started, initialize the [Brewify]{.title-ref} class with your API
key:

``` python
from brewify import Brewify

brewify = Brewify("YOUR_API_KEY")
```

**Example Methods**

*Get Google Images*

``` python
image_response = brewify.get_google_image(query="cats")
print(image_response.link)
```

*Search Google*

``` python
text_response = brewify.search_google(query="Python programming")
print(text_response.title, text_response.link, text_response.snippet)
```

*IMDb Search*

``` python
imdb_response = brewify.imdb_search(query="Inception")
print(imdb_response.plot)
```

*Discord Guild Search*

``` python
guild_response = brewify.discord_guild_search(invite_code="your_invite_code")
print(guild_response.id)
```

*Sentiment Analysis*

``` python
sentiment_response = brewify.sentiment_analysis(sentence="I love Python!")
print(sentiment_response.negative, sentiment_response.positive, sentiment_response.neutral)
```

*Get a Joke*

``` python
joke_response = brewify.joke()
print(f"{joke_response.setup} {joke_response.punchline}")
```

## Error Handling

Brewify raises a custom exception called [Brexception]{.title-ref} for
handling errors. You can catch it as follows:

``` python
try:
    brewify.some_method()
except Brexception as e:
    print(f"An error occurred: {e}")
```

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an
issue.

## License

This project is licensed under the MIT License - see the
[LICENSE] file for details.

## Acknowledgments

-   Thanks to the developers of the APIs used in this library.
-   Special thanks to [FastAPI](https://fastapi.tiangolo.com/) for
    making API development a breeze.