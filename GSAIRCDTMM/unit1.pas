unit Unit1;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs,   StdCtrls, ScktComp, ActnList, ExtCtrls,ShellApi, Buttons,
  ActnMan, ActnColorMaps, Menus, ComCtrls;

type
gs_peerchat_ctx = record
  gs_peerchat_1:byte;
  gs_peerchat_2:byte;
  gs_peerchat_crypt:byte;
end;
  TForm1 = class(TForm)
    Memo1: TMemo;
    Daemon: TServerSocket;
    CS: TClientSocket;
    Com: TEdit;
    Button3: TButton;
    Button4: TButton;
    Panel1: TPanel;
    Edit1: TEdit;
    Panel2: TPanel;
    Button11: TButton;
    Edit2: TEdit;
    Panel3: TPanel;
    Clitoris: TEdit;
    Panel4: TPanel;
    Button1: TButton;
    Label1: TLabel;
    Button2: TButton;
    Button5: TButton;
    Memo2: TMemo;
    RichEdit1: TRichEdit;

    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure Button2Click(Sender: TObject);
    procedure DaemonClientConnect(Sender: TObject;
      Socket: TCustomWinSocket);
    procedure DaemonClientDisconnect(Sender: TObject;
      Socket: TCustomWinSocket);
    procedure DaemonGetThread(Sender: TObject;
      ClientSocket: TServerClientWinSocket;
      var SocketThread: TServerClientThread);
    procedure DaemonClientRead(Sender: TObject; Socket: TCustomWinSocket);
    procedure Button466Click(Sender: TObject);
    procedure Button3Click(Sender: TObject);
    procedure CSRead(Sender: TObject; Socket: TCustomWinSocket);
    procedure Button5Click(Sender: TObject);
    procedure CSConnect(Sender: TObject; Socket: TCustomWinSocket);
    procedure FormKeyDown(Sender: TObject; var Key: Word;
      Shift: TShiftState);
    procedure Button7Click(Sender: TObject);
    procedure Memo1KeyDown(Sender: TObject; var Key: Word;
      Shift: TShiftState);
    procedure FormCreate(Sender: TObject);
    procedure Button1Click(Sender: TObject);
    procedure DaemonAccept(Sender: TObject; Socket: TCustomWinSocket);
    procedure Panel1Click(Sender: TObject);
    procedure Button11Click(Sender: TObject);
    procedure Button12Click(Sender: TObject);
    procedure DaemonClientError(Sender: TObject; Socket: TCustomWinSocket;
      ErrorEvent: TErrorEvent; var ErrorCode: Integer);
    procedure ClitorisKeyDown(Sender: TObject; var Key: Word;
      Shift: TShiftState);
    procedure Button12KeyDown(Sender: TObject; var Key: Word;
      Shift: TShiftState);
    procedure FormShow(Sender: TObject);
    procedure ClitorisKeyPress(Sender: TObject; var Key: Char);
  private
    { Private declarations }
  public
    { Public declarations }
  procedure Write(wat:string);
  procedure Termite();
  procedure IRCDGetMoist();
  procedure IRCDExterminate(index:integer);//add exterminate by other params
  function IRCDFUCKASS(Raddress:string;RPort:integer;socketnumbr:integer):integer;
  procedure IRCDDongers();
  function IRCDThrowShitOnTheFan(shid:string;DESNUM:integer;cm:integer;game:string):pansichar;

  procedure IRCDJohnTheCamel(Channelindex,USERINDEX:integer);
  function IRCDCamelIdentify(cname:string):integer;
  function  IRCDCretanParty(name,title:string):integer;
  procedure IRCDAbandonTheChannel(index:integer);
procedure IRCDParadrop({Channelindex,}userindex{,USERINDEXinsidechannel_userlist}:integer;channelname:string);
  procedure IRCDLubricate(msg:string;raddr:string;rip:integer;CU:integer;crypton:bool);

  procedure IRCDSETMODES(ci:integer;fluids:string);
  procedure IRCDTittieBong();
  procedure IRCDPenetrate(Rhost:string;Rport:integer);

  procedure IRCDGenitalDirect(genital:string);
  function IRCDVagooSniff(lulz:string):string;

  procedure IRCDExplosions(fluids:string;Rhost:string;Rport:integer);
  //procedure IRCDGenerateChannelUsersREPLY();
  //channel leave proc
  function IRCDGMatsurebate(Channelindex,userindex:integer):string;
  function IRCDGeneratePubicHair1(user,nick,ipaddr:string):string;
  function IRCDGeneratePubicHair2(user,nick,ipaddr:string):string;

  procedure IRCDHowMoistExactly();
  function IRCDDecToHex(DecString:string):string;
  end;
  

  TUSER = class
  RHost,User,RealName,nick,userhost:string;
  Crypton:boolean;
  gamename{,gamekey}:string;//for crypting;
  RPort,{UserListIndex,}DESN_C,DESN_S:integer;
  ChannelsJoined:tlist;

  TitleRoom_b_flag,Game_b_flag:string;

  public
  procedure CheckIfOnline();
  end;

  TChannel = class
  name,topic:string;
  userlist:tlist;// of ^TUSER;
  //channelindex:integer;
  modes:string;

  //GETCKEY
  //SOME SHIT HERE
  end;


  const HOST='s';//MOSTMOIST.lul';//'GSAIRCD.THE.MOST.MOIST.com';
  const THEIP='192.168.0.1';
  const cvi4titleroom='#GSP!civ4';
  const cvi4btstitleroom='#GSP!civ4bts';
  const cvi4btsjptitleroom='#GSP!civ4bts';

var
  Form1: TForm1;
  //dong:tlist;
  //array of users
  USERLIST:TLIST;
  CHANNELS:TLIST;
  ctx1:gs_peerchat_ctx;
  dongers:integer=1;
  MrCrypton,clothes:bool;
  dun:bool=false;
  gngk:array [0..2,0..1] of string;
  CommandStack:array[1..10] of string;
  CCount:integer;
  CSPos:integer;
  //
  //ctx:gs_peerchat_ctx;
  //array of channels
  //array of arrays of users in channel


function bongciv4(codedshid:PAnsiChar;DESNUMBR:integer;size1:integer):PAnsiChar; cdecl;external 'project4.dll';//'project4gmtest.dll';//I:\programs\Dev-Cpp\projects\LIB1\project4.dll';
function bongciv4bts(codedshid:PAnsiChar;DESNUMBR:integer;size1:integer):PAnsiChar; cdecl;external 'project4.dll';//'project4gmtest.dll';//I:\programs\Dev-Cpp\projects\LIB1\project4.dll';
//function bong(codedshid:PAnsiChar;DESNUMBR:integer;size1:integer):PAnsiChar; cdecl;external 'project4gmtest.dll';

implementation

{$R *.dfm}

function Tform1.IRCDDecToHex(DecString:string):string;
var
i,z:integer;
ts,ts2:string;
begin
ts2:='';
//254,253,1,130,102,99,183,68,61,115,126,106,89,48,48,55,67,57,53,65,66,66,53,55,52,67,67
for i:=1 to length(DecString) do begin
z:=pos(',',DecString);
if (z=0) then break;
ts:=copy(DecString,1,z-1);
ts:='0x'+inttohex(strtoint(ts),2);
DecString:=copy(DecString,z+1,length(decstring));
ts2:=ts2+ts+',';


end;
//memo1.lines.add(ts2);
result:=ts2;
end;

procedure Tform1.IRCDSETMODES(ci:integer;fluids:string);
var
modes:array [0..8] of bool;
modesS:array [0..8] of string;
mnum:integer;
i,tmp1:integer;
channelspart:string;
modifier:bool;//true +, false -
ts:string;
begin
modesS[0]:='t';
modesS[1]:='p';
modesS[2]:='n';
modesS[3]:='i';
modesS[4]:='s';
modesS[5]:='m';
modesS[6]:='l';
modesS[7]:='e';
modesS[7]:='k';


//strip off MODE #CHAN
tmp1:=pos(' ',fluids);
channelspart:=copy(fluids,tmp1+1,length(fluids));
tmp1:=pos(' ',channelspart);

channelspart:=copy(channelspart,tmp1+1,length(channelspart));
channelspart:=copy(channelspart,1,length(channelspart)-2);
//parsing
//check each symbol 1 by one
//there might be +/-
//and letter of mode
//then if SPACE then next text is number

//TEMPMODES RESET
for i:=0 to 8 do
modes[i]:=false;
mnum:=-1;
//TM SET TO CURRENT
for i:=1 to length(channelspart) do begin
ts:=copy(Tchannel(channels.Items[ci]).modes,i,1);
if ts='t' then modes[0]:=true;
if ts='p' then modes[1]:=true;
if ts='n' then modes[2]:=true;
if ts='i' then modes[3]:=true;
if ts='s' then modes[4]:=true;
if ts='m' then modes[5]:=true;
if ts='l' then modes[6]:=true;
if ts='e' then modes[7]:=true;
if ts='k' then modes[8]:=true;
if ts=' ' then begin
mnum:=strtoint(copy(Tchannel(channels.Items[ci]).modes,i+1,2));
break;
end;
end;

//TM SET TO NEW
modifier:=true;
for i:=1 to length(channelspart) do begin
ts:=copy(channelspart,i,1);
if ts='+' then modifier:=true else
if ts='-' then modifier:=false else
if ts='t' then modes[0]:=modifier else
if ts='p' then modes[1]:=modifier else
if ts='n' then modes[2]:=modifier else
if ts='i' then modes[3]:=modifier else
if ts='s' then modes[4]:=modifier else
if ts='m' then modes[5]:=modifier else
if ts='l' then modes[6]:=modifier else
if ts='e' then modes[7]:=modifier else
if ts='k' then modes[8]:=modifier else
   if ts=' ' then begin
   mnum:=strtoint(copy(channelspart,i+1,2));
   break;
   end;

end;

//MODES SET TO NEW
Tchannel(channels.Items[ci]).modes:='+';
for i:=0 to 8 do begin
if modes[i]=true then
Tchannel(channels.Items[ci]).modes:=Tchannel(channels.Items[ci]).modes+modesS[i];
end;
if mnum>0 then
Tchannel(channels.Items[ci]).modes:=Tchannel(channels.Items[ci]).modes+' '+inttostr(mnum);

end;

function Tform1.IRCDCamelIdentify(cname:string):integer;
var
ci,i:integer;
begin
ci:=-1;
  for i:=0 to channels.Count-1 do begin
    if TChannel(channels.Items[i]).name=cname then begin
    ci:=i;
    break;
    end;
  end;
result:=ci;
//
end;


function Tform1.IRCDVagooSniff(lulz:string):string;
var
i:integer;
begin
for i:=0 to 2 do begin
    if gngk[i,0]=lulz then
    result:=gngk[i,1];
end;
//
end;

procedure Tform1.IRCDHowMoistExactly();
var
i:integer;
begin
//USERLIST := TList.Create;
Write('Exact moistness report.');
Write('USERS:'+inttostr(USERLIST.count));
if  userlist.Count<>0 then
  for i:=0 to userlist.Count-1 do begin
  Write(inttostr(i)+'. '+TUSER(USERLIST.Items[i]).Nick+'; user:'+TUSER(USERLIST.Items[i]).User+'; rn:'+TUSER(USERLIST.Items[i]).RealName);
  Write('TRBF:'+TUSER(USERLIST.Items[i]).TitleRoom_b_flag+';GRBF:'+TUSER(USERLIST.Items[i]).Game_b_flag);
//  Write('  '+TUSER(USERLIST.Items[i]).RealName);
//  Write('  '+TUSER(USERLIST.Items[i]).Nick);
//  Write('  '+inttostr(TUSER(USERLIST.Items[i]).DESN_C));
  end;
  //Write(inttostr(USERLIST.count)+#13#10);

Write('Channels:'+inttostr(channels.count));
if  channels.Count<>0 then
//showmessage(inttostr(channels.Count));
  for i:=0 to channels.Count-1 do begin
  Write(inttostr(i+1)+'.'+TChannel(channels.Items[i]).name+' '+TChannel(channels.Items[i]).modes+' topic:'+TChannel(channels.Items[i]).topic+' #Users:'+inttostr(TChannel(channels.Items[i]).userlist.count)) ;
  end;

end;

procedure Tform1.IRCDGenitalDirect(genital:string);
var
dosh,dosh2,dosh3:string;
doshint:integer;
i:integer;
begin
//
write('>'+genital);
if CommandStack[1]<>genital then begin
if CCount<10 then CCount:=CCount+1;

if ccount>1 then
for i:=1 to CCount do begin
if i<>CCount then
CommandStack[CCount+1-i]:=CommandStack[CCount-i];
end;

CommandStack[1]:=genital;

end;

//for i:=1 to ccount do memo1.Lines.Add(CommandStack[i]);
if uppercase(copy(genital,1,5))='/HELP' then begin
memo1.Lines.Add('~'+'/help - to get help;');
memo1.Lines.Add('~'+'/howgswrks - explanation for nabs;');
memo1.Lines.Add('~'+'/reset - exterminate all users(and channels);');
//memo1.Lines.Add('~'+'/ping - ping specified user(with index of userlist-1), exmple: "/ping 0";');
memo1.Lines.Add('~'+'/grep - general userlist and channels report;');
memo1.Lines.Add('~'+'/erep - extended report;');
//memo1.Lines.Add('~'+'/crep - channel report');
memo1.Lines.Add('~'+'/clear - clear shit;');
memo1.Lines.Add('~'+'/byte - turn on/off byte log on encoding');
memo1.Lines.Add('~'+'/serv - check daemon status, /serv on - to turn on, off to turn off');
memo1.Lines.Add('~'+'/exit - to exit;');
end else
if uppercase(copy(genital,1,7))='/HEXSEX' then begin
dosh:=copy(genital,9,length(genital));
if dosh='' then dosh:='254,253,1,130,102,99,183,68,61,115,126,106,89,48,48,55,67,57,53,65,66,66,53,55,52,67,67';
write('~'+IRCDDecToHex(dosh));
end else
if uppercase(copy(genital,1,10))='/HOWGSWRKS' then begin
for i:=0 to memo2.Lines.Count-1 do begin
write('~'+memo2.Lines[i]);
end;

end else
if uppercase(copy(genital,1,6))='/RESET' then begin

if userlist.Count>0 then begin
for i:=0 to userlist.Count-1 do begin
form1.IRCDExterminate(i);
end;
if  daemon.Socket.ActiveConnections>0 then
for i:=0 to daemon.Socket.ActiveConnections-1 do begin
daemon.Socket.Disconnect(i);
end;
daemon.Active:=false;
daemon.Active:=true;
end else write('There is nothing already');

end else
if uppercase(copy(genital,1,5))='/BATS' then begin
dosh:=copy(genital,7,length(genital));
dosh2:='';
dosh3:='eb9279982226a42afdf2860dbdc29b45';
dosh3:='f7c0e071db137f5ae65382041c7cef4b';
for i:=0 to round(length(dosh3)/2) do begin
//eb9279982226a42afdf2860dbdc29b45
if i=0 then dosh:=char(235);
if i=1 then dosh:=char(146);
if i=2 then dosh:=char(121);
if i=3 then dosh:=char(152);
if i=4 then dosh:=char(34);
if i=5 then dosh:=char(38);
if i=6 then dosh:=char(164);
if i=7 then dosh:=char(42);
if i=8 then dosh:=char(253);
if i=9 then dosh:=char(242);
if i=10 then dosh:=char(134);
if i=11 then dosh:=char(13);
if i=12 then dosh:=char(189);
if i=13 then dosh:=char(194);
if i=14 then dosh:=char($9b);
if i=15 then dosh:=char($45);

dosh2:=dosh2+'0x'+copy(dosh3,i*2,2)+',';//IRCDThrowShitOnTheFan(dosh,0,1,'civ4bts');
end;
write('~result:'+dosh2);

write('~dong:'+dosh2);

end else
if uppercase(copy(genital,1,5))='/BYTE' then begin
if uppercase(copy(genital,7,2))='ON' then clothes:=false else
if uppercase(copy(genital,7,3))='OFF' then clothes:=true;
if clothes=false then dosh:='ON';
if clothes=true then dosh:='OFF';
memo1.Lines.Add('~'+'byte log is '+dosh);
end else
if uppercase(copy(genital,1,6))='/CLEAR' then begin
memo1.Lines.Clear;

end else
if uppercase(copy(genital,1,5))='/PING' then begin
doshint:=strtoint((copy(genital,7,length(genital))));
if doshint<daemon.Socket.ActiveConnections-1 then begin
write('~'+'ping command');
IRCDLubricate('PING :12SomeJizz3321'+#13#10,TUser(Userlist.Items[doshint]).Rhost,TUser(Userlist.Items[doshint]).Rport,doshint,TUser(Userlist.Items[doshint]).crypton);
end
else
write('~'+'ping command failed - wrong client number');
end else
if uppercase(copy(genital,1,5))='/EREP' then begin
IRCDHowMoistExactly();
end else
if uppercase(copy(genital,1,5))='/GREP' then begin
ircdtittiebong();
end else
if uppercase(copy(genital,1,5))='/SERV' then begin
if uppercase(copy(genital,7,2))='ON' then daemon.Active:=true else
if uppercase(copy(genital,7,3))='OFF' then daemon.Active:=false;
//daemon.Active:=not daemon.Active;
if daemon.Active=false then dosh:='OFF';
if daemon.Active=true then dosh:='ON';
memo1.Lines.Add('~'+'daemon is now '+dosh);
end else
if uppercase(copy(genital,1,5))='/EXIT' then begin
termite();
end;
end;

function TForm1.IRCDThrowShitOnTheFan(shid:string;DESNUM:integer;cm:integer;game:string):pansichar;

begin
//memo1.Lines.Add('THROWSHID');
if game='civ4' then
result:=bongciv4(PAnsichar(shid),DESNUM,cm) else
if game='civ4bts' then
result:=bongciv4bts(PAnsichar(shid),DESNUM,cm)
else if game='civ4btsjp' then
result:=bongciv4bts(PAnsichar(shid),DESNUM,cm)
else memo1.Lines.Add('game is wat?');
//
end;


function CountOccurences( const SubText: string; const Text: string): Integer;
begin
  if (SubText = '') OR (Text = '') OR (Pos(SubText, Text) = 0) then
    Result := 0
  else
    Result := (Length(Text) - Length(StringReplace(Text, SubText, '', [rfReplaceAll]))) div  Length(subtext);
end;










function TForm1.IRCDGMatsurebate(Channelindex,userindex:integer):string;
var
i:integer;
rstr,cname11:string;
ztmp:bool;
begin
//:my.server.name 353 DONGERH = #fage :@DONGERH
//:my.server.name 366 DONGERH #fage :End of /NAMES list.
//
if (TUSER(USERLIST.Items[userindex]).gamename='civ4btsjp') and (TChannel(Channels.Items[Channelindex]).name='#GSP!civ4bts') then
cname11:='#GSP!civ4btsjp' else
cname11:=TChannel(Channels.Items[Channelindex]).name;

rstr:=//':s 332 '+TUSER(USERLIST.Items[userindex]).nick+' '+TChannel(Channels.Items[Channelindex]).name+' :Click on the "Game Info" button at the top of your screen for the latest information on patches, add-on files, interviews, strategy guides and more!  It`s all there!'+#13#10+
':s 333 '+TUSER(USERLIST.Items[userindex]).nick+' '+cname11+' SERVER 1225379572'+#13#10+
':s 353 '+TUSER(USERLIST.Items[userindex]).nick+' * '+cname11+' :';


//':'+HOST+' 353 '+TUSER(USERLIST.Items[userindex]).nick+' = '+TChannel(Channels.Items[Channelindex]).name+' :';
for i:=0 to TChannel(Channels.Items[Channelindex]).userlist.Count-1 do begin
 if TUSER(TChannel(Channels.Items[Channelindex]).userlist.Items[i])<>TUSER(USERLIST.Items[userindex]) then
 rstr:=rstr+TUSER(TChannel(Channels.Items[Channelindex]).userlist.Items[i]).nick+' ';
end;
if Channelindex<2 then rstr:=rstr+' ';
rstr:=rstr+'@'+TUSER(USERLIST.Items[userindex]).nick+#13#10;
rstr:=rstr+':'+HOST+' 366 '+TUSER(USERLIST.Items[userindex]).nick+ ' '+ cname11+ ' :End of /NAMES list.'+#13#10;

//:s 332 muzer-think #GSP!worms4 :Click on the "Game Info" button at the top of your screen for the latest information on patches, add-on files, interviews, strategy guides and more!  It`s all there!
//:s 333 muzer-think #GSP!worms4 SERVER 1360960046
//:s 353 muzer-think * #GSP!worms4 :muzer-think
//:s 366 muzer-think #GSP!worms4 :End of NAMES list

result:=rstr;
end;

function TForm1.IRCDGeneratePubicHair2(user,nick,ipaddr:string):string;
begin
result:=':s 375 '+nick+' :- (M) Message of the day -'    +#13#10+
':s 372 '+nick+' :- Welcome to GameSpy(for real)'    +#13#10+
':s 376 '+nick+' :End of MOTD command'           +#13#10;//+
end;
function TForm1.IRCDGeneratePubicHair1(user,nick,ipaddr:string):string;
var
tmph:string;
begin
//                                      REAL GAMESPY SHIT:
{:s 001 muzer-think :Welcome to the Matrix muzer-think
:s 002 muzer-think :Your host is xs2, running version 1.0
:s 003 muzer-think :This server was created Fri Oct 19 1979 at 21:50:00 PDT
:s 004 muzer-think s 1.0 iq biklmnopqustvhe
:s 375 muzer-think :- (M) Message of the day -
:s 372 muzer-think :- Welcome to GameSpy
:s 376 muzer-think :End of MOTD command}
                    
tmph:=':'+host;
{result:=':s 001 '+nick+':Welcome to the Matrix '+nick+#13#10+
':s 002 '+nick+' :Your host is '+host+', running version 1.0'+#13#10+
':s 003 '+nick+' :This server was created Fri Oct 19 1979 at 21:50:00 PDT'  +#13#10+
':s 004 '+nick+' s 1.0 iq biklmnopqustvhe'       +#13#10;
}
result:=//tmph+' NOTICE Auth :Dis is gona be good!'+#13#10;// //
tmph+' 001 '+nick+' :Welgome to ze  MADRIX '+nick+'!'+user+'@'+ipaddr+'+'+#13#10;
//tmph+' 001 '+nick+' :Your host is '+HOST+', running version 666'+#13#10;//+
//tmph+' 002 '+nick+' :This server was created 16:51:48 Jul 28 2014'+#13#10+
//tmph+' 004 '+nick+' '+HOST+' 2.0 iosw biklmnopstv bklov'+#13#10+
//+tmph+' 003 '+nick+' AWAYLEN=200 CASEMAPPING=rfc1459 CHANMODES=+tnp,tnp,b,k,l,imnpst CHARSET=ascii  :are supported by this server'+#13#10+
//tmph+' 375 '+nick+' :'+HOST+'message of the day'+#13#10+                                                      //CHANTYPES=# ELIST=MU FNC KICKLEN=255 MAP MAXBANS=60 MAXCHANNELS=20 MAXPARA=32
//tmph+' 372 '+nick+' :- GAYSPY2: MATRIX REBOOTED: INCREASED LAGS, CRASHES AND OTHER SHID'+#13#10+
//tmph+' 376 '+nick+' :End of message of the day.'+#13#10;
//}
//'PING :'+inttostr(random(9))+inttostr(random(9))+'S0meJiz'+inttostr(random(9))+'zz'+#13#10;//+

end;



procedure TForm1.IRCDLubricate(msg:string;raddr:string;rip:integer;CU:integer;crypton:bool);
var
AppropriateOpening:integer;
i,jizzdescription,nipplesquantity:integer;
MrCryptonsJizz:array of byte;
donger332:pansichar;
shid1:string;
friction:byte;
otherjuice:string;
begin
//determine right connection number
if Daemon.Socket.ActiveConnections<1 then showmessage('activeconnectionsNONE');
for i:=0 to Daemon.Socket.ActiveConnections-1 do begin
 if (Daemon.Socket.Connections[i].RemoteAddress=raddr) and (Daemon.Socket.Connections[i].RemotePort=rip) then begin
 AppropriateOpening:=i;
 break;
 end;

end;

//write({TimeToStr(Now)+}'Lubricated('+inttostr(length(msg))+'):'+trim(msg));
if crypton=true then begin

SetLength(MrCryptonsJizz, 0);
//write('---MrCrypton is raping---');
jizzdescription:=TUSER(USERLIST.Items[CU]).DESN_S;

com.Text:='';
otherjuice:='';
for nipplesquantity:=1 to length(msg) do begin
shid1:=msg[nipplesquantity];

SetLength(MrCryptonsJizz, length(MrCryptonsJizz)+1);
donger332:=IRCDThrowShitOnTheFan(shid1,TUSER(userlist.Items[CU]).DESN_S,1,TUSER(userlist.Items[CU]).gamename);


MrCryptonsJizz[nipplesquantity-1]:=ord(donger332[0]);
otherjuice:=otherjuice+donger332[0];
if clothes=false then
com.Text:=com.Text+'¹'+inttostr(nipplesquantity)+'#'+inttostr(MrCryptonsJizz[nipplesquantity-1])+',';
//MrCryptonsJizz:=MrCryptonsJizz+donger332;

TUSER(userlist.Items[CU]).DESN_S:=TUSER(userlist.Items[CU]).DESN_S+1;

end;

//memo1.Lines.Add(com.Text);
com.Text:='';

//write('Prev Desn_S='+inttostr(jizzdescription)+';new Desn_S='+inttostr(TUSER(USERLIST.Items[CU]).DESN_S));
//memo1.Lines.Add('PRECRYPTLEN:'+inttostr(length(msg))+'BUFFLEN:'+inttostr(length(MrCryptonsJizz)));

//write('Really lubricated:'+otherjuice);

//daemon.Socket.Connections[AppropriateOpening].SendText(MrCryptonsJizz);

daemon.Socket.Connections[AppropriateOpening].SendBuf(MrCryptonsJizz[0],length(MrCryptonsJizz));
end else
//just send
daemon.Socket.Connections[AppropriateOpening].SendText(msg);
//send message
end;

procedure TForm1.IRCDExplosions(fluids:string;Rhost:string;Rport:integer);
//Parse and execute
var
i,i2,cu,argsnum,ci,temp,tmpsoc,cryptontmp:integer;
tmpstr,ts2,ts3,tmpstr3,ts4,ts5,ts6,ts7:string;
args:array [0..12] of string;
nick:string;
tmpbool:bool;
//RESPONSE:string;
//MRCRYPTON:bool;
begin
//USER
//set username
//and realname
//and shid
//RESPONSE:='fagt';
//MRCRYPTON:=false;
cu:=-1;
for i:=0 to userlist.Count-1 do begin
   if (TUSER(userlist.Items[i]).Rhost=Rhost) and(TUSER(userlist.Items[i]).Rport=Rport) then
     begin
       cu:=i;
     end;
end;

write(Rhost+'('+inttostr(Rport)+'):'+fluids);




{if TUSER(userlist.Items[cu]).Crypton=true then begin
   //
   //s
   cryptontmp:=length(fluids);
   fluids:=IRCDThrowShitOnTheFan(fluids, TUSER(userlist.Items[cu]).DESN_C);
   write(' ');
write(TimeToStr(Now)+'_CRPTD'+'_____('+fluids+')');
write('Prev Desn_C='+inttostr(TUSER(USERLIST.Items[CU]).DESN_C)+';new Desn_C='+inttostr(TUSER(USERLIST.Items[CU]).DESN_C+cryptontmp));
   TUSER(userlist.Items[cu]).DESN_C:=TUSER(userlist.Items[cu]).DESN_C+cryptontmp;
//   MRCRYPTON:=true;
end; }

for i:=0 to 12 do
args[i]:='';

tmpstr:=fluids;
tmpstr := StringReplace(tmpstr, sLineBreak, ' ', [rfReplaceAll]);

argsnum:=CountOccurences(' ',tmpstr)+1;
//showmessage(inttostr(argsnum));
//write('CHECKPOINT X-1:'+fluids+'::::'+args[0]+'::::'+inttostr(argsnum));

//showmessage(tmpstr);
if (argsnum>0) then begin

  for i:=0 to argsnum-1 do begin
      if (i=2) and (UpperCase(args[0])='PRIVMSG') then begin
      args[2]:=tmpstr;
      //write('CHECKPOINT X:'+fluids+'::::'+args[2]);
      break;
      end;
  args[i]:=copy(tmpstr,1,pos(' ',tmpstr)-1);

  //showmessage(':'+args[i]+':');
  tmpstr:=Copy(tmpstr,pos(' ',tmpstr)+1,length(tmpstr));

  end;
end;
//write('CHECKPOINT X+1:'+fluids+'::::'+args[0]+'\\\'+inttostr(pos(' ',fluids)));


args[0]:=UpperCase(args[0]);

if args[0]='CRYPT' then begin
//CRYPT des 1 civ4#0d#0a
//response: ':s 705 * 0'+'00000000'+'0000000 '+'00000000'+'00000000'+#0d#0a
ts2:=':s 705 * 0'+'00000000'+'0000000 '+'00000000'+'00000000'+#13#10;

//write('incrypt preparations:'+ts2);
//1good line
TUSER(USERLIST.Items[cu]).gamename:=args[3];
IRCDLubricate(ts2,Rhost,Rport,cu,false);
//RESPONSE:=ts2;
TUSER(USERLIST.Items[cu]).Crypton:=true;

///////TUSER(USERLIST.Items[cu]).gamekey:=IRCDVagooSniff(args[4]);
//not yet needed
MrCrypton:=true;
TUSER(USERLIST.Items[cu]).DESN_C:=0;
TUSER(USERLIST.Items[cu]).DESN_S:=0;
//write('CRYPT DONE');

end else
if args[0]='USRIP' then begin
//:s 302  :=+@0.0.0.0
ts2:=':s 302  :=+@'+TUSER(USERLIST.Items[cu]).RHost; //'0.0.0.0';
ts2:=ts2+#13#10;
//write('USRIP preparations:'+ts2);
//Write('ts2 sent____'+ts2);
//3good lines
/////////////ts2:=IRCDThrowShitOnTheFan(ts2,TUSER(USERLIST.Items[cu]).DESN_S);
//write('USRUP');
IRCDLubricate(ts2,Rhost,Rport,cu,true);
/////////////TUSER(USERLIST.Items[cu]).DESN_S:=TUSER(USERLIST.Items[cu]).DESN_S+length(ts2);
//RESPONSE:=ts2;
//write('USRUP LUBRICATED?');
//Write('crypted ts2____'+ts2);

end else
if (args[0]='LOGIN') then begin
TUSER(userlist.items[cu]).nick:=args[2];
//write('fluids:'+fluids);
//write('LOGINARG0:'+args[0]+'LOGINARG1:'+args[1]+'LOGINARG2:'+args[2]+'LOGINARG3:'+args[3]);
//TUSER(userlist.items[cu]).User:='VIPIPADDRESS|'+inttostr(random(10000));
//TUSER(userlist.items[cu]).RealName:='JustADongus';
ts2:=':s 707 '+args[2]+' 12345678 87654321'+#13#10;//'CALL AuthClient("'+args[2]{+'-tk2'}+'","'+args[3]+{'","'++}'","qqq@aas.com",10,0)'+#13#10;

IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);

//LOGIN 17 rrrr-tk eb9279982226a42afdf2860dbdc29b45
end else
if (args[0]='USER') {or (args[0]='LOGIN')} then begin

   //showmessage(tmpstr);
TUSER(userlist.items[cu]).User:=args[1];
TUSER(userlist.items[cu]).RealName:=copy(args[4],2,length(args[4]));
if (args[6]<>'*') and (args[6]<>'') then
TUSER(userlist.items[cu]).nick:=args[6] ;//else

//write('Nick *');
//Write('USER REQ RECIEVED.');

richedit1.lines.add(TUSER(userlist.items[cu]).RHost+':'+inttostr(TUSER(userlist.items[cu]).rport)+'('+TUSER(userlist.items[cu]).nick+') enters.');


//IRCDLubricate(IRCDGeneratePubicHair(TUSER(userlist.items[cu]).User,TUSER(userlist.items[cu]).nick,TUSER(userlist.items[cu]).RHost),Rhost,Rport);

//ts2:=IRCDGeneratePubicHair2(TUSER(userlist.items[cu]).User,TUSER(userlist.items[cu]).nick,Rhost);
//IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);
{nick:=TUSER(userlist.items[cu]).nick;
ts2:=':s 001 '+nick+':Welcome to the Matrix '+nick+#13#10;
IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);
ts2:=':s 002 '+nick+' :Your host is '+host+', running version 1.0'+#13#10;
IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);
ts2:=':s 003 '+nick+' :This server was created Fri Oct 19 1979 at 21:50:00 PDT'  +#13#10;
IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);
ts2:=':s 004 '+nick+' s 1.0 iq biklmnopqustvhe'       +#13#10;
IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);

ts2:=':s 375 '+nick+' :- (M) Message of the day -'    +#13#10;
IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);
ts2:=':s 372 '+nick+' :- Welcome to GameSpy(for real)'    +#13#10;
IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);
ts2:=':s 376 '+nick+' :End of MOTD command'           +#13#10;//+
IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton); }


     //?

//     IRCDLubricate('PING :SomeJizz332199',Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);


end else

//NICK
if args[0]='NICK' then begin
if args[1]<>'*' then
TUSER(userlist.items[cu]).nick:=args[1] else
//write('Nick *');
write(TUSER(userlist.items[cu]).nick);
ts2:=IRCDGeneratePubicHair1(TUSER(userlist.items[cu]).User,TUSER(userlist.items[cu]).nick,Rhost);
IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);

//write('NICK preparations (giving no response).'{+fluids});

end else

//USERHOST
if args[0]='USERHOST' then begin
TUSER(userlist.items[cu]).userhost:=copy(args[1],2,length(args[1]));
//answer with
//:irc.somedomain.com 302 PokPok :PokPok=+pokpoker@127.0.0.1
tmpstr:=':'+HOST+' 302 '+TUSER(userlist.items[cu]).nick+' :'+TUSER(userlist.items[cu]).userhost+'=+~'+TUSER(userlist.items[cu]).User+'@'+Rhost+#13#10;
//1 good line
//IRCDLubricate(tmpstr,Rhost,Rport);
IRCDLubricate(tmpstr,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);
//write('USERHOST preparations:'+tmpstr);
//RESPONSE:=tmpstr;

//write('Dsent:'+tmpstr);

end else

//JOIN
if args[0]='JOIN' then begin
//recieved: JOIN #ddd
//check if channel is up
ts5:=args[1];
if args[1]='#GSP!civ4btsjp' then args[1]:='#GSP!civ4bts';
tmpstr:=args[1];//copy(args[1],1,length(args[1]));

ci:=IRCDCamelIdentify(args[1]);

//if channel exists send notifications to everybody
if (ci>-1) and (TChannel(channels.Items[ci]).userlist.Count>0) then begin
     ts4:=':'+TUSER(userlist.items[cu]).nick+'!~'+TUSER(userlist.items[cu]).user+'@'+HOST+' JOIN :';//+TChannel(channels.Items[ci]).name+#13#10;

     for i:=0 to TChannel(channels.Items[ci]).userlist.Count-1 do begin
     //if TUSER(TChannel(channels.Items[ci]).userlist.Items[i])<>TUSER(userlist.Items[cu]) then
     if (TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).gamename='civ4btsjp')  and (args[1]='#GSP!civ4bts') then
     ts6:=ts4+'#GSP!civ4btsjp'+#13#10 else
     ts6:=ts4+args[1]+#13#10;
     IRCDLubricate(ts6,TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).RHost,TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).RPort,  USERLIST.IndexOf(TUSER(TChannel(channels.Items[ci]).userlist.Items[i])),TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).Crypton);//Rhost,Rport);
     end;
   end;// else write('channel either unpopulated or nonexistent');// else IRCDLubricate('NOCHANNEL',TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).RHost,TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).RPort);




//create new or not
if ci=-1 then begin //new one needed
ci:=IRCDCretanParty(tmpstr,'UsualGSOrgy');
write('Channel created: '+tmpstr);
end;
//then add user there
//add channel to the userlist
///



IRCDJohnTheCamel(ci,cu);
//then get list of users in channel and send reply
//ts2:=':'+TUSER(userlist.items[cu]).nick+'!~'+'pokpoker1@my.server.name'+' JOIN :'+TChannel(channels.items[ci]).name+#13#10;
if (TUSER(userlist.items[cu]).gamename='civ4btsjp') and (args[1]='#GSP!civ4bts') then
ts6:='#GSP!civ4btsjp' else
ts6:=args[1];

ts2:=':'+TUSER(userlist.items[cu]).nick+'!'+TUSER(userlist.items[cu]).user+'@*'+' JOIN :'+ts6+#13#10;





//IRCDLubricate(ts2,Rhost,Rport);
//ts2:=':'+HOST+' 353 '+TUSER(USERLIST.Items[cu]).nick+' = '+TChannel(Channels.Items[ci]).name+' :'+TUSER(USERLIST.Items[cu]).nick+' @'+TUSER(USERLIST.Items[cu]).nick+#13#10;
//IRCDLubricate(ts2,Rhost,Rport);
//Write('[]'+ts2);
//ts2:=':'+HOST+' 366 '+TUSER(USERLIST.Items[cu]).nick+ ' '+ TChannel(Channels.Items[ci]).name+ ' :End of /NAMES list.'+#13#10;

ts2:=ts2+IRCDGMatsurebate(ci,cu);

IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);
//Write('[]'+ts2);


end else
if args[0]='PART' then begin
ts5:=args[1];
if args[1]='#GSP!civ4btsjp' then args[1]:='#GSP!civ4bts';
tmpstr:=args[1];//copy(args[1],1,length(args[1]));

ci:=IRCDCamelIdentify(args[1]);

//remove from channellist
if ci>-1 then begin
TChannel(channels.items[ci]).userlist.Remove(userlist.items[cu]);
//remove channel from user

TUSER(userlist.items[cu]).ChannelsJoined.Remove(channels.items[ci]);
Write(TUSER(userlist.items[cu]).nick+' parted'+TChannel(channels.items[ci]).name);
//send message to the parting user
//////or to all?
//:PokPok22!~pokpoker2@my.server.name PART #fage

if (ci>-1) and (TChannel(channels.Items[ci]).userlist.Count>0) then begin
     ts4:=':'+TUSER(userlist.items[cu]).nick+'!~'+TUSER(userlist.items[cu]).user+'@'+HOST+' PART :';//+TChannel(channels.Items[ci]).name+#13#10;
     for i:=0 to TChannel(channels.Items[ci]).userlist.Count-1 do begin
     //if TUSER(TChannel(channels.Items[ci]).userlist.Items[i])<>TUSER(userlist.Items[cu]) then
     if (TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).gamename='civ4btsjp') and (args[1]='#GSP!civ4bts') then
     ts6:=ts4+'#GSP!civ4btsjp'+#13#10 else
     ts6:=ts4+args[1]+#13#10;

     IRCDLubricate(ts6,TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).RHost,TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).RPort,USERLIST.IndexOf(TUSER(TChannel(channels.Items[ci]).userlist.Items[i])),TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).Crypton);//Rhost,Rport);

     end;
   end else write('user parted empy channel');// else IRCDLubricate('NOCHANNEL',TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).RHost,TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).RPort);


//ts2:=':'+TUSER(userlist.items[cu]).nick+'!~'+TUSER(userlist.items[cu]).user+'@'+HOST+' PART '+ TChannel(channels.items[ci]).name+#13+#10;
//IRCDLubricate(ts2,Rhost,Rport);
//when last one parting - kill channel
if TChannel(channels.Items[ci]).userlist.Count=0 then
IRCDAbandonTheChannel(ci);
end else write('not appropriate channel - '+tmpstr);
//say to all that smn parted
end else

//list of channels
if args[0]='LIST' then begin
//showmessage('list');
ts2:=':'+HOST+' 321 '+TUSER(userlist.items[cu]).nick+' Channel :Users  Name'+#13#10;
for i2:=0 to Channels.Count-1 do  begin
    ts2:=ts2+':'+HOST+' 322 '+TUSER(userlist.items[cu]).nick+' '+TChannel(Channels.Items[i2]).name+' '+inttostr(TChannel(Channels.Items[i2]).userlist.count)+' :'+#13#10;
end;
ts2:=ts2+':'+HOST+' 323 '+TUSER(userlist.items[cu]).nick+' :End of /LIST'+#13#10;
IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).crypton);
//Write(ts2);
end else

//PRIVMSG #CHANNELS :MESSAGE
if args[0]='PRIVMSG' then begin
i2:=random(10);
case i2 of
0 : richedit1.SelAttributes.Color:=clred;
1 : richedit1.SelAttributes.Color:=clgreen;
2 : richedit1.SelAttributes.Color:=clblue;
3 : richedit1.SelAttributes.Color:=clgreen;
4 : richedit1.SelAttributes.Color:=clfuchsia;
5 : richedit1.SelAttributes.Color:=clgray;
6 : richedit1.SelAttributes.Color:=clblack;
7 : richedit1.SelAttributes.Color:=clpurple;
8 : richedit1.SelAttributes.Color:=clteal;
9 : richedit1.SelAttributes.Color:=clnavy;
10 : richedit1.SelAttributes.Color:=clolive;
end;
richedit1.Lines.Add(TUSER(userlist.items[cu]).nick+'['+args[1]+']'+args[2]);//copy(fluids,1,length(fluids)-2));
ts5:=args[1];
if args[1]='#GSP!civ4btsjp' then args[1]:='#GSP!civ4bts';
tmpstr:=args[1];//copy(args[1],2,length(args[1]));  //CHAN NAME
//ts2:=//copy(args[2],2,length(args[2])); //MESSAGE
//write('PRIVMSG at the point of args parsing:'+fluids);
//write('PRIVMSG CHECKPOINT Y:'+args[2]);
{ci:=-1;
  for i2:=0 to channels.Count-1 do begin
    if TChannel(channels.Items[i2]).name=tmpstr then begin
    ci:=i2;
    break;
    end;
  end; }
ci:=IRCDCamelIdentify(args[1]);


tmpstr3:=':'+TUSER(userlist.items[cu]).nick+'!~'+TUSER(userlist.items[cu]).user+'@'+HOST+' PRIVMSG ';//+args[1]{TChannel(channels.Items[ci]).name}+' '+args[2]+#13#10;

 //send to all on the channel but the sender
   if (ci>-1) and (TChannel(channels.Items[ci]).userlist.Count>0) then begin

     for i:=0 to TChannel(channels.Items[ci]).userlist.Count-1 do begin
     if TUSER(TChannel(channels.Items[ci]).userlist.Items[i])<>TUSER(userlist.Items[cu]) then
          begin
          if TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).gamename='civ4btsjp' then
          ts7:='#GSP!civ4btsjp' else ts7:='#GSP!civ4bts';
          ts6:=tmpstr3+ts7+' '+args[2]+#13#10;
          IRCDLubricate(ts6,TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).RHost,TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).RPort,USERLIST.IndexOf(TUSER(TChannel(channels.Items[ci]).userlist.Items[i])),TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).Crypton);//Rhost,Rport);

          end;

     end;
   end else write('channel either unpopulated or nonexistent');// else IRCDLubricate('NOCHANNEL',TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).RHost,TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).RPort);



end else
//PING
if args[0]='PING' then begin
//TUSER(userlist.items[cu]).nick:=args[1];
ts2:='PONG'+args[2]+#13#10;
IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);

end else
if args[0]='MODE' then begin
//:my.server.name 329 kloun-tk #GSP!civ4 1410880935
if copy(args[1],1,1)<>'#' then
write('!!!!!!!1USER MODE OPERATION, ERROR!!!!!!!!!!')
else
if args[2]='' then begin

if args[1]='#GSP!civ4btsjp' then ts5:='#GSP!civ4bts' else ts5:=args[1];
//write('MODE REQUEST');
ts2:=':'+HOST+' 324 '+TUSER(userlist.Items[cu]).nick+ ' '+args[1]+' '+Tchannel(Channels.Items[IRCDCamelIdentify(ts5)]).modes +#13#10
//IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);

end
else begin
//SETTING NEW MODES
//check out normal irc
//write('MODE UPDATE'+' '+args[2]);

//if args[1]='civ4btsjp' then ts5:='civ4bts' else ts5:=args[1];   PLAYER WILL ONLY SET MODES OF NONTITLE ROOMS

ts2:=':'+HOST+' 324 '+TUSER(userlist.Items[cu]).nick+ ' '+args[1]+' '+Tchannel(Channels.Items[IRCDCamelIdentify(args[1])]).modes +#13#10;

IRCDSETMODES(IRCDCamelIdentify(args[1]),fluids);

end;
IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);
//+':'+HOST+' 329 '+TUSER(userlist.Items[cu]).nick+ ' '+args[1]+' 1410880935'+#13#10


{//GETCKEY part of response
ts2:=':'+HOST+' 702 '+TUSER(userlist.Items[cu]).nick+' '+args[1]+' '+TUSER(userlist.Items[cu]).nick+' 000 :\'+TUSER(userlist.Items[cu]).user+'\'+#13#10+
':'+HOST+' 702 '+TUSER(userlist.Items[cu]).nick+' '+args[1]+' RightTit 000 :\XDaupalslX|155978172\'+#13#10+
':'+HOST+' 703 '+TUSER(userlist.Items[cu]).nick+' '+args[1]+' 000 :End of GETCKEY'+#13#10;

IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);
}
//ts2:=':'+HOST+' 001 '+TUSER(userlist.Items[cu]).nick+' :UNSTUCKING '+TUSER(userlist.Items[cu]).nick+'!'+TUSER(userlist.Items[cu]).user+'@'+TUSER(userlist.Items[cu]).RHost+'+'+#13#10;
//IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);
{>>>GETCKEY #GSP!civ4 * 000 0 :\username\b_flags
>GETCKEY #GPG!2266 * 000 0 :\username\b_flags Response
:s 702 Sidonuke #GPG!2266 LeftTit 000 :\XlG1W4OFpX|153849803\
:s 702 Sidonuke #GPG!2266 RightTit 000 :\XDaupalslX|155978172\
:s 703 Sidonuke #GPG!2266 000 :End of GETCKEY  }
//write('MODE REQUEST LEL'{+fluids});
end else
if args[0]='TOPIC' then begin
//TOPIC #GSP!civ4bts!MKhq3h3qhM :admin's Game
//  0               1               2
//:s 332 Sidonuke #GPG!2176 :Click on the "Game Info" button a
ci:=IRCDCamelIdentify(args[1]);
Tchannel(channels.items[ci]).topic:=copy(args[2],2,length(args[2]));
ts2:=':s 332 '+TUSER(userlist.items[cu]).nick+args[1]+' '+args[2]+#13#10;
//
IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);
write('TOPIC COMMAND(Not working)');
end else
//on getckey - list all users and their requested room flags
if args[0]='GETCKEY' then begin
//GETCKEY #GSP!civ4bts * 000 0 :\username\b_flags
//  0         1        2  3  4        5
//GETCKEY #GSP!civ4bts!M1Kh1DJzDM * 001 0 :\username\b_flags
{:s 702 Sidonuke #GPG!2266 Sidonuke 000 :\XlG1W4OFpX|153849803\
:s 702 Sidonuke #GPG!2266 TonyFerelli 000 :\XDaupalslX|155978172\
:s 702 Sidonuke #GPG!2266 Dunkelherz 000 :\XlDDfqOfaX|155981948\s
:s 702 Sidonuke #GPG!2266 chriswar 000 :\XGsqlaGfqX|153361449\s
:s 702 Sidonuke #GPG!2266 Night-Hawk 000 :\XG9sfl1spX|153159886\
:s 702 Sidonuke #GPG!2266 RebelWithout 000 :\XfO19GpWOX|154008306\s
:s 702 Sidonuke #GPG!2266 Trismegistus 000 :\XWWfFfFFlX|155776766\
:s 702 Sidonuke #GPG!2266 ChatMonitor-gs 000 :\XaaaaaaaaX|25677635\s
:s 703 Sidonuke #GPG!2266 000 :End of GETCKEY
}
//loop through users inside the channel
ts4:=args[1];
if args[1]='#GSP!civ4btsjp' then args[1]:='#GSP!civ4bts';
ci:=IRCDCamelIdentify(args[1]);
write(inttostr(Tchannel(channels.items[ci]).userlist.Count));
for i:=0 to Tchannel(channels.items[ci]).userlist.Count-1 do begin
if (args[1]=cvi4titleroom) or (args[1]=cvi4btstitleroom) or (args[1]=cvi4btsjptitleroom) then
ts3:=copy(TUser(Tchannel(channels.items[ci]).userlist.Items[i]).TitleRoom_b_flag,9,length(TUser(Tchannel(channels.items[ci]).userlist.Items[i]).TitleRoom_b_flag)) else
ts3:=copy(TUser(Tchannel(channels.items[ci]).userlist.Items[i]).Game_b_flag,9,length(TUser(Tchannel(channels.items[ci]).userlist.Items[i]).Game_b_flag));
ts2:=':s 702 '+TUSER(userlist.items[cu]).nick+ts4+' '+TUser(Tchannel(channels.items[ci]).userlist.Items[i]).nick+' '+args[3]+' '+':\'+TUser(Tchannel(channels.items[ci]).userlist.Items[i]).User+'\'+ts3+#13#10;
IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);
end;
ts2:=':s 703 '+TUSER(userlist.items[cu]).nick+ts4+' '+args[3]+' :End of GETCKEY'+#13#10;
IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);


end else
if args[0]='SETCKEY' then begin
//SETCKEY #GPG!2166 Sidonuke :\b_flags\
// 0         1        2          3
//change user's own flag,
ts4:=args[1];
if args[1]='#GSP!civ4btsjp' then args[1]:='#GSP!civ4bts';
ci:=IRCDCamelIdentify(args[1]);
if (args[1]=cvi4btstitleroom) and ((TUser(Userlist.items[cu]).gamename='civ4bts') or (TUser(Userlist.items[cu]).gamename='civ4btsjp')) then begin
TUser(Userlist.items[cu]).TitleRoom_b_flag:=trim(copy(args[3],2,length(args[3])-1)) end else
ts2:={':s 702 '+args[1]+}' '+args[1]+' '+TUser(Userlist.items[cu]).nick+' BCAST :'+TUser(Userlist.items[cu]).TitleRoom_b_flag+#13#10;
if (args[1]=cvi4titleroom) and (TUser(Userlist.items[cu]).gamename='civ4') then begin
TUser(Userlist.items[cu]).TitleRoom_b_flag:=trim(copy(args[3],2,length(args[3])-1));
ts2:={':s 702 '+args[1]+}' '+args[1]+' '+TUser(Userlist.items[cu]).nick+' BCAST :'+TUser(Userlist.items[cu]).TitleRoom_b_flag+#13#10 end else begin
TUser(Userlist.items[cu]).Game_b_flag:=trim(copy(args[3],2,length(args[3])-1));
ts2:={':s 702 '+args[1]+}' '+args[1]+' '+TUser(Userlist.items[cu]).nick+' BCAST :'+TUser(Userlist.items[cu]).Game_b_flag+#13#10;
end;

//send BCAST to everyone in the room which the flag was related to
//:s 702 #GSP!redalert3pcb!MaPJ9aPhaM #GSP!redalert3pcb!MaPJ9aPhaM Sidonuke BCAST :\b_flags\s
//SETCKEY #GSP!civ4!MzhK3a4l3M PeerPlayer11 :\b_flags\srh
//SETCKEY #GSP!civ4bts dingus221-tk :\b_flags\s
// SETCKEY #GSP!civ4bts!M0K3cP4zzM dingus221-tk :\b_flags\sh
//     0              1                 2             3
//:s 702 #GSP!worms4!MD3Dhcl1cM #GSP!worms4!MD3Dhcl1cM muzer-think BCAST :\b_flags\s
 //tmpstr3:=':'+TUSER(userlist.items[cu]).nick+'!~'+TUSER(userlist.items[cu]).user+'@'+HOST+' PRIVMSG '+tmpstr{TChannel(channels.Items[ci]).name}+' '+args[2]+#13#10
 ; // else
// tmpstr3:=':'+copy(TUSER(userlist.items[cu]).nick,1,length(TUSER(userlist.items[cu]).nick))+'!~'+TUSER(userlist.items[cu]).user+'@'+HOST+' PRIVMSG '+tmpstr{TChannel(channels.Items[ci]).name}+' '+args[2]+#13#10;
 //send to all on the channel but the sender


 for i:=0 to TChannel(channels.Items[ci]).userlist.Count-1 do begin
     //if TUSER(TChannel(channels.Items[ci]).userlist.Items[i])<>TUSER(userlist.Items[cu]) then
 //if ts4<>'civ4btsjp' then
 if (TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).gamename='civ4btsjp') and (args[1]='#GSP!civ4bts') then
 ts5:='#GSP!civ4btsjp' else
 ts5:=args[1];

 ts3:=':s 702 '+ts5+ts2;
 IRCDLubricate(ts3,TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).RHost,TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).RPort,USERLIST.IndexOf(TUSER(TChannel(channels.Items[ci]).userlist.Items[i])),TUSER(TChannel(channels.Items[ci]).userlist.Items[i]).Crypton);//Rhost,Rport);
 //form1.Caption:=form1.Caption+'S';
 end;


//IRCDLubricate(ts2,Rhost,Rport,cu,TUSER(userlist.items[cu]).Crypton);
end;

//
end;

procedure TForm1.IRCDPenetrate(Rhost:string;Rport:integer);
var
temp:integer;
begin
//
//user creation
temp:=IRCDFUCKASS(Rhost,Rport,0);
IRCDLubricate(':'+HOST+' NOTICE Auth :*** Looking up your hostname...biatch'+#13+#10,rhost,rport,-1,false);
//send shid
//
end;

procedure TForm1.IRCDTittieBong();

begin
//Write('');
Write('MoistnessLevelReport:');
Write('UserListCount:'+inttostr(USERLIST.Count));
Write('DaemonsActiveConnections:'+inttostr(daemon.Socket.ActiveConnections));
Write('ChannelsCount:'+inttostr(CHANNELS.Count));

//
end;

procedure TForm1.IRCDParadrop({Channelindex,}userindex{,USERINDEXinsidechannel_userlist}:integer;channelname:string);
var
i,tci:integer;
begin
//
for i:=0 to TUser(Userlist.Items[userindex]).ChannelsJoined.Count-1 do begin
if TChannel(TUser(Userlist.Items[userindex]).ChannelsJoined.items[i]).name=channelname then
  begin
  tci:=Channels.IndexOf(TChannel(TUser(Userlist.Items[userindex]).ChannelsJoined.items[i]));
  write('tci:'+inttostr(tci));
  TUser(Userlist.Items[userindex]).ChannelsJoined.Delete(i);
  end;
end;

TChannel(Channels.Items[tci]).userlist.Remove(TUser(Userlist.Items[userindex])); //.Delete();//USERINDEXinsidechannel_userlist);
//IS THIS WORKING?
end;

function compareChByname(Item1 : Pointer; Item2 : Pointer) : Integer;

begin
  // We start by viewing the object pointers as TCustomer objects


  // Now compare by string
  if      TChannel(Item1).name > TChannel(Item2).name
  then Result := 1
  else if TChannel(Item1).name = TChannel(Item1).name
  then Result := 0
  else Result := -1;
end;

procedure TForm1.IRCDAbandonTheChannel(index:integer);
var
i:integer;
begin
//showmessage('doritos1');
write(TChannel(channels.Items[index]).name+' abandoned');
TChannel(Channels.Items[index]).userlist.Free;
TChannel(channels.Items[index]).Free;
Channels.Delete(index);


//channels.Sort(compareChByname);
//FREE THE SHIT
end;
function TForm1.IRCDCretanParty(name,title:string):integer;
var
temp:integer;
begin
  temp:=CHANNELS.Add(TChannel.NewInstance);
  TChannel(CHANNELS.Items[temp]).name:=name;
  TChannel(CHANNELS.Items[temp]).topic:=title;
  TChannel(CHANNELS.Items[temp]).modes:='+tnp';
  //TChannel(CHANNELS.Items[temp]).channelindex:=temp;
   TChannel(CHANNELS.Items[temp]).userlist := TList.Create;
   result:=temp;
//
end;

procedure TForm1.IRCDJohnTheCamel(Channelindex,USERINDEX:integer);
var
temp:integer;
begin
  //
  temp:=TChannel(CHANNELS.Items[Channelindex]).userlist.Add(USERLIST.Items[USERINDEX]);
  TUSER(USERLIST.Items[USERINDEX]).ChannelsJoined.Add(CHANNELS.Items[Channelindex]);
  Write('Camel['+inttostr(USERINDEX)+'].Created.Moisture increased.');

end;


procedure TUSER.CheckIfOnline();
begin
//send ping
//set timer or callback for pong
end;


procedure TForm1.IRCDExterminate(index:integer);       //<-----
var
i:integer;
begin
//first part the channels one by one
if TUSER(USERLIST.Items[index]).ChannelsJoined.Count>0 then begin
  for i:=0 to TUSER(USERLIST.Items[index]).ChannelsJoined.Count-1 do begin
      write('user:'+TUSER(USERLIST.Items[index]).nick+' kicked out of:'+TChannel(TUSER(USERLIST.Items[index]).ChannelsJoined.Items[i]).name);
      TChannel(TUSER(USERLIST.Items[index]).ChannelsJoined.Items[i]).userlist.Remove(TUSER(USERLIST.Items[index]));
  //if channel is wack, delete
  if TChannel(TUSER(USERLIST.Items[index]).ChannelsJoined.Items[i]).userlist.Count<1 then
  IRCDAbandonTheChannel(channels.IndexOf(Tchannel(TUSER(USERLIST.Items[index]).ChannelsJoined.Items[i])));

  end;
end;
TUSER(USERLIST.Items[index]).ChannelsJoined.Free;
TUSER(USERLIST.Items[index]).Free;
USERLIST.Remove(userlist.Items[index]);

end;

function TForm1.IRCDFUCKASS(Raddress:string;RPort:integer;{username,nick:string;}socketnumbr:integer):integer;           //<--------
var
temp:integer;
begin
//
  temp:=USERLIST.Add(TUSER.NewInstance);
  TUSER(USERLIST.Items[temp]).Rhost:=Raddress;
  TUSER(USERLIST.Items[temp]).Rport:=Rport;
  TUSER(USERLIST.Items[temp]).Crypton:=false;
  TUSER(USERLIST.Items[temp]).TitleRoom_b_flag:='\b_flags\';
  TUSER(USERLIST.Items[temp]).Game_b_flag:='\b_flags\';
 // TUSER(USERLIST.Items[temp]).User:=username;
 // TUSER(USERLIST.Items[temp]).nick:=nick;
  //TUSER(USERLIST.Items[temp]).SocketIndex:=socketnumbr;
  //TUSER(USERLIST.Items[temp]).UserListIndex:=temp;
  TUSER(USERLIST.Items[temp]).ChannelsJoined:=TList.Create;
  Write('UserAssfucking['+inttostr(temp)+'].Done.');
  result:=temp;//USERLIST.Count-1;
  //for i:=0 to userlist.Count-1 do begin
  //Write(TUSER(USERLIST.Items[i]).User);
  //end;
  //Write(inttostr(USERLIST.count));
end;

procedure TForm1.IRCDGetMoist();   //<-----
//var
//i:integer;
begin
{ Create a new List. }
write('/help command must be working');
  USERLIST := TList.Create;
  CHANNELS := TList.Create;
  try Daemon.Active:=true except write('Error starting daemon');end;
  if daemon.Active=true then write('Daemon has started(with no error).');
gngk[0][0]:='civ4';
gngk[0][1]:='y3D9Hw';
gngk[1][0]:='civ4bts';
gngk[1][1]:='Cs2iIq';
gngk[2][0]:='gmtest';
gngk[2][1]:='HA6zkS';
CCount:=0;
CSPos:=0;


//showmessage(  booltostr(daemon.Active));

//does tlist have to be freed or removed in some way?    YES
end;

procedure TForm1.IRCDDongers();   //<-----
var
i,i2:integer;
begin
  for i:=userlist.Count-1 downto 0 do begin
  TUSER(USERLIST.Items[i]).Free;
      for i2:=TUSER(USERLIST.Items[i]).ChannelsJoined.Count-1 downto 0 do begin
          TUSER(USERLIST.Items[i]).ChannelsJoined.Free;
      end;
  end;
  USERLIST.Free;
    for i:=channels.Count-1 downto 0 do begin
      IRCDAbandonTheChannel(i);
  end;

  CHANNELS.Free;

end;


procedure TForm1.Termite();
begin
cs.Active:=false;
daemon.Active:=false;
application.Terminate;
 //dong.

end;


procedure TForm1.Write(wat:string);
var
i:integer;
bongerss:string;
begin

//bongerss:=wat;
{for i:=0 to length(wat)-1 do begin
if (wat[i]=#13) then wat[i]:='G';
if (wat[i]=#10) then wat[i]:='G';
//if (wat[i]=#0) then wat[i]:='M';

//bongerss[i]:=wat[i];
//memo1.Lines[memo1.Lines.Count-1]
//(wat);
end;}
//memo1.Lines.Add(bongerss);
memo1.Lines.Add('['+TimeToStr(Now)+'] '+trim(wat));
{if memo1.Lines.Capacity>500 then
memo1.Lines.Delete(0);
memo1.Lines.Add('-');
memo1.Lines.Delete(memo1.Lines.Capacity-1);  }
end;




procedure TForm1.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Termite();
end;

procedure TForm1.Button2Click(Sender: TObject);
begin

//LOGIN 17 rrrr-tk eb9279982226a42afdf2860dbdc29b45
//cs.Active:=true;

end;

procedure TForm1.DaemonClientConnect(Sender: TObject;
  Socket: TCustomWinSocket);
begin

write('Client joined:'+inttostr(Daemon.socket.ActiveConnections));
richedit1.SelAttributes.Color:=clblack;
//richedit1.Lines.Add(Socket.RemoteAddress+':'+inttostr(socket.RemotePort)+' connected.');

  //  Socket.RemoteAddress;
  //  Socket.RemotePort;
  // those 2 identify user
   //IRCDPenetrate(Socket.RemoteAddress,Socket.RemotePort);
end;

procedure TForm1.DaemonClientDisconnect(Sender: TObject;
  Socket: TCustomWinSocket);
  var
  i,cu:integer;
begin
//write('Client disconnected:'+socket.LocalAddress);
//kill user
//remove him from channels
//kill channels if empty

//figure which user is corresponded
//call procedures
//IRCDExterminate

if Daemon.Socket.ActiveConnections>0 then begin
for i:=0 to Daemon.Socket.ActiveConnections-1 do begin
  if ({Daemon.Socket.Connections[i]}Socket.RemoteAddress=TUser(userlist[i]).RHost) and (Socket.RemotePort=TUser(userlist[i]).RPort) then begin
  cu:=i;
  break;
  end;
end;
end;
Write(TUser(userlist[cu]).RHost+'('+TUser(userlist[cu]).nick+ ') disconnected.');
Richedit1.lines.add(TUser(userlist[cu]).RHost+'('+TUser(userlist[cu]).nick+ ') disconnected.');
IRCDExterminate(cu);

end;

procedure TForm1.DaemonGetThread(Sender: TObject;
  ClientSocket: TServerClientWinSocket;
  var SocketThread: TServerClientThread);
begin
write('thread got');
end;

procedure TForm1.DaemonClientRead(Sender: TObject;
  Socket: TCustomWinSocket);
  var
  dong,strr,strr2:string;
  i,tmp1:integer;
  Size,S3: Integer;
  Bytes: array [0..2024] of byte;
  shid1:string;
  shid2:pansichar;
  donger332:PAnsiChar;
  cu:integer;
  a13:bool;
begin
  Size := Socket.ReceiveLength;
  Socket.ReceiveBuf(Bytes[0], Size);

  tmp1:=0;
  strr:='';
 strr2:='';
cu:=-1;
for i:=0 to userlist.Count-1 do begin
   if (TUSER(userlist.Items[i]).Rhost=Socket.RemoteAddress) and(TUSER(userlist.Items[i]).Rport=Socket.RemotePort) then
     begin
       cu:=i;
     end;
end;
//can be -1;
//memo1.Lines.Add('OldDesnC'+inttostr(TUSER(userlist.Items[cu]).DESN_C));
a13:=false;
for i:=0 to Size-1 do begin
if clothes=false then
com.Text:=com.Text+',0x'+{inttostr(i+1)+'#'+}(inttohex(Bytes[i],2));
strr:=strr+char(Bytes[i]);

if (cu>-1) then begin
   if (TUSER(userlist.Items[cu]).Crypton=true) then begin
   shid1:=char(Bytes[i]);
   donger332:=IRCDThrowShitOnTheFan(shid1,TUSER(userlist.Items[cu]).DESN_C,1,TUSER(userlist.Items[cu]).gamename);//bongciv4(pansichar(shid1),TUSER(userlist.Items[cu]).DESN_C,1);

   TUSER(userlist.Items[cu]).DESN_C:=TUSER(userlist.Items[cu]).DESN_C+1;
   strr2:=strr2+donger332;
   if copy(strr2,length(strr2)-1,2)=#13#10 then begin
   //memo1.Lines.Add('!!!!!DONGERs!!!!!'+copy(strr2,1,length(strr2)-2)+'!!!!DONGERs!');
   IRCDExplosions(copy(strr2,1,length(strr2){-2}),socket.remoteaddress,socket.remoteport);
   //memo1.Lines.Add('!!!!!DONGERs!!!!!'+copy(strr2,1,length(strr2)-2)+'!!!!DONGERs!');
   strr2:='';
   end;
   dun:=true;
   end;
end;

tmp1:=tmp1+1;
end;
//memo1.Lines.add('Recieved(till \0):'+strr);
if dun=false then
IRCDExplosions(strr,socket.remoteaddress,socket.remoteport);
//strr:=strr2;
dun:=false;

//memo1.Lines.Add('NEWDesnC'+inttostr(TUSER(userlist.Items[cu]).DESN_C));


if clothes=false then
memo1.Lines.Add(com.Text);

com.Text:='';
//memo1.Lines.Add('SIZE:'+inttostr(tmp1)+'TEXT:'+char(Bytes[tmp1-6])+'_'+char(Bytes[tmp1-5])+'_'+char(Bytes[tmp1-4])+'_'+char(Bytes[tmp1-3])+'_'+char((Bytes[tmp1-2]))+'_'+char((Bytes[tmp1-1])));
//strr:= Copy(string(@Bytes), 1, S2);
//strr :=GetString(Bytes);

//showmessage(strr);


//showmessage(strr);


//memo1.lines.add(inttostr(socket.ReceiveLength));
//dong:=socket.ReceiveText;
//IRCDExplosions(dong,socket.remoteaddress,socket.remoteport);

end;

procedure TForm1.Button466Click(Sender: TObject);
begin
cs.Active:=true;

end;

procedure TForm1.Button3Click(Sender: TObject);
begin
cs.Socket.SendText(com.Text+#13#10);

end;

procedure TForm1.CSRead(Sender: TObject; Socket: TCustomWinSocket);
begin
write('[cs] '+socket.ReceiveText);
end;

procedure TForm1.Button5Click(Sender: TObject);
begin
//cs.Socket.SendText('LOGIN 17 rrrr-tk eb9279982226a42afdf2860dbdc29b45'+#13+#10);




//daemon.Socket.Connections[0].SendText(com.Text+#13#10);
//daemon.Socket.SendText(com.Text+#13#10);
end;

procedure TForm1.CSConnect(Sender: TObject; Socket: TCustomWinSocket);
begin
//socket.SendText('LOCALDUD.COM');
end;

procedure TForm1.FormKeyDown(Sender: TObject; var Key: Word;
  Shift: TShiftState);
begin
if key=vk_Return then
Termite();
end;

procedure TForm1.Button7Click(Sender: TObject);
var
i:integer;
begin
{//USERLIST := TList.Create;
Write('USERS');
if  userlist.Count<>0 then
  for i:=0 to userlist.Count-1 do begin
  Write(inttostr(i)+'. '+TUSER(USERLIST.Items[i]).User+'; rn:'+TUSER(USERLIST.Items[i]).RealName+'; nick:'+TUSER(USERLIST.Items[i]).Nick);
//  Write('  '+TUSER(USERLIST.Items[i]).RealName);
//  Write('  '+TUSER(USERLIST.Items[i]).Nick);
//  Write('  '+inttostr(TUSER(USERLIST.Items[i]).DESN_C));
  end;
  Write(inttostr(USERLIST.count)+#13#10);

Write('Channels:'+inttostr(channels.count));
if  channels.Count<>0 then
//showmessage(inttostr(channels.Count));
  for i:=0 to channels.Count-1 do begin
  Write(TChannel(channels.Items[i]).name);
  end;
           }


end;

procedure TForm1.Memo1KeyDown(Sender: TObject; var Key: Word;
  Shift: TShiftState);
begin
if key=vk_escape then
Termite();
end;

procedure TForm1.FormCreate(Sender: TObject);
begin
MrCrypton:=false;
clothes:=true;
IRCDGetMoist();

end;

procedure TForm1.Button1Click(Sender: TObject);
var
tmp33:integer;
begin

end;

procedure TForm1.DaemonAccept(Sender: TObject; Socket: TCustomWinSocket);
var
dong:string;
begin
IRCDPenetrate(Socket.RemoteAddress,Socket.RemotePort);


end;

procedure TForm1.Panel1Click(Sender: TObject);
var
ctx1:gs_peerchat_ctx;
AnsiStr: AnsiString;
  Str: string;
begin
//GS_PC_Init(ctx1,'y3D9Hw','00000000',0);
//str:={'Enc.exe '+}edit1.Text;//+' > out.txt';
{AnsiStr := AnsiString(Str);
  ShellExecute(0, nil, 'Enc.exe', PAnsiChar(AnsiStr), nil, SW_HIDE);
  Sleep(100);
  memo2.lines.LoadFromFile('o1.txt');
 }
 str:=':s 302  :=+@'+'0.0.0.0';

 str:='USER X14saFv19X|100000011 127.0.0.1 peerchat.gamespy.com :9095b890a236b7779d85c7ec80cf3443';
// str:=chr($ed)+chr($79)+chr($f6)+chr($f7)+chr($44)+chr($cb)+chr($9c)+chr($f7)+chr($4f)+chr($9d)+chr($c2)+chr($b4)+chr($20)+chr($24)+chr($f3)+chr($32)+chr($b4)+chr($15)+chr($51)+chr($27)+chr($f5)+chr($87);//++;

//str:=chr($83)+chr($64)+chr($bc)+chr($61)+chr($df)+chr($4c)+chr($99);
//str:=chr($6c)+chr($b4)+chr($8f)+chr($6f)+chr($a8)+chr($d3)+chr($f9)+chr($bf)+chr($1e)+chr($8d)+chr($8a)+chr($4b)+chr($20)+chr($b4)+chr($8c)+chr($ec)+chr($ab);

 str:=edit1.Text;

str:=chr($aa)+chr($03)+chr($0a)+chr($e5)+chr($68)+chr($61)+chr($a6)+chr($66)+chr($81)+chr($48)+chr($a8)+chr($83)+chr($d4)+chr($29)+chr($52)+chr($68)+chr($31)+chr($19)+chr($ea)+chr($af)+chr($6f)+chr($83)+chr($bf)+chr($f1)+chr($13)+chr($1b)+chr($a6)+chr($85)+chr($d1)+chr($ff)+chr($d6)+chr($4c)+chr($fb)+chr($47)+chr($98)+chr($86)+chr($58)+chr($29)+chr($a7)+chr($dd)+chr($af)+chr($f5)+chr($e6)+chr($09)+chr($0a)+chr($98)+chr($e6)+chr($d0)+chr($a7)+chr($b2)+chr($b4)+chr($7a)+chr($77)+chr($5e)+chr($a1)+chr($bf)+chr($49)+chr($98)+chr($eb)+chr($32)+chr($fd)+chr($c5)+chr($40)+chr($8e)+chr($50)+chr($41)+chr($4f)+chr($31)+chr($5e)+chr($29)+chr($ad)+chr($02)+chr($67)+chr($cd)+chr($2e)+chr($30)+chr($45)+chr($92)+chr($cc)+chr($c9)+chr($9f)+chr($37)+chr($aa)+chr($30)+chr($9a)+chr($1b)+chr($75)+chr($98)+chr($16)+chr($27)+chr($b9)+chr($5c)+chr($71)+chr($d2)+chr($9b)+chr($dc)+chr($8b)+chr($11)+chr($90)+chr($1a)+chr($73)+chr($94)+chr($58)+chr($eb)+chr($69)+chr($3a)+chr($1d);

//str:=chr($ec)+chr($44)+chr($ce)+chr($1b)+chr($bf)+chr($73)+chr($b3)+chr($df)+chr($6a)+chr($72)+chr($9c)+chr($08)+chr($09)+chr($b9)+chr($62)+chr($dc)+chr($19)+chr($c0)+chr($c5)+chr($e8)+chr($1a);
// str:=chr($33)+chr($34);
 showmessage(str);
end;

procedure TForm1.Button11Click(Sender: TObject);
var
i:integer;
begin
for i:=0 to (length(edit1.text)) do begin
if Odd(i) then
edit2.Text:=edit2.Text+'0x'+copy(edit1.Text,i,2)+',';

end;

end;


procedure TForm1.Button12Click(Sender: TObject);
begin
//showmessage(inttostr(strtoint(edit3.Text)));

//daemon.Socket.Connections[0].SendText('PING :SomeJizz332199');
end;

procedure TForm1.DaemonClientError(Sender: TObject;
  Socket: TCustomWinSocket; ErrorEvent: TErrorEvent;
  var ErrorCode: Integer);
  var
  s:string;
  begin
s:=inttostr(errorcode);
if (errorcode=10053) then begin
socket.Close;
//errorcode:=0;
end;

write('error:'+s);
errorcode:=0;
//showmessage(s);
end;

procedure TForm1.ClitorisKeyDown(Sender: TObject; var Key: Word;
  Shift: TShiftState);
begin
if key=vk_return then  begin
CSPos:=0;
IRCDGenitalDirect(Clitoris.Text);
clitoris.Text:='';
end else

if key=vk_up then begin
CSPos:=CSPos+1;
if cspos=CCount+1 then cspos:=1;
Clitoris.Text:=CommandStack[cspos];
end
else


if key=vk_escape then
Termite();
end;

procedure TForm1.Button12KeyDown(Sender: TObject; var Key: Word;
  Shift: TShiftState);
begin
if key=vk_escape then
Termite();
end;

procedure TForm1.FormShow(Sender: TObject);
begin
clitoris.SetFocus;
end;

procedure TForm1.ClitorisKeyPress(Sender: TObject; var Key: Char);
begin
if (key = #13) or (key = #27) then // #13 = Return
  begin
    key := #0;
    // so that it doesnt beep
  end;
end;

end.
