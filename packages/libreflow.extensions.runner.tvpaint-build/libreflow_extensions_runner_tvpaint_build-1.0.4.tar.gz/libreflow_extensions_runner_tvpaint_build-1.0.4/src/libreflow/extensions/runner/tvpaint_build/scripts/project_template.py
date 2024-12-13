import sys
import argparse

from pytvpaint import george
from pytvpaint.project import Project
import os
import time

start = time.time()
print("start", start)

def process_remaining_args(args):
    parser = argparse.ArgumentParser(
        description='TVPaint Project Template Arguments'
    )
    parser.add_argument('--ref-path', dest='ref_path')
    parser.add_argument('--audio-path', dest='audio_path')
    # parser.add_argument('--height', dest='height')
    # parser.add_argument('--width', dest='width')

    values, _ = parser.parse_known_args(args)

    return (
        values.ref_path,values.audio_path
    )

print("HALF")
ref_path = process_remaining_args(sys.argv)[0]# .replace(".mov", "_HALF.mov")
print(ref_path)
print("exists", os.path.exists(ref_path))
AUDIO_PATH = process_remaining_args(sys.argv)[1]
print(AUDIO_PATH)
print("exists", os.path.exists(AUDIO_PATH))
# CAMERA_WIDTH = process_remaining_args(sys.argv)[1]
# CAMER_HEIGHT = process_remaining_args(sys.argv)[2]

# change project resolution

print("get current project")
project = Project.current_project()
# project = Project.new(r"C:\projets\2h14\_2h14\sq060\sh0160\layout\layout_tvpp\thomasthiebaut\sq060_sh0160_layout.tvpp")
print(project)
clip = project.current_clip
camera = clip.camera

# project_width = camera_width+300
# project_height = camera_height+170

print("resize")
project = project.resize(4240,2385,overwrite=True)
# project = project.resize(1920,1080,overwrite=True)

project = Project.current_project()
# project = Project.new(r"C:\projets\2h14\_2h14\sq060\sh0160\layout\layout_tvpp\thomasthiebaut\sq060_sh0160_layout.tvpp")
print(project)
clip = project.current_clip
camera = clip.camera


print("set fps")
project.set_fps(25)
print(project)
# project.resize(project_width,project_height,overwrite=True)

print("set camera")
camera.get_point_data_at(0)
george.tv_camera_set_point(0,2120,1192,0,scale=1)
# george.tv_camera_set_point(0, project_width/2, project_height/2, 0, scale=1)

# -- import img sequence --

print("Loading", time.time() - start)
print("importing ref")
img_seq = clip.load_media(media_path=ref_path, with_name="[REF]", preload=True)
print("Loading done", time.time() - start)

# -- Import Audio --
print('importing audio')
audio = clip.add_sound(AUDIO_PATH)
clip = project.current_clip
print(clip)
print('audio imported')

print("resize 2")
project = project.resize(4240,2385,overwrite=True)
# -- change img seq layer position
img_seq.position = 1
print("Saving", time.time() - start)
print(project)
print("saving")
project.save()
print("importing closing")
project.close()
