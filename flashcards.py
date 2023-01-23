import argparse
import csv
from fugashi import Tagger
from dictionary.dictionary import build_dict, build_jm_dict
from frequency.frequency import build_frequency_dict, build_rank_dict

frequency_dict = build_frequency_dict("frequency/bccwj.csv")
rank_dict = build_rank_dict("frequency/bccwj.csv")

def frequency_lookup(rank_or_frequency, lemma, pos_list):
    try:
        for pos in pos_list:
        # if we find one entry in the rank/frequency dict, move on to the next step, that's good enough, parser
        # doesn't know pos well enough to distinguish every time
            lookup = lemma + ' ' + pos
            if rank_or_frequency == "frequency":
                freq = int(frequency_dict[lookup])
            else:
                freq = int(rank_dict[lookup])
            return freq
    except KeyError:
        return 0

def main():
    parser = argparse.ArgumentParser(description="Parse a Japanese text and generate a csv of \
        vocabulary words and definitions. Set an optional alternative dictionary. Set an optional frequency rank or raw \
        frequency threshold to return only words less frequent than threshold. You can only \
        choose rank OR frequency, not both.")
    parser.add_argument("--text", required=True, help="Path to text file you want to parse")
    parser.add_argument("--dictionary_path", required=True, help="Path to dictionary file(s)")
    parser.add_argument("--jmdict", action="store_true", help="Use flag if path to dictionary is JMDict")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--rank_threshold", help="Rank threshold (minimum rank to return)")
    group.add_argument("--frequency_threshold", help="Frequency threshold (minimum frequency to return)")
    args = parser.parse_args()

    print("Building dictionaries...")
    if args.jmdict:
        dictionary = build_jm_dict(args.dictionary_path)
    else:
        dictionary = build_dict(args.dictionary_path)

    if args.frequency_threshold:
        threshold = int(args.frequency_threshold)
        rank_or_frequency = "frequency"
    elif args.rank_threshold:
        threshold = int(args.rank_threshold)
        rank_or_frequency = "rank"
    else:
        threshold = 0
        rank_or_frequency = "rank"

    words_not_found = open("words_not_found.txt", "w")

    print("Parsing text...")
    with open(args.text, "r") as file:
        text = file.read()

    tagger = Tagger("-Owakati")
    tagger.parse(text)

    print("Building flashcards list...")

    lemma_set = set()
    with open("flashcards.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter="\t")

        for word in tagger(text):
            lemma = word.feature.lemma
            pos_list = word.pos.split(",")

            # If the tagger identifies a lemma from the text, look it up. If user has specified
            # a rank or frequency threshold, only write words that are above the threshold.
            if lemma and (lemma not in lemma_set):
                freq = frequency_lookup(rank_or_frequency, lemma, pos_list)

                if freq > threshold or freq == 0:
                    try:
                        csvwriter.writerow([lemma, dictionary[lemma], freq])
                        lemma_set.add(lemma)

                    except KeyError:
                        words_not_found.write(lemma + " is not in the dictionary.\n")
            else:
                words_not_found.write(str(word) + " is not in the dictionary.\n")

    csvfile.close()
    words_not_found.close()

if __name__ == "__main__":
    main()


