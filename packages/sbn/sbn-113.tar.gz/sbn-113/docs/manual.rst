.. _manual:


.. raw:: html

   <br><br>


.. title:: Manual


**NAME**


    ``SBN`` - Skull, Bones and Number


**SYNOPSIS**


    | ``sbn  <cmd> [key=val] [key==val]``
    | ``sbnc``
    | ``sbnd`` 
    | ``sbns``


**DESCRIPTION**


    ``SBN`` holds evidence that king
    netherlands is doing a genocide, a
    :ref:`written response <king>` where king
    netherlands confirmed taking note
    of “what i have written”, namely
    :ref:`proof  <evidence>` that medicine
    he uses in treatment laws like zyprexa,
    haldol, abilify and clozapine are
    poison.

    Poison that makes impotent, is both
    physical (contracted muscles) and
    mental (make people hallucinate)
    torture and kills members of the
    victim groups: Elderly, Handicapped, Criminals
    and Psychiatric patients.

    ``SBN`` contains :ref:`correspondence
    <writings>` with the International Criminal
    Court, asking for arrest of the king of the
    netherlands, for the genocide he is committing
    with his new treatment laws.

    Current status is a :ref:`"no basis to proceed"
    <writings>` judgement of the prosecutor which
    requires a :ref:`"basis to prosecute" <reconsider>`
    to have the king actually arrested.


**INSTALL**

    | ``pipx install sbn``
    | ``pipx ensurepath``

    <new terminal>

    | ``$ sbn srv > sbn.service``
    | ``$ sudo mv sbn.service /etc/systemd/system/``
    | ``$ sudo systemctl enable sbn --now``
    |
    | joins ``#sbn`` on localhost

**USAGE**

    without any argument the bot does nothing

    | ``$ sbn``
    | ``$``

    see list of commands

    | ``$ sbn cmd``
    | ``cfg,cmd,dne,dpl,err,exp,imp,log,mod,mre,nme,``
    | ``pwd,rem,req,res,rss,srv,syn,tdo,thr,upt``

    start a console

    | ``$ sbnc``
    | ``>``

    use -i to init modules

    | ``$ sbnc -i``
    | ``>``

    start daemon

    | ``$ sbnd``
    | ``$``

    start service

    | ``$ sbns``
    |
    | ``<runs until ctrl-c>``

    show request to the prosecutor

    | $ ``sbn req``
    | Information and Evidence Unit
    | Office of the Prosecutor
    | Post Office Box 19519
    | 2500 CM The Hague
    | The Netherlands

**COMMANDS**

    here is a list of available commands

    | ``cfg`` - irc configuration
    | ``cmd`` - commands
    | ``dpl`` - sets display items
    | ``err`` - show errors
    | ``exp`` - export opml (stdout)
    | ``imp`` - import opml
    | ``log`` - log text
    | ``mre`` - display cached output
    | ``pwd`` - sasl nickserv name/pass
    | ``rem`` - removes a rss feed
    | ``res`` - restore deleted feeds
    | ``req`` - reconsider
    | ``rss`` - add a feed
    | ``syn`` - sync rss feeds
    | ``tdo`` - add todo item
    | ``thr`` - show running threads
    | ``upt`` - show uptime

**CONFIGURATION**

    irc

    | ``$ sbn cfg server=<server>``
    | ``$ sbn cfg channel=<channel>``
    | ``$ sbn cfg nick=<nick>``

    sasl

    | ``$ sbn pwd <nsvnick> <nspass>``
    | ``$ sbn cfg password=<frompwd>``

    rss

    | ``$ sbn rss <url>``
    | ``$ sbn dpl <url> <item1,item2>``
    | ``$ sbn rem <url>``
    | ``$ sbn nme <url> <name>``

    opml

    | ``$ sbn exp``
    | ``$ sbn imp <filename>``


**SOURCE**

    source is at `https://github.com/bthate/sbn <https://github.com/bthate/sbn>`_

**FILES**

    | ``~/.sbn``
    | ``~/.local/bin/sbn``
    | ``~/.local/bin/sbnd``
    | ``~/.local/bin/sbns``
    | ``~/.local/pipx/venvs/sbn/*``

**AUTHOR**

    | Bart Thate <bthate@dds.nl>

**COPYRIGHT**

    | ``SBN`` is Public Domain.
    |
