; =====================================================================
; AetherNet Desktop - High-Performance DPI & Network Optimizer
; Production Inno Setup 6 Script
; Completely white-labeled, scrubs all legacy engine mentions
; =====================================================================

#define MyAppName "AetherNet"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "Aether Network Technologies"
#define MyAppURL "https://github.com/aethernet-desktop"
#define MyAppExeName "AetherNet.exe"
#define MyCoreWorkerName "core-worker.exe"

[Setup]
; Unique GUID for clean upgrades and uninstallation
AppId={{E6D8A279-9941-477F-9BC4-A515152862B8}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=
OutputDir=..\dist
OutputBaseFilename=AetherNet_Setup_v2.0
SetupIconFile=
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern

; Require administrative privileges for WinDivert driver installation
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=commandline
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startup"; Description: "Запускать автоматически при входе в Windows"; GroupDescription: "Автозагрузка:"

[Files]
; Main Executable & Binaries
Source: "..\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; Core Filtering Engine, AI Smart Daemon & Signed Drivers
Source: "..\dist\bin\*"; DestDir: "{app}\bin"; Flags: ignoreversion recursesubdirs createallsubdirs
; Configs and Hostlists
Source: "..\config\*"; DestDir: "{app}\config"; Flags: ignoreversion recursesubdirs createallsubdirs
; Diagnostic Engine & Modern GUI
Source: "..\core\*"; DestDir: "{app}\core"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\gui\*"; DestDir: "{app}\gui"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Диагностика сети"; Filename: "python.exe"; Parameters: """{app}\core\health_checker.py"""; WorkingDir: "{app}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
; Autorun on startup if task selected
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "{#MyAppName}"; ValueData: """{app}\{#MyAppExeName}"" --minimized"; Flags: uninsdeletevalue; Tasks: startup

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallRun]
; Stop running engine and clean up WinDivert driver service before removing files
Filename: "taskkill.exe"; Parameters: "/F /IM {#MyCoreWorkerName} /IM ai-worker.exe /IM {#MyAppExeName}"; Flags: runhidden
Filename: "sc.exe"; Parameters: "stop WinDivert"; Flags: runhidden
Filename: "sc.exe"; Parameters: "delete WinDivert"; Flags: runhidden

[Code]
// Terminate running processes before installation
function InitializeSetup(): Boolean;
var
  ErrorCode: Integer;
begin
  ShellExec('open', 'taskkill.exe', '/F /IM {#MyAppExeName} /IM {#MyCoreWorkerName} /IM ai-worker.exe', '', SW_HIDE, ewWaitUntilTerminated, ErrorCode);
  Result := True;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  ErrorCode: Integer;
begin
  if CurUninstallStep = usUninstall then
  begin
    // Stop all processes on uninstall
    ShellExec('open', 'taskkill.exe', '/F /IM {#MyAppExeName} /IM {#MyCoreWorkerName} /IM ai-worker.exe', '', SW_HIDE, ewWaitUntilTerminated, ErrorCode);
    ShellExec('open', 'sc.exe', 'stop WinDivert', '', SW_HIDE, ewWaitUntilTerminated, ErrorCode);
  end;
end;
    ShellExec('open', 'sc.exe', 'stop WinDivert', '', SW_HIDE, ewWaitUntilTerminated, ErrorCode);
    ShellExec('open', 'sc.exe', 'delete WinDivert', '', SW_HIDE, ewWaitUntilTerminated, ErrorCode);
  end;
end;
