'''
Search for all duplicate files, and report them to the user. It's the responsibility of the user to 
delete the duplicates.
'''

import os, zlib, sys, time, pprint
from collections import defaultdict
from hashlib import md5

# Using the '.update' method allows me to work on large files w/o 
# w/o loading all the content in memory
def hash_big_file(f):
    h = md5()
    with open(f) as ff:
        while True:
            d = ff.read(1024 * 16)
            if not d:
                break
            h.update(d)
    return h.hexdigest()
    
def find_duplicates(src_dir, hash_fn=hash_big_file, verbose=False):
    files_sizes, files_hashes = defaultdict(list), defaultdict(list)
    num_skipped_files = 0 # the number of num_skipped_files files
    for root, _, files in os.walk(src_dir):
        for f in files:
            f = os.path.join(root, f)
            try:
                stat = os.stat(f)
            except WindowsError:
                if verbose:
                    print 'Cannot get stats about file "{0}". Skipping it...'.format(f)
                num_skipped_files += 1
            else:
                files_sizes[stat.st_size].append(f)
                
    for size, files in files_sizes.items():
        if len(files) > 1:
            for f in files:
                hash = hash_fn(f)
                files_hashes[hash].append(f)
                
    return [files for hash, files in files_hashes.items() if len(files) > 1], num_skipped_files
    
if __name__ == '__main__':
    before = time.time()
    duplicates, num_skipped_files = find_duplicates(sys.argv[1])
    print 'Finished "{0}" in {1} seconds'.format(sys.argv[1], time.time() - before)
    print 'Duplicates: \n{0}'.format(pprint.pformat(duplicates))
            