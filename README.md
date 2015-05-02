PRMasterServer
==============

A GameSpy replacement Master Server for Civilization 4 (and Beyond the Sword addon). This emulates the GameSpy API in order to keep Civilziation 4 playable via the lobby after the GameSpy shutdown.

This is a cleaned up version of
https://github.com/dingus221/PRMasterServer

Features
---------------------
- Master server(port 29900) - logging in and registering new users (works)
- Natneg server (port 27901) - provides connection information to players about other players when they join staging room.
- Serverbrowser (port 28910) is currently not fully functional. People in lobby can see the hosted games. But refresh button doesn't work. To refresh you need to re-login.
- Queryserver (port 27900) - game hosts report status of their server into it. Interlinked with serverbrowser. Refreshing problem might be in this one.
- Webserver (port 80) - I suspect it is needed only for automatically downloading of new patches (or just checking for them). 
- For a peerchat server(port 6667) see https://github.com/Zulan/miniircd

There are different implementations for most of the servers. All servers are implemented in  C#  (PRMasterServer), but some of the servers seem to be not really stable, at least on Linux/wine. In SBQRC4, there is the Serverbrowser and Queryserver in python2. In  GP there is the Master (login) server in python2. In python3, there are implementations of Master (login) and Querybrowser/Serverbrowser (gamebrowser). The python3 implementation is the most recent and cleaned up version.

Setting up the project
---------------------
1. Be sure to have [Visual Studio 2013](http://www.microsoft.com/en-us/download/details.aspx?id=40787) installed.  You might be able to compile it using previous versions of Visual Studio or using Mono, but this is untested and may not work.

2. Open **PRMasterServer.sln**, and build. This should download via NuGet any extra packages required.

3. Grab the latest [MaxMind GeoIP2 Country](https://www.maxmind.com/en/country) database, or use the free [GeoLite2 Country](http://dev.maxmind.com/geoip/geoip2/geolite2/) database. Put it in the same folder as **PRMasterServer.exe**.

4. Run **PRMasterServer.exe +db logindb.db3 +game civ4bts +servers master,login,cdkey,list,natneg**, now game parameter doesnt matter, it will service civ4, civ4bts and civ4btsjp. Servers can be run in different instances. Or run the respective python verions.

5. Setup the IRC server https://github.com/Zulan/miniircd

6. To join the lobby from the game you need to configure windows/system32/drivers/etc/hosts file (or redirect dead official GameSpy server traffic of the game to the server in other ways such as modifying the exe file). A hosts file  with necessary redirects is included.

---------------------
Current issues

1. Buddy system does not work

Credits
---------------------

- [dingus221] for the modifications of the masterserver towards Civilization 4 support
- [novice-rb] for natneg
- [AncientMan2002] for original masterserver
- [Luigi Auriemma](http://aluigi.org) </strong> for reverse engineering the GameSpy protocol and encryption.
- [Caledorn] - users on realmsbeyond.net, for running the initial natneg server
- [SexIsBad2TheBone], [DimosEngel] civ4 players (testing)
- [GameSpy] for not being too hard encrypted and secretive [Rest in peace]
- [Sid Meyer and Firaxis] for great game
- [Zulan] code cleanup and server hosting
