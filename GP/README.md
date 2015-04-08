gs presence server (GP)
based on works: prmasterserver, miniircd, gsopensdk, aluigi's works

Works on two sockets 29900(GP), 29901(GPSearch)
29901 socket doesnt process any commands, because they are related to buddysystem. Needed because game disconnects itself
when client tries to add a buddy without tcp connection to 29901.

GP29900. In this implementation it processes 2 main commands and 2 small commands.
Main commands:
1. NEWUSER - adds entry in database and sends correct response to client.
2. LOGIN - checks user data in db and sends correct response.
Small commands:
1. STATUS \logout\. Disconnects client.
2. \lc\1. Initial command, sent to client when new connection is accepted.
There potentially can be implemented more commands, that are all related to buddysystem.
