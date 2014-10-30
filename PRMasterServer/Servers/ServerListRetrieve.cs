using PRMasterServer.Data;
using Reality.Net.Extensions;
using Reality.Net.GameSpy.Servers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Dynamic;
using System.Net;
using System.Net.Sockets;
using System.Reflection;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;

namespace PRMasterServer.Servers
{
	internal class ServerListRetrieve
	{
		private const string Category = "ServerRetrieve";

		public Action<string, string> Log = (x, y) => { };
		public Action<string, string> LogError = (x, y) => { };

        public Thread Thread;
        

		private static Socket _socket;
		public static ServerListReport _report;//was private readonly slr 07.10

		private readonly ManualResetEvent _reset = new ManualResetEvent(false);
		private AsyncCallback _socketSendCallback;
		private AsyncCallback _socketDataReceivedCallback;


        static public int tmp1=0;
        static public Socket tmpS1;

        
            


        public static void DecodeShit()
        {
            byte[] buff1 = { 0x1b, 0x0d, 0x0e, 0x39, 0x62, 0x2c, 0x1a, 0x5b, 0x25, 0x2b, 0x0d, 0x08, 0x0b, 0x34, 0x15, 0x25, 0x7b, 0x15, 0x0f, 0x2a, 0x35, 0x23, 0x1d, 0x22, 0x20, 0x65, 0x18, 0x2e, 0x05, 0x31, 0x54, 0x0f, 0x16, 0x10, 0x5d, 0x25, 0x2b, 0x3d };
            byte[] buff2 = {0xee, 0x00, 0x00, 0xe7, 0xe9, 0x72, 0xcb, 0x7c, 0x6f, 0x3a, 0x17, 0x54, 0xe1, 0xab, 0x6f, 0xdc, 0x81, 0xb3, 0x86, 0x56, 0x4d, 0xd7, 0x0a, 0xc3, 0xbb, 0xea, 0xc1, 0xdc, 0x75, 0x95, 0xbc, 0x44, 0x87, 0x57, 0x02, 0xd4, 0xac, 0xd4, 0xb8, 
                            0x95, 0x43, 0x6c, 0xa7, 0x00, 0x3e, 0x84, 0xcf, 0x09, 0x5c, 0xb9, 0xfa, 0xc0, 0x8b, 0x20, 0x26, 0x69, 0xdf, 0x55, 0x50, 0xbf, 0x7e, 0x03, 0x9f, 0x3f, 0xad, 0xad, 0x32, 0x76, 0x07, 0xdb, 0xcc, 0xdc, 0xe3, 0x71, 0x7f, 0x9a, 0x0e, 0xd5, 
                            0x93, 0x96, 0x4a, 0xc7, 0xb9, 0xc8, 0x6b, 0xf0, 0x5a, 0x25, 0xb6, 0xfc, 0x8a, 0x9d, 0xec, 0x8d, 0x10, 0x9a, 0xc7, 0x43, 0xfc, 0x2b, 0xfa, 0xa4, 0x09, 0xa4, 0xf8, 0x7e, 0x4d, 0xe0, 0x2c, 0x61, 0xbc, 0x2a, 0xc4, 0xe8, 0x33, 0x91, 0x16, 
                            0xbe, 0x5d, 0x61, 0xc4, 0x86, 0xfe, 0xa5, 0xa9, 0x5c, 0x97, 0xa8, 0xd7, 0xfa, 0xc0, 0x93, 0xcb, 0xd1, 0x64, 0x3a, 0x15, 0x3e, 0x65, 0xb0, 0xc9, 0xf0, 0xfe, 0x2d, 0x63, 0xa7, 0x19, 0xbb, 0xf2, 0xdb, 0x7f, 0xba, 0xaf, 0x9a, 0xf3, 0x7b, 
                            0xb7, 0xc2, 0x92, 0xb3, 0xe6, 0x41, 0x7a, 0xb7, 0x42, 0x3d, 0x36, 0x85, 0x77, 0xdc, 0xaf, 0xd8, 0x26, 0x1c, 0x72, 0x5d, 0x24, 0x15, 0x32, 0x78, 0x3f, 0x85, 0xff, 0xab, 0xb4, 0xec, 0xcb, 0xba, 0x10, 0xfd, 0xd3, 0xf8, 0xd5, 0xa4, 0x15, 
                            0x7b, 0x44, 0x5b, 0x4e, 0x44, 0xa6, 0xb6, 0x2e, 0x07, 0x0d, 0xd7, 0x35, 0x22, 0x56, 0xc6, 0x26, 0x4f, 0x13, 0x70, 0x89, 0x0e, 0x44, 0x9d, 0xa2, 0xe4, 0x32, 0x2f, 0xae, 0x53, 0x5d, 0xfc, 0xa2, 0xca, 0xc5, 0x08, 0x33, 0xf4, 0xa8, 0xc6, 
                            0x4a, 0xe5, 0xc9, 0x03, 0xb8, 0xac, 0x60, 0xe3, 0xcf, 0x1d, 0x2f, 0xb1, 0xb5, 0x5a, 0x73, 0x9f, 0x08, 0x81, 0x83, 0xda, 0xd3, 0xd8, 0xbf, 0x82, 0x70, 0xb0, 0x9b, 0x50, 0x95, 0x80, 0x59, 0x37, 0x88, 0x53, 0x8d, 0xbb, 0xd3, 0xae, 0x5b, 
                            0xe6, 0xa2, 0xe8, 0x66, 0xde, 0x03, 0xa4, 0xcd, 0x40, 0x79, 0xab, 0x47, 0x68, 0x90, 0x62, 0xa1, 0x8c, 0x8a, 0x9c, 0xfe, 0xe6, 0x21, 0xef, 0xb4, 0xbe, 0xf8, 0x6d, 0x6a, 0x3c, 0x5c, 0xc7, 0xd6, 0xf8, 0xb6, 0x74, 0xb7, 0x2e, 0xee, 0xa1, 
                            0xae, 0x98, 0xcf, 0x61, 0x83, 0xfe, 0xeb, 0x91, 0x90, 0x61, 0xa1, 0xd4, 0xad, 0x4b, 0x1b, 0x9a, 0x0a, 0xe4, 0xc6, 0x80, 0x86, 0x17, 0xed, 0x46, 0x06, 0xba, 0x55, 0xfe, 0x9c, 0x6d, 0x40, 0x19, 0x30, 0x8b, 0x16, 0x50, 0x5d, 0x0e, 0x8f, 
                            0xbe, 0x1b, 0xba, 0x94, 0xe4, 0x49, 0x66, 0x8e, 0x53, 0x43, 0xd9, 0x9c, 0x82, 0x75, 0x66, 0x0c, 0x3a, 0x23, 0xb5, 0x8c, 0xd4, 0xaf, 0xca, 0x5d, 0x15, 0x4d, 0xf5, 0xba, 0xe3, 0x12, 0x73, 0x51, 0x01, 0xa0, 0xd5, 0xd0, 0x14, 0xb8, 0x27, 
                            0x17, 0xff,0x16,0x0c,0xfc,0x64,0xba,0x9e,0x11,0xf1,0xf8,0x18,0xcd,0x67,0xe7,0x50,0x77,0xd1,0xc3,0x5a,0x81,0x67,0x14,0xdf,0x56,0xd0,0x6c,0xa6,0x67,0xe0,0x71,0x8e,0xa3,0xca,0xb6,0x5a,0xae,0x28,0x26,0xdf,0x8c,0x2f,0xa9,0xcb,0x3b,0x7b,0xcc,0xbb,0x0f,0x19,0xa7,0xe3,0xc1,0x8c,0x13,0x76,0x9b,0x45,0xbe,0x84,0xd8,0x00,0xf9,0x38,0x25,0x31,0x51,0xa3,0x8b,0x83,0x27,0x06,0x6a,0x6b,0x06,0xee,0x29,0x87,0x54,0x0e,0xb7,0x30,0x2b,0x1e,0xc5,0x97,0xc0,0xd6,0x55,0x29,0x4e,0x25,0x31,0xac,0x15,0x88,0x57,0x86,0x66,0x68,0xbf,0xcb,0xb8,0xbd,0x65,0x1e,0xec,0xda,0x02,0x0c,0x94,0xf5,0x14,0x50,0x28,0x70,0x60,0x67,0xa0,0x7f,0xd9,0xf4,0x90,0xeb,0x42,0xcd,0xe5,0x63,0xac,0x32,0x4d,0x02,0xa3,0x01,0xc2,0xa2,0x13,0x83,0x77,0xf8,0x8e,0xdc,0xc4,0x9e,0xfd,0x34,0x1c,0xb3,0x4c,0x7e,0xc7,0x01,0xea,0x1b,0xeb,0x8b,0xdb,0xae,0x63,0x42,0x06,0x5d,0x07,0x26,0x8a,0xc7,0xf8,0x8c,0xea,0x9c,0x1f,0xdd,0xcf,0x5d,0xdb,0xb6,0x79,0x98,0xee,0xa4,0x4a,0x40,0x5e,0x2b,0x6c,0x3b,0x04,0x2f,0xf0,0x2b,0x18,0xf8,0xa8,0xae,0x5b,0x7d,0x5c,0x01,0x67,0x5a,0x34,0xbd,0x7a,0x23,0x95,0x6e,0x14,0xe2,0xae,0xa1,0xbd,0x3a,0x9d,0x9b,0x1e,0x72,0xdf,0x1c,0xa2,0x59,0x67,0xf6,0x89,0x39,0x86,0x2a,0xc8,0x80,0x35,0xfb,0x7e,0x92,0x22,0x85,0x3e,0x58,0xbd,0xd5,0x26,0x26,0xeb,0x0e,0x39,0x50,0xca,0x7f,0x09,0xb5,0x98,0x0a,0x40,0x44,0x9f,0xaf,0xbc,0x79,0x78,0x89,0x2f,0x33,0x1f,0xe9,0x2c,0x4d,0xa5,0xcc,0x5f,0xb4,0x59,0xfc,0x78,0xcb,0xc5,0xc4,0x1f,0xd4,0xcd,0x5a,0x04,0xc3,0x9a,0x31,0xcf,0x5a,0x41,0xb6,0x24,0x46,0xd0,0xdf,0x10,0x73,0xdc,0x75,0x87,0x0d,0x64,0xe0,0xa8,0xf2,0xd1,0x3e,0x6c,0xa1,0x90,0x5f,0x34,0xd3,0x15,0x60,0xaf,0x3a,0x8b,0xd2,0x8c,0xf6,0xe6,0x4e,0x52,0xdc,0x82,0x29,0x73,0x0b,0xca,0x10,0xfc,0x31,0x08,0xb0,0x03,0xa9,0xc9,0xc3,0x62,0x80,0xb9,0x12,0xe1,0xea,0x7c,0xe7,0x1e,0x1c,0xd1,0x05,0x20,0xdf,0x67,0xa1,0x20,0x45,0x73,0x27,0xc1,0x72,0x67,0x7e,0xfe,0x21,0x72,0x26,0x39,0xe9,0x51,0xfa,0xc3,0x81,0xd0,0x87,0x80,0x49,0xe9,0xce,0xb8,0x32,0xb7,0xcc,0x2b };
            byte[] buff3 = {0xeb,0x00,0x00,0xc8,0x60,0x80,0x03,0x77,0xe4,0x4a,0x2f,0xf8,0x22,0xaa,0xea,0xf5,0xec,0x0a,0x2d,0x82,0xab,0xc8,0x19,0x2d,0xa5,0x5d,0xaa,0x92,0x22,0x0c,0xc4,0xff,0x5e,0x48,0x62,0x77,0x5d,0x14,0x08,0xf3,0x40,0x25,0xe6,0x34,0x0d,0xe5,0x48,0xc8,0x39,0x2e,0x51,0x69,0x69,0x52,0xb7,0xbe,0xd5,0x60,0x2b,0x7a,0x2a,0x82,0x26,0x54,0xb8,0xcd,0x96,0x6f,0x39,0x10,0x04,0x25,0x41,0x1c,0x50,0xa8,0x3d,0x40,0x27,0x28,0x1a,0xf8,0x05,0x36,0x8f,0x50,0xec,0x68,0xe3,0xec,0x7d,0x43,0xdd,0x95,0x7e,0x91,0x2e,0x6a,0x87,0x18,0x7c,0x8f,0x07,0x9e,0x42,0x72,0xaf,0x19,0x3a,0x83,0xec,0x55,0x22,0x72,0xe0,0xa7,0xa9,0xd3,0xab,0x8e,0x54,0x45,0xda,0x1c,0x3e,0x68,0xaf,0x74,0x26,0x86,0xce,0xdb,0xe6,0x24,0x87,0x08,0x94,0x72,0x9e,0x79,0x21,0x5b,0x66,0x02,0x52,0x2e,0x6f,0xd4,0xda,0x7a,0x9d,0x80,0xb0,0xd3,0xbb,0x23,0x79,0xd2,0x1c,0x7b,0xbc,0xc7,0x94,0xfa,0xbc,0xdc,0xeb,0x5e,0x6b,0x5e,0x20,0x70,0x67,0xeb,0x2d,0x06,0xea,0x90,0x8f,0xd3,0x20,0xc4,0xcc,0x76,0x1b,0x11,0xdd,0x50,0x66,0x4c,0xee,0x58,0xc2,0x4b,0x96,0x62,0xed,0xd8,0x90,0x4e,0x00,0xfd,0xd3,0xab,0x98,0xaa,0xe5,0xca,0x73,0xe6,0x7a,0x65,0x33,0x5c,0xdf,0x8d,0x5e,0xda,0xfc,0xc6,0x5e,0x39,0x6b,0xf8,0xc6,0x10,0x33,0x7d,0x1f,0x85,0x82,0x62,0x3e,0xc1,0xc6,0x7a,0xdb,0x58,0x19,0x1b,0x90,0xf2,0xf1,0xd1,0xfa,0xb0,0x54,0x62,0x40,0xe2,0x1b,0x4e,0x97,0x63,0x1d,0x22,0x81,0xb2,0x6b,0x9e,0xe3,0xe5,0x01};

            string gkey1 = "Cs2iIq";//"h3D7Lc";
            string validate = "EX4D=vn=";// "gI\"E\\mI5";
            string gname1 = "lotrbme";
            Program.LogControl("Decoding.CP1..."+gkey1+validate);
            Console.WriteLine(" ");
            byte[] bytesGKEY = new byte[gkey1.Length * sizeof(char)];
            System.Buffer.BlockCopy(gkey1.ToCharArray(), 0, bytesGKEY, 0, bytesGKEY.Length);
            byte[] bytesVAL = new byte[validate.Length * sizeof(char)];
            System.Buffer.BlockCopy(validate.ToCharArray(), 0, bytesVAL, 0, bytesVAL.Length);

            byte[] decodedbuff1 = GSEncoding.Decode(bytesGKEY, bytesVAL,  buff3, buff3.Length);
            Program.LogControl("Decoding.CP2...");
            Program.LogBlue(System.Text.Encoding.UTF8.GetString(decodedbuff1));
        }

        public static void SendToAllConnected(string validateX)
        {

            //byte[] key = DataFunctions.StringToBytes(Program.getGKey(Program.gameName));
            //Program.LogBlue(Encoding.ASCII.GetString(key));
            //Program.LogBlue(tmpS1.Connected.ToString());
            //byte[] resp13 = GSEncoding.Encode(key, DataFunctions.StringToBytes(validateX), resp11, resp11.LongLength);
            //Program.LogBlue(Encoding.ASCII.GetString(resp13));
            //tmpS1.Send(resp13);
           
            // ParseRequest.
            
        }

       
        public static void printSLinfo() {
        IQueryable<GameServer> servers = _report.Servers.ToList().Select(x => x.Value).Where(x => x.Valid).AsQueryable();
        int zz = 0;
            foreach (var server in servers) {
                zz = zz + 1;
        Program.LogControl(zz.ToString() + "." + server.hostname + "(" + server.mynumplayers + "/" + server.maxnumplayers + ");"+"Staging:"+server.staging.ToString());
        }
        Program.LogControl("SL.Count: " + servers.Count().ToString()); 
           
        
        }

		public ServerListRetrieve(IPAddress listen, ushort port, ServerListReport report, Action<string, string> log, Action<string, string> logError)
		{
			Log = log;
			LogError = logError;
            
            //logError("public","serverlistretrieve");
			_report = report;
			//*
			/*_report.Servers.TryAdd("test", 
				new GameServer() {
					Valid = true,
                          
             newgame=false,
            staging=false,
            mynumplayers=61,
            maxnumplayers=139,
            nummissing=78,
            pitboss=false,
					IPAddress = "192.168.1.2",
					QueryPort = 29300,
					country = "AU",
					hostname = "Teamer 35vs49",
					gamename = "civ4",
					gamever = "3.19",
					mapname = "Awesome Map",
					gametype = "gpm_cq",
					gamevariant = "pr",
					numplayers = 61,
					maxplayers = 183,
					gamemode = "openplaying",
					password = false,
					timelimit = 14400,
					roundtime = 1,
					hostport = 16567}
                / *    ,
					bf2_dedicated = true,
					bf2_ranked = true,
					bf2_anticheat = false,
					bf2_os = "win32",
					bf2_autorec = true,
					bf2_d_idx = "http://",
					bf2_d_dl = "http://",
					bf2_voip = true,
					bf2_autobalanced = false,
					bf2_friendlyfire = true,
					bf2_tkmode = "No Punish",
					bf2_startdelay = 240.0,
					bf2_spawntime = 300.0,
					bf2_sponsortext = "Welcome to an awesome server!",
					bf2_sponsorlogo_url = "http://",
					bf2_communitylogo_url = "http://",
					bf2_scorelimit = 100,
					bf2_ticketratio = 100.0,
					bf2_teamratio = 100.0,
					bf2_team1 = "US",
					bf2_team2 = "MEC",
					bf2_bots = false,
					bf2_pure = false,
					bf2_mapsize = 64,
					bf2_globalunlocks = true,
					bf2_fps = 35.0,
					bf2_plasma = true,
					bf2_reservedslots = 16,
					bf2_coopbotratio = 0,
					bf2_coopbotcount = 0,
					bf2_coopbotdiff = 0,
					bf2_novehicles = false* /
				
			);*/

			IQueryable<GameServer> servers = _report.Servers.Select(x => x.Value).AsQueryable();
            //Console.WriteLine(servers.Where("gamever = '3.19' and gamevariant = 'pr' and hostname like '%[[]PR v1.2.0.0% %' and hostname like '%2%'").Count());
		//	*/

			Thread = new Thread(StartServer) {
				Name = "Server Retrieving Socket Thread"
			};
			Thread.Start(new AddressInfo() {
				Address = listen,
				Port = port
			});
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

		~ServerListRetrieve()
		{
			Dispose(false);
		}

		private void StartServer(object parameter)
		{
			AddressInfo info = (AddressInfo)parameter;
            
			Program.LogCyan(Category +":Starting Server List Retrieval");

			try {
				_socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp) {
					SendTimeout = 5000,
					ReceiveTimeout = 5000,
					SendBufferSize = 65535,
					ReceiveBufferSize = 65535
				};
				_socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ExclusiveAddressUse, true);
				_socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.DontLinger, true);

				_socket.Bind(new IPEndPoint(info.Address, info.Port));
				_socket.Listen(10);
			} catch (Exception e) {
				LogError(Category, String.Format("Unable to bind Server List Retrieval to {0}:{1}", info.Address, info.Port));
				LogError(Category, e.ToString());
				return;
			}

			while (true) {
				_reset.Reset();
				_socket.BeginAccept(AcceptCallback, _socket);
				_reset.WaitOne();
			}
		}

		private void AcceptCallback(IAsyncResult ar)
		{
			_reset.Set();

			Socket listener = (Socket)ar.AsyncState;
			Socket handler = listener.EndAccept(ar);
            tmp1=tmp1+1;
            if (tmp1==1){
                tmpS1 = handler;
                //handler.AddressFamily.
                //TmpS1. handler;
                //AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp)
            }
			SocketState state = new SocketState() {
				Socket = handler
			};
            //Program.LogCyan("SB.AcceptCallBack");
			WaitForData(state);
            
		}

		private void WaitForData(SocketState state)
		{
			Thread.Sleep(10);
			if (state == null || state.Socket == null || !state.Socket.Connected)
				return;

            
           try {
				if (_socketDataReceivedCallback == null)
					_socketDataReceivedCallback = OnDataReceived;

				state.Socket.BeginReceive(state.Buffer, 0, state.Buffer.Length, SocketFlags.None, _socketDataReceivedCallback, state);
			} catch (ObjectDisposedException) {
				state.Socket = null;
			} catch (SocketException e) {
				if (e.SocketErrorCode == SocketError.NotConnected)
					return;

				LogError(Category, "Error receiving data");
				LogError(Category, String.Format("{0} {1}", e.SocketErrorCode, e));
				return;
			}
		}

		private void OnDataReceived(IAsyncResult async)
		{
			SocketState state = (SocketState)async.AsyncState;
            
			if (state == null || state.Socket == null || !state.Socket.Connected)
				return;

			try {
				// receive data from the socket
				int received = state.Socket.EndReceive(async);
				if (received == 0) {
					// when EndReceive returns 0, it means the socket on the other end has been shut down.
					return;
				}

				// take what we received, and append it to the received data buffer
				state.ReceivedData.Append(Encoding.UTF8.GetString(state.Buffer, 0, received));
				string receivedData = state.ReceivedData.ToString();
                Program.LogCyan("SB.OnDataReceived:"+ receivedData);


				// does what we received end with \x00\x00\x00\x00\x??
				if (receivedData.Substring(receivedData.Length - 5, 4) == "\x00\x00\x00\x00") {
					state.ReceivedData.Clear();

					// lets split up the message based on the delimiter
					string[] messages = receivedData.Split(new string[] { "\x00\x00\x00\x00" }, StringSplitOptions.RemoveEmptyEntries);
                    //LogError(messages[1], messages[2]);
                    //LogError(messages[3], messages[4]);
					for (int i = 0; i < messages.Length; i++) {
						/*if (messages[i].StartsWith(Program.gameName/*"civ4"/*battlefield2)) COMMENTED OUT 07.10*/{
							if (ParseRequest(state, messages[i]))
								return;
						}
					}
				}
			} catch (ObjectDisposedException) {
				if (state != null)
					state.Dispose();
				state = null;
				return;
			} catch (SocketException e) {
				switch (e.SocketErrorCode) {
					case SocketError.ConnectionReset:
						if (state != null)
							state.Dispose();
						state = null;
						return;
					case SocketError.Disconnecting:
						if (state != null)
							state.Dispose();
						state = null;
						return;
					default:
						LogError(Category, "Error receiving data");
						LogError(Category, String.Format("{0} {1}", e.SocketErrorCode, e));
						if (state != null)
							state.Dispose();
						state = null;
						return;
				}
			} catch (Exception e) {
				LogError(Category, "Error receiving data");
				LogError(Category, e.ToString());
			}

			// and we wait for more data...
			WaitForData(state);
		}

		public void SendToClient(SocketState state, byte[] data)
		{
            Program.LogCyan("SB.SendToClient");
			if (state == null)
				return;

			if (state.Socket == null || !state.Socket.Connected) {
				state.Dispose();
				state = null;
				return;
			}

			if (_socketSendCallback == null)
				_socketSendCallback = OnSent;

			try {
                
				state.Socket.BeginSend(data, 0, data.Length, SocketFlags.None, _socketSendCallback, state);
			} catch (SocketException e) {
				LogError(Category, "Error sending data");
				LogError(Category, String.Format("{0} {1}", e.SocketErrorCode, e));
			}
		}
    
		private void OnSent(IAsyncResult async)
		{
			SocketState state = (SocketState)async.AsyncState;
            //LogError("pfpfpf","is sent");
			if (state == null || state.Socket == null)
				return;

			try {
				int sent = state.Socket.EndSend(async);
                Log(Category, String.Format("Sent {0} byte response to: {1}:{2}", sent, ((IPEndPoint)state.Socket.RemoteEndPoint).Address, ((IPEndPoint)state.Socket.RemoteEndPoint).Port));
			} catch (SocketException e) {
				switch (e.SocketErrorCode) {
					case SocketError.ConnectionReset:
					case SocketError.Disconnecting:
						return;
					default:
						LogError(Category, "Error sending data");
						LogError(Category, String.Format("{0} {1}", e.SocketErrorCode, e));
						return;
				}
			} finally {
				state.Dispose();
				state = null;
			}
		}

		public bool ParseRequest(SocketState state, string message)
		{
            /////////////////Ahtung
            Program.LogCyan("SB.Parserequest." + message);
			string[] data = message.Split(new char[] { '\x00' }, StringSplitOptions.RemoveEmptyEntries);
           if (data.Length != 4 || /*                COMOUT 07.10
               */ (!data[0].Equals("civ4bts"/*Program.gameName/*"civ4"/*battlefield2*/, StringComparison.InvariantCultureIgnoreCase) && !data[0].Equals("civ4btsjp", StringComparison.InvariantCultureIgnoreCase)         && !data[0].Equals("civ4", StringComparison.InvariantCultureIgnoreCase)             ) ||//*/   
		  	(

                  /*COMOUT 07.10 */ (!data[1].Equals("civ4bts"/*Program.gameName/*"civ4"/*battlefield2*/, StringComparison.InvariantCultureIgnoreCase) && !data[1].Equals("civ4btsjp", StringComparison.InvariantCultureIgnoreCase) && !data[1].Equals("civ4", StringComparison.InvariantCultureIgnoreCase) && !data[1].Equals("gmtest", StringComparison.InvariantCultureIgnoreCase)) &&
					!data[1].Equals("gslive", StringComparison.InvariantCultureIgnoreCase)       
				)
			) {
                Program.LogCyan("SB.CHECKPOINT X.");
				return false;
			}

			string gamename = data[1].ToLowerInvariant();
            //if (gamename == "gmtest") { gamename = "civ4bts"; }
			string validate = data[2].Substring(0, 8);
            Program.LogCyan("SB.validate cp:"+validate);
            string filter = "numplayers>-1";//Temporarily so that it shows all games //"gamemode=\"openstaging\"";//FixFilter(data[2].Substring(8));
            Program.LogCyan("filtar:" + '(' + filter + ')');
			string[] fields = data[3].Split(new char[] { '\\' }, StringSplitOptions.RemoveEmptyEntries);

			Log(Category, String.Format("Received client request: {0}:{1}", ((IPEndPoint)state.Socket.RemoteEndPoint).Address, ((IPEndPoint)state.Socket.RemoteEndPoint).Port));

            IQueryable<GameServer> servers = _report.Servers.ToList().Select(x => x.Value).Where(x => x.Valid).AsQueryable();
			if (!String.IsNullOrWhiteSpace(filter)) {
				try {
					//Console.WriteLine(filter);
					servers = servers.Where(filter);
                    //Console.ForegroundColor = ConsoleColor.DarkCyan;
                    //Console.WriteLine(servers.Where(filter));
                    //Console.ForegroundColor = ConsoleColor.Gray;
				} catch (Exception e) {
					LogError(Category, "Error parsing filter");
					LogError(Category, filter);
					LogError(Category, e.ToString());
				}
			}

			// http://aluigi.altervista.org/papers/gslist.cfg
			byte[] key;
            //if (gamename == Program.gameName)     COMOUT 07.10
            {/*"civ4")/*battlefield2*/
                //Program.LogCyan("GKey:" + Program.getGKey(gamename));
                key = DataFunctions.StringToBytes(Program.getGKey(gamename));
            }//("y3D9Hw"/*"Cs2iIq"/*hW6m9a*/);
           /* else if (gamename == "arma2oapc")
                key = DataFunctions.StringToBytes("sGKWik");
            else
                key = DataFunctions.StringToBytes("Xn221z");
			*/
			byte[] unencryptedServerList = PackServerList(state, servers, fields);


            
			byte[] encryptedServerList = GSEncoding.Encode(key, DataFunctions.StringToBytes(validate), unencryptedServerList, unencryptedServerList.LongLength);

            //Program.LogCyan("SB.UnencSL. "+System.Text.Encoding.ASCII.GetString(unencryptedServerList));
            if (encryptedServerList.Count() < 1) { Program.LogCyan("SB.CheckPoint44.EncrSList is empty."); }


            //ADDING /final/ to encryptedserverlist bytes
          /* byte[] bytes1 = {92,102,105,110,97,108,92};
            

            byte[] c = new byte[encryptedServerList.Length + bytes1.Length];
            encryptedServerList.CopyTo(c, 0);
            bytes1.CopyTo(c, encryptedServerList.Length);

            Program.LogBlue(System.Text.Encoding.Default.GetString(c));
                
            SendToClient(state, c);*/
            SendToClient(state, encryptedServerList);
            //state.Socket.Disconnect(false);
            Program.LogCyan("SB.SL sent.");
            //SendToClient(state, unencryptedServerList);
            
			return true;
		}

		private static byte[] PackServerList(SocketState state, IEnumerable<GameServer> servers, string[] fields)
		{
			IPEndPoint remoteEndPoint = ((IPEndPoint)state.Socket.RemoteEndPoint);
            Program.LogCyan("SB.PackSL.");
			byte[] ipBytes = remoteEndPoint.Address.GetAddressBytes();
            byte[] value2 = BitConverter.GetBytes((ushort)remoteEndPoint.Port);//was 6500//changed 24.10
			byte fieldsCount = (byte)(fields.Length);

			List<byte> data = new List<byte>();
			data.AddRange(ipBytes);
            data.AddRange(BitConverter.IsLittleEndian ? value2.Reverse() : value2);
			data.Add(fieldsCount);
			data.Add(0);
            //Console.WriteLine("Packlist, checkpoint 1, fields count:");
            foreach (var field in fields) {
				data.AddRange(DataFunctions.StringToBytes(field));
				data.AddRange(new byte[] { 0, 0 });
			}
            

            //Console.WriteLine("Packlist, checkpoint 2");
			foreach (var server in servers) {
				// commented this stuff out since it caused some issues on testing, might come back to it later and see what's happening...
				// NAT traversal stuff...
				// 126 (\x7E)	= public ip / public port / private ip / private port / icmp ip
				// 115 (\x73)	= public ip / public port / private ip / private port
				// 85 (\x55)	= public ip / public port
				// 81 (\x51)	= public ip / public port
                //WAS COMMENTED OUT
                //30.09
                /*Console.WriteLine(server.IPAddress);
                Console.WriteLine(server.QueryPort);
                Console.WriteLine(server.localip0);
                Console.WriteLine(server.localip1);
                Console.WriteLine(server.localport);
                Console.WriteLine(server.natneg);/*
                if (!String.IsNullOrWhiteSpace(server.localip0) && !String.IsNullOrWhiteSpace(server.localip1) && server.localport > 0) {
                    data.Add(126);
                    data.AddRange(IPAddress.Parse(server.IPAddress).GetAddressBytes());
                    data.AddRange(BitConverter.IsLittleEndian ? BitConverter.GetBytes((ushort)server.QueryPort).Reverse() : BitConverter.GetBytes((ushort)server.QueryPort));
                    data.AddRange(IPAddress.Parse(server.localip0).GetAddressBytes());
                    data.AddRange(BitConverter.IsLittleEndian ? BitConverter.GetBytes((ushort)server.localport).Reverse() : BitConverter.GetBytes((ushort)server.localport));
                    data.AddRange(IPAddress.Parse(server.localip1).GetAddressBytes());
                }
                else if (!String.IsNullOrWhiteSpace(server.localip0) && server.localport > 0)
                {
                    data.Add(115);
                    data.AddRange(IPAddress.Parse(server.IPAddress).GetAddressBytes());
                    data.AddRange(BitConverter.IsLittleEndian ? BitConverter.GetBytes((ushort)server.QueryPort).Reverse() : BitConverter.GetBytes((ushort)server.QueryPort));
                    data.AddRange(IPAddress.Parse(server.localip0).GetAddressBytes());
                    data.AddRange(BitConverter.IsLittleEndian ? BitConverter.GetBytes((ushort)server.localport).Reverse() : BitConverter.GetBytes((ushort)server.localport));
                }
                else
                {//*/
                    data.Add(81); //WAS 81//it could be 85 as well, unsure of the difference, but 81 seems more common...
                    data.AddRange(IPAddress.Parse(server.IPAddress).GetAddressBytes());
                    data.AddRange(BitConverter.IsLittleEndian ? BitConverter.GetBytes((ushort)server.QueryPort).Reverse() : BitConverter.GetBytes((ushort)server.QueryPort));
                
                    //**/ }

                    data.Add(255);
                //Console.WriteLine("Packlist, checkpoint 3");
				for (int i = 0; i < fields.Length; i++) {
                    //Console.WriteLine(fields[i]);
                    
					data.AddRange(DataFunctions.StringToBytes(GetField(server, fields[i])));

					if (i < fields.Length - 1)
						data.AddRange(new byte[] { 0, 255 });
				}

                
				data.Add(0);
			}



            data.AddRange(new byte[] { 0, 255, 255, 255, 255 });

            //Program.LogCyan("SB.ListCount:"+data.Count.ToString());
            /*byte[] bong = data.ToArray();
            
                for (int i = 0; i < bong.Count(); i++)
                {
                    //Console.Write(bong[i] + ",");
                }
                Console.WriteLine("end");
                Console.WriteLine("end");
                Console.WriteLine("end");
                Console.WriteLine("end");
                Console.WriteLine("end");
                Console.WriteLine("end");
                Console.WriteLine("end");
                Console.WriteLine("end");
                Console.WriteLine("end");
                Console.WriteLine("end");
                Console.WriteLine("end");
                Console.WriteLine("end");
                Console.WriteLine("end");
                Console.WriteLine("end");
                Console.WriteLine("end");
               // Program.LogCyan(color.ToString());
             
            //}
            Program.LogCyan( System.Text.Encoding.ASCII.GetString(bong));
         */   


			return data.ToArray();
		}

		private static string GetField(GameServer server, string fieldName)
        {
            
                object value = server.GetType().GetProperty(fieldName).GetValue(server, null);
           
                if (value == null)
				return String.Empty;
			else if (value is Boolean)
				return (bool)value ? "1" : "0";
			else
				return value.ToString();
		}

		private string FixFilter(string filter)
		{
			// escape [
			filter = filter.Replace("[", "[[]");

			// fix an issue in the BF2 main menu where filter expressions aren't joined properly
			// i.e. "numplayers > 0gametype like '%gpm_cq%'"
			// becomes "numplayers > 0 && gametype like '%gpm_cq%'"
			try {
				filter = FixFilterOperators(filter);
			} catch (Exception e) {
				LogError(Category, e.ToString());
			}

			// fix quotes inside quotes
			// i.e. hostname like 'flyin' high'
			// becomes hostname like 'flyin_ high'
			try {
				filter = FixFilterQuotes(filter);
			} catch (Exception e) {
				LogError(Category, e.ToString());
			}

			// fix consecutive whitespace
			filter = Regex.Replace(filter, @"\s+", " ").Trim();

			return filter;
		}

		private static string FixFilterOperators(string filter)
		{
			PropertyInfo[] properties = typeof(GameServer).GetProperties();
			List<string> filterableProperties = new List<string>();

			// get all the properties that aren't "[NonFilter]"
			foreach (var property in properties) {
				if (property.GetCustomAttributes(false).Any(x => x.GetType().Name == "NonFilterAttribute"))
					continue;

				filterableProperties.Add(property.Name);
			}

			// go through each property, see if they exist in the filter,
			// and check to see if what's before the property is a logical operator
			// if it is not, then we slap a && before it
			foreach (var property in filterableProperties) {
				IEnumerable<int> indexes = filter.IndexesOf(property);
				foreach (var index in indexes) {
					if (index > 0) {
						int length = 0;
						bool hasLogical = IsLogical(filter, index, out length, true) || IsOperator(filter, index, out length, true) || IsGroup(filter, index, out length, true);
						if (!hasLogical) {
							filter = filter.Insert(index, " && ");
						}
					}
				}
			}
			return filter;
		}

		private static string FixFilterQuotes(string filter)
		{
			StringBuilder newFilter = new StringBuilder(filter);

			for (int i = 0; i < filter.Length; i++) {
				int length = 0;
				bool isOperator = IsOperator(filter, i, out length);

				if (isOperator) {
					i += length;
					bool isInsideString = false;
					for (; i < filter.Length; i++) {
						if (filter[i] == '\'' || filter[i] == '"') {
							if (isInsideString) {
								// check what's after the quote to see if we terminate the string
								if (i >= filter.Length - 1) {
									// end of string
									isInsideString = false;
									break;
								}
								for (int j = i + 1; j < filter.Length; j++) {
									// continue along whitespace
									if (filter[j] == ' ') {
										continue;
									} else {
										// if it's a logical operator, then we terminate
										bool op = IsLogical(filter, j, out length);
										if (op) {
											isInsideString = false;
											j += length;
											i = j;
										}
										break;
									}
								}
								if (isInsideString) {
									// and if we're still inside the string, replace the quote with a wildcard character
									newFilter[i] = '_';
								}
								continue;
							} else {
								isInsideString = true;
							}
						}
					}
				}
			}

			return newFilter.ToString();
		}

		private static bool IsOperator(string filter, int i, out int length, bool previous = false)
		{
			bool isOperator = false;
			length = 0;

			if (i < filter.Length - 1) {
				string op = filter.Substring(i - (i >= 2 ? (previous ? 2 : 0) : 0), 1);
				if (op == "=" || op == "<" || op == ">") {
					isOperator = true;
					length = 1;
				}
			}

			if (!isOperator) {
				if (i < filter.Length - 2) {
					string op = filter.Substring(i - (i >= 3 ? (previous ? 3 : 0) : 0), 2);
					if (op == "==" || op == "!=" || op == "<>" || op == "<=" || op == ">=") {
						isOperator = true;
						length = 2;
					}
				}
			}

			if (!isOperator) {
				if (i < filter.Length - 4) {
					string op = filter.Substring(i - (i >= 5 ? (previous ? 5 : 0) : 0), 4);
					if (op.Equals("like", StringComparison.InvariantCultureIgnoreCase)) {
						isOperator = true;
						length = 4;
					}
				}
			}

			if (!isOperator) {
				if (i < filter.Length - 8) {
					string op = filter.Substring(i - (i >= 9 ? (previous ? 9 : 0) : 0), 8);
					if (op.Equals("not like", StringComparison.InvariantCultureIgnoreCase)) {
						isOperator = true;
						length = 8;
					}
				}
			}

			return isOperator;
		}

		private static bool IsLogical(string filter, int i, out int length, bool previous = false)
		{
			bool isLogical = false;
			length = 0;

			if (i < filter.Length - 2) {
				string op = filter.Substring(i - (i >= 3 ? (previous ? 3 : 0) : 0), 2);
				if (op == "&&" || op == "||" || op.Equals("or", StringComparison.InvariantCultureIgnoreCase)) {
					isLogical = true;
					length = 2;
				}
			}

			if (!isLogical) {
				if (i < filter.Length - 3) {
					string op = filter.Substring(i - (i >= 4 ? (previous ? 4 : 0) : 0), 3);
					if (op.Equals("and", StringComparison.InvariantCultureIgnoreCase)) {
						isLogical = true;
						length = 3;
					}
				}
			}

			return isLogical;
		}

		private static bool IsGroup(string filter, int i, out int length, bool previous = false)
		{
			bool isGroup = false;
			length = 0;

			if (i < filter.Length - 1) {
				string op = filter.Substring(i - (i >= 2 ? (previous ? 2 : 0) : 0), 1);
				if (op == "(" || op == ")") {
					isGroup = true;
					length = 1;
				}
				if (!isGroup && previous) {
					op = filter.Substring(i - (i >= 1 ? (previous ? 1 : 0) : 0), 1);
					if (op == "(" || op == ")") {
						isGroup = true;
						length = 1;
					}
				}
			}

			return isGroup;
		}

		public class SocketState : IDisposable
		{
			public Socket Socket = null;
			public byte[] Buffer = new byte[8192];
			public StringBuilder ReceivedData = new StringBuilder(8192);

			public void Dispose()
			{
				Dispose(true);
				GC.SuppressFinalize(this);
			}

			protected virtual void Dispose(bool disposing)
			{
				try {
					if (disposing) {
						if (Socket != null) {
							try {
								Socket.Shutdown(SocketShutdown.Both);
							} catch (Exception) {
							}
							Socket.Close();
							Socket.Dispose();
							Socket = null; //29.09
						}
					}

					GC.Collect();
				} catch (Exception) {
				}
			}

			~SocketState()
			{
				Dispose(false);
			}
		}
	}
}
