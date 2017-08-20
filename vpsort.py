#!/usr/bin/env python3

import argparse
import exifread
import shutil
from os import path
from datetime import datetime


def _time_created(image_file):
    exif_creation_date = 'DateTimeOriginal'
    exif_date_fmt = '%Y:%m:%d %H:%M:%S'
    with open(image_file, 'rb') as img:
        tags = exifread.process_file(img)
        date_str = None
        for k, v in tags.items():
            if exif_creation_date.lower() in k.lower():
                date_str = str(v)
        try:
            return datetime.strptime(date_str, exif_date_fmt)
        except ValueError:
            pass
        except TypeError:
            print('Failed reading creation date of {f:}'.format(f=image_file))
    return None


def _store_image(original, target, use_move=False):
    if original == target:
        pass
    if path.isfile(target):
        print('ERR Target file', target, 'already exists. Preserving original!')
        return
    print('Storing', original, 'as', target, '...')
    if use_move:
        shutil.move(original, target)
    else:  # use copy instead
        shutil.copy(original, target)


def main():
    parser = argparse.ArgumentParser(description='Sort vacation photos by date taken.')
    parser.add_argument('--files', nargs='+', metavar='F', required=True,
                        help='Files to be sorted.')
    parser.add_argument('--target', type=str, metavar='T', required=True,
                        help='Target folder to which files should be stored.')
    parser.add_argument('--basename', type=str, metavar='B', default='IMG-',
                        help='Basename of all sorted files ie. file names will be of the form "<B>00.jpg"')
    parser.add_argument('--remove-originals', action='store_true', help='Move files instead of copying.')
    parser.add_argument('--list-options', action='store_true',
                        help='Do nothing else but printing available options (intended for auto completion).')
    # TODO: Epilog with extended description

    # Read cmd line arguments
    args = parser.parse_args()

    # TODO: handle list_options flag

    # Collect (existing) images
    img_files = [f for f in args.files if path.isfile(f)]

    # Sort images ascending in creation date
    img_files = sorted(img_files, key=lambda x: _time_created(x))

    # Put images where they belong
    num_fmt = '{:0' + str(len(str(len(img_files)))) + 'd}'
    for num, img in enumerate(img_files):
        new_img = path.join(args.target, args.basename + num_fmt.format(num) + path.splitext(img)[1].lower())
        _store_image(img, new_img, use_move=args.remove_originals)

if __name__ == "__main__":
    main()
