#!/usr/bin/env bash

deepspeech_path=$(realpath $1)
alphabet_path=$(realpath $2)
exp_path=$(realpath $3)

current_dir=$(pwd)
cd $deepspeech_path

if [ ! -f DeepSpeech.py ]; then
    echo "Please make sure you run this from DeepSpeech's top level directory."
    exit 1
fi;

mkdir -p $exp_path/tmp

python -u DeepSpeech.py --noearly_stop \
    --alphabet_config_path $alphabet_path \
    --train_files $exp_path/data/train.csv \
    --train_batch_size 32 \
    --feature_cache $exp_path/tmp/featcache \
    --dev_files $exp_path/data/dev.csv \
    --dev_batch_size 16 \
    --test_files $exp_path/data/test.csv \
    --test_batch_size 16 \
    --epochs 100 \
    --checkpoint_dir $exp_path/checkpoints \
    --learning_rate 0.0005 \
    --dropout_rate 0.2  \
    --export_dir $exp_path/output \
    --lm_binary_path $exp_path/lm/lm_6.bin \
    --lm_trie_path $exp_path/trie \
    --audio_sample_rate 16000

cd $current_dir
