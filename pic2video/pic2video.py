# -*- coding: utf-8 -*-
from __future__ import print_function
import logging
from threading import Timer, Lock
import srt_tools.utils
import srt
import sys
import time
import os


subtitle_generator = srt.parse('''\
1
00:31:37,894 --> 00:31:39,928
OK, look, I think I have a plan here.

2
00:31:39,931 --> 00:31:41,931
Using mainly spoons,

3
00:31:41,933 --> 00:31:43,435
we dig a tunnel under the city and release it into the wild.

''')
#subtitles = list(subtitle_generator)
#print(subtitles)


def mkdir(path):
	# ȥ����λ�ո�
	path=path.strip()
	# ȥ��β�� \ ����
	path=path.rstrip("\\")

	# �ж�·���Ƿ����
	# ����     True
	# ������   False
	isExists=os.path.exists(path)

	# �жϽ��
	if not isExists:
		# ����������򴴽�Ŀ¼
		# ����Ŀ¼��������
		os.makedirs(path) 

		return True
	else:
		# ���Ŀ¼�����򲻴���������ʾĿ¼�Ѵ���
		return False

def main():
	outputPath = "./out"
	width = 640
	height = 360

	mkdir(outputPath)

	logger = logging.getLogger("mylog")
	logger.setLevel(logging.DEBUG)
	# ����һ��filehandler������־��¼���ļ������Ϊdebug����
	fh = logging.FileHandler(".\\out\\logging.log", encoding="utf-8")
	fh.setLevel(logging.DEBUG)
	# ����һ��streamhandler������־����CMD�����ϣ�����Ϊerror����
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)
	# ������־��ʽ
	#formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	formatter = logging.Formatter("%(message)s")
	ch.setFormatter(formatter)
	fh.setFormatter(formatter)
	#����Ӧ��handler�����logger������
	logger.addHandler(ch)
	logger.addHandler(fh)

	args = srt_tools.utils.basic_parser(no_output=True).parse_args()
	logger.info(args)

	logging.basicConfig(level=args.log_level)
	srt_tools.utils.set_basic_args(args)
	logger.info(args.input)

	fileList = ''
	for sub in args.input:
		start = sub.start.total_seconds()
		end = sub.end.total_seconds()
		logger.info('#%s %s %s %s' % (sub.index, start, end, sub.content) + '\r\n')
		
		if os.path.exists('page%03d.jpg'%(sub.index)):
			cmd = 'ffmpeg -i page%03d.jpg -vf scale="trunc(iw*min(%d/(iw)\,%d/(ih))/2)*2:trunc(ih*min(%d/(iw)\,%d/(ih))/2)*2" -y %s/img%03d.jpg' % (sub.index, width, height, width, height, outputPath, sub.index)
			os.system(cmd)
			
			if sub.index == 1:
				cmd = 'ffmpeg -loop 1 -i %s/img%03d.jpg -t %f -c:v libx264 -y %s/silent%03d.ts' % (outputPath, sub.index, end, outputPath, sub.index)
			else:
				cmd = 'ffmpeg -loop 1 -i %s/img%03d.jpg -t %f -c:v libx264 -y %s/silent%03d.ts' % (outputPath, sub.index, end - lastEnd, outputPath, sub.index)

			fileList += '%s/silent%03d.ts|' % (outputPath, sub.index)
			
			lastEnd = end
			os.system(cmd)
		

	fileList = fileList[:-1]
	cmd = 'ffmpeg -i "concat:%s" -i audio.mp3  -acodec copy -vcodec copy -y %s/output.mp4' % (fileList, outputPath)
	os.system(cmd)

if __name__ == '__main__':
    main()