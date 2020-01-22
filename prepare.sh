DATA_PATH=$1
LM_REPO=$2

#
# DATA
#

mkdir -p exp/data
python prepare_data.py \
    $DATA_PATH \
    exp/data

#
# VOCABULARY
#

# mkdir -p exp/vocab
# python prepare_vocab.py \
#     exp/vocab/sentences.txt \
#     -t $LM_REPO/data/normalized/europarl.txt \
#     -t $LM_REPO/data/normalized/news_commentary.txt \
#     -t $LM_REPO/data/normalized/tuda_text.txt \
#     -c $DATA_PATH

#
# LM
#

# mkdir -p exp/lm
# cp $LM_REPO/data/models/kenlm/full/lm_6.bin exp/lm/lm_6.bin
