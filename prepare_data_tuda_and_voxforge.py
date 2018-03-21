#! /usr/bin/env python

import os
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, os.path.pardir)))

import argparse

import pingu
from pingu.corpus import io
from pingu.corpus import subset

import text_cleaning


def clean_transcriptions(corpus):
    for utterance in corpus.utterances.values():
        transcription = utterance.label_lists['transcription'][0].value
        cleaned = text_cleaning.clean_sentence(transcription)
        utterance.label_lists['transcription'][0].value = cleaned


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare data for training.')
    parser.add_argument('tuda_path', type=str)
    parser.add_argument('voxforge_path', type=str)
    parser.add_argument('target_path', type=str)

    args = parser.parse_args()

    tuda_corpus = pingu.Corpus.load(args.tuda_path, reader='tuda')
    clean_transcriptions(tuda_corpus)

    voxforge_corpus = pingu.Corpus.load(args.voxforge_path, reader='voxforge')
    clean_transcriptions(voxforge_corpus)

    merged_corpus = pingu.Corpus.merge_corpora([tuda_corpus, voxforge_corpus])

    splitter = subset.Splitter(merged_corpus, random_seed=38)
    splits = splitter.split_by_length_of_utterances({'train': 0.7, 'dev': 0.15, 'test': 0.15})

    merged_corpus.import_subview('train', splits['train'])
    merged_corpus.import_subview('dev', splits['dev'])
    merged_corpus.import_subview('test', splits['test'])

    deepspeech_writer = io.MozillaDeepSpeechWriter(transcription_label_list_idx='transcription')
    deepspeech_writer.save(merged_corpus, args.target_path)
