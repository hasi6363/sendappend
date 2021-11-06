#!/usr/bin/python3

import os
import sys
import argparse
import subprocess
import shutil
import glob
import os.path
import re

# get dir_list (current organized title)
# for
#   get title
#   add title to title_list
#   if dir_list has title:
#     move file
#   else if title_list has title:
#     mkdir title
#     move file


def organize(dirname, f, f_basename):
    if os.path.exists(dirname) == False:
        print('mkdir: "' + dirname + '"')
        if args.dry_run == False:
            os.mkdir(dirname)
    
    #print('move from "' + f + '" to "' + os.path.join(dirname,f_basename) + '"')
    print('move to:' + dirname)
    if args.dry_run == False:
        shutil.move(f,os.path.join(dirname,f_basename))
        
def get_title(f_basename):
    title = re.sub(r'\[[0-9]{6}-[0-9]{4}\] |\[新\]|\[字\]|\[再\]|\[デ\]|\[終\]|\[ニ\]|\[生\]|\[解\]|\[多\]|\[出\]|\[実\]|\..*|\(.*\)|（.*）|【.*】|＜.*＞|～.*～|\[GR.{2}\]|\[Mirakurun \(UnixSocket\)\]|アニメ　|映画　','',f_basename)

    split_str = r'＃|▽|▼|★'
    special_str_list = ['ぐるナイ','火曜サプライズ','おしゃれイズム','ヒルナンデス！','サッカー★アース','有吉ゼミ','激レアさんを連れてきた。','イッテＱ！','ソレダメ！','タイプライターズ','スッキリ','サンデー・ジャポン','２４時間テレビ４３','世界一受けたい授業','踊る！さんま御殿！！']

    for sp_str in special_str_list:
        if re.search(sp_str, title) != None:
            title = sp_str
    
    if title[0] == '「':
        title = re.findall(r'「(.*)」', title)[0]
    else:
        title = re.sub(r'「.*」', '', title)
        if re.search(split_str,title) != None:
            title = re.split(split_str, title)[0]
        else:
            title = re.split(r'　| ',title)[0]
        if title[-1] == '　':
            title = title[:-1]
    return title

def get_dir_list():
    dir_list = list()
    for d in glob.glob('**'+os.sep):
        d = re.sub(os.sep, '', d)
        dir_list.append(d)
    return dir_list

def main():
    dir_list = get_dir_list()
    title_list = list()
    for f in glob.glob('*.mp4'):
        print('filename:' + f)
        f_basename = os.path.basename(f)
        if args.auto == True:
            title = get_title(f_basename)
            print('title:' + title)
            if title in dir_list:
                organize(title, f, f_basename)
            elif title in title_list:
                print('mkdir: "' + title + '"')
                if args.dry_run == False:
                    os.mkdir(title)
                    dir_list.append(title)
                organize(title, f, f_basename)
            else:
                title_list.append(title)
        else:
            title = args.name
            if title in f_basename:
                organize(title, f, f_basename)

parser = argparse.ArgumentParser()
parser.add_argument('--dir', required=True, help='target directory')
parser.add_argument('--dry-run', action='store_true')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--name', help='part of the title, etc.')
group.add_argument('--auto', action='store_true')
args = parser.parse_args()

os.chdir(args.dir)
main()
