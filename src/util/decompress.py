import os
import zlib

base_path = './download'
filenames = [f for f in os.listdir(base_path)
            if os.path.isfile(os.path.join(base_path, f))]

# Create empty decompressed folder
base_path_decompressed = './download-decompressed'
if not os.path.exists(base_path_decompressed):
    os.mkdir(base_path_decompressed)

for filename in filenames:
    # Open
    with open(os.path.join(base_path, filename), 'rb') as f:
        content = f.read()

    # Decompress
    xml_string = zlib.decompress(content).decode('utf-8')

    # Save decompressed
    # Get rid of ".compressed" file ending
    filename_new = filename[0:filename.rfind('.')]
    with open(os.path.join(base_path_decompressed, filename_new), 'w') as f:
        f.write(xml_string)
