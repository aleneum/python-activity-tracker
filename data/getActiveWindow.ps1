[CmdletBinding()]            
Param(            
)            
Add-Type @"
  using System;
  using System.Runtime.InteropServices;
  public class UserWindows {
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
}
"@

try {
    $ActiveHandle = [UserWindows]::GetForegroundWindow()
    $Process = Get-Process | Where-Object {$_.MainWindowHandle -eq $activeHandle}
    $Process[0] | ForEach-Object{ "{0}, {1}, {2}" -f $_.Name,$_.Description,$_.MainWindowTitle}
} catch {
    ", , $_"
}
