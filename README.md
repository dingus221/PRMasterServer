<strong>Fully functional(not yet) gayspy substitute for civ4bts and civ4 (which is based on https://github.com/novice-rb/PRMasterServer)


<strong>1. Give a man a lobby and he spams shit in it for a life or what is done so far.</strong><br>

1. Master server(port 29900) - logging in and registering new users - works like a swiss clock.
2. Peerchat server(port 6667) - chatting works perfectly good (as far as tested) 
3. Natneg server (port 27901) - provides connection information to players about other players when they join staging room.
4. Serverbrowser (port 28910) is currently not fully functional. People in lobby can see the hosted games. But refresh button doesnt work. To refresh u need to relogin.
5. Queryserver (port 27900) - game hosts report status of their server into it. Interlinked with SB. Refreshing problem might be in this one.
6. Webservver (port 80) - i suspect it is needed only for automatically downloading of new patches (or just checking for them). 


<strong>2. How shit is done.</strong><br>
Most functionality is already implemented in PR Master server. We just comment out parts of code that give errors. And substitute all mentions of battlefield for civ4.

<strong>3. WANTED LOGS OF REAL GAMESPY<->CIV4 COMMUNICATIONS</strong><br>
Logs of wireshark or other software, would help significantly. Is really lame that nobody figured out how to use wireshark while gamespy was still up.


<strong>4. PEERCHAT SERVER</strong><br>
Python implementatnion of irc server, supporting gs crypting https://github.com/Zulan/miniircd
Delphi implementation, little bit messy, but works good is included here in folder GSAIRCDTMM.



<strong>
5. Current progress</strong>
It is roughly 75% done yet.<br>


<strong>6. Current problems and directions of investigation:<br></strong>
1. Serverlist refresh button doesn't work and information about servers like number of players in game, map and ping is not updated. Supposedly game should request that info directly from other gameservers.<br>

<strong>7. How gamespy server works for nabs</strong>
<br>
Here i will write some bullshit for nabs


<strong>8. Setting up the project</strong><br>

1. Be sure to have [Visual Studio 2013](http://www.microsoft.com/en-us/download/details.aspx?id=40787) installed.  You might be able to compile it using previous versions of Visual Studio or using Mono, but this is untested and may not work.

2. Open **PRMasterServer.sln**, and build. This should download via NuGet any extra packages required.

3. Grab the latest [MaxMind GeoIP2 Country](https://www.maxmind.com/en/country) database, or use the free [GeoLite2 Country](http://dev.maxmind.com/geoip/geoip2/geolite2/) database. Put it in the same folder as **PRMasterServer.exe**.

5. Run **PRMasterServer.exe +db logindb.db3 +game civ4bts +servers master,login,cdkey,list,natneg**, now game parameter doesnt matter, it will service civ4, civ4bts and civ4btsjp

6. Run irc server.

7. To join the lobby from the game you need to configure windows/system32/drivers/etc/hosts file (or redirect dead official gamespy server traffick of the game to the server in other ways). Correct hosts file included.


9. Credits (in order of importance)
<br><font size=14><strong>[novice-rb]</strong> for natneg
<br><font size=14><strong>[AncientMan2002]</strong> for original masterserver
<br><font size=14><strong>[Luigi Auriemma](http://aluigi.org) </strong> for reverse engineering the GameSpy protocol and encryption.
<br><font size=14><strong>[Caledorn], [Zulan] </strong> - users on realmsbeyond.net, for running natneg servers
<br><font size=14><strong>[SexIsBad2TheBone], [DimosEngel]</strong> civ4 players (testing)
<br><font size=14><strong>[gamespy] </strong> for not being too hard encrypted and secretive [Rest in peace]
<br><font size=14><strong>[sid meyer and firaxis] </strong> for great game
