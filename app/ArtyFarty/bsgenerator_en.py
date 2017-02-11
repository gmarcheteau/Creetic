# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# use lowecase and then capitalizeFirstWords at the end, to allow more flexibility
# -------------------------------------------------------------------------
import numpy as np
import random
import re
from bs_bits_en import *

def generatePhrase(*maincolors):
  parts = selectRandomParts(maincolors)

  colorcomment = ''
  colorcomment2 = ''
  
  if maincolors:
    firstcolor=maincolors[0][0][1]
    colorcomment = ''.join([
        ',',
        space,
        parts['colorlocution'],
        space,
        firstcolor,#use main color or random (randColorNumber)?
        ',',
      ])
      
    #if more than 1 color, write second comment too
    if(len(maincolors[0])>1):
      #if first two colors have same name
      secondcolor=maincolors[0][1][1]
      if secondcolor==firstcolor and maincolors[0][2][1]:
        secondcolor=maincolors[0][2][1]
      
      colorcomment2 = ''.join([
        parts['secondcolorlocution'],
        space,
        secondcolor,
        space,
        parts['verb2'],
        space,
        parts['noun3']
      ])
  
  
  phrase = ''.join([
    parts['start_locution'],
    parts['noun1'],
    colorcomment,
    space,
    parts['verb1'],
    space,
    parts['noun2'],
    #add comment about second color
    colorcomment2,
    #no space before finish_locution
    parts['finish_locution'],
    ])
    
  
  phrase = capitalizeFirstWords(phrase)
  phrase = unicode(phrase, 'utf-8')
  return phrase

def generatePhrase_short(limit=116):
  
  bstext = generatePhrase()
  counter = 1
  
  print "\n###BULLSHIT GENERATION###"
  print "Generated BS #%d | length: %d" %(counter,len(bstext))
  
  while len(bstext)>limit:
    counter += 1
    bstext = generatePhrase()
    print "Generated BS #%d | length: %d" %(counter,len(bstext))
  
  print "###END OF BULLSHIT GENERATION###\n"
  
  return bstext

def capitalizeFirstWords(phrase):
  return re.sub(r"(\A\w)|"+                  # start of string
               "(?<!\.\w)([\.?!] )\w|"+     # after a ?/!/. and a space,
                                            # but not after an acronym
               "\w(?:\.\w)|"+               # start/middle of acronym
               "(?<=\w\.)\w",               # end of acronym
               lambda x: x.group().upper(),
               phrase)

def selectRandomParts(*maincolors):
  randLocution = random.randint(0,len(locutions)-1)
  
  #pick nouns from different buckets
  randNounBucket1 = random.randint(0,len(nouns)-1)
  randNounBucket2 = randNounBucket1
  while randNounBucket2==randNounBucket1:
    randNounBucket2=random.randint(0,len(nouns)-1)
  
  randVerb1 = random.randint(0,len(verbes)-1)
  randFinish = random.randint(0,len(finish_locutions)-1)
  
  if maincolors:
    print "colors detected -- choosing randoms for color bits"
    #randColorNumber = random.randint(0,len(maincolors)-1)
    randColorLocution = random.randint(0,len(colorlocutions)-1)
    randSecondColorLocution = random.randint(0,len(secondcolorlocutions)-1)
    #avoid using same item twice
    randVerb2 = randVerb1
    while(randVerb2 == randVerb1):
      randVerb2 = random.randint(0,len(verbes)-1)
    
    randNounBucket3 = randNounBucket1
    while(randNounBucket3 in [randNounBucket1,randNounBucket2]):
      randNounBucket3=random.randint(0,len(nouns)-1)
  
  # set a 2/3 chance to add an initial locution
  optional_start = ''
  if random.randint(1,3)%3 != 0:
    optional_start += locutions[randLocution]
    optional_start += space
  
  return {
    'start_locution': optional_start,
    'noun1':nouns[randNounBucket1][random.randint(0,len(nouns[randNounBucket1])-1)],
    'verb1':verbes[randVerb1],
    'noun2':nouns[randNounBucket2][random.randint(0,len(nouns[randNounBucket2])-1)],
    
    'colorlocution':colorlocutions[randColorLocution],
    'secondcolorlocution':secondcolorlocutions[randSecondColorLocution],
    
    'verb2':verbes[randVerb2],
    'noun3':nouns[randNounBucket3][random.randint(0,len(nouns[randNounBucket3])-1)],
    
    'finish_locution':finish_locutions[randFinish]
    }