#!/usr/bin/python3

import os
import sys
import argparse
import subprocess
import shutil
import glob
import os.path

def convert(f_input, f_output):
    print('#### CONVERT START ####')
    loglevel = f'-loglevel {args.loglevel}'
    analyzeduration = f'-analyzeduration 60M'
    probesize = f'-probesize 60M'
    if args.codec == 'libx264':
        hwaccel = ''
        hwoptions = ''
        options = '-preset veryfast -tune animation,zerolatency -movflags +faststart -vsync 1 -threads 8'
        vcodec = '-c:v libx264'
        voptions = '-crf 23 -deinterlace'
        acodec = '-c:a ac3'
        #aoptions = '-bsf:a aac_adtstoasc -fflags +discardcorrupt'
        aoptions = ''
    elif args.codec == 'h264_vaapi':
        hwaccel = '-vaapi_device /dev/dri/renderD128 -hwaccel vaapi -hwaccel_output_format vaapi'
        hwoptions = '-vf "format=nv12|vaapi,hwupload,deinterlace_vaapi,scale_vaapi=w=1280:h=720"'
        options = '-preset veryfast -tune animation,zerolatency -movflags +faststart -vsync 1'
        vcodec = '-c:v h264_vaapi'
        voptions = '-level 41 -b:v 6M'
        #vquality = '-qp:v 30'
        acodec = '-c:a ac3'
        #aoptions = '-bsf:a aac_adtstoasc -fflags +discardcorrupt'
        aoptions = ''
    elif args.codec == 'h264_nvenc':
        hwaccel = '-hwaccel cuvid -c:v mpeg2_cuvid'  
        #hwaccel = ''
        hwoptions = '-deint adaptive -drop_second_field 1'
        #hwoptions = ''
        options = ''
        vcodec = '-c:v h264_nvenc'
        #voptions = '-rc constqp -qp 24 -zerolatency 1'
        voptions = '-preset:v medium -profile:v high -spatial-aq 1 -zerolatency 1'
        acodec = '-c:a ac3'
        #aoptions = '-bsf:a aac_adtstoasc -fflags +discardcorrupt'
        aoptions = ''
    others = ''#'-s:c copy'
    command = f'ffmpeg {analyzeduration} {probesize} {hwaccel} {hwoptions} -i "{f_input}" {options} {vcodec} {voptions} {acodec} {aoptions} {loglevel} {others} "{f_output}"'
    
    print(command)
    ret = 0
    if args.dry_run == False:
        ret = -1
        ret = subprocess.run(command,shell=True,check=True)
    print('#### CONVERT FINISH ####')
    return ret

def main():
    count = 0
    filelist = sorted(glob.glob(os.path.join(args.input_dir,'**/*.m2ts'), recursive=True))
    for f in filelist:
        if args.max != 0 and count >= args.max:
            break
        print('#### START ####')
        # input_dir = m2ts
        # output_dir = mp4
        # f_input = m2ts/anime/title/file.m2ts
        f_input = f
        # f_input_rel = anime/title/file.m2ts
        f_input_rel = os.path.relpath(f,args.input_dir)
        # f_output = anime/title/file.mp4
        f_output = os.path.splitext(f_input_rel)[0] + '.mp4'
        # f_output = mp4/anime/title/file.mp4
        f_output = os.path.join(args.output_dir, f_output)
        # dir_output = mp4/anime/title
        dir_output = os.path.dirname(f_output)
        # dir_done = m2ts/done
        dir_done = os.path.join(args.input_dir, 'done')
        # f_input_done = m2ts/done/anime/title/file.m2ts        
        f_input_done = os.path.join(dir_done, f_input_rel)
        # f_input_done_dir = m2ts/done/anime/title
        f_input_done_dir = os.path.dirname(f_input_done)
    
        if dir_done in f:
            continue
        if (args.test == True or os.path.exists(f_output) == False) and args.no_encode == False:
            if os.path.exists(dir_output) == False:
                print('mkdir: ' + dir_output)
                if args.dry_run == False:
                    os.mkdir(dir_output)
            print('Convet from: ' + f_input)
            print('         to: ' + f_output)
            if args.dry_run == False:
                convert_result = convert(f_input, f_output)
                print('convert result: ' + convert_result)
        else:
            print('#### NO CONVERT ####')
        
        if args.test == False and os.path.exists(f_output) == True:
            if args.move_done == True:
                if os.path.exists(f_input_done_dir) == False:
                    print('mkdir: ' + f_input_done_dir)
                    if args.dry_run == False:
                        os.mkdir(f_input_done_dir)
                print('Move from: ' + f_input)
                print('       to: ' + f_input_done)
                if args.dry_run == False:
                    if convert_result == 0:
                        shutil.move(f_input, f_input_done)
                    else:
                        print('no move because convert is failed:' + convert_result)
            elif args.delete_m2ts == True:
                print('Delete: '+ f_input)
                if args.dry_run == False:
                    os.remove(f_input)
        count += 1
        print('#### FINISH ####')
    cmd_del_empty_dir = 'find '
    subprocess.run(f'find {input_dir} -type d -empty -delete', shell=True)
    print('#### ALL FILES FINISHED ####')

parser = argparse.ArgumentParser()
parser.add_argument('--input-dir', required=True, help='input directory')
parser.add_argument('--output-dir', required=True, help='output directory')
parser.add_argument('--codec', choices=['libx264','h264_vaapi','h264_qsv','h264_nvenc'],default='libx264')
parser.add_argument('--max', type=int, default=0)
parser.add_argument('--test', action='store_true')
parser.add_argument('--loglevel', choices=['quiet','fatal','error','warning','info','verbose','debug'],default='warning')
parser.add_argument('--dry-run', action='store_true')
group = parser.add_mutually_exclusive_group()
group.add_argument('--move-done', action='store_true')
group.add_argument('--delete-m2ts', action='store_true')
parser.add_argument('--no-encode', action='store_true')
args = parser.parse_args()

main()
