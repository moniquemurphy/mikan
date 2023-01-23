from os import listdir
from os.path import isfile, join
import json

def build_dict(path):
    dictionary = {}
    filenames = [f for f in listdir(path) if isfile(join(path, f))]

    for filename in filenames:
        file_path = ("{0}/{1}".format(path, filename))
        with open(file_path, "r") as read_file:
            data = json.load(read_file)
        for entry in data:
            word = entry[0]
            reading_and_def = entry[5][0]
            dictionary[word] = reading_and_def
    return dictionary

def build_jm_dict(path):
    dictionary = {}
    counter = 0
    with open (path, "r") as read_file:
        data = json.load(read_file)
    # word block
    for entry in data["words"]:
        if entry["kanji"]:
            for kanji in entry["kanji"]:
                word = kanji["text"]
                gloss = build_gloss_string(entry)
        else:
            for kana in entry["kana"]:
                word = kana["text"]
                gloss = build_gloss_string(entry)
        dictionary[word] = gloss
    return dictionary

def build_gloss_string(entry):
    out_string = ""
    gloss_list = []
    for sense in entry["sense"]:
        for gloss in sense["gloss"]:
            gloss_list.append(gloss["text"])
    out_string = ", ".join(gloss_list)
    return out_string