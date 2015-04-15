<strong>Gs presence server (GP)

<strong>based on works: prmasterserver, miniircd, gsopensdk, aluigi's works

Works on two sockets 29900(GP), 29901(GPSearch)<br>
29901 socket doesnt need to process any commands, because they are related to buddysystem. Needed because game disconnects itself
when client tries to add a buddy without tcp connection to 29901.

<strong>GP29900. In this (minimalistic?) implementation it processes 2 main commands and 2 small commands.<br></strong>
<strong>Main commands:<br></strong>
1. NEWUSER - adds entry in database and sends correct response to client.<br>
2. LOGIN - checks user data in db and sends correct response.<br>
<strong>Small commands:<br></strong>
1. STATUS \logout\. Disconnects client.<br>
2. \lc\1. Initial command, sent to client when new connection is accepted.<br>
There potentially can be implemented more commands, that are all related to buddysystem.<br>
