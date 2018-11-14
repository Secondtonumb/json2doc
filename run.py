import pickle
import re
import spacy
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_pkl',
                    default='result/output.pkl',
                    help='input pickle file, format=dict[T_class_1, T_class_2, ...m T_class_n]')
parser.add_argument('--valid_words',
                    default='config/valid_words',
                    help='valid_words dictionary')
parser.add_argument('--output_path',
                    default='result/plain_texts/')
args = parser.parse_args()

nlp = spacy.load('en')


def clean_html(text):
    imp_ptn = re.compile(r'<img.*?>')
    href_ptn = re.compile(r'<.*?href.*?><.*?>')
    em_ptn = re.compile(r'<em>.*?</em>')
    center_ptn = re.compile(r'<center>')
    text = re.sub(imp_ptn, 'img_mark', text)
    text = re.sub(href_ptn, ' ', text)
    text = re.sub(em_ptn, 'em_mark', text)
    text = re.sub(center_ptn, ' ', text)
    return text


def tokenizer(text, need_punct=False):
    if need_punct:
        return [word.orth_ for word in nlp(text) if not word.is_space]
    else:
        return [word.orth_ for word in nlp(text) if not word.is_punct and not word.is_space]


def is_website(w):
    if('http' in w and '/' in w) or ('.com' in w and '@' not in w):
        return True
    else:
        return False


def is_email(w):
    if('@') in w and('.com' in w or '.cn' in w):
        return True
    else:
        return False


def is_number(w):
    if re.search(r'[^\d, ]', w):
        return False
    return True


def is_time(w):
    if re.search(r'[^\d\.]', w):
        return False
    return True


def is_atperson(w):
    arperson_re = re.compile(r'^@\w+$')
    if arperson_re.match(w):
        return True
    else:
        return False


def check_word(text, valid_words_dict, need_check=False):
    '''
    text:
      text without preprocessed
    valid_words_dict: 
      import valid word dictionary from outside
      If need_check = True, then only append valid words
      both in "text" and 'valid_words_dict" , or word will
       be changed into <unk>
    -----------
    RETURN:
      new_text: cleaned text
    '''
    new_text = []
    for w in text:
        # w = word.lower().strip()
        # print(w)
        if is_website(w):
            new_text.append('<url>')
        elif is_email(w):
            new_text.append('<email>')
        elif is_number(w):
            new_text.append('<number>')
        elif is_time(w):
            new_text.append('<time>')
        elif is_atperson(w):
            new_text.append('<atperson>')
        elif w == 'img_mark':
            new_text.append('<img>')
        elif need_check==True:
            if w in valid_words_dict:
                new_text.append(w)
            else:
                new_text.append('<unk>')
            # # # remove punctuation
            # w = remove_punct(w)
            # fine_text = []
            # for i, w_fine in enumerate(w):
            #     if is_number(w_fine):
            #         fine_text.append('<number>')
            #     elif w_fine in word_vector_keys:
            #         fine_text.append(w_fine)
            #     elif i>0 and fine_text[i-1] is '<unk>':
            #         fine_text.append('<unk>')
        else:
            new_text.append(w)
    if len(new_text) == 0:
        return ['<blank>']
    return new_text


def generate_plain_text(Ts, output_file_name):
    plain_text = []
    for item in tqdm(Ts):
        item = clean_html(item)
        final_text = check_word(tokenizer(item,
                                          need_punct=False),
                                valid_words_dict=valid_words,
                                need_check=False)
        plain_text.append(final_text)

    with open(output_file_name, 'w') as f_opt:
        for item in tqdm(plain_text):
            print(*item, file=f_opt)


if __name__ == '__main__':

    with open(args.input_pkl, 'rb') as f_pkl:
        Contents = pickle.load(f_pkl)
    with open(args.valid_words, 'r') as f_vw:
        valid_words = [str(x).strip('\n') for x in f_vw.readlines()]

    for cls in Contents:
        generate_plain_text(cls,
                            args.output_path + str(Contents.index(cls)) + '_plain_text')
