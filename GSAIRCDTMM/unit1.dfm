object Form1: TForm1
  Left = 390
  Top = 121
  Width = 622
  Height = 583
  Caption = 'GS adapted IRC Daemon "The Most Moist"'
  Color = clBlack
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  OldCreateOrder = False
  OnClose = FormClose
  OnCreate = FormCreate
  OnKeyDown = FormKeyDown
  OnShow = FormShow
  PixelsPerInch = 96
  TextHeight = 13
  object Memo1: TMemo
    Left = 0
    Top = 20
    Width = 606
    Height = 493
    Align = alClient
    BorderStyle = bsNone
    Color = clBlack
    Font.Charset = RUSSIAN_CHARSET
    Font.Color = clWhite
    Font.Height = -11
    Font.Name = 'Fixedsys'
    Font.Style = []
    ParentFont = False
    ScrollBars = ssVertical
    TabOrder = 0
    OnKeyDown = Memo1KeyDown
  end
  object Com: TEdit
    Left = 608
    Top = 304
    Width = 137
    Height = 21
    TabOrder = 1
    Visible = False
  end
  object Button3: TButton
    Left = 640
    Top = 336
    Width = 105
    Height = 25
    Caption = 'send from clientsocket'
    TabOrder = 2
    Visible = False
    OnClick = Button3Click
  end
  object Button4: TButton
    Left = 712
    Top = 368
    Width = 41
    Height = 25
    Caption = 'connect with clsocket'
    TabOrder = 3
    Visible = False
    OnClick = Button466Click
  end
  object Panel1: TPanel
    Left = 480
    Top = 40
    Width = 57
    Height = 17
    Caption = 'enc/dec'
    TabOrder = 4
    Visible = False
    OnClick = Panel1Click
  end
  object Edit1: TEdit
    Left = 368
    Top = 0
    Width = 345
    Height = 20
    Font.Charset = OEM_CHARSET
    Font.Color = clWindowText
    Font.Height = -8
    Font.Name = 'Terminal'
    Font.Style = []
    ParentFont = False
    TabOrder = 5
    Text = 
      'f38d958d401c1d8f873deaf238eeda0896271e0e6a097aa141708872270dc8c1' +
      '8d9f599850b033018c182d81650ea9e1a09a4cf17f'
    Visible = False
  end
  object Panel2: TPanel
    Left = 536
    Top = 40
    Width = 113
    Height = 17
    Caption = 'DECODENEW'
    TabOrder = 6
    Visible = False
  end
  object Button11: TButton
    Left = 616
    Top = 16
    Width = 161
    Height = 17
    Caption = 'edit1HEX->memo1HEXFORCPP'
    TabOrder = 7
    Visible = False
    OnClick = Button11Click
  end
  object Edit2: TEdit
    Left = 712
    Top = 0
    Width = 65
    Height = 21
    TabOrder = 8
    Visible = False
  end
  object Panel3: TPanel
    Left = 0
    Top = 513
    Width = 606
    Height = 32
    Align = alBottom
    Color = clLime
    TabOrder = 9
    object Clitoris: TEdit
      Left = 2
      Top = 2
      Width = 599
      Height = 27
      BorderStyle = bsNone
      Color = clBlack
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clLime
      Font.Height = -19
      Font.Name = 'Tahoma'
      Font.Style = [fsBold]
      ParentFont = False
      TabOrder = 0
      OnKeyDown = ClitorisKeyDown
      OnKeyPress = ClitorisKeyPress
    end
  end
  object Panel4: TPanel
    Left = 0
    Top = 0
    Width = 606
    Height = 20
    Align = alTop
    Caption = 'MOISTURE PARAMETERS(DONT WORK YET)'
    Color = clLime
    TabOrder = 10
    object Label1: TLabel
      Left = 1
      Top = 1
      Width = 144
      Height = 10
      Caption = 'buttons for those who can see too good:'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Height = -8
      Font.Name = 'Tahoma'
      Font.Style = []
      ParentFont = False
    end
    object Button1: TButton
      Left = 1
      Top = 9
      Width = 33
      Height = 10
      Caption = 'refresh'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Height = -8
      Font.Name = 'Tahoma'
      Font.Style = []
      ParentFont = False
      TabOrder = 0
      OnClick = Button1Click
    end
    object Button2: TButton
      Left = 152
      Top = 0
      Width = 17
      Height = 17
      Caption = 'Button2'
      TabOrder = 1
      OnClick = Button2Click
    end
    object Button5: TButton
      Left = 168
      Top = 0
      Width = 17
      Height = 17
      Caption = 'Button5'
      TabOrder = 2
      OnClick = Button5Click
    end
  end
  object Memo2: TMemo
    Left = 568
    Top = 24
    Width = 17
    Height = 17
    Lines.Strings = (
      '               GS MASTER SERVER'
      '                    .---.'
      '                   (_,/\ \'
      '                  (`a a(  )'
      '     (irc)3-------->\O  ) ('
      '      6667       (.--'#39' '#39'--.)'
      '                 / (_)^(_) \'
      '                | / \   / \ |'
      '                 \\ / . \ //'
      '                  \/\___/\<------2(ServerBrowser)'
      '     (Master)------->\1/  |'
      '      29900        \  /  /'
      '                    \/  /'
      '                     ( ('
      '                     |\ \'
      '               jgs   | \ \'
      '                    /_Y/_Y'
      ''
      '1. Master Server Main[MS] on port 29900 handles logging'
      
        'Somewhere near there is QueryResponse[QR] on 29700, that collect' +
        's info from hosted games'#39' servers'
      
        '2. ServerBrowser[SB](28910) sends responses with serverlist to c' +
        'lients'
      
        '3. Peerchaht [IRC](6667) handles chat (and some stuff like who i' +
        's ready in a staging game)'
      
        '4. WebPort [WB] (80) Game will try to connect but we only need t' +
        'o make sure it doesn'#39't cause any delays in logging.')
    TabOrder = 11
    Visible = False
    WordWrap = False
  end
  object Daemon: TServerSocket
    Active = False
    Port = 6667
    ServerType = stNonBlocking
    OnAccept = DaemonAccept
    OnGetThread = DaemonGetThread
    OnClientConnect = DaemonClientConnect
    OnClientDisconnect = DaemonClientDisconnect
    OnClientRead = DaemonClientRead
    OnClientError = DaemonClientError
    Left = 504
    Top = 192
  end
  object CS: TClientSocket
    Active = False
    Address = '127.0.0.1'
    ClientType = ctNonBlocking
    Port = 6000
    OnConnect = CSConnect
    OnRead = CSRead
    Left = 520
    Top = 456
  end
end
