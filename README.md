# DeepSpeech German
This repository contains scripts used to test deepspeech (https://github.com/mozilla/DeepSpeech).

## Requirements
First, create a virtual-env.
Install requirements from this repository ``pip install -r requirements.txt``.
Next, download or clone deepspeech (v0.6.1)
[https://github.com/mozilla/DeepSpeech/releases/tag/v0.6.1](https://github.com/mozilla/DeepSpeech/releases/tag/v0.6.1).
Install Deepspeech dependencies.

```
pip install -r requirements.txt
pip3 uninstall tensorflow
pip3 install 'tensorflow-gpu==1.14.0'
python3 util/taskcluster.py --target native_client --branch "v0.2.0-alpha.8" --arch gpu
```

## Preparation

```
./prepare.sh \
    [german-asr-data]/data/full_waverized \
    [german-asr-lm]
```

## Training

### Generate Trie
```
exp/DeepSpeech-0.6.1/native_client/generate_trie data/alphabet.txt exp/lm/lm_6.bin exp/trie
```

### Training
```
./run_training.sh \
    exp/DeepSpeech-0.6.1 \
    data/alphabet.txt \
    exp
```
