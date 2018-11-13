# !/usr/bin/env python
# coding:utf-8
# Filename: json2doc.py
# Edited Time: 2018-11-12 09:35
# Writer: Haopeng Geng
'''
TODO:
   Parse json data and return texts whose classes are  defined in 'config/valid_classes'
RETURN:
   Pickle file(dict with index of every class) and 
   txt file ( where output can be checked) 
'''
import json
import jsonpath
import pickle as pkl
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input',
                    default='rawdata/semeval-2016_2017-task3-subtaskA-unannotated-english.json')
parser.add_argument('--output_txt',
                    default='result/output.txt')
parser.add_argument('--output_pkl',
                    default='result/output.pkl')
parser.add_argument('--valid_text_class_file',
                    default='config/valid_classes')
args = parser.parse_args()


def get_text(js_data, valid_c):
    res = []
    for x in valid_classes:
        print('----Start preprocessing %s----' % x)
        item = jsonpath.jsonpath(js_data, expr='$..'+x)
        print('----Add %s to output pickle file----' % x)
        res.append(item)
    return res


if __name__ == '__main__':

    with open(args.input, 'r') as f_input:
        rawdata = json.load(f_input)

    with open(args.valid_text_class_file, 'r') as f_valid_class:
        valid_classes = [str(x).strip('\n') for x in f_valid_class.readlines()]

    result_test = get_text(rawdata, valid_classes)

    with open(args.output_txt, 'w') as f_output:
        f_output.write(str(result_test))

    with open(args.output_pkl, 'wb') as f_pkl_output:
        print('----Pickle File written----')
        pkl.dump(result_test, f_pkl_output)
