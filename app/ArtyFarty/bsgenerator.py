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
        'Il est évident que',
        'Nul doute que',
        'Il saute aux yeux que',
        'Bien entendu,',
        'Cela va sans dire,',
        'Force est de constater que',
        'Indubitablement,',
        'Certains diront que',
        'Malgré les apparences,',
        'Loin des clichés,',
        'Chacun aura son avis, mais il est clair que ',
        'Cela en surprendra certains, mais',
        'Une fois n\'est pas coutume,',
        'Un oeil expert constatera que',
        'Un examen attentif permet de constater que',
        'Inutile de se voiler la face :',
        'Soyons francs :',
        'Prenant le contrepied de l\'anticonformisme,',
        'Dans la plus pure tradition vénitienne,',
    ])

nouns = np.array([
    #utiliser 'ce' pour masculin au lieu de 'le', pour pouvoir faire 'de ce'
        'l\'ordonnancement matriciel des points de fuite',
        'la perspective mouvante',
        'la plasticité du trait',
        'le recours au figuralisme',
        'le rapport à la matière',
        'l\'irréversibilité des contraintes exogènes',
        'la prégnance des couleurs primaires',
        'le chromatisme auquel le peintre a recours',
        'le mouvement de la lumière',
        'la scission des structures sérielles',
        'la rotondité des angles',
        'le cynisme avec lequel les ombres sont délaissées',
        'la tendance à infléchir les lignes droites',
        'la matérialité de la texture',
        'l\'opacité des polygones',
        'l\'oscillation obstinée des perspectives',
        'la couleur dominante',
        'l\'anamorphose intrinsèque de la rhétorique utilisée',
        'cette hésitation constante entre ombre et lumière',
        'le flou impertinent (bien que nécessaire)',
        'le trait enjoué',
        'la frustrante inertie avec laquelle les formes prennent vie',
        'la structure même de la toile',
        'le mépris manifeste des tons célestes',
        'la corrélation quasi insolente entre les nuances de tons et l\'angulosité appuyée des segments'
    ])

verbes = np.array([
        'contredit',
        'est en contradiction avec',
        'rappelle',
        'met en évidence',
        'ne fait qu\'accentuer',
        'ne doit pas faire perdre de vue',
        'ne doit pas faire oublier',
        'omet',
        'néglige',
        'alimente',
        'reflète',
        'masque presque',
        'exprime clairement',
        'transcende',
        'justifie',
        'sous-tend',
        'soutient',
        'conspue',
        'établit un contraste inattendu avec',
        'permet à la composition de prendre ses distances avec',
        'amplifie',
        'cache',
        'réduit à néant',
        'déconstruit',
        's\'estompe devant',
    ])

finish_locutions = np.array([
        '. Inspiration ou plagiat ?',
        ', une première pour ce maestro.',
        ', conséquence malheureuse d\'une adhésion tardive au kandinskisme.',
        ' - et ce n\'est malheureusement pas la première fois.',
        ' - une infraction arrogante à toutes les règles que l\'artiste a lui-même contribué à créer.',
        ', sans pour autant en nier l\'existence.',
        ' - une référence aux travaux de Barlowstovitch sur le sujet ?',
        ' - ce qui ne manque pas de panache !',
        ', tout en s\'inscrivant dans une continuité stylistique que les amateurs apprécieront.',
        ', ce qui est somme toute choquant pour qui garde en mémoire l\'orientation politique de l\'artiste...',
        ' - ce point faisant cependant toujours débat bien des années plus tard.',
        ' - oecuménisme bienveillant ou prosélytisme effronté ?',
        '. Un retour aux sources, en quelque sorte.',
        '. Il s\'agit là d\'un phénomène qui n\'a cessé d\'imprégner la production stylistique de cet artiste.',
        '. Tout cela est clairement autobiographique.',
        '. Le rapport de l\'artiste à sa mère n\'y est pas pour rien.',
        '. Une interprétation toute personnelle du rapport à la spiritualité.'
    ])

space = ' '

def generatePhrase(*maincolors):
  a = ''
  rand1 = random.randint(0,len(locutions)-1)
  rand2 = random.randint(0,len(nouns)-1)
  rand3 = random.randint(0,len(verbes)-1)
  #cannot use the same random int multiple times for nouns
  #initialize as same, then while loop
  rand4 = rand2
  while(rand4==rand2):
      rand4 = random.randint(0,len(nouns)-1)
  rand5 = random.randint(0,len(finish_locutions)-1)

  b = ''.join([
          locutions[rand1],
          space,
          nouns[rand2],
          space,
          verbes[rand3],
          space,
          nouns[rand4],
          #no space before finish_locution
          finish_locutions[rand5]
      ])
  phrase = b
  
  
  if maincolors:
    number_colors = len(maincolors)
    a =  "One can identify %d dominant colours. The use of %s is particularly striking." % (number_colors, maincolors[0][1])
    if number_colors>1:
      abis = "Touches of %s come as a clever surpise." % maincolors[1][1]
      a = ' '.join((a,abis))
      phrase = ''.join((a,' ',b))
  
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

