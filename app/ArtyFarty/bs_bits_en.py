# -*- coding: utf-8 -*-
import numpy as np

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
  'impressive! ',
  'hmm,',
  'oh,',
  'damn,'
  ])

#One big bucket of nouns, divided into smaller, incompatible buckets
nouns = np.array([
  #structure and texture
  [
    'the antagonism of most parts of the structural system',
    'the materiality of the texture',
    'the texturality',
  ],
  
  #lines and curves
  [
  'the tendency to bend straight lines',
  'the linearity of curves',
  'the unintended circularity of lines',
  ],
  #shapes
  [
  'the frustrating inertia with which shapes come alive',
  'this big unidentified shape',
  'that thing in the middle',
  'an invisible but blatant shape',
  ],
  #blur
  [
  'the insolent but necessary blur',
  'a blurry intention',
  'the severe blurness',
  ],
  #arrangement
  [
  'the wobbly arrangement',
  'an unclear arrangement',
  'this strict arragement',
  ],
  #perspective
  [
  'the shifting perspective',
  'the evading perspective',
  'the stubborn wavering of perspectives',
  ],
  #others
  [
  'the opacity of polygons',
  ],
  #strokes
  [
  'the plasticity of the strokes',
  'the joyful succession of dashes',
  ],
  #symmetry
  [
  'the swirling symmetry',
  'this witty symmetry',
  'the inverted symmetricity'
  ],
  #shadow/light
  [
  'this warm light',
  'the constant hesitation between shadow and light',
  'the cynicism with which the shadows are neglected',
  'the patent scorn for light hue',
  ],
  #angles
  [
  'the softness of the angles',
  'the angularity of the shadows',
  ],
  #series/serial
  [
  'the simplicity of the main serial elements',
  ],
  #tones
  [
  'the saturation of tones',
  'the plurality of tones',
  ],
  #constraints
  [
  'the multiplicity of exogenous constraints',
  'the self-imposed tone constraint',
  ],
  #movement/stillness
  [
  'the vibrant stillness that emerges from this piece',
  'the idle movement of this piece',
  ],
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
  'emphasizes',
  'establishes a sharp contrast with',
  'does nothing but accentuate',
  'is reinforced by',
  'reinforces',
  'should not lead one to disregard',
  'should not obliterate',
  'obliterates',
  'corroborates',
  'bolsters',
  'buttresses',
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
  '. absolutely delightful!',
  '. a first for this maestro.',
  '. this is fascinating.',
  '. this is remarkable.',
  '. hard to top.',
  '. hats off!',
  '. brilliant!',
  '. daring!',
  '. stunning!',
  '. glorious!',
  '. shocking!',
  '. a regrettable consequence of a late subscription to kandinskism.',
  " - and it's not the first time.",
  ' - an arrogant transgression of all the rules that the artist contributed to setting...',
  ', yet not negating its existence.',
  ' - a reference to Barlowstovitch\'s work on the subject?',
  '. bravo!',
  '. the artist gets away with panache!',
  ' - artistic flair at its best.',
  ', while still subscribing to an artistic continuity, which will surely be appreciated by the connoisseurs.',
  ' - the connoisseurs will appreciate.',
  ' - which, all things considered, is quite shocking for anyone aware of the artist\'s political views...',
  ' - although this interpretation is still quite controversial many years later.',
  ' - benevolent ecumenism or shameless proselytism?',
  '. back to basics, in a way.',
  '. this is a phenomenon which never ceased to pervade the artist\'s stylistic production.',
  '. this is all obviously very autobiographic.',
  '. the artist\'s childhood has to do with this.',
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
  '. absolutely amazing.',
  ". it doesn't get much better"
    ])

space = ' '
