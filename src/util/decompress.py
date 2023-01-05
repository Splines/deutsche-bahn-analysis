import os
import zlib

filenames = os.listdir('./download')
if not os.path.exists('./download-decompressed'):
    os.mkdir('./download-decompressed/')

for filename in filenames:
    # Open
    with open(os.path.join('./download', filename), 'rb') as f:
        content = f.read()

    # Decompress
    xml_string = zlib.decompress(content).decode('utf-8')

    # Save decompressed
    # Get rid of ".compressed" file ending
    filename_new = filename[0:filename.rfind('.')]
    with open(os.path.join('./download-decompressed/', filename_new), 'w') as f:
        f.write(xml_string)
