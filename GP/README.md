GS Presence(?) implementation for civ4<br>

Based on works: prmasterserver, miniircd, gsopensdk, aluigi's works<br>

Works on two sockets 29900(GP), 29901(GPSearch)<br>
29901's commands:
1. SEARCH - get user's id by his nick, so then game would ask about him on 29900, using that id. 
/Server itself even without the command is needed because game disconnects itself when client tries to add a buddy without tcp connection to 29901.<br>

GP29900's commands:<br>
1. NEWUSER - adds entry in database and sends correct response to client.<br>
2. LOGIN - checks user data in db and sends correct response.<br>
3. STATUS \logout\. Disconnects client.<br>
4. \lc\1. Initial command, sent to client when new connection is accepted.<br>
5. ADDBUDDY - client wants the server to ask the other dude if he wants to be the buddy, etc. Ignore and just send notification that the mentioned dude is now online and is staging in 'chilling' room as if he is a buddy.
6. GETPROFILE - user gets info about the other user to show, then shows him as a buddy with some of this info 
7. BUDDYMSG - send message to a buddy

There potentially can be implemented more commands, that are related to buddysystem.
