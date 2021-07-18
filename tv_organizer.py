#!/usr/bin/python3

import os
import sys
import argparse
import subprocess
import shutil
import glob
import os.path
import re

def exec_func(dirname, f, f_basename):
    if os.path.exists(dirname) == False:
        print('mkdir: "' + dirname + '"')
        if args.dry_run == False:
            os.mkdir(dirname)
    
    #print('move from "' + f + '" to "' + os.path.join(dirname,f_basename) + '"')
    print('move to:' + dirname)
    if args.dry_run == False:
        shutil.move(f,os.path.join(dirname,f_basename))

def main():
    for f in glob.glob('*.mp4'):
        f_basename = os.path.basename(f)
        print('filename:' + f)
        if args.auto == True:
            DIRNAME = re.sub(r'\[[0-9]{6}-[0-9]{4}\] |\[新\]|\[字\]|\[再\]|\[デ\]|\[終\]|\[ニ\]|\[生\]|\[解\]|\[出\]|\[実\]|\..*|\(.*\)|（.*）|【.*】|＜.*＞|～.*～|\[GR.{2}\]|\[Mirakurun \(UnixSocket\)\]|アニメ　|映画　','',f_basename)

            split_str = r'＃|▽|▼|★'
            special_str_list = ['ぐるナイ','火曜サプライズ','おしゃれイズム','ヒルナンデス！','サッカー★アース','有吉ゼミ','激レアさんを連れてきた。','イッテＱ！','ソレダメ！','タイプライターズ','スッキリ','サンデー・ジャポン','２４時間テレビ４３','世界一受けたい授業','踊る！さんま御殿！！']

            for sp_str in special_str_list:
                if re.search(sp_str, DIRNAME) != None:
                    DIRNAME = sp_str
            
            if DIRNAME[0] == '「':
                DIRNAME = re.findall(r'「(.*)」', DIRNAME)[0]
            else:
                DIRNAME = re.sub(r'「.*」', '', DIRNAME)
                if re.search(split_str,DIRNAME) != None:
                    DIRNAME = re.split(split_str, DIRNAME)[0]
                else:
                    DIRNAME = re.split(r'　| ',DIRNAME)[0]
                if DIRNAME[-1] == '　':
                    DIRNAME = DIRNAME[:-1]
            exec_func(DIRNAME, f, f_basename)
        else:
            DIRNAME = args.name
            if DIRNAME in f_basename:
                exec_func(DIRNAME, f, f_basename)

parser = argparse.ArgumentParser()
parser.add_argument('--dir', required=True, help='target directory')
parser.add_argument('--dry-run', action='store_true')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--name', help='part of the title, etc.')
group.add_argument('--auto', action='store_true')
args = parser.parse_args()

os.chdir(args.dir)
main()
