# mikan

## Introduction

This package runs a script to extract Japanese vocabulary from a text, glosses each word, and puts the results in a tab-delimited CSV file. This file can then be imported into Anki or used as a reference list while reading.

You can also restrict which words are glossed by frequency rank (1 being the most frequent word in Japanese, and higher numbers because less frequent) or frequency value (lower being less frequent) from the [BCCWJ corpus](https://clrd.ninjal.ac.jp/bccwj/en/).

It uses [fugashi](https://github.com/polm/fugashi) to parse and tag Japanese text and the [JMDict Simplified English Only](https://github.com/scriptin/jmdict-simplified/releases/tag/3.3.1+20230123121924) JSON file to gloss as default.

## Why does this exist?

One of the most helpful Japanese courses I ever took forced us to memorize a bunch of vocab words out of context the day before class, and then we would encounter the words in a text during class. I wanted to mock this experience (which is commonly used with guided readers as well) without having to read through the text and look words up manually.

## Instructions

1. Install requirements with  `pip install -r requirements.txt`
2. Install fugashi with unidic with `pip install fugashi[unidic]` and download the unidic file with `python -m unidic download`
3. Download the JMDict Simplified English only json file and place it in the "dictionary" directory (or, if you know what you're doing, place it wherever you like and refer to it using the `--dictionary_path` argument).
3. Create a text file with the text you want to parse and gloss. Create the text file inside the `mikan` top-level folder if you don't do much computer stuff and just want to make it work, otherwise, place it where you like and refer to it by path.
4. Run the script with no frills with `python flashcards.py --text <path-to-text.txt> --dictionary_path "dictionary/jmdict-eng-3.3.1.json" --jmdict`. You can view the generated CSV file as `flashcards.csv`. Words not found in the dictionary will be in a text file called `words_not_found.txt`
5. To run the script with a frequency or rank threshold (example: only gloss words that are less frequent than the top 1000 words), add a `--rank_threshold` or `--frequency_threshold` argument. (Example: `python flashcards.py --text <path-to-text.txt> --dictionary_path <path-to-dictionary> --jmdict --rank_threshold 1000`)

## Notes
* JMDict is recommended because it is freely available. If you have local files you would rather use, you can see `build_dict` in `dictionary.py` for an example using a folder with multiple json files from a JSONified EPWING file (https://github.com/FooSoft/zero-epwing).
* Kana/readings are not included because it was too much of a pain, tbh, but if you use something like [Japanese Input](https://ankiweb.net/shared/info/3918629684) for Anki, you can zoom through adding furigana to cards.
* This is an imperfect tool, and merely a jumping-off point for learning. It's highly recommended you read through your text and look up any words that seem odd on your own.
* It's not the fastest thing in the world. This is a little side project I made for myself, and I haven't done much in the way of refactoring or optimization. If you're a python whiz and you'd like to PR to clean anything up, contributions are welcome!