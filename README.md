<strong>Fully functional(not yet) gayspy substitute for civ4bts and civ4 (which is based on https://github.com/novice-rb/PRMasterServer)


<strong>1. Give a man a lobby and he spams shit in it for a life or what is done so far.</strong><br>

1. Master server(port 29900) - logging in and registering new users - works like a swiss clock.
2. Peerchat server(port 6667) - chatting works perfectly good (as far as tested) 
3. Natneg - might need some modifications, some people can join and play games, some cant. Not 100% sure if its natneg problem yet.
3. Serverbrowser (port 28910) is currently working lame. People in lobby can see the hosted games. But refreshing is glitchy. Only works on relogging. Refresh button doesnt work.  
4. Queryserver (port 27900) - game hosts report status of their server into it. Interlinked with SB. Refreshing problem might be in this one.
5. Webservver (port 80) - i suspect it is needed only for automatically downloading of new patches (or just checking for them). It needs to direct to some fast reacheable place that either responds with 404 or propper stuff or port isnt listened to. The key point is that it responds fast, else u will have 90 seconds freeze on login.
xxx. Buddying system is not implemented yet


<strong>2. How shit is done.</strong><br>
Most functionality is already implemented in PR Master server. We just comment out parts of code that give errors. And substitute all mentions of battlefield for civ4.

<strong>3. WANTED LOGS OF REAL GAMESPY<->CIV4 COMMUNICATIONS</strong><br>
Logs of wireshark or other software, would help significantly. Is really lame that nobody figured out how to use wireshark while gamespy was still up.


<strong>4. PEERCHAT SERVER</strong><br>
GSAIRCDTMM - irc daemon supporting gs encoding and some gs custom irc commands.  It is written in delphi7SE, it uses additional dll(LALCIRCENCDEC).


<strong>
5. Current progress</strong>
It is roughly 75% done yet.<br>


<strong>6. Current problems and directions of investigation:<br></strong>
1. Serverlist refresh button doesn't work. Or works only cosmetically, pretending that serverlist is refreshed (NO FUCKIGN KIDDING).
It turns out to be hard to figure out how to fix this. The reason for that is that when player hits refresh button, no data is sent from gameclient. And thereafter no new data is recieved when refresh is hit.<br>
Currently I have 2 hypothesis why no data is sent and how it works.<br>
1.1. Refreshing doesn't send any data because gameclient thinks its not logged in particularly in SB. It might be expecting and not getting some kind of SB related challenge at logging in. And refreshing button checks if that SB challenge was recieved everytime and if no doesnt do its function.<br>
1.2. It doesn't send any data because it was designed to be a fraud button. Data is sent at the point of logging in. And each time new game is hosted only new data about this game is sent. And gameclient has unshown serverlist that is being updated. But visible list of games is updated from that invisible one on hitting refresh. It makes sense cause this way gamespy saves its traffick, sending whole list of servers each time someone hits refresh might take some bandwidth.<br>
Investigation directions.<br>
1.1.1. To find out if its the right hypothesis, it is needed to look into more logs of communications with real gamespy SB available on internet, and hopefully find some of more similar game than bf.<br>
1.2.1. I tested it a little, and if this is the right hypothesis, correct content of the header of this kind of updating serverlist for client is needed. Currently i only tried to send whole serverlist.<br>
<br>
2. Testing shows, that some players connect better than others, while some can't connect to anyone. We were able to start a game with 3 people somehow (needs testing)<br>
3. Hosts still get error from time to time - "sb not responsive"<br>

<strong>7. How gamespy server works for nabs</strong>
<br>
Here i will write some bullshit for nabs


<strong>8. Setting up the project</strong><br>

1. Be sure to have [Visual Studio 2013](http://www.microsoft.com/en-us/download/details.aspx?id=40787) installed.  You might be able to compile it using previous versions of Visual Studio or using Mono, but this is untested and may not work.

2. Open **PRMasterServer.sln**, and build. This should download via NuGet any extra packages required.

3. Grab the latest [MaxMind GeoIP2 Country](https://www.maxmind.com/en/country) database, or use the free [GeoLite2 Country](http://dev.maxmind.com/geoip/geoip2/geolite2/) database. Put it in the same folder as **PRMasterServer.exe**.

5. Run **PRMasterServer.exe +db logindb.db3 +game civ4 +servers master,login,cdkey,list,natneg** or **PRMasterServer.exe +db logindb.db3 +game civ4bts +servers master,login,cdkey,list,natneg**

6. Set up irc server - run GSAIRCDTMM, doesnt need no configurationing.

7. To join the lobby from the game you need to configure windows/system32/drivers/etc/hosts file (or redirect dead official gamespy server traffick of the game to the server in other ways). Will include hosts file for hosts testing, redirecting all to 127.0.0.1.


9. Credits (in order of importance)
---------------------

[novice-rb] for natneg
--
[AncientMan2002] for original masterserver
--
[Luigi Auriemma](http://aluigi.org) for reverse engineering the GameSpy protocol and encryption.
--
[Caledorn], [Zulan] - users on realmsbeyond.net, for running natneg servers
--
[SexIsBad2TheBone], [DimosEngel] civ4 players (testing)
--
[gamespy] for not being too hard encrypted and secretive [Rest in peace]
--
[sid meyer and firaxis] for great game
--
