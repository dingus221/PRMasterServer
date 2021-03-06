using Alivate;
using MaxMind.GeoIP2;
using PRMasterServer.Data;
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Reflection;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;

namespace PRMasterServer.Servers
{
	internal class ServerListReport
	{
		private const string Category = "ServerReport";

		public Action<string, string> Log = (x, y) => { };
		public Action<string, string> LogError = (x, y) => { };

		public readonly ConcurrentDictionary<string, GameServer> Servers;

		private string[] ModWhitelist;
		private IPAddress[] PlasmaServers;

		public Thread Thread;

		private const int BufferSize = 65535;
		public static Socket _socket;
		private SocketAsyncEventArgs _socketReadEvent;
		private byte[] _socketReceivedBuffer;

		// 09 then 4 00's then battlefield2
        private string _gameName = Program.gameName;//"civ4";//changed from battlefield2
		private byte[] _initialMessage;

      //  public static void SendToAllConnected()
      //  {
        //_socket.
    //    }
		public ServerListReport(IPAddress listen, ushort port, Action<string, string> log, Action<string, string> logError, string gameName)
		{
            if (gameName != null) _gameName = gameName;
            List<byte> initialMessage = new byte[] { 0x09, 0x00, 0x00, 0x00, 0x00 }.ToList();
            initialMessage.AddRange(Encoding.ASCII.GetBytes(_gameName));
            initialMessage.Add(0x00);
            //Console.WriteLine("[initial:]" + _initialMessage[0] + _initialMessage[1] + _initialMessage[2] + _initialMessage[3] + _initialMessage[4] + ',' + _initialMessage[5] + ',' + _initialMessage[6] + ',' + _initialMessage[7] + ',' + _initialMessage[8] + ',' + _initialMessage[9]);
            _initialMessage = initialMessage.ToArray();
            //Console.WriteLine("[initial:]" + _initialMessage[0] + _initialMessage[1] + _initialMessage[2] + _initialMessage[3] + _initialMessage[4] + ',' + _initialMessage[5] + ',' + _initialMessage[6] + ',' + _initialMessage[7] + ',' + _initialMessage[8]);

			Log = log;
			LogError = logError;

			GeoIP.Initialize(log, Category);

			Servers = new ConcurrentDictionary<string, GameServer>();

			Thread = new Thread(StartServer) {
				Name = "Server Reporting Socket Thread"
               
			};
			Thread.Start(new AddressInfo() {
				Address = listen,
				Port = port
			});

			new Thread(StartCleanup) {
				Name = "Server Reporting Cleanup Thread"
			}.Start();

			new Thread(StartDynamicInfoReload) {
				Name = "Dynamic Info Reload Thread"
                
			}.Start();


            

		}

		public void Dispose()
		{
			Dispose(true);
			GC.SuppressFinalize(this);
            
		}

		protected virtual void Dispose(bool disposing)
		{
			try {
				if (disposing) {
					if (_socket != null) {
						_socket.Close();
						_socket.Dispose();
						_socket = null;
					}
				}
			} catch (Exception) {
			}
		}

		~ServerListReport()
		{
			Dispose(false);
		}

		private void StartServer(object parameter)
		{
			AddressInfo info = (AddressInfo)parameter;

			Log(Category, "Starting Server List Reporting");

			try {
				_socket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp) {
					SendTimeout = 5000,
					ReceiveTimeout = 5000,
					SendBufferSize = BufferSize,
					ReceiveBufferSize = BufferSize
				};

				_socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ExclusiveAddressUse, true);
				_socket.Bind(new IPEndPoint(info.Address, info.Port));

				_socketReadEvent = new SocketAsyncEventArgs() {
					RemoteEndPoint = new IPEndPoint(IPAddress.Any, 0)
				};
				_socketReceivedBuffer = new byte[BufferSize];
				_socketReadEvent.SetBuffer(_socketReceivedBuffer, 0, BufferSize);
				_socketReadEvent.Completed += OnDataReceived;
			} catch (Exception e) {
				LogError(Category, String.Format("Unable to bind Server List Reporting to {0}:{1}", info.Address, info.Port));
				LogError(Category, e.ToString());
				return;
			}

			WaitForData();
		}

		private void StartCleanup(object parameter)
		{
			while (true) {
				foreach (var key in Servers.Keys) {
					GameServer value;

					if (Servers.TryGetValue(key, out value)) {
						if (value.LastPing < DateTime.UtcNow - TimeSpan.FromSeconds(30)) {
							Log(Category, String.Format("Removing old server at: {0}", key));

							GameServer temp;
							Servers.TryRemove(key, out temp);
						}
					}
				}

				Thread.Sleep(10000);
			}
		}

		private void StartDynamicInfoReload(object obj)
		{
			while (true) {
				// the modwhitelist.txt file is for only allowing servers running certain mods to register with the master server
				// by default, this is pr or pr_* (it's really pr!_%, since % is wildcard, _ is placeholder, ! is escape)
				// # is for comments
				// you either want to utilize modwhitelist.txt or hardcode the default if you're using another mod...
				// put each mod name on a new line
				// to allow all mods, just put a single %
				if (File.Exists("modwhitelist.txt")) {
					Log(Category, "Loading mod whitelist");
					ModWhitelist = File.ReadAllLines("modwhitelist.txt").Where(x => !String.IsNullOrWhiteSpace(x) && !x.Trim().StartsWith("#")).ToArray();
				} else {
					ModWhitelist = new string[] { "pr", "pr!_%" };
				}

				// plasma servers (bf2_plasma = 1) makes servers show up in green in the server list in bf2's main menu (or blue in pr's menu)
				// this could be useful to promote servers and make them stand out, sponsored servers, special events, stuff like that
				// put in the ip address of each server on a new line in plasmaservers.txt, and make them stand out
				if (File.Exists("plasmaservers.txt")) {
					Log(Category, "Loading plasma servers");
					PlasmaServers = File.ReadAllLines("plasmaservers.txt").Select(x => {
						IPAddress address;
						if (IPAddress.TryParse(x, out address))
							return address;
						else
							return null;
					}).Where(x => x != null).ToArray();
				} else {
					PlasmaServers = new IPAddress[0];
				}

				GC.Collect();

				Thread.Sleep(5 * 60 * 1000);
			}
		}

		private void WaitForData()
		{
			Thread.Sleep(10);
			GC.Collect();

			try {
				_socket.ReceiveFromAsync(_socketReadEvent);
                
			} catch (SocketException e) {
				LogError(Category, "Error receiving data");
				LogError(Category, e.ToString());
				return;
			}
		}

		private void OnDataReceived(object sender, SocketAsyncEventArgs e)
		{
            //Program.LogPink("Q&R.DataReceived");
			try {
				IPEndPoint remote = (IPEndPoint)e.RemoteEndPoint;
                
				byte[] receivedBytes = new byte[e.BytesTransferred];
				Array.Copy(e.Buffer, e.Offset, receivedBytes, 0, e.BytesTransferred);
                                
               Program.LogPink("Q&R. Data recieved.");
               /* Program.LogPink("[Bytes(" + e.BytesTransferred + ")]");
                for (int i = 0; i < e.BytesTransferred; i++)
                {
                    Console.Write(receivedBytes[i] + ",");
                }
                Console.WriteLine(' ');*/
                Program.LogPink("[Q&R, Characters]"+System.Text.Encoding.ASCII.GetString(receivedBytes));
                if (receivedBytes.Length < 1) { receivedBytes[0] = 0x77; }
                
              if (receivedBytes.Length > 5 && receivedBytes[0] == 0x09)//(receivedBytes.SequenceEqual(_initialMessage)) replaced on 07.10
                {

                    // the initial message is basically the gamename, 0x09 0x00 0x00 0x00 0x00 battlefield2
                    // reply back a good response
                    byte[] uniqueId = new byte[4];
                    Array.Copy(receivedBytes, 1, uniqueId, 0, 4);


                    ///byte[] response = new byte[] { 0xfe, 0xfd, 0x00, uniqueId[0], uniqueId[1], uniqueId[2], uniqueId[3], 0xff, 0xff,0xff,0x01 };
                    byte[] response = new byte[] { 0xfe, 0xfd, 0x09, uniqueId[0], uniqueId[1], uniqueId[2], uniqueId[3],0x30,0x00 }; //0x00, 0x00, 0x00, 0x00};//{ 0x0A, 0x00, 0x00, 0x00, 0x00 };//0xfe, 0xfd, 0x09, 0x00, 0x00, 0x00, 0x00 /* added new line & shit, 0x0d, 0x0a*/ };
                    //byte[] response2 = new byte[] { 0xFE, 0xFD, 0x02 };
                    //byte[] nl = new byte[] { 0x0d, 0x0a };
                    Program.LogPink("0x09 requested");

                    try
                    {
                        _socket.SendTo(response, remote);
                    }
                    catch (Exception eee) { Program.LogGreen("Error with QR socketsending09" + eee); }
                    //_socket.SendTo(response, remote);
                    //_socket.SendTo(nl, remote);
                    
                    //_socket.SendTo(response2, remote);
                    Program.LogPink("[Response to client's 0x09]"+ System.Text.Encoding.ASCII.GetString(response));
                }
                else
                {
                    if (receivedBytes.Length > 5 && receivedBytes[0] == 0x03)
                    {
                        // this is where server details come in, it starts with 0x03, it happens every 60 seconds or so
                        Program.LogPink("0x03 requested");
                        byte[] uniqueId = new byte[4];
                        Array.Copy(receivedBytes, 1, uniqueId, 0, 4);
                        //Program.LogPink("0x03UID:" +  uniqueId[0] + ',' + uniqueId[1] + ',' + uniqueId[2] + ',' + uniqueId[3] + ',');
                        
                        //17:25
                         if (!ParseServerDetails(remote, receivedBytes.Skip(5).ToArray()))//) COMMENTED OUT 08.10
                        {
                            // this should be some sort of proper encrypted challenge, but for now i'm just going to hard code it because I don't know how the encryption works...
                            //byte[] response = new byte[] { 0xfe, 0xfd, 0x01, uniqueId[0], uniqueId[1], uniqueId[2], uniqueId[3], 0x44, 0x3d, 0x73, 0x7e, 0x6a, 0x59, 0x30, 0x30, 0x37, 0x43, 0x39, 0x35, 0x41, 0x42, 0x42, 0x35, 0x37, 0x34, 0x43, 0x43, 0x00 };
                            // trying different challenge
                            //1,86,95,97,96,65,67,78,43,120,56,68,109,87,73,118,109,100,90,65,81,69,55,104,65,118,115,90,106,120,90,115,65,0,
                            //0x01,0x56,0x5F,0x61,0x60,
                            //0x41,0x43,0x4E,0x2B,0x78,0x38,0x44,0x6D,0x57,0x49,0x76,0x6D,0x64,0x5A,0x41,0x51,0x45,0x37,0x68,0x41,
                            byte[] response = new byte[] { 0xfe, 0xfd, 0x01, uniqueId[0], uniqueId[1], uniqueId[2], uniqueId[3], 0x41, 0x43, 0x4E, 0x2B, 0x78, 0x38, 0x44, 0x6D, 0x57, 0x49, 0x76, 0x6D, 0x64, 0x5A, 0x41, 0x51, 0x45, 0x37, 0x68, 0x41, 0x00 };
                            Program.LogPink("QR.03before socketsend");
                            try
                            {
                                _socket.SendTo(response, remote);
                            }
                            catch (Exception eee) { Program.LogGreen("Error with QR socketsending03" + eee); }
                            Program.LogPink("QR.03after socketsend");
                            //Program.LogPink("ResponseTo0x03: ");
                            //for (int i = 0; i < response.Length-1; i++)
                            //{
                             //   Console.Write(response[i] + "!");
                            //}
                            //Console.WriteLine(" ");
                            Program.LogPink("ResponseTo0x03(S): " + System.Text.Encoding.ASCII.GetString(response));
                            
                        }
                    }
                    else if (receivedBytes.Length > 5 && receivedBytes[0] == 0x01)
                    {
                        // this is a challenge response, it starts with 0x01
                        Program.LogPink("0x01Requested(with challange from 0x03)");
                        byte[] uniqueId = new byte[4];
                        Array.Copy(receivedBytes, 1, uniqueId, 0, 4);
                        
                        // confirm against the hardcoded challenge
                        //byte[] validate = new byte[] { 0x72, 0x62, 0x75, 0x67, 0x4a, 0x34, 0x34, 0x64, 0x34, 0x7a, 0x2b, 0x66, 0x61, 0x78, 0x30, 0x2f, 0x74, 0x74, 0x56, 0x56, 0x46, 0x64, 0x47, 0x62, 0x4d, 0x7a, 0x38, 0x41, 0x00 };
                        //trying diff one for civ
                        //1,21,67,66,101,
                        //65,66,74,54,71,116,78,66,53,109,85,89,72,122,48,43,120,52,56,70,54,52,118,74,84,81,69,65,0,
                        //0x41,0x42,0x4A,0x36,0x47,0x74,0x4E,0x42,0x35,0x6D,0x55,0x59,0x48,0x7A,0x30,0x2B,0x78,0x34,0x38,0x46,0x36,0x34,0x76,0x4A,0x54,0x51,0x45,0x41
                        byte[] validate = new byte[] { 0x41, 0x42, 0x4A, 0x36, 0x47, 0x74, 0x4E, 0x42, 0x35, 0x6D, 0x55, 0x59, 0x48, 0x7A, 0x30, 0x2B, 0x78, 0x34, 0x38, 0x46, 0x36, 0x34, 0x76, 0x4A, 0x54, 0x51, 0x45, 0x41, 0x00 };
                        
                        
                        byte[] clientResponse = new byte[validate.Length];
                        Array.Copy(receivedBytes, 5, clientResponse, 0, clientResponse.Length);
                        Program.LogPink("crctchal(S): " + System.Text.Encoding.ASCII.GetString(clientResponse));
                        // if we validate, reply back a good response
                        if (/*clientResponse.SequenceEqual(validate)*/true)//29.09 so is always accepted
                        {
                            //Program.LogPink("Challenge accepted");
                            byte[] response = new byte[] { 0xfe, 0xfd, 0x0a, uniqueId[0], uniqueId[1], uniqueId[2], uniqueId[3] };//, 0x00, 0x00, 0x00, 0x00
                            try
                            {
                                _socket.SendTo(response, remote);
                            }
                            catch (Exception eee) { Program.LogGreen("Error with QR socketsending01" + eee); }

                            //AddValidServer(remote);

                            //Console.WriteLine("0x01 response: ");
                            // + System.Text.Encoding.ASCII.GetString(clientResponse));
                         //   for (int i = 0; i < response.Length - 1; i++)
                          //  {
                            //    Console.Write(response[i] + ",");
                           // }
                           // Console.WriteLine(" ");

                        }
                        //else Program.LogPink("CHALLENGE IS WRONGUS"); COMMENTED OUT 07.10

                    }
                    else if (receivedBytes.Length == 5 && receivedBytes[0] == 0x08)
                    {
                        // this is a server ping, it starts with 0x08, it happens every 20 seconds or so

                        byte[] uniqueId = new byte[4];
                        Array.Copy(receivedBytes, 1, uniqueId, 0, 4);
                        //Program.LogPink("SERVERLISTREPORT PING");
                        RefreshServerPing(remote);
                        //byte[] response = new byte[] { 0xfe, 0xfd, 0x0a, uniqueId[0], uniqueId[1], uniqueId[2], uniqueId[3] };
                        byte[] response = new byte[] { 0xfe, 0xfd, 0x08,uniqueId[0], uniqueId[1], uniqueId[2], uniqueId[3]};
                        try
                        {
                            _socket.SendTo(response, remote);
                        }
                        catch (Exception eee) { Program.LogGreen("Error with QR socketsending08" + eee); }
                        //there was none originaly in bf, and seems there shouldnt be _socket.SendTo(response, remote);
                        //Program.LogPink("Q&R.Ping.Response." + System.Text.Encoding.ASCII.GetString(uniqueId));
                        //{ 0xfe, 0xfd, 0x0a, uniqueId[0], uniqueId[1], uniqueId[2], uniqueId[3],0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00};

                    }
                    else if (receivedBytes[0] == 0x09) { Console.WriteLine("CHALLENGE RESPONSE?????"); }
                    else if (receivedBytes[0] == 0xFE && receivedBytes[1] == 0xFD) { Console.WriteLine("QYERRY??????"); }
                    else { Program.LogPink("UNKNOWN REQUEST"); }
                }
			} catch (Exception ex) {
				LogError(Category, ex.ToString());
			}

			WaitForData();
		}

		private void RefreshServerPing(IPEndPoint remote)
		{
            //Program.LogPink("QR.RSP CHECKPOINT 1");
			string key = String.Format("{0}:{1}", remote.Address, remote.Port);
            
			if (Servers.ContainsKey(key)) {
                //Program.LogPink("QR.RSP CHECKPOINT 2");
				GameServer value;
				if (Servers.TryGetValue(key, out value)) {
                    //Program.LogPink("QR.RSP CHECKPOINT 3");
					value.LastPing = DateTime.UtcNow;
                    
					Servers[key] = value;
				}
			}
		}

		private bool ParseServerDetails(IPEndPoint remote, byte[] data)
		{
			string key = String.Format("{0}:{1}", remote.Address, remote.Port);
			string receivedData = Encoding.UTF8.GetString(data);

            Program.LogPink("Q&R.ParsingSDetails.");
			Console.WriteLine(receivedData.Replace("\x00", "\\x00").Replace("\x02", "\\x02"));

			// split by 000 (info/player separator) and 002 (players/teams separator)
			// the players/teams separator is really 00, but because 00 may also be used elsewhere (an empty value for example), we hardcode it to 002
			// the 2 is the size of the teams, for BF2 this is always 2.
			string[] sections = receivedData.Split(new string[] { "\x00\x00\x00", "\x00\x00\x02" }, StringSplitOptions.None);

            //Program.LogPink("QR.PARS.SecLen:" + sections.Length.ToString());
            //Program.LogPink("QR.PARS.receivedData.EndsWith:" + receivedData.EndsWith("\x00\x00").ToString());
			if (sections.Length != 3 && !receivedData.EndsWith("\x00\x00"))// COMMENTED OUT ON 23.09
				return true; // true means we don't send back a response
            
			string serverVars = sections[0];
			//string playerVars = sections[1];//turned that on on 2809
			//string teamVars = sections[2];

			string[] serverVarsSplit = serverVars.Split(new string[] { "\x00" }, StringSplitOptions.None);

			GameServer server = new GameServer() {
				Valid = false,
				IPAddress = remote.Address.ToString(),
				QueryPort = remote.Port,
				LastRefreshed = DateTime.UtcNow,
				LastPing = DateTime.UtcNow
			};
            
			// set the country based off ip address
            // do we need it in civ4?
			/* if (GeoIP.Instance == null || GeoIP.Instance.Reader == null) {
				server.country = "??";
			} else {
				try {
					server.country = GeoIP.Instance.Reader.Omni(server.IPAddress).Country.IsoCode.ToUpperInvariant();
				} catch (Exception e) {
					LogError(Category, e.ToString());
					server.country = "??";
				}
			}*/

			for (int i = 0; i < serverVarsSplit.Length - 1; i += 2) {
                PropertyInfo property = server.GetType().GetProperty(serverVarsSplit[i]);
				if (property == null)
					continue;

				if (property.Name == "hostname") {
					{
                        property.SetValue(server, Regex.Replace(serverVarsSplit[i + 1], @"\s+", " ").Trim(), null);
                    }
				} else if (property.PropertyType == typeof(Boolean)) {
					// parse string to bool (values come in as 1 or 0)
					int value;
					if (Int32.TryParse(serverVarsSplit[i + 1], NumberStyles.Integer, CultureInfo.InvariantCulture, out value)) {
						property.SetValue(server, value != 0, null);
					}
				} else if (property.PropertyType == typeof(Int32)) {
					// parse string to int
					int value;
					if (Int32.TryParse(serverVarsSplit[i + 1], NumberStyles.Integer, CultureInfo.InvariantCulture, out value)) {
						property.SetValue(server, value, null);
					}
				} else if (property.PropertyType == typeof(Double)) {
					// parse string to double
					double value;
					if (Double.TryParse(serverVarsSplit[i + 1], NumberStyles.Float, CultureInfo.InvariantCulture, out value)) {
						property.SetValue(server, value, null);
					}
				} else if (property.PropertyType == typeof(String)) {
					// parse string to string
					property.SetValue(server, serverVarsSplit[i + 1], null);
				}
			}
            
           

         //   if (String.IsNullOrWhiteSpace(server.gamename) /*|| !server.gamename.Equals(Program.gameName  COMMENTED OUT 07.10 */  /*"civ4"/*changed from battlefield2, StringComparison.InvariantCultureIgnoreCase)*/)
        //    {
                //Program.LogBlue("dosh");
                    // only allow servers with a gamename of battlefield2
				//return true; // true means we don't send back a response COMENTED OUT 07.10
			/*}/* else if (String.IsNullOrWhiteSpace(server.gamevariant) || !ModWhitelist.ToList().Any(x => SQLMethods.EvaluateIsLike(server.gamevariant, x))) {
				// only allow servers with a gamevariant of those listed in modwhitelist.txt, or (pr || pr_*) by default
				return true; // true means we don't send back a response
			}*/

			// you've got to have all these properties in order for your server to be valid
            bool tits = false;
			if (!String.IsNullOrWhiteSpace(server.hostname) && server.hostport > 1024 && server.hostport <= UInt16.MaxValue)
                {
				server.Valid = true;
                server.groupid = null;//were "1", changed 28.09
                tits = true;
                }
            
            if (server.statechanged == 2 && String.IsNullOrWhiteSpace(server.hostname)) { Program.LogPink("QR.ServerDeleted"); GameServer temp; Servers.TryRemove(key, out temp); }
            if (tits == true)
            {
                //23//bool vaginaworship = false;
                //23//if (!Servers.ContainsKey(key)) { vaginaworship = false; } else { vaginaworship = true; }
                

                
                    Servers.AddOrUpdate(key, server, (k, old) =>
                    {
                        if (!old.Valid && server.Valid)
                        {//if (old.Valid && server.Valid) {//WAS: if (!old.Valid && server.Valid) {
                            Log(Category, String.Format("Added new server at: {0}:{1} ({2}) ({3})", server.IPAddress, server.QueryPort, server.country, server.gamevariant));
                            
                        }
                        return server;
                    });

                    return false;
                //23//if (!vaginaworship) { Program.LogBlue("NOKEY"); return false; } else { Program.LogBlue("YESKEY"); return false; }//true; }

                
            }
            else return true;
            //return  true;// false;//true; commented out 23.09
		}

		private void AddValidServer(IPEndPoint remote)
		{
			string key = String.Format("{0}:{1}", remote.Address, remote.Port);
            Program.LogPink("Q&A.Server added.");
			GameServer server = new GameServer() {
				Valid = true,                    
				IPAddress = remote.Address.ToString(),
				QueryPort = remote.Port,
				LastRefreshed = DateTime.UtcNow,
				LastPing = DateTime.UtcNow
			};

			Servers.AddOrUpdate(key, server, (k, old) => {
				return server;
			});
		}
	}
}
