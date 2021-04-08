#-------------------------------------------------------------------------------
# Dakota Graphical User Interface (Dakota GUI)
# Copyright 2019 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.
#   
# This software is distributed under the Eclipse Public License.  For more
# information see the files copyright.txt and license.txt included with the software.
#-------------------------------------------------------------------------------

import collections
import re

###############
#  Constants  #
###############

BEFORE = True
AFTER  = False

LINES = 0
FIELDS = 1
CHARACTERS = 2

#############
#  Classes  #
#############  
    
# Class QoiAnchor
#   Represents a simplified regular expression that defines how to locate a quantity of interest in
#   generated output, starting from a unique key identifier.
#
#   The best way to understand how this class works is to read its parameters as a sentence structured as follows:
#   "My quantity of interest is <resultLength> <resultType> that is <anchorDist> <anchorType> <before> the keyword <anchorText>."
#
#   Example:
#   "My quantity of interest is 1 word that is 2 lines after the keyword MASS."
#
#   resultLength   - The size of the quantity of interest, defined with the measurement specified by the resultType.
#   resultType     - The measurement used to define the size of the quantity of interest (characters, words, or lines).
#   anchorDist     - The distance that the quantity of interest is away from the anchor text, defined with the measurement specified by the anchorType.
#   anchorType     - The measurement used to define the distance that the anchor text is away from the quantity of interest (characters, words, or lines).
#   before         - A boolean value that specifies whether the quantity of interest is before or after the anchor text.
#   anchorText     - The unique, key phrase used to identify the relative location of a quantity of interest.

class QoiAnchor:
    def __init__(self, name, resultLength, resultType, anchorDist, anchorType, before, anchorText):
        self.name = name
        self.resultLength = resultLength
        self.resultType = resultType
        self.anchorDist = anchorDist
        self.anchorType = anchorType
        self.before = before
        self.anchorText = anchorText
        
    def __str__(self):
        return "[Get " + str(self.resultLength) + " " + str(self.resultType) + " that are " + str(self.anchorDist) + \
               " " + str(self.anchorType) + (" before " if self.before else " after ") + " the text " + str(self.anchorText) + "]"
        
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
        
    def __hash__(self):
        return hash(len(str(self.name)) * len(str(self.resultLength)) * len(str(self.resultType)) * len(str(self.anchorDist)) * \
                    len(str(self.anchorType)) * len(str(self.anchorText)) * (2 if self.before else 1))
    
    # extract(self, text)
    #   Searches a blob of text for quantities of interest.
    #
    #   text - The output text to search.
    #
    #   return - A map of keys and values found in the output text.
    def extract(self, text):
        new_resp_val = None
        
        try: # First of all, try placing our starting index at the index of anchorText in the output file, if it exists.
            start_anchor_index = text.index(self.anchorText)
        except:
            new_resp_val = " "
            
        # Next, get the remaining text either before or after the anchor index (depending on whether we're looking before or after).
        remaining_text = (text[start_anchor_index:]
                          if not self.before
                          else text[:(start_anchor_index + len(self.anchorText))])
        remaining_words = []
        if self.anchorType == LINES:
            remaining_words = re.split("\r|\n", remaining_text)   # Lines:  Split based on line-ending characters
        elif self.anchorType == FIELDS:
            remaining_words = re.split(" |\r|\n", remaining_text) # Words:  Split based on line-ending characters and spaces
    
        remaining_words_minus_spaces = []
        for word in remaining_words:
            if word:
                remaining_words_minus_spaces.append(word) # Remove blanks from consideration.

        try:
            # Find the index of the result word (based on whether we're looking before or after)
            result_index = ((self.anchorDist)
                            if not self.before
                            else (len(remaining_words_minus_spaces) - 1 - self.anchorDist))
            try:
                # Next, get the result word.
                result_word = remaining_words_minus_spaces[result_index]
                
                # If we're searching based on lines, we need to perform an additional split to get the first word on
                # the result line.
                if self.anchorType == LINES:
                    result_words = result_word.split(" ") # Split on spaces.
                    remaining_words_minus_spaces = []                    
                    for word in result_words:
                        if word:
                            remaining_words_minus_spaces.append(word) # Remove spaces from consideration.
                    try:
                        result_index = (0 if not self.before else (len(remaining_words_minus_spaces) - 1))
                        result_word = remaining_words_minus_spaces[0]
                    except:
                        new_resp_val = " "
                try:
                    if self.resultType == CHARACTERS:
                        # If we specified characters for resultType, get the necessary amount of characters.
                        end_index = 0
                        if not self.before:
                            end_index = self.resultLength if (self.resultLength < len(result_word)) else len(result_word)
                            new_resp_val = result_word[:end_index]
                        else:
                            end_index = (len(result_word) - self.resultLength) if (self.resultLength < len(result_word)) else 0
                            new_resp_val = result_word[end_index:]
                    elif self.resultType == FIELDS:
                        # If we specified words for resultType, get the remaining amount of words, by working either
                        # backwards or forwards depending on whether we're looking before or after.
                        if not self.before:
                            new_resp_val = result_word
                            for x in range(result_index + 1, self.resultLength):
                                try:
                                    new_resp_val = new_resp_val + " " + remaining_words_minus_spaces[x]
                                except:
                                    new_resp_val = " "
                        else:
                            new_resp_val = result_word
                            for x in range(result_index - 1, result_index - self.resultLength, -1):
                                try:
                                    new_resp_val = remaining_words_minus_spaces[x] + " " + new_resp_val
                                except:
                                    new_resp_val = " "
                except:
                    new_resp_val = " "
            except:
                new_resp_val = " "
        except:
            new_resp_val = " "                
        return new_resp_val
