#!/bin/bash

set -e
stage=1

RAWDATA_DIR='./rawdata/'
mkdir -p $RAWDATA_DIR
RAWDATA="$RAWDATA_DIR/semeval-2016_2017-task3-subtaskA-unannotated-english.json"

VALID_CLASSES='config/valid_classes'

RESULT_DIR='./result'
PLAINTEXT_PATH="$RESULT_DIR/plain_texts/"
mkdir -p $PLAINTEXT_PATH

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
    fi
echo "Stage 1 Finished"
let stage++
fi

if [ $stage == 2 ]; then
    echo "Stage 2 Started"
    python run.py \
	   --input_pkl=$OUTPUT_PICKLE \
	   --valid_words=$VALID_WORDS \
	   --output_path=$PLAINTEXT_PATH
fi
echo "Stage 2 Finished"

echo "Plain texts are saved in $PLAINTEXT_PATH"

	
       
    

    
    

