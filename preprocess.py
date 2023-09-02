import argparse
import text
import csv
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("--out_extension", default="cleaned")
parser.add_argument("--csv_delimiter", type=str, default='|')
parser.add_argument("--filelists", nargs="+", default=["filelists/ljs_audio_text_val_filelist.txt", "filelists/ljs_audio_text_test_filelist.txt"])
parser.add_argument("--text_cleaners", nargs="+", default=["english_cleaners2"])

def main():
    args = parser.parse_args()

    for filelist in args.filelists:
        print("START:", filelist)

        with open(filelist + '.' + args.out_extension, 'w', encoding='utf-8') as cleaned_file:
            filelist_lines = open(filelist, encoding='utf-8').readlines()
            filelist_csv_reader = csv.reader(filelist_lines, delimiter=args.csv_delimiter)

            original_texts = []
            filepaths = []

            for (filepath, original_text) in tqdm(filelist_csv_reader, total=len(filelist_lines)):
                original_texts.append(original_text)
                filepaths.append(filepath)

            cleaned_texts = text._clean_text(original_texts, cleaner_names=args.text_cleaners)
            cleaned_file.write('\n'.join(f'{filepath}|{original_text}' for filepath, original_text in zip(filepaths, cleaned_texts)))
    
    return

if __name__ == '__main__':
    main()