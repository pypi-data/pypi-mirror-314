# 设置脚本在遇到错误时停止执行
$ErrorActionPreference = "Stop"

# 启用调试模式，打印每个命令
Set-PSDebug -Trace 1

# 获取脚本的绝对路径
$scriptPath = $MyInvocation.MyCommand.Path
$toolRoot = Split-Path -Path $scriptPath -Parent
$toolRoot = Split-Path -Path $toolRoot -Parent
$toolRoot = Split-Path -Path $toolRoot -Parent

# 输出 TOOL_ROOT
Write-Output $toolRoot

# 输出 TESTSOLAR_WORKSPACE 环境变量
Write-Output $env:TESTSOLAR_WORKSPACE

# 调用外部命令
& "/usr/local/bin/testtools_sdk" version
& "/usr/local/bin/testtools_sdk" serve --tool replace_____me