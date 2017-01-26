# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import numpy as np
import random

# DEFINE IDIOMS

locutions = np.array([
        'No doubt that',
        'To the expert eye, it will be obvious that',
        'Some will claim that',
        'Most critics agree:',
        'As usual,',
        'Let\'s be honest:',
        'Let\'s face it:',
        'As expected,'
    ])

nouns = np.array([
        'the structure of this work',
        'the shifting perspectives',
        'the plasticity of the strokes',
        'the softness of the angles',
        'this warm light',
        'the main serial structures',
        'the multiplicity of exogeneous constraints',
        'the cynism with which the shadows are neglected',
        'the tendency to bend straight lines',
        'the materiality of the texture',
        'the joyful succession of dashes',
        'this constant hesitation between shadow and light',
        'the frustrating inertia with which shapes come alive',
        'the insolent (though necessary) blur',
        'the patent scorn for light hue',
        'the saturation of tones',
        'the opacity of polygons',
        'the stubborn wavering of perspectives',
        'the swirling symmetry',
        'the vibrant boredom that emerges from this piece',
        'the antagonism of most elements of the structural system',
    ])

colorlocutions = np.array([
  'combined with the use of colors such as',
  'through a signigicant use of',
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
  '. Inspiration or plagiarism?',
  ', a first for this maestro.',
  '. A regrettable consequence of a late subscription to kandinskism.',
  ' - and it\'s unfortunately not the first time.',
  ' - an arrogant transgression of all the rules that the artist contributed to setting...',
  ', yet not negating its existence.',
  ' - a reference to Barlowstovitch\'s work on the subject?',
  '. Bravo!',
  '. The artist gets away with panache!',
  ' - artistic flair at its best.',
  ', while still subscribing to an artistic continuity, which will surely be appreciated by the connoisseurs.',
  ' - which, all things considered, is quite shocking for anyone having aware of the artist\'s political views...',
  ' - altough this interpretation is still quite controversial many years later.',
  ' - benevolent ecumenism or shameless proselytism?',
  '. Back to basics, in a way.',
  '. This is a phenomenon which never ceased to pervade the artist\'s stylistic production',
  '. This is all obviously very autobiographic.',
  '. The artist\'s relationship with their mother has to do with this.',
  '. A very personal take on spirituality.'
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
    colorcomment = ''.join([
        ',',
        space,
        colorlocutions[randColorLocution],
        space,
        #use main color or random (randColorNumber)?
        maincolors[0][0][1],
        ',',
      ])
      
    #if more than 1 color, write b comment too
    if(len(maincolors[0])>1):
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
        maincolors[0][1][1],
        space,
        verbes[randVerb2],
        space,
        nouns[randNoun3]
      ])
      
  
  
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
  
  phrase = unicode(phrase, 'utf-8')
  return phrase

def generatePhrase_short(limit=116):
  
  bstext = generatePhrase()
  counter = 1
  
  print "Generated BS #%d" %counter
  print "Length: %d" %len(bstext)
  
  while len(bstext)>limit:
    counter += 1
    bstext = generatePhrase()
    print "Generated BS #%d" %counter
    print "Length: %d" %len(bstext)
  
  return bstext