
Supernova
=========

The python version of the Supernova bot. The bot itself is contained in the
[suno](suno) directory.

The [setup.py](setup.py) file serves the purpose of describing the package,
it's associated python version and other metadata.

Commands
========

Commands are stored in the Makefile and thus, are run with `make command`.

To better understand how each command work, open the [Makefile](Makefile).

install
-------

installs virtualenv if not found, then create the virtuial env for the project.
Everythin will be installed into this env.

Then, installs the whole python module and its dependencies, as defined in
[requirements.txt](requirements.txt) .

start
-----
Starts the bot in daemon mode (in the background). Needs your github token
if the hidden [.token](.token) file. This file is not versionned and **must
not** be.

The bot will write its pid in the file defined in in the makefile (search for
the PIDFILE constantm default if [.pid](.pid)).

Logs are stored in the "suno.{{subpart}}.log" file. For example, the main
app's logs are stored in [suno.app.log](suno.app.log) .

stop
----
Stops the bot, using the bot's pid, stored in the pidfile. The bot will remove
the pidfikle itself.

dev
---

Like start, but runs the bot in foreground. The logs are then visible in the
terminal. The pidfile is not written, but your token is still needed.



commands to deploy
===
 * `git reset --hard`
 * `git pull --rebase`
 * remove logs if necessary
 * `vi suno/config.py ## set debug to False`
 * `make kill start`

zad
---
```
!react gives_role "Réagissez pour vous (dés-)assigner les roles:
** **
**Non-mixités**
** **
🖤 - Racisæ
🇫 - Féminisme
♿  - Handi
🎭 - Neuro-divergent·e
🐱 - Système multiple
🇰 - Alterhumainæ/otherkin
🇳 - Non-binaire
🏳️‍⚧️ - Trans
🏹 - Aro-ace 
" 🖤 "Racisæ" 🇫 "Féminisme" ♿ "Handi" 🎭 "Neuro-divergent·e" 🐱 "Système multiple" 🇰 "Alterhumainæ/otherkin" 🇳 "Non-binaire" 🏳️‍⚧️ "Trans" 🏹 "Aro-ace"
```



Metadata
========

 * **@author**: The Ex-Tipoui community
 * **@creation data**: 17/03/2022
