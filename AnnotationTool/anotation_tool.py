# script to annotate more easy
# author: Matisse Colombon

import csv
import os
import time
from statistics import mean



def main():
    start_line = input('Start line? (0-based)')
    desired_lines = int(input('How many lines do you want to annotate?'))
    start_line = int(start_line)

    anon_times = [7]

    raw_data = load_data('data/data_raw.csv')

    writer = touch_anotation_file('data/data_annotation.csv')

    for i, line in enumerate(raw_data[start_line + 1:]):
        print('anotations done: ' + str(i))
        print('anotations left: ' + str(desired_lines - i))
        estimated_time_left_minutes = ((desired_lines - i) * mean(anon_times)) / 60
        print('estimated time left: ' + str(estimated_time_left_minutes) + ' minutes')
        print_reply_and_tweet(line[2], line[4])
        # start timer
        start_time = time.time()
        get_anotation_from_user(writer, line)

        # end timer
        end_time = time.time()
        time_taken = end_time - start_time
        anon_times.append(time_taken)
        print('Annotation took: ' + str(time_taken) + ' seconds')


   # start_line = input('Start line? (0-based)')
   # start_line = int(start_line)

    #for line in raw_data[start_line + 1:]:
       # print_reply_and_tweet(line[2], line[4])
        #get_anotation_from_user(writer, line)


def load_data(raw_data_path):
    with open(raw_data_path, 'r', encoding="ISO-8859-1") as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

def touch_anotation_file(anotation_file_path):
    # create csv if not exist if exist open csv
    # check if file already exists
    # if not create file
    # return writer
    if not os.path.isfile(anotation_file_path):
        f = open(anotation_file_path, 'w', encoding="ISO-8859-1")
        writer = csv.writer(f)
        writer.writerow(['line_nr', 'hate', 'explicit', 'target', 'annotator_notes' 'root_tweet', 'reply_tweet'])
    else:
        f = open(anotation_file_path, 'a', encoding="ISO-8859-1")
        writer = csv.writer(f)

    return writer


def print_reply_and_tweet(reply_tweet, root_tweet):
    reply_tweet = chop_tweet(reply_tweet)
    root_tweet = chop_tweet(root_tweet)
    print('Root Tweet:\n ' + root_tweet)
    print('------------------------------------------------------------------------------------')
    print('Reply Tweet:\n ' + reply_tweet)
    print('------------------------------------------------------------------------------------')

def chop_tweet(tweet):
    # add new lines to tweet if tweet contains more than 30 words
    # return tweet
    words = tweet.split(' ')
    if len(words) > 30:
        tweet = ''
        for i in range(0, len(words), 30):
            tweet += ' '.join(words[i:i+30]) + '\n'
    return tweet

def get_anotation_from_user(writer, line):
    # get user input for anotation
    # write to csv
    targets = ['race', 'nationality', 'religion', 'sex', 'ideology', 'disability', 'misogyny']
    hate = input('hate? (y/n)')

    if hate == 'y':
        explicit = input('explicit? (y/n)')
        # print targets
        print('Available targets: please use number after target')
        for i, target in enumerate(targets):
            print(target + ': ' + str(i), end=';  ')
        target = input('\ntarget?')
    else:
        explicit = ''
        target = ''
    anotation_notes = input('annotator notes? (optional)')


    writer.writerow([line[0], hate, explicit, target,anotation_notes, line[2], line[4]])


if __name__ == '__main__':
    main()
