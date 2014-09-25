<strong>Fully functional(not yet) gayspy substitute for civ4bts and civ4 (which is based on https://github.com/novice-rb/PRMasterServer)


<strong>1. Give a man a lobby and he spams shit in it for a life or what is done so far.</strong><br>

1. Logging in gamespy interface works like a swiss clock.
2. Chatting works perfectly good (as far as tested) 
3. Serverbrowsing and shit is currently working lame. Can host game. Others can see the hosted games in the list. But can't join them yet. And refreshing is superglitchy and buggy.
4. buddying system is not implemented in any way, but nobody needs it


<strong>2. You can get more of what you want with a kind word and a google, than you can with just a kind word.</strong><br>
I am no big coder, but using google is everything that has been needed here (all was largely already done before me, just needed minor adjustments from battlefield). Commenting stuff out and substituting "battlefield" for "civ4" are 2 methods that i have been using the most so far.


<strong>3. WANTED LOGS OF REAL GSSERVER<->CIV4 COMMUNICATIONS</strong><br>
Logs of wireshark or other software, would help significantly. Currently i dont know what actually was sent.
I am working with logs from similar games found on google. If you have any usefull related logs, please send them to me.


<strong>4. More detail about irc server</strong><br>
So far I can say that irc server doesnt need to communicate with masterserver. You can use any normal irc + GS peerchat server emulator 0.1.3b (http://aluigi.altervista.org/papers.htm#peerchat) from luigi. But it seems to be limited to max 2 clients. U can also use GSAIRCDTMM. It is written in delphi, but it contains dll(LALCIRCENCDEC) with encrypting functionality in c++ (this unnecesarily complicates things, but who gives a dong, was fastest way to implement).


<strong>
5. Current progress</strong>
It is roughly 50% done yet.<br>
  Current directons of development:<br>
    0) investigate no challenge error<br>
    1) test gsSDK peer demos more thoroughly<br>
    2) implement GETCKEY handling in irc<br>
    3) inspect server responses at ports 28910, 27900 <br>

<strong>
6. Current problems:<br></strong>
1. Serverlist refreshing is glitchy and buggy<br>
2. Host gets error from time to time (test: maybe only on joining him?) - "sb not responsive"<br>
3. Can't join staging rooms - "brandmauer didnt allow" error




<strong>7. How gamespy server works for nabs</strong>
<br>
Here ill write some bullshit for nabs


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
