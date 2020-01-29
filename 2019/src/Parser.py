
def parseIn(path):
    with open(path, 'r') as fp:
        numPhotos = int(fp.readline().strip().split()[0])
        photos    = []
        for line in fp:
            orientation, numTags, *tags = line.strip().split()
            photos.append({'orient':  orientation,
                           'numTags': int(numTags),
                           'tags':    tags,
                           'id':      str(len(photos))})

    return numPhotos, photos

def parseOut(path, slideshow):
    print(slideshow)
    with open(path, 'w') as fp:
        fp.write('{}\n'.format(len(slideshow)))
        [fp.write('{}\n'.format(slide)) for slide in slideshow]
