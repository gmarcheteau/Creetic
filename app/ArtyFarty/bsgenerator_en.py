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
    ])

nouns = np.array([
        'the structure of this work',
        'the shifting perspectives',
        'the plasticity of the strokes',
        'the softness of the angles',
        'this warm light',
        'the simplicity of the main serial structures',
        'the multiplicity of exogenous constraints',
        'the cynicism with which the shadows are neglected',
        'the tendency to bend straight lines',
        'the materiality of the texture',
        'the joyful succession of dashes',
        'the constant hesitation between shadow and light',
        'the frustrating inertia with which shapes come alive',
        'the insolent (though necessary) blur',
        'the patent scorn for light hue',
        'the saturation of tones',
        'the opacity of polygons',
        'the stubborn wavering of perspectives',
        'the swirling symmetry',
        'the vibrant stillness that emerges from this piece',
        'the antagonism of most elements of the structural system',
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
  'misses',
  'feeds',
  'amplifies',
  'reflects',
  'translates',
  'almost overshadows',
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
  ' - which, all things considered, is quite shocking for anyone having aware of the artist\'s political views...',
  ' - although this interpretation is still quite controversial many years later.',
  ' - benevolent ecumenism or shameless proselytism?',
  '. back to basics, in a way.',
  '. this is a phenomenon which never ceased to pervade the artist\'s stylistic production.',
  '. this is all obviously very autobiographic.',
  '. the artist\'s relationship with their mother has to do with this.',
  '. a very personal take on spirituality.',
  '. wow!',
  '. a politically marked piece indeed.',
  '. this is reckless art.',
  '. quite an artistic stunt.',
  '. best art ever. period.',
  '. not bad!',
    ])

space = ' '

def generatePhrase(*maincolors):
  #define randoms
  randLocution = random.randint(0,len(locutions)-1)
  randNoun1 = random.randint(0,len(nouns)-1)
  randVerb = random.randint(0,len(verbes)-1)
  #cannot use the same random int multiple times for nouns
  #initialize as same, then while loop
  randNoun2 = randNoun1
  while(randNoun2==randNoun1):
      randNoun2 = random.randint(0,len(nouns)-1)
  randFinish = random.randint(0,len(finish_locutions)-1)

  colorcomment = ''
  colorcomment2 = ''
  if maincolors:
    number_colors = len(maincolors)
    randColorNumber = random.randint(0,number_colors-1)
    randColorLocution = random.randint(0,len(colorlocutions)-1)
    firstcolor=maincolors[0][0][1]
    colorcomment = ''.join([
        ',',
        space,
        colorlocutions[randColorLocution],
        space,
        #use main color or random (randColorNumber)?
        firstcolor,
        ',',
      ])
      
    #if more than 1 color, write second comment too
    if(len(maincolors[0])>1):
      #if first two colors have same name
      secondcolor=maincolors[0][1][1]
      if secondcolor==firstcolor and maincolors[0][2][1]:
        secondcolor=maincolors[0][2][1]
      
      randSecondColorLocution = random.randint(0,len(secondcolorlocutions)-1)
      randVerb2 = randVerb
      while(randVerb2 == randVerb):
        randVerb2 = random.randint(0,len(verbes)-1)
      randNoun3 = randNoun1
      while(randNoun3 in [randNoun1,randNoun2]):
        randNoun3 = random.randint(0,len(nouns)-1)
      
      colorcomment2 = ''.join([
        secondcolorlocutions[randSecondColorLocution],
        space,
        secondcolor,
        space,
        verbes[randVerb2],
        space,
        nouns[randNoun3]
      ])
      
  
  # set a 1/3 chance that the phrase won't have initial locution
  randLocutionOrNot = random.randint(1,3)
  if randLocutionOrNot%3 == 0:
    NO_LOCUTION = True
  else: NO_LOCUTION = False
  
  if NO_LOCUTION: #don't use first locution, capitalize first Noun
    phrase = ''.join([
          nouns[randNoun1],
          colorcomment,
          space,
          verbes[randVerb],
          space,
          nouns[randNoun2],
          #add comment about second color
          colorcomment2,
          #no space before finish_locution
          finish_locutions[randFinish]
      ])
  
  else: #full phrase
    phrase = ''.join([
          locutions[randLocution],
          space,
          nouns[randNoun1],
          colorcomment,
          space,
          verbes[randVerb],
          space,
          nouns[randNoun2],
          #add comment about second color
          colorcomment2,
          #no space before finish_locution
          finish_locutions[randFinish]
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