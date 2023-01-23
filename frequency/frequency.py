import csv

def build_frequency_dict(path):

    frequency_dict = {}

    with open(path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pos_list = row['pos'].split('-')
            for pos in pos_list:
                word = row['lemma'] + ' ' + pos
                frequency = row['frequency']

                try:
                    frequency_dict[word]
                except KeyError:
                    frequency_dict[word] = frequency

    return frequency_dict

def build_rank_dict(path):
    rank_dict = {}

    with open(path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
                pos_list = row['pos'].split('-')
                for pos in pos_list:
                    word = row['lemma'] + ' ' + pos
                    rank = row['rank']

                    try:
                        rank_dict[word]
                    except KeyError:                
                        rank_dict[word] = rank

    return rank_dict