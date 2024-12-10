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

# 切换到 TOOL_ROOT 目录
Set-Location -Path $toolRoot

# 安装到全局的python中，无需创建虚拟环境(当前已经使用uniSDK，对运行环境的依赖很少)
pip install -r requirements.txt

# 安装 uniSDK
Invoke-WebRequest -Uri "https://testsolar-1321258242.cos.ap-guangzhou.myqcloud.com/cli/testtools_sdk-install/stable/install.sh" -OutFile "install.sh"
bash .\install.sh