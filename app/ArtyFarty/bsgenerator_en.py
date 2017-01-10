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
        'the cynism with which the shadows are neglected',
        'the tendency to bend straight lines',
        'the materiality of the texture',
        'the joyful succession of dashes',
        'this constant hesitation between shadow and light',
        'the frustrating inertia with which shapes come alive',
        'the insolent (though necessary) blur',
        'the patent scorn for light hue',
        
        # 'l\'ordonnancement matriciel des points de fuite',
        # 'le recours au figuralisme',
        # 'le rapport à la matière',
        # 'la prégnance des couleurs primaires',
        # 'le chromatisme auquel le peintre a recours',
        # 'l\'opacité des polygones',
        # 'l\'oscillation obstinée des perspectives',
        # 'l\'anamorphose intrinsèque de la rhétorique utilisée',
        # 'la structure même de la toile',
        # 'la corrélation quasi insolente entre les nuances de tons et l\'angulosité appuyée des segments'
    ])

colorlocutions = np.array([
  'and the use of colors such as ',
  'through a signigicant use of ',
  'made obvious by touches of ',
  'which derives from the predominance of '
])

verbes = np.array([
  'contradicts',
  'is in contradiction with',
  'brings out',
  'highlights',
  'establishes a sharp contrast with',
  'does nothing but accentuate',
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
  'pales before'
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
  ' - altough this interpretation is quite controversial many years later.',
  'benevolent ecumenism or shameless proselytism?',
  '. Back to basics, in a way.',
  '. This is a phenomenon which never ceased to pervade the artist\'s stylistic production',
  '. This is all obviously very autobiographic.',
  '. The artist\'s relationship with their mother has to do with this.',
  '. A very personal take on spirituality.'
    ])

space = ' '

def generatePhrase(*maincolors):
  a = ''
  if maincolors:
    number_colors = len(maincolors)
    randColorNumber = random.randint(0,number_colors-1)
    randColorLocution = random.randint(0,len(colorlocutions)-1)
    a = ''.join([
        colorlocutions[randColorLocution],
        #use main color or random (randColorNumber)?
        maincolors[0][0][1],
        space
      ])
  
  rand1 = random.randint(0,len(locutions)-1)
  rand2 = random.randint(0,len(nouns)-1)
  rand3 = random.randint(0,len(verbes)-1)
  #cannot use the same random int multiple times for nouns
  #initialize as same, then while loop
  rand4 = rand2
  while(rand4==rand2):
      rand4 = random.randint(0,len(nouns)-1)
  rand5 = random.randint(0,len(finish_locutions)-1)
  
  phrase = ''.join([
          locutions[rand1],
          space,
          nouns[rand2],
          space,
          a,
          verbes[rand3],
          space,
          nouns[rand4],
          #no space before finish_locution
          finish_locutions[rand5]
      ])
  
  phrase = unicode(phrase, 'utf-8')
  return phrase

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("ArtyFarty")
    return dict(message=T(generatePhrase()))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


