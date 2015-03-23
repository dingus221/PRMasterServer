using PRMasterServer.Data;
using PRMasterServer.Servers;
using System;
using System.Globalization;
using System.Net;
using System.Threading;
using System.Linq;
using System.Collections.Generic;

namespace PRMasterServer
{
    /// <summary>
    /// To run as a battlefield2 master server:
    /// PRMasterServer.exe +db logindb
    /// 
    /// To run as a (Civilization 4 Beyond the Sword) NAT Negotiation server:
    /// PRMasterServer.exe +game civ4bts +servers master,natneg
    /// 
    /// </summary>
	class Program
	{
        //public struct supportedgames { string gamename;}
        
        public static string gameName = null;


        public static string getGKey(string gname)
        {
            string[] gamelist = { "civ4", "civ4bts", "civ4btsjp" };
            string[] GKlist = { "y3D9Hw", "Cs2iIq", "Cs2iIq" };
            for (int i = 0; i < gamelist.Length; i++) {
                if (gname == gamelist[i]) {
                    return GKlist[i];
                }
            }
            return "UNKNOWN GAME";
        }

        public static bool isSupported(string gn) 
        { 
            string[] gamelist = { "civ4", "civ4bts", "civ4btsjp" };
            for (int i = 0; i < gamelist.Length; i++) {
                if (gamelist[i] == gn) return true;
            }
            return false; 
        }
		private static readonly object _lock = new object();

		static void Main(string[] args)
		{
			Action<string, string> log = (category, message) => {
				lock (_lock) {
					Log(String.Format("[{0}] {1}", category, message));
				}
			};

			Action<string, string> logError = (category, message) => {
				lock (_lock) {
					LogError(String.Format("[{0}] {1}", category, message));
				}
			};

            bool runLoginServer = true;
            bool runNatNegServer = true;
            bool runCdKeyServer = false;
            bool runMasterServer = true;
            bool runListServer = true;
            string gameName = null;

            IPAddress bind = IPAddress.Any;
            if (args.Length >= 1)
            {
                for (int i = 0; i < args.Length; i++)
                {
                    if (args[i].Equals("+bind"))
                    {
                        if ((i >= args.Length - 1) || !IPAddress.TryParse(args[i + 1], out bind))
                        {
                            LogError("+bind value must be a valid IP Address to bind to!");
                        }
                    }
                    else if (args[i].Equals("+db"))
                    {
                        if ((i >= args.Length - 1))
                        {
                            LogError("+db value must be a path to the database");
                        }
                        else
                        {
                            LoginDatabase.Initialize(args[i + 1], log, logError);
                        }
                    }
                    else if (args[i].Equals("+game"))
                    {
                        if ((i >= args.Length - 1))
                        {
                             //gameName = "civ4bts";
                             Log("supported games: civ4, civ4bts, civ4btsjp");
                        }
                        else
                        {
                            gameName = args[i + 1];
                        }
                    }
                    else if (args[i].Equals("+servers"))
                    {
                        if ((i >= args.Length - 1))
                        {
                            LogError("+servers value must be a comma-separated list of server types (master,login,cdkey,list,natneg)");
                        }
                        else
                        {
                            List<string> serverTypes = args[i + 1].Split(char.Parse(",")).Select(s => { return s.Trim().ToLower(); }).ToList();
                            runLoginServer = serverTypes.IndexOf("login") >= 0;
                            runNatNegServer = serverTypes.IndexOf("natneg") >= 0;
                            runListServer = serverTypes.IndexOf("list") >= 0;
                            runMasterServer = serverTypes.IndexOf("master") >= 0;
                            runCdKeyServer = serverTypes.IndexOf("cdkey") >= 0;
                        }
                    }
                }
            }

            if (runLoginServer && !LoginDatabase.IsInitialized())
            {
                LogError("Error initializing login database, please confirm parameter +db is valid");
                LogError("Press any key to continue");
                Console.ReadKey();
                return;
            }

            if (runCdKeyServer)
            {
                CDKeyServer serverCdKey = new CDKeyServer(bind, 29910, log, logError);
            }
            ServerListRetrieve serverListRetrieve = null;
            if (runMasterServer)
            {
                ServerListReport serverListReport = new ServerListReport(bind, 27900, log, logError, gameName);
                if (runListServer)
                {
                    serverListRetrieve = new ServerListRetrieve(bind, 28910, serverListReport, log, logError);
                }
            }
            ServerNatNeg serverNatNeg = null;
            if (runNatNegServer)
            {
                serverNatNeg = new ServerNatNeg(bind, 27901, log, logError);
            }
            if (runLoginServer)
            {
                LoginServer serverLogin = new LoginServer(bind, 29900, 29901, log, logError);
            }

			while (true) {
//*
                string command = Console.ReadLine();

                Log("Executing command: " + command);
                if (command == "/nndclear" && serverNatNeg != null)
                {
                    serverNatNeg.clientsClear();
                }
                else if (command == "/list" && serverListRetrieve != null)
                { 
                    serverListRetrieve.printSLinfo(); 
                }
                else if (command == "/quit")
                {
                    Log("Good bye");
                    serverListRetrieve.Dispose();

                    Environment.Exit(0);
                }
                else
                {
                    Log("Unknown command");
                }
 //*/
                /*
                ConsoleKeyInfo cki = Console.ReadKey(false);
                Console.Write("You pressed ");
                if ((cki.Modifiers & ConsoleModifiers.Alt) != 0) Console.Write("ALT+");
                if ((cki.Modifiers & ConsoleModifiers.Shift) != 0) Console.Write("SHIFT+");
                if ((cki.Modifiers & ConsoleModifiers.Control) != 0) Console.Write("CTL+");
                Console.WriteLine("{0} (character '{1}')", cki.Key, cki.KeyChar);
                */
				Thread.Sleep(1000);
			}
		}

		private static void Log(string message)
		{
			Console.WriteLine(String.Format("[{0}] {1}", DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss.fff", CultureInfo.InvariantCulture), message));
		}

		private static void LogError(string message)
		{
			ConsoleColor c = Console.ForegroundColor;
			Console.ForegroundColor = ConsoleColor.Red;
			Console.Error.WriteLine(String.Format("[{0}] {1}", DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss.fff", CultureInfo.InvariantCulture), message));
			Console.ForegroundColor = c;
		}
	}
}
