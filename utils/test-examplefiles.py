#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 08:48:20 2018

@author: dmvigi
"""
import logging
import json
import argparse
import os

class Example:

    def __init__(self, json_file, md_file):

        self.get_JSON_data(json_file)
        self.get_MD_data(md_file)


    def get_JSON_data(self, f):
        # serialized python data from json file
        self.jdata = json.load(self.read_file(f))
        logging.debug('%s jdata:\n%s', f, self.jdata)
        logging.info('File %s processed', f)

    def get_MD_data(self, f):
        # md_data is array of lines of data
        self.md_data = (self.read_file(f)).readlines()
        lstr = f + ' has ' + str(len(self.md_data)) + ' lines'
        logging.debug(lstr)

        # remove \n from end of lines of list
        self.md_data = map(lambda s: s.strip(), self.md_data)

        # print to logger
        for line in self.md_data:
            logging.debug('[%s]', line)
        logging.info('File %s processed', f)

    def read_file(self, filename):

        try:
            f = open(filename, 'r')
        except OSError:
            print('Unable to open file', filename)
        return f


def process_examples(json_file=None, md_file=None):

    # the files we will test on
    if json_file == None:
        json_file = 'example.json'
    if md_file == None:
        md_file = "README.md"
    example = Example(json_file, md_file)


def parse_md(mdfile):

    # read file
    print('not implemented')


def parse_args():

    parser = argparse.ArgumentParser(
        description='Sanity check of README and JSON files')
    parser.add_argument('-r', '--readmefile', 
                        required = True,
                        help = 'specify path to and name of README')
    parser.add_argument('-j', '--jsonfile',
                        required = True,
                        help = 'specify path to and name of JSON')
    parser.add_argument('-v', '--verbose',
                        action='store_true', default=False,
                        help='verbose flag (creates dakota-examples.log file)' )

    return vars(parser.parse_args())

    
if __name__ == "__main__":

    print('Testing files... (Use -v flag to print debugging information.)')
    
    args = parse_args()

    logging_file = 'test.log'
    try:
        os.remove(logging_file)
    except OSError:
        pass

    
    if args['verbose'] == True:
        logging.basicConfig(filename=logging_file,level=logging.DEBUG)
    else:
        logging.basicConfig(filename=logging_file,level=logging.INFO)
    logging.info('Started')

    # do the actual sanity checking
    process_examples(args['jsonfile'], args['readmefile'])
    
    logging.info("Finished.")

    print('Completed. See test.log for more information.')
