@echo off
chcp 65001 >nul
rem 以仓库根目录为工作目录运行更新器（脚本自身按 __file__ 定位输出目录）
cd /d "%~dp0.."
set "PY=python"
where py >nul 2>nul && set "PY=py -3"
echo 正在抓取上次成功时间之后的新论文，请稍候……
"%PY%" "%~dp0数学前沿更新器.py"
if errorlevel 1 (
  echo.
  echo 更新失败，已保留上一版页面。详情见 09-前沿动态\_update.log
) else (
  echo.
  echo 更新完成，正在打开论文日报。
)
start "" "%~dp0论文日报.html"
