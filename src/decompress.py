import os
import zlib

filenames = os.listdir('./download')
os.mkdir('./download-decompressed/')

for filename in filenames:
    # Open
    with open(os.path.join('./download', filename), 'rb') as f:
        content = f.read()

    # Decompress
    xml_string = zlib.decompress(content).decode('utf-8')

    # Save decompressed
    with open(os.path.join('./download-decompressed/', filename), 'w') as f:
        f.write(xml_string)
