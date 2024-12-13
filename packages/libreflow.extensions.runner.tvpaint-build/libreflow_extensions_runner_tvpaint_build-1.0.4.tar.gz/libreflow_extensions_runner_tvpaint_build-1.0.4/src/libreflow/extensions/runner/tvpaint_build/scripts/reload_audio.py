import sys
import argparse
import os

from pytvpaint import george
from pytvpaint.project import Project

print ("RELOADING AUDIO")

def process_remaining_args(args):
    parser = argparse.ArgumentParser(
        description='TVPaint Project Template Arguments'
    )
    parser.add_argument('--file-path', dest='file_path')
    parser.add_argument('--audio-path', dest='audio_path')

    values, _ = parser.parse_known_args(args)

    return (
        values.audio_path,values.file_path
    )

AUDIO_PATH, FILE_PATH = process_remaining_args(sys.argv)


print("exists", os.path.exists(AUDIO_PATH))

project = Project.current_project()

project_name = os.path.split(os.path.splitext(FILE_PATH)[0])[1]
print(project_name)

# check si le projet est déjà ouvert
if project.get_project(by_name=project_name) is None:
    project.load(FILE_PATH)
else : 
    project.get_project(by_name=project_name).make_current()


project = Project.current_project()
clip = project.current_clip
audio = clip.get_sound()

if audio is None :
    audio = clip.add_sound(AUDIO_PATH)
else : 
    audio.reload()

print("saving")
project.save()
