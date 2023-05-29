import os
import re
import glob
import sqlite3 as db
eps = glob.glob('*.mp4')
fps = 1
os.mkdir('frames')

regex = re.compile(
    r"(?:.*)(?:s|season|)\s?(\d{1,2})\s?(?:e|x|episode|ep|\n)\s?(\d{1,2})", re.IGNORECASE)

for ep in eps:
    ep_regex = regex.match(ep)
    if ep_regex:
        season, episode = ep_regex.groups()

        out_path = f'./frames/S{season.zfill(2)}'
        if not os.path.isdir(out_path):
            os.mkdir(out_path)

        # print("yesyt")

        os.system(
            f'ffmpeg -i "{ep}" -vf "fps={fps},scale=640:360" {out_path}/{episode}x%d.jpg')
