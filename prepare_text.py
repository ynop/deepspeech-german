#! /usr/bin/env python

import os
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, os.path.pardir)))

import argparse

import text_cleaning

parser = argparse.ArgumentParser(description='Clean text corpus.')
parser.add_argument('source_path', type=str)
parser.add_argument('target_path', type=str)

args = parser.parse_args()

index = 0

with open(args.source_path, 'r') as source_file, open(args.target_path, 'w') as target_file:
    for index, line in enumerate(source_file):
        cleaned_sentence = text_cleaning.clean_sentence(line)
        target_file.write('{}\n'.format(cleaned_sentence))

        if index % 1000 == 0:
            print(index)

print('Cleaned {} lines!'.format(index))
