<strong>GameSpy server substitute for civ4bts and civ4 (which is based on https://github.com/novice-rb/PRMasterServer)


<strong>1. Give a man a lobby and he spams shit in it for life or what is done so far.</strong><br>

1. Gamespy Presence and Search (port 29900 and 29901) - works 8.5/10 good, needs testing. Buddies functions: implemented only sending messages.
2. Irc server(port 6667) - works 10/10 in miniircd implementation.
3. Natneg server (port 27901) - works 8.5/10 (Sometimes people can't join supposedly because of bad works of this server, there is a branch of natnegging that was implemented in official gs, that isn't here). Not tested much with people who are inside inner networks that are inside other inner networks. Nested networks or some such clownery. Found no good testing material.
4. Serverbrowser (port 28910) - works 10/10. Didn't crash once for about a year somewhere between 2015 and 2016.
5. Queryserver (port 27900) - works 10/10. Didn't crash once for about a year somewhere between 2015 and 2016.
6. Webservver (port 80) - use any, or use none, but make sure skype doesnt use your port 80 (or people will wait 2 minutes to enter lobby).

<strong>2. Subprojects that are included in this repository.</strong><br>
1) PRMasterserver - 4 servers in one application. Has option to run only wanted separate servers, so you can use other applications for other servers. Written in c#<br>
2) GPC4 - GP and GPS servers in python.
3) SBQRC4  - ServerBrowser and Query&Reporting servers in one project. Has 2 more functions than PRMasterserver's version of these servers. Written in python.<br>
4) Miniircd - basic irc server with gs encription support (latest version https://github.com/Zulan/miniircd). Written in python.<br>
5) GSAIRCDTMM - irc server with gs encoding, written on delphi. It works with some bugs, i used it in the beginning. Miniircd is a better irc server.<br>


<strong>3. Wanted logs of gs<->civ4 traffic</strong><br>
Captures taken in wireshark or other programs. Send them to my mail bobodobo11@gmail.com. Quick.


<strong>
4. Current progress</strong>
It is roughly 96% done now.(4% that arent done include: testing, buddy functions, which i dont want to implement because they add alot of traffic and take processing resources that goes to getting info from the database about users each time someone logs in)<br>


<strong>6. Current problems and directions of investigation:<br></strong>
2. NatNeg is implemented only in basic form atm. It needs to be reasearched how exactly to improve it for civ4 though.<br>


<strong>7. How gamespy server works for nabs with small brains</strong>
<br>
to be written later 


<strong>8. Running the server</strong><br>

1. Be sure to have [Visual Studio 2013](http://www.microsoft.com/en-us/download/details.aspx?id=40787) installed.  You might be able to compile it using previous versions of Visual Studio or using Mono, but this is untested and may not work.

2. Open **PRMasterServer.sln**, and build. This should download via NuGet any extra packages required.

3. Run **PRMasterServer.exe +db logindb.db3 +game civ4bts +servers natneg** (it will include civ4 vanilla and japan version too). That will get 27901(natneg) server running.

4. Get python 2.7.8.

5. Run GPC4.py. That will get 29900(GS Presence) and 29901 (GP Search) servers running

6. Run SBQRC4.py. That will get 28910(ServerBrowser) and 27900 (Q&R) servers running

7. Run miniircd.py. That will get 6667(irc) server running.

8. Check that skype is not listening on port 80.

That's all<br>


<strong>9. To join the lobby from the game you need to redirect traffic that is going to official gs ip address to ur server. Best way known to me at this point is to configure windows/system32/drivers/etc/hosts file. Correctly configured hosts file for Zulan's server is included.</strong><br>


<strong>10. Credits</strong><br>
<br><font size=14><strong>[novice-rb]</strong> for work on natneg
<br><font size=14><strong>[AncientMan2002]</strong> for work on PRMasterServer
<br><font size=14><strong>[polaris-]</strong> and others who created this: https://github.com/polaris-/dwc_network_server_emulator
<br><font size=14><strong>[Luigi Auriemma](http://aluigi.org) </strong> for reverse engineering the GameSpy protocol and encryption.
<br><font size=14><strong>[Zulan]</strong> , for running the testing lobby servers, help with testing and his works: https://github.com/Zulan 
<br><font size=14><strong>[Zulan], [Caledorn]</strong> - users on realmsbeyond.net, for running natneg servers
<br><font size=14><strong>[gamespy] </strong> For GsOpenSDK. [Rest in peace]
<br><font size=14><strong>[SexIsBad2TheBone], [DimosEngel], [galatt]</strong> civ4 players (testing)
<br><font size=14><strong>[sid meier and firaxis] </strong> for great game
