#!/bin/bash
# Filename: run.sh
# Edited Time: 2018-11-15 21:13
# Writer: Haopeng Geng

# This is a toolkit for generating plaintext from json file
# With an Additional function which can also be used for xml file

set -e

stage=1
# Stage 1: Get pickle file from json file
# Stage 2: Generate plain text from pickle file  # (Refactoring Needed)
# Stage 3: Generate plain text from xml file  
# Stage 4: Training GloVe Vector from json and xml plain texts #(Refactoring Needed)


RAWDATA_DIR='./rawdata/'
mkdir -p $RAWDATA_DIR
RAWDATA="$RAWDATA_DIR/semeval-2016_2017-task3-subtaskA-unannotated-english.json"

VALID_CLASSES='config/valid_classes'

RESULT_DIR='./result'
PLAINTEXT_PATH="$RESULT_DIR/plain_texts/"
XML_PLAINTEXT_PATH="$RESULT_DIR/xml_plain_texts"

mkdir -p $PLAINTEXT_PATH
mkdir -p $XML_PLAINTEXT_PATH

OUTPUT_TXT="$RESULT_DIR/output.txt"
OUTPUT_PICKLE="$RESULT_DIR/output.pkl"

VALID_WORDS='config/valid_words'


if [ $stage == 1 ]; then
    echo "Stage 1 Started"
    if [ -s "./config/valid_classes" ]; then
	python json2doc.py \
	       --input $RAWDATA \
	       --output_txt $OUTPUT_TXT \
	       --output_pkl $OUTPUT_PICKLE \
	       --valid_text_class_file $VALID_CLASSES
	let $stage++
    fi
echo "Stage 1 Finished"
fi

if [ $stage == 2 ]; then
    echo "Stage 2 Started"
    echo "Generating plain text from json file"
    echo "It may take a LONG LONG time :)"
    python run.py \
	   --input_pkl=$OUTPUT_PICKLE \
	   --valid_words=$VALID_WORDS \
	   --output_path=$PLAINTEXT_PATH
    let $stage++

    echo "Stage 2 Finished"
    echo "Plain texts are saved in $PLAINTEXT_PATH"

fi

if [ $stage == 3 ]; then
    echo "Stage 3 Started"
    echo "Generating plain text from xml file"
    echo "It may take a LONG LONG time :)"
    python xml.py


    let stage++
    echo "Stage 3 Finished"
    echo "Plain texts are save in $XML_PLAINTEXT_PATH"

fi

if [ $stage == 4 ]; then
    echo "Stage 4 Started"
    echo "Training GloVe"
    
    if [ ! -d ./GloVe ]; then
	echo "Download Glove repo from Github"
	git clone https://github.com/stanfordnlp/GloVe.git
	cd GloVe && make
	./demo.sh
	cd ..
    fi

    echo "GloVe toolkit Avaliable"

    cat $PLAINTEXT_PATH/* > json
    cat $XML_PLAINTEXT_PATH/* > xml
    cat json xml > ./GloVe/text
    cd ./GloVe && ./train.sh
    cd ..
    rm json xml
    echo "GloVe result save in ./GloVe/vector.txt"
fi

   
