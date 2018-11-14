import pickle as pkl
import json
import os
import xml.etree.ElementTree as ET

xml_path = './rawdata/xml/'
xmls = os.listdir(xml_path)
os.path.join(xml_path)
for f_n in xmls:
    t_f_n = xml_path + f_n
    root = ET.parse(t_f_n).getroot()
    for child in root:
        print(child.tag)

# with open('./data/dataset.pkl', 'rb') as fr, \
#      open('./data/embedding_matrix.pkl', 'rb') as fr_embed, \
#      open('./data/char2index.json', 'r') as fr_char:
#     data = pkl.load(fr)
#     embedding_matrix = pkl.load(fr_embed)
#     char2index = json.load(fr_char)

# train_list = ['15dev', '15test', '15train', '16dev', '16test', '16train1', '16train2', '17test']
    
# train_samples = embedding_matrix[']
# print(train_samples)
    
