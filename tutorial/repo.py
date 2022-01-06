# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python3.9
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

# # Getting data from online repos
#
# We show the various automatic ways by which you can get data that is out there on GitHub to your computer.
#
# The work horse is the function `checkoutRepo()` in `tf.applib.repo`.
#
# Text-Fabric uses this function for all operations where data flows from GitHub to your computer.
#
# There are quite some options, and here we explain all the `checkout` options, i.e. the selection of
# data from the history.
#
# See also the [documentation](https://annotation.github.io/text-fabric/tf/advanced/repo.html).

# %load_ext autoreload
# %autoreload 2

# ## Leading example
#
# We use markdown display from IPython purely for presentation.
# It is not needed to run `checkoutRepo()`.

from tf.advanced.helpers import dm
from tf.advanced.repo import checkoutRepo

# We work with our tiny example TF app: `banks`.

ORG = "annotation"
REPO = "banks"
MAIN = "tf"
MOD = "sim/tf"


# `MAIN`points to the main data, `MOD` points to a module of data: the similarity feature.

# ## Presenting the results
#
# The function `do()` just formats the results of a `checkoutRepo()` run.
#
# The result of such a run, after the progress messages, is a tuple.
# For the explanation of the tuple, read the [docs](https://annotation.github.io/text-fabric/tf/advanced/repo.html).


def do(task):
    md = f"""
commit | release | local | base | subdir
--- | --- | --- | --- | ---
`{task[0]}` | `{task[1]}` | `{task[2]}` | `{task[3]}` | `{task[4]}`
"""
    dm(md)


# + [markdown] toc-hr-collapsed=false
# ## All the checkout options
#
# We discuss the meaning and effects of the values you can pass to the `checkout` option.
# -

# ### `clone`
#
# > Look whether the appropriate folder exists under your `~/github` directory.
#
# This is merely a check whether your data exists in the expected location.
#
# * No online checks take place.
# * No data is moved or copied.
#
# **NB**: you cannot select releases and commits in your *local* GitHub clone.
# The data will be used as it is found on your file system.
#
# **When to use**
#
# > If you are developing new feature data.
#
# When you develop your data in a repository, your development is private as long as you
# do not push to GitHub.
#
# You can test your data, even without locally committing your data.
#
# But, if you are ready to share your data, everything is in place, and you only
# have to commit and push, and pass the location on github to others, like
#
# ```
# myorg/myrepo/subfolder
# ```

do(checkoutRepo(org=ORG, repo=REPO, folder=MAIN, version="0.2", checkout="clone"))

# We show what happens if you do not have a local github clone in `~/github`.

# + language="sh"
#
# mv ~/github/annotation/banks/tf ~/github/annotation/banks/tfxxx
# -

do(checkoutRepo(org=ORG, repo=REPO, folder=MAIN, version="0.2", checkout="clone"))

# Note that no attempt is made to retrieve online data.

# + language="sh"
#
# mv ~/github/annotation/banks/tfxxx ~/github/annotation/banks/tf
# -

# ### `local`
#
# > Look whether the appropriate folder exists under your `~/text-fabric-data` directory.
#
# This is merely a check whether your data exists in the expected location.
#
# * No online checks take place.
# * No data is moved or copied.
#
# **When to use**
#
# > If you are using data created and shared by others, and if the data
# is already on your system.
#
# You can be sure that no updates are downloaded, and that everything works the same as the last time
# you ran your program.
#
# If you do not already have the data, you have to pass `latest` or `hot` or `''` which will be discussed below.

do(checkoutRepo(org=ORG, repo=REPO, folder=MAIN, version="0.2", checkout="local"))

# You see this data because earlier I have downloaded release `v2.0`, which is a tag for
# the commit with hash `9713e71c18fd296cf1860d6411312f9127710ba7`.

# If you do not have any corresponding data in your `~/text-fabric-data`, you get this:

# + language="sh"
#
# mv ~/text-fabric-data/annotation/banks/tf ~/text-fabric-data/annotation/banks/tfxxx
# -

do(checkoutRepo(org=ORG, repo=REPO, folder=MAIN, version="0.2", checkout="local"))

# + language="sh"
#
# mv ~/text-fabric-data/annotation/banks/tfxxx ~/text-fabric-data/annotation/banks/tf
# -

# ### `''` (default)
#
# This is about when you omit the `checkout` parameter, or pass `''` to it.
#
# The destination for local data is your `~/text-fabric-data` folder.
#
# If you have already a local copy of the data, that will be used.
#
# If not:
#
# > Note that if your local data is outdated, no new data will be downloaded.
# You need `latest` or `hot` for that.
#
# But what is the latest online copy? In this case we mean:
#
# * the latest *release*, and from that release an appropriate attached zip file
# * but if there is no such zip file, we take the files from the corresponding commit
# * but if there is no release at all, we take the files from the *latest commit*.
#
# **When to use**
#
# > If you need data created/shared by other people and you want to be sure that you always have the
# same copy that you initially downloaded.
#
# * If the data provider makes releases after important modifications, you will get those.
# * If the data provider is experimenting after the latest release, and commits them to GitHub,
#   you do not get those.
#
# However, with `hot`, you `can` get the latest commit, to be discussed below.

do(checkoutRepo(org=ORG, repo=REPO, folder=MAIN, version="0.2", checkout=""))

# Note that no data has been downloaded, because it has detected that there is already local data on your computer.

# If you do not have any checkout of this data on your computer, the data will be downloaded.

# + language="sh"
#
# rm -rf ~/text-fabric-data/annotation/banks/tf
# -

do(checkoutRepo(org=ORG, repo=REPO, folder=MAIN, version="0.2", checkout=""))

# #### Note about versions and releases
#
# The **version** of the data is not necessarily the same concept as the **release** of it.
#
# It is possible to keep the versions and the releases strictly parallel,
# but in text conversion workflows it can be handy to make a distinction between them,
# e.g. as follows:
#
# > the version is a property of the input data
# > the release is a property of the output data
#
# When you create data from sources using conversion algorithms,
# you want to increase the version if you get new input data, e.g. as a result of corrections
# made by the author.
#
# But if you modify your conversion algorithm, while still running it on the same input data,
# you may release the new output data as a **new release** of the **same version**.
#
# Likewise, when the input data stays the same, but you have corrected typos in the metadata,
# you can make a **new release** of the **same version** of the data.
#
# The conversion delivers the features under a specific version,
# and Text-Fabric supports those versions: users of TF can select the version they work with.
#
# Releases are made in the version control system (git and GitHub).
# The part of Text-Fabric that auto-downloads data is aware of releases.
# But once the data has been downloaded in place, there is no machinery in Text-Fabric to handle
# different releases.
#
# Yet the release tag and commit hash are passed on to the point where it comes to recording
# the provenance of the data.

# #### Download a different version
#
# We download version `0.1` of the data.

do(checkoutRepo(org=ORG, repo=REPO, folder=MAIN, version="0.1", checkout=""))

# Several observations:
#
# * we obtained the older version from the *latest* release, which is still release `v2.0`
# * the download looks different from when we downloaded version `0.2`;
#   this is because the data producer has zipped the `0.2` data and has attached it to release `v2.0`,
#   but he forgot, or deliberately refused, to attach version `0.1` to that release;
#   so it has been retrieved directly from the files in the corresponding commit, which is
#   `9713e71c18fd296cf1860d6411312f9127710ba7`.

# For the verification, an online check is needed. The verification consists of checking the release tag and/or commit hash.
#
# If there is no online connection, you get this:

# + language="sh"
#
# networksetup -setairportpower en0 off
# -

do(checkoutRepo(org=ORG, repo=REPO, folder=MAIN, version="0.1", checkout="latest"))

# or if you do not have local data:

# + language="sh"
#
# mv ~/text-fabric-data/annotation/banks/tf/0.1 ~/text-fabric-data/annotation/banks/tf/0.1xxx
# -

do(checkoutRepo(org=ORG, repo=REPO, folder=MAIN, version="0.1", checkout="latest"))

# + language="sh"
#
# mv ~/text-fabric-data/annotation/banks/tf/0.1xxx ~/text-fabric-data/annotation/banks/tf/0.1

# + language="sh"
#
# networksetup -setairportpower en0 on
# -

# ### `latest`
#
# > The latest online release will be identified,
# and if you do not have that copy locally, it will be downloaded.
#
# **When to use**
#
# > If you need data created/shared by other people and you want to be sure that you always have the
# latest *stable* version of that data, unreleased data is not good enough.
#
# One of the difference with `checkout=''` is that if there are no releases, you will not get data.

do(checkoutRepo(org=ORG, repo=REPO, folder=MAIN, version="0.2", checkout="latest"))

# There is no sim/tf data in any release commit, so if we look it up, it should fail.

do(checkoutRepo(org=ORG, repo=REPO, folder=MOD, version="0.2", checkout="latest"))

# But with `checkout=''` it will only be found if you do not have local data already:

do(checkoutRepo(org=ORG, repo=REPO, folder=MOD, version="0.2", checkout=""))

# In that case there is only one way: `hot`:

do(checkoutRepo(org=ORG, repo=REPO, folder=MOD, version="0.2", checkout="hot"))

# ### `hot`
#
# > The latest online commit will be identified,
# and if you do not have that copy locally, it will be downloaded.
#
# **When to use**
#
# > If you need data created/shared by other people and you want to be sure that you always have the
# latest version of that data, whether released or not.
#
# The difference with `checkout=''` is that if there are releases,
# you will now get data that may be newer than the latest release.

do(checkoutRepo(org=ORG, repo=REPO, folder=MAIN, version="0.2", checkout="hot"))

# Observe that data has been downloaded, and that we have now data corresponding to a different commit hash,
# and not corresponding to a release.
#
# If we now ask for the latest *stable* data, the data will be downloaded anew.

do(checkoutRepo(org=ORG, repo=REPO, folder=MAIN, version="0.2", checkout="latest"))

# ### `v1.0` a specific release
#
# > Look for a specific online release to get data from.
#
# **When to use**
#
# > When you want to replicate something, and need data from an earlier point in the history.

do(checkoutRepo(org=ORG, repo=REPO, folder=MAIN, version="0.1", checkout="v1.0"))

# We might try to get version `0.2` from this release.

do(checkoutRepo(org=ORG, repo=REPO, folder=MAIN, version="0.2", checkout="v1.0"))

# At that early point in the history there is not yet a version `0.2` of the data.

# ### `a81746c` a specific commit
#
# > Look for a specific online commit to get data from.
#
# **When to use**
#
# > When you want to replicate something, and need data from an earlier point in the history, and there is no
# release for that commit.

do(
    checkoutRepo(
        org=ORG,
        repo=REPO,
        folder=MAIN,
        version="0.1",
        checkout="a81746c5f9627637db4dae04c2d5348bda9e511a",
    )
)

# + [markdown] toc-hr-collapsed=false
# ## *source* and *dest*: an alternative for `~/github` and `~/text-fabric-data`
#
# Everything so far uses the hard-wired `~/github` and `~/text-fabric-data` directories.
# But you can change that:
#
# * pass *source* as a replacement for `~/github`.
# * pass *dest* as a replacement for `~/text-fabric-data`.
#
# **When to use**
#
# > if you do not want to interfere with the `~/text-fabric-data` directory.
#
# Text-Fabric manages the `~/text-fabric-data` directory,
# and if you are experimenting outside Text-Fabric
# you may not want to touch its data directory.
#
# > if you want to clone data into your `~/github` directory.
#
# Normally, TF uses your `~/github` directory as a source of information,
# and never writes into it.
# But if you explicitly pass `dest=~/github`, things change: downloads will
# arrive under `~/github`. Use this with care.
#
# > if you work with cloned data outside your `~/github` directory,
#
# you can let the system look in *source* instead of `~/github`.
# -

# We customize source and destination directories:
#
# * we put them both under `~/Downloads`
# * we give them different names

MY_GH = "~/Downloads/repoclones"
MY_TFD = "~/Downloads/textbase"

# Download a fresh copy of the data to `~/Downloads/textbase` instead.

do(
    checkoutRepo(
        org=ORG,
        repo=REPO,
        folder=MAIN,
        version="0.2",
        checkout="",
        source=MY_GH,
        dest=MY_TFD,
    )
)

# Lookup the same data locally.

do(
    checkoutRepo(
        org=ORG,
        repo=REPO,
        folder=MAIN,
        version="0.2",
        checkout="",
        source=MY_GH,
        dest=MY_TFD,
    )
)

# We copy the local github data to the custom location:

# + language="sh"
#
# mkdir -p ~/Downloads/repoclones/annotation
# cp -R ~/github/annotation/banks ~/Downloads/repoclones/annotation/banks
# -

# Lookup the data in this alternative directory.

do(
    checkoutRepo(
        org=ORG,
        repo=REPO,
        folder=MAIN,
        version="0.2",
        checkout="clone",
        source=MY_GH,
        dest=MY_TFD,
    )
)

# Note that the directory trees under the customised *source* and *dest* locations have exactly the same shape as before.

# ## Conclusion
#
# With the help of `checkoutRepo()` you will be able to make local copies of online data in an organized way.
#
# This will help you when
#
# * you use other people's data
# * develop your own data
# * share and publish your data
# * go back in history.

# ---
# All chapters:
#
# * [use](use.ipynb)
# * [share](share.ipynb)
# * [app](app.ipynb)
# * *repo*
# * [compose](compose.ipynb)
#
# ---
