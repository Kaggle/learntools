import os
import re
import requests
import shutil



def get_url_and_fname(line):
    if 'i.imgur.com/' in line:
        regex = r"(https?://i.imgur.com/(.*.png))"
    elif 'imgur.com' in line:
        regex = r"(https?://imgur.com/(.*.png))"
    else:
        print("No valid imgur url found in {}".format(line))
    try:
        url, fname = re.findall(regex, line)[0]
    except:
        import pdb; pdb.set_trace()
    return url, fname

def dl_image(url, out_fname):
    response = requests.get(url, stream=True)
    with open(out_fname, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


os.makedirs('images', exist_ok=True)
with open('urls.txt', 'r') as f:
    for line in f:
        url, fname = get_url_and_fname(line)
        print('Downloading {}'.format(url))
        dl_image(url, fname)
