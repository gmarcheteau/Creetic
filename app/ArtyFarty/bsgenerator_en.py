# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# use lowecase and then capitalizeFirstWords at the end, to allow more flexibility
# -------------------------------------------------------------------------
import numpy as np
import random
import re

# DEFINE IDIOMS

locutions = np.array([
        'well,',
        'of course,',
        'no doubt that',
        'undoubtedly,',
        'to the expert eye, it will be obvious that',
        'some will claim that',
        'most critics agree:',
        'as usual,',
        'let\'s be honest:',
        'let\'s face it:',
        'as expected,',
        'unexpectedly,',
        'it seems that',
        'I believe that',
        'I think that',
        'frankly,',
        'honestly,',
        'some say that',
        'once more,',
        'I see that',
        'I say,',
        'impressive,',
        'hmm,',
        'oh,',
        'damn,'
    ])

###define two buckets for two sentence bits###
#group by themes to avoid repetition and allow for more variants
#all singular

nouns1 = np.array([
  #structure and texture
  'the antagonism of most parts of the structural system',
  'the materiality of the texture',
  'the texturality',
  
  #lines and curves
  'the tendency to bend straight lines',
  'the linearity of curves',
  'the unintended circularity of lines',
  
  #shapes
  'the frustrating inertia with which shapes come alive',
  'this big unidentified shape',
  'that thing in the middle',
  'an invisible but blatant shape',
  
  #blur
  'the insolent but necessary blur',
  'a blurry intention',
  'the severe blurness',
  
  #arrangement
  'the wobbly arrangement',
  'an unclear arrangement',
  'this strict arragement',
  
  #perspective
  'the shifting perspective',
  'the evading perspective',
  'the stubborn wavering of perspectives',
  
  #others
  'the opacity of polygons',
  
  ])

nouns2 = np.array([
  #strokes
  'the plasticity of the strokes',
  'the joyful succession of dashes',
  
  #symmetry
  'the swirling symmetry',
  'this witty symmetry',
  
  #shadow/light
  'this warm light',
  'the constant hesitation between shadow and light',
  'the cynicism with which the shadows are neglected',
  'the patent scorn for light hue',
  
  #angles
  'the softness of the angles',
  'the angularity of the shadows',
  
  #series/serial
  'the simplicity of the main serial elements',
  
  #tones
  'the saturation of tones',
  'the plurality of tones',
  
  #constraints
  'the multiplicity of exogenous constraints',
  'the self-imposed tone constraint',
  
  #movement/stillness
  'the vibrant stillness that emerges from this piece',
  'the idle movement of this piece',
  
  ])

colorlocutions = np.array([
  'combined with the use of colors such as',
  'through a significant use of',
  'evidenced by touches of',
  'which derives from the predominance of',
  'even with the use of colors such as',
  'considering the resort to tones like',
  'notwithstanding the use of',
  ])

secondcolorlocutions = np.array([
  '. The touch of',
  '. In addition to this, the choice of',
  '. Furthermore, a minor tone such as',
  '. Far from opposing this, the use of',
  '. On the opposite end of the spectrum, the touch of',
  '. An even further examination reveals that the use of',
  '. What is more, the artist\'s preference for'
  ])

verbes = np.array([
  'contradicts',
  'is in contradiction with',
  'brings out',
  'highlights',
  'establishes a sharp contrast with',
  'does nothing but accentuate',
  'is reinforced by',
  'reinforces',
  'should not lead one to disregard',
  'should not obliterate',
  'obliterates',
  'misses',
  'feeds',
  'amplifies',
  'reflects',
  'translates',
  'almost outshines',
  'dampens',
  'clearly expresses',
  'transcends',
  'justifies',
  'underlies',
  'propels',
  'allows the composition to distance itself from',
  'hides',
  'shatters',
  'reduces',
  'deconstructs',
  'pales before',
  'makes up for the shortcomings of',
  'trumps',
  'is incompatible with',
  'departs from',
])

finish_locutions = np.array([
  '. inspirational!',
  '. a first for this maestro.',
  '. this is regrettable.',
  '. this is remarkable.',
  '. hard to top.',
  '. hats off!',
  '. brilliant!',
  '. stunning!',
  '. scandalous!',
  '. shocking!',
  '. a regrettable consequence of a late subscription to kandinskism.',
  ' - and it\'s unfortunately not the first time.',
  ' - an arrogant transgression of all the rules that the artist contributed to setting...',
  ', yet not negating its existence.',
  ' - a reference to Barlowstovitch\'s work on the subject?',
  '. bravo!',
  '. the artist gets away with panache!',
  ' - artistic flair at its best.',
  ', while still subscribing to an artistic continuity, which will surely be appreciated by the connoisseurs.',
  ' - the connoisseurs will appreciate.',
  ' - which, all things considered, is quite shocking for anyone having aware of the artist\'s political views...',
  ' - although this interpretation is still quite controversial many years later.',
  ' - benevolent ecumenism or shameless proselytism?',
  '. back to basics, in a way.',
  '. this is a phenomenon which never ceased to pervade the artist\'s stylistic production.',
  '. this is all obviously very autobiographic.',
  '. the artist\'s relationship with their mother has to do with this.',
  '. a very personal take on spirituality.',
  '. wow!',
  '. a political message indeed.',
  '. this is reckless art.',
  '. quite an artistic stunt.',
  '. best art ever. period.',
  '. not bad!',
  '. close to perfection.',
  '. good stuff.',
  '. history in the making.',
  '. quite scary!',
  '. well done!',
  '. astonishing!',
  '. powerful stuff.',
  '. quite fantastic.',
    ])

space = ' '

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
  #define randoms
  randLocution = random.randint(0,len(locutions)-1)
  randNoun1 = random.randint(0,len(nouns1)-1)
  randNoun2 = random.randint(0,len(nouns2)-1)
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
    randNoun3 = randNoun1
    while(randNoun3 in [randNoun1,randNoun2]):
      #choose from one or the other of the 2 noun buckets
      if random.randint(1,2)%2==0:
        randNoun3 = random.randint(0,len(nouns1)-1)
        nouns3bit=nouns1[randNoun3]
      else:
        randNoun3 = random.randint(0,len(nouns2)-1)
        nouns3bit=nouns2[randNoun3]
  
  # set a 1/2 chance to swap the 2 noun bits (they come from incompatible buckets, so this does introduce some variety)
  noun1bit=nouns1[randNoun1]
  noun2bit=nouns2[randNoun2]
  tempNounBit=''
  if random.randint(1,2)%2 == 0:
    tempNounBit=noun1bit
    noun1bit=noun2bit
    noun2bit=tempNounBit
  
  # set a 2/3 chance to add an initial locution
  optional_start = ''
  if random.randint(1,3)%3 != 0:
    optional_start += locutions[randLocution]
    optional_start += space
  
  return {
    'start_locution': optional_start,
    'noun1':noun1bit,
    'verb1':verbes[randVerb1],
    'noun2':noun2bit,
    
    'colorlocution':colorlocutions[randColorLocution],
    'secondcolorlocution':secondcolorlocutions[randSecondColorLocution],
    
    'verb2':verbes[randVerb2],
    'noun3':nouns3bit,
    
    'finish_locution':finish_locutions[randFinish]
    }