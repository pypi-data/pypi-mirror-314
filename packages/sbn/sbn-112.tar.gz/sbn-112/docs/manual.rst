.. _manual:


.. raw:: html

   <br><br>


.. title:: Manual



**NAME**


    ``GENOCIDE`` - Since 4 march 2019


**SYNOPSIS**


    | ``genocide  <cmd> [key=val] [key==val]``
    | ``genocided`` 
    | ``genocides``


**DESCRIPTION**


    ``GENOCIDE`` holds evidence that king
    netherlands is doing a genocide, a
    written response where king
    netherlands confirmed taking note
    of “what i have written”, namely
    :ref:`proof  <evidence>` that medicine
    he uses in treatment laws like zyprexa,
    haldol, abilify and clozapine are
    poison that make impotent, is both
    physical (contracted muscles) and
    mental (make people hallucinate)
    torture and kills members of the
    victim groups.

    ``GENOCIDE`` contains :ref:`correspondence
    <writings>` with the International Criminal
    Court, asking for arrest of the king of the
    netherlands, for the genocide he is committing
    with his new treatment laws.

    Current status is a :ref:`"no basis to proceed"
    <writings>` judgement of the prosecutor which
    requires a :ref:`"basis to prosecute" <reconsider>`
    to have the king actually arrested.


**INSTALL**

    | ``pipx install genocide``
    | ``pipx ensurepath``

    <new terminal>

    | ``$ genocide srv > genocide.service``
    | ``$ sudo mv genocide.service /etc/systemd/system/``
    | ``$ sudo systemctl enable genocide --now``
    |
    | joins ``#genocide`` on localhost

**USAGE**

    without any argument the bot does nothing

    | ``$ genocide``
    | ``$``

    see list of commands

    | ``$ genocide cmd``
    | ``cfg,cmd,dne,dpl,err,exp,imp,log,mod,mre,nme,``
    | ``pwd,rem,req,res,rss,srv,syn,tdo,thr,upt``

    start a console

    | ``$ genocidec``
    | ``>``

    use -i to init modules

    | ``$ genocidec -i``
    | ``>``

    start daemon

    | ``$ genocided``
    | ``$``

    start service

    | ``$ genocides``
    |
    | ``<runs until ctrl-c>``

    show request to the prosecutor

    | $ ``genocide req``
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

    | ``$ genocide cfg server=<server>``
    | ``$ genocide cfg channel=<channel>``
    | ``$ genocide cfg nick=<nick>``

    sasl

    | ``$ genocide pwd <nsvnick> <nspass>``
    | ``$ genocide cfg password=<frompwd>``

    rss

    | ``$ genocide rss <url>``
    | ``$ genocide dpl <url> <item1,item2>``
    | ``$ genocide rem <url>``
    | ``$ genocide nme <url> <name>``

    opml

    | ``$ genocide exp``
    | ``$ genocide imp <filename>``


**SOURCE**

    source is at `https://github.com/bthate/genocide <https://github.com/bthate/genocide>`_

**FILES**

    | ``~/.genocide``
    | ``~/.local/bin/genocide``
    | ``~/.local/bin/genocided``
    | ``~/.local/bin/genocides``
    | ``~/.local/pipx/venvs/genocide/*``

**AUTHOR**

    | Bart Thate <bthate@dds.nl>

**COPYRIGHT**

    | ``GENOCIDE`` is Public Domain.
    |
