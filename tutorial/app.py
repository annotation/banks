# ---
# jupyter:
#   jupytext:
#     formats: ipynb,md,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# <img align="right" src="images/tf-small.png" width="128"/>
# <img align="right" src="images/phblogo.png" width="128"/>
# <img align="right" src="images/dans.png"/>
#
# ---
# Start with [convert](https://nbviewer.jupyter.org/github/annotation/banks/blob/master/programs/convert.ipynb)
#
# ---

# # The Banks example corpus as app

# %load_ext autoreload
# %autoreload 2

from tf.app import use

# We do not only load the main corpus data, but also the additional *sim* (similarity) feature that is in a
# module.
#
# For the very last version, use `hot`.
#
# For the latest release, use `latest`.
#
# If you have cloned the repos (TF app and data), use `clone`.
#
# If you do not want/need to upgrade, leave out the checkout specifiers.

A = use(
    "banks:clone",
    checkout="clone",
    mod="annotation/banks/sim/tf:clone",
    hoist=globals(),
)
# A = use('banks:hot', checkout="hot", mod='annotation/banks/sim/tf:hot', hoist=globals())
# A = use('banks:latest', checkout="latest", mod='annotation/banks/sim/tf:latest', hoist=globals())
# A = use('banks', mod='annotation/banks/sim/tf', hoist=globals())

# # Use the similarity edge feature
#
# We print all similar pairs of words that are at least 50% similar but not 100%.

query = """
word
<sim>50> word
"""

results = A.search(query)

A.table(results, end=10, withPassage="1 2")

A.show(results, end=5)

# We sort each pair.
# We keep track of pairs we have seen in order to prevent printing duplicate pairs.

seen = set()
for (w1, w2) in results:
    if (w2, 100) in E.sim.b(w1):
        continue
    letters1 = F.letters.v(w1)
    letters2 = F.letters.v(w2)
    pair = tuple(sorted((letters1, letters2)))
    if pair in seen:
        continue
    seen.add(pair)
    print(" ~ ".join(pair))

# ---
# All chapters:
#
# * [use](use.ipynb)
# * [share](share.ipynb)
# * *app*
# * [repo](repo.ipynb)
# * [compose](compose.ipynb)
#
# ---
#
# CC-BY Dirk Roorda
