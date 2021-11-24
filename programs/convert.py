# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# <img align="right" src="images/tf-small.png" width="128"/>
# <img align="right" src="images/phblogo.png" width="128"/>
# <img align="right" src="images/dans.png"/>
#
# # Turn your corpus into a Text-Fabric dataset
#
# ## Corpus
#
# We start with a baby corpus in a markdown like format.
#
# **This is not meant as a preferred format of a corpus.**
#
# The point of this tutorial is to show what it takes
# to turn arbitrary data into TF.
#
# Below you see a string which contains 
# 1 "book", with 2 "chapters", each having one or two sentences.
#
# Here is the complete corpus source material:

source = '''
# Consider Phlebas
$ author=Iain M. Banks

## 1
Everything about us,
everything around us,
everything we know [and can know of] is composed ultimately of patterns of nothing;
that’s the bottom line, the final truth.

So where we find we have any control over those patterns,
why not make the most elegant ones, the most enjoyable and good ones,
in our own terms?

## 2
Besides,
it left the humans in the Culture free to take care of the things that really mattered in life,
such as [sports, games, romance,] studying dead languages,
barbarian societies and impossible problems,
and climbing high mountains without the aid of a safety harness.
'''

# Note a few details:
#
# * `# ` starts a "book" and the line contains its title: section level 1.
# * `$` starts a line with key=value metadata: the author.
#   This line is not part of the text.
# * `## ` starts a "chapter" and the line contains its number: section level 2.
# * *blank lines* separate sentences.
#   There are 2 sentences in the first chapter and 1 in the second one.
# * We will give each sentence a number within its chapter.
# * The sentences are divided into lines.
# * We will give each line a number within its sentence.
# * Words within [ ] will not be part of the line, the line has a gap.
#   But these words still belong to the text.
# * The gapped words will have a feature `gap=1`.
# * Lines will be split into words: the slot nodes.
# * We separate the word from its punctuation, which gets added in a `punc` feature.

# ## Fire up
#
# Now we start the engines: Text-Fabric, and the *walker* conversion module.

# +
import os
import re

from tf.fabric import Fabric
from tf.convert.walker import CV
# -

# We call up TF and let it look into the directory where the output has to land,
# in this case a subdirectory of the tutorials repo on annotation.

# +
# TF_DIR = os.path.expanduser('~/Downloads/banks/tf')  # if you want it in your Downloads directory instead
BASE = os.path.expanduser('~/github')
ORG = 'annotation'
REPO = 'banks'
RELATIVE = 'tf'

TF_DIR = os.path.expanduser(f'{BASE}/{ORG}/{REPO}/{RELATIVE}')

VERSION = '0.2'

TF_PATH = f'{TF_DIR}/{VERSION}'
TF = Fabric(locations=TF_PATH, silent=True)
# -

# ## TF configuration
#
# A Text-Fabric dataset is a bunch of individual `.tf` files that start with a little bit of metadata and then contain 
# a stream of data, typically the values of a single feature for each node or edge in the graph.
#
# We specify the metadata bit by bit.
#
# ### slot type
#
# A crucial design aspect of each TF dataset is its granularity. What are the slots?
#
# Words, morphemes, characters?
#
# You decide.

slotType = 'word'

# ### Provenance
#
# Users that encounter your TF data in the wild, will be thankful to you if you took the
# trouble to say in a few key-value pairs what that data is about.
#
# The metadata you specify here will end up in all generated TF features.

generic = {
    'name': 'Culture quotes from Iain Banks',
    'compiler': 'Dirk Roorda',
    'source': 'Good Reads',
    'url': 'https://www.goodreads.com/work/quotes/14366-consider-phlebas',
    'version': '0.2',
    'purpose': 'exposition',
    'status': 'with for similarities in a separate module'
}

# ### Text matters
#
# A few things concerning the presentation of your text can be specified in the `otext` feature.
# This is a tf feature without data, it has only metadata.
#
# It contains the specs for the section structure of your corpus and the text formats.
#
# #### Section structure
#
# TF assumes that there are two or three section levels it can work with.
# For each level you have to specify the corresponding node type and the feature that contains the section name or number
# (`sectionTypes` and `sectionFeatures`).
#
# #### Your own section structure
#
# But you can also define a more extensive and flexible section structure for your own purposes
# (`structureTypes` and `structureFeatures`).
# Both systems may use the same types and features, but they are completely independent.
#
# #### Text formats
#
# When you ask TF to render slot nodes (the nodes with text), TF needs to know
# which features to render. 
#
# A text format is a template with placeholders for the features you want to use.

otext = {
    'fmt:text-orig-full': '{letters}{punc} ',
    'fmt:line-term': 'line#{terminator} ',
    'fmt:line-default': '{letters:XXX}{terminator} ',
    'sectionTypes': 'book,chapter,sentence',
    'sectionFeatures': 'title,number,number',
    'structureTypes': 'book,chapter,sentence,line',
    'structureFeatures': 'title,number,number,number',
}

# ### Typing
#
# The values of features are usually strings.
# But if you know that they are always integers, you can declare a feature as an integer valued feature.
#
# The only thing you have to do is to declare them in the following set:

intFeatures = {
  'number',
  'gap',
}

# ### Descriptions
#
# You can say per feature what it does.
# Use as many key-values as you like.
#
# A good *description* is particularly helpful.
#
# It is surprising how often you want to consult those descriptions yourself.

featureMeta = {
    'number': {
        'description': 'number of chapter, or sentence in chapter, or line in sentence',
    },
    'gap': {
        'description': '1 for words that occur between [ ], which are inserted by the editor',
    },
    'title': {
        'description': 'the title of a book',
    },
    'author': {
        'description': 'the author of a book',
    },
    'terminator': {
        'description': 'the last character of a line',
    },
    'letters': {
        'description': 'the letters of a word',
    },
    'punc': {
        'description': 'the punctuation after a word',
    },
}


# ## Director
#
# This is the heart of the matter.
#
# The director is a function to be written by you.
#
# It needs to plough through your source material, and fire actions towards the TF machinery.
# The TF work is done for you by these actions, you can concentrate on the aspects of your
# source data.
#
# Every time the director encounters a new textual object in the source,
# it issues an action requesting a new node.
# The director gets a receipt, by which it can issue subsequent
# actions for that node, like adding feature values to it.
#
# And when the object is done, the director issues a `terminate` action.
#
# During all this, the `cv` machine is busy to translate these actions into
# the construction of a proper TF graph representing all the
# source material that you have exposed to it.
#
# A few things to note
#
# * If you want to terminate a node, you do not have to worry whether the node exists or has already
#   been terminated: just do it;
# * If you have terminated a node, you can resume it later;
# * When you add nodes, slot and non-slots, there is magic behind the scenes:
#   * when a **slot** node is added, it will be linked to all active non-slot nodes,
#     i.e. the ones that have not been terminated or have been resumed;
#   * when a **non-slot** node is added, is becomes automatically active,
#     in the sense that it will be linked to subsequent slot nodes, before it is terminated,
#     or after it has been resumed;
# * If a fatal error is encountered, the director can simply say `cv.stop(message)`;
#   the director is responsible for returning control after issuing a `cv.stop)`;
# * If the actions involve section nodes, it will be checked whether all slots occur in a section,
#   and whether big sections such as books will not start, end, or terminate inside small sections such
#   as verses. Warnings will be issued, but you can suppress them;
# * After the director is done, TF will perform several checks on the result.

def director(cv):
  counter = dict(
    sentence=0,
    line=0,
  )
  cur = dict(
    book=None,
    chapter=None,
    sentence=None,
  )

  wordRe = re.compile(r'^(.*?)([^A-Za-z0-9]*)$')
  metaRe = re.compile(r'^\$\s*([^= ]+)\s*=\s*(.*)')
  
  for line in source.strip().split('\n'):
    line = line.rstrip()
    if not line:
      cv.terminate(cur['sentence'])               # action
      for ntp in counter:
        counter[ntp] += 1
      cur['sentence'] = cv.node('sentence')       # action
      cv.feature(
        cur['sentence'],
        number=counter['sentence'],
      )                                           # action
      continue
      
    if line.startswith('# '):
      for ntp in ('sentence', 'chapter', 'book'):
        cv.terminate(cur[ntp])                    # action
        cur[ntp] = None         
      title = line[2:].strip()
      cur['book'] = cv.node('book')               # action
      for ntp in counter:
        counter[ntp] = 0
      cv.feature(
        cur['book'],
        title=title,
      )                                           # action
      continue

    if line.startswith('## '):
      for ntp in ('sentence', 'chapter'):
        cv.terminate(cur[ntp])                    # action
        cur[ntp] = None         
      number = line[2:].strip()
      cur['chapter'] = cv.node('chapter')         # action
      for ntp in counter:
        counter[ntp] = 0
      cv.feature(
        cur['chapter'],
        number=number,
      )                                           # action
      continue

    if line.startswith('$'):
      match = metaRe.match(line)
      if not match:
        cv.stop(
          f'Malformed metadata line: "{line}"'
        )                                         # action
        return
      name = match.group(1)
      value = match.group(2)
      cv.feature(
        cur['book'],
        **{name: value},
      )                                           # action
      continue
        
    if not cur['sentence']:
      cur['sentence'] = cv.node('sentence')       # action
      counter['sentence'] += 1
      cv.feature(
        cur['sentence'],
        number=counter['sentence'],
      )                                           # action
      
    cur['line'] = cv.node('line')                 # action
    counter['line'] += 1
    cv.feature(
      cur['line'],
      terminator=line[-1],
      number=counter['line'],
    )                                             # action
    
    gap = False
    for word in line.split():
      if word.startswith('['):
        gap = True
        cv.terminate(cur['line'])                 # action
        w = cv.slot()                             # action
        cv.feature(w, gap=1)                      # action
        word = word[1:]
      elif word.endswith(']'):
        w = cv.slot()                             # action
        cv.resume(cur['line'])                    # action
        cv.feature(w, gap=1)                      # action
        gap = False
        word = word[0:-1]
      else:
        w = cv.slot()
        if gap:
          cv.feature(w, gap=1)                    # action

      (letters, punc) = wordRe.findall(word)[0]
      cv.feature(w, letters=letters)              # action
      if punc:
        cv.feature(w, punc=punc)                  # action
    cv.terminate(cur['line'])                     # action
    curLine = None
    
  # just for informational purposes
  print('\nINFORMATION:', cv.activeTypes(), '\n') # action
  
  for ntp in ('sentence', 'chapter', 'book'):
    cv.terminate(cur[ntp])                        # action

  cv.meta(
    'punc', remark='a bit more info is needed',
  )                                               # action


# ## Run
#
# We are going to run the conversion and check whether all is well.

# Next we initialize the conversion machinery: we obtain an object with methods.

# +
cv = CV(TF)

good = cv.walk(
    director,
    slotType,
    otext=otext,
    generic=generic,
    intFeatures=intFeatures,
    featureMeta=featureMeta,
)

good
# -

# ## Inspect
#
# Let's inspect some of the files:
#
# ### otype

with open(f'{TF_PATH}/otype.tf') as fh:
  print(fh.read())

# ### otext

with open(f'{TF_PATH}/otext.tf') as fh:
  print(fh.read())

# ### oslots

with open(f'{TF_PATH}/oslots.tf') as fh:
  print(fh.read())

# #### Explanation
#
# * line `100	1-99` tells that node 100 (the first book node, see *otext*, is linked to slots 1-99, which are all slots.
# * the next line has only `1-55`. These are the slots of node 101, being 1 + the previous node.
#
# And so on.

# ### number

with open(f'{TF_PATH}/number.tf') as fh:
  print(fh.read())

# #### Explanation
#
# Node 101 is the first chapter node, which has chapter number 1.
#
# The next line is about node 102, the second chapter, with number 2.
#
# The following line refers to node 103, and a quick glance at the *otype* feature shows that this is a line.
#
# The last three lines are about the three sentences, which are numbered within their chapter:
# `1` then `2` and then again `1`.

# ### letters

with open(f'{TF_PATH}/letters.tf') as fh:
  print(fh.read())

# #### Explanation
#
# The plain, clean text of everything.

# ### punc

with open(f'{TF_PATH}/punc.tf') as fh:
  print(fh.read())

# Note the metadata field `remark=a bit more info is needed` which was added "last-minute" by means of a `cv.meta()` action.

# # Links
#
# Of course, there is much more to TF.
#
# Have a look through tutorials for several corpora: Hebrew and Syriac Bible, Quran, Uruk Cuneiform.
#
# Navigate from [here](https://nbviewer.jupyter.org/github/annotation/tutorials/tree/master/).
#
# Now conversion is this easy, more corpora will follow.
#
# The docs for conversion are [here](https://annotation.github.io/text-fabric/Create/Convert/).

# ---
# Tutorial for Banks
#
# * [use](https://nbviewer.jupyter.org/github/annotation/tutorials/blob/master/banks/use.ipynb)
#
# ---
