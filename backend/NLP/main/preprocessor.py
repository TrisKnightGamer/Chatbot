import numpy as np
from pyvi import ViTokenizer
from NLP.main.vi_stop_words import STOP_WORDS   #NLP.main.
from NLP.main.vi_spec_words import SPEC_WORDS   #NLP.main.
import pandas as pd
import os
import numpy as np


class Preprocessor:
    def __init__(self):
        path = os.getcwd().split("\\")
        root_dir = path[:-1]
        self.root_dir = '/'.join(root_dir)
        self.data_path = self.root_dir + '/data'
        #self.data_path = self.root_dir + '/data'
        self.raw_path = self.data_path + '/raw'
        self.csv_path = self.data_path + '/processed_data4.csv'
        #self.data_path = '/Volumes/ESD-USB/share/chatobt/backend/NLP/data/processed_data3.csv'

    def tokenize_sentence(self, sentence):
        for spec in SPEC_WORDS:
            sentence = sentence.replace(spec, ' ')
        sentence = ViTokenizer.tokenize(sentence)
        words = sentence.rsplit()
        words = [w for w in words if w not in STOP_WORDS]
        sentence = ''
        for w in words:
            sentence += w + ' '
        return sentence[:-1]


    def tokenize_list_sentences(self, list_sentences):
        df_tokened = []   
        for sen in list_sentences:
            try:
                #sen1 = sen
                sen = sen.strip()
                sen = sen.lower()
                tokened_sen = self.tokenize_sentence(sen)
                if len(tokened_sen) > 0:
                    df_tokened.append(tokened_sen)
                    #df_tokened += str(sen)
                    #df_tokened = [] # kiểu float k dùng strip đc nên nó báo
                    #df_tokened.append(tokened_sen)
            except:
                continue
        return df_tokened

    def tokenize_file(self, input_path, label):
        input_file = open(input_path, 'r', encoding="utf8", errors='ignore')
        lines = list(input_file.readlines())
        token_lines = self.tokenize_list_sentences(lines)
        token_lines = np.array(token_lines)
        token_lines = token_lines.reshape(-1,1)
        label_tag = np.full_like(token_lines, fill_value=label)
        label_tag = label_tag.reshape(-1, 1)
        df = np.concatenate((token_lines, label_tag), axis=1)
        input_file.close()
        return df

    def save_csv(self, df, output_path):
        df = pd.DataFrame(df, columns=['feature', 'label'])
        df.to_csv(output_path, header=False, mode='a')
        print("Saved csv ~")

    def run(self):
        for folder in os.listdir(self.raw_path):
            sub_path = self.raw_path + '/' +folder
            for raw_file in os.listdir(sub_path):
                input_file_path = sub_path + '/' + raw_file
                print(os.path.splitext(raw_file)[0])
                if os.path.splitext(raw_file)[0] != '._general_asking':
                    label = os.path.splitext(raw_file)[0]
                    df = self.tokenize_file(input_path=input_file_path,label=label)
                    self.save_csv(df, self.csv_path)


if __name__ == "__main__":
    p = Preprocessor()
    print("Start preprocessing ... ")
    p.run()
    print("Done !")
