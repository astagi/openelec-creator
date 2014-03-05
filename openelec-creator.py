import os
import requests
import sys
import time
import re
import tempfile
import zipfile

from sdcardburner.imgburner import Burner, ProgressListener

class MyProgressListener(ProgressListener):
  def on_progress_update(self, progress_pct):
    sys.stdout.write("\rWriting: %d percent" % progress_pct)

  def on_error(self, error):
    print "\nError during writing!"

  def on_eject(self):
    print "\nEjecting..."

  def on_completed(self):
    print "\nYour OpenELEC sdcard is ready!"

def download_file(url, file_path) :
  localFilename = url.split('/')[-1]
  with open(file_path, 'wb') as f:
    start = time.clock()
    r = requests.get(url, stream=True)
    total_length = int(r.headers.get('content-length'))
    dl = 0
    if total_length is None: # no content length header
      f.write(r.content)
    else:
      for chunk in r.iter_content(1024):
        dl += len(chunk)
        f.write(chunk)
        done = int(50 * dl / total_length)
        sys.stdout.write("\r[%s%s] %s bps" % ('=' * done, ' ' * (50-done), dl//(time.clock() - start)))
  return (time.clock() - start)

def get_images_list():
  r = requests.get('http://openelec.thestateofme.com/official_images/')
  html = r.text
  pattern = "<a href=\"(.*)\">(.*)</a> (.*)   (.*)"
  i = 0
  images_list = []
  for m in re.finditer(pattern, html):
    if i >= 2:
      images_list.append({
        'url': "http://openelec.thestateofme.com/official_images/" + m.group(1),
        'name': m.group(2),
        'date': m.group(3), 'size': m.group(4)})
    i += 1
  return images_list[::-1]

def unzip_image(zip_file, outpath):
  fh = open(zip_file, 'rb')
  z = zipfile.ZipFile(fh)
  img_name = ""
  for name in z.namelist():
    z.extract(name, outpath)
    img_name = name
  fh.close()
  return os.path.join(outpath, img_name)

def main():
  images = get_images_list()
  i = 0
  for image in images:
    i += 1
    print "%d\t%s\t%s\t%s" % (i, image['date'], image['name'], image['size'])
  image_index = -1
  while not 0 <= image_index < len(images):
    image_index = int(input('\nSelect the image you want to flash: ')) - 1
  temp_dir = tempfile.gettempdir()
  img_zip = os.path.join(temp_dir, images[image_index]['name'])
  download_file(images[image_index]['url'], img_zip)
  print "\nDownload completed!"
  print "Unzipping image... Please wait.."
  img_to_flash = unzip_image(img_zip, temp_dir)
  print "Unzipping image completed!"
  progress_listener = MyProgressListener()
  burner = Burner()
  devices = burner.list_devices()
  i = 0
  for device in devices:
    i += 1
    print "%d\t%s" % (i, device['DeviceIdentifier'])
  device_index = -1
  while not 0 <= device_index < len(devices):
    device_index = int(input('\nSelect the device you want to use: ')) - 1
  selected_device = devices[device_index]
  burner.burn(selected_device, img_to_flash, progress_listener)

if __name__ == "__main__":
  main()
