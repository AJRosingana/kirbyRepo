@echo off
rem Launch Kirby Companion in Microsoft Edge Frameless App Window with Core 0 Disabled (Affinity 0xFE)
title 🌸 Kirby Edge Companion (Core 0 Shielded) 🌸
start "" /belownormal /affinity FE msedge.exe --app=http://100.121.245.47:8088/win11 --window-size=560,780 --window-position=1300,200 --enable-gpu-rasterization --enable-zero-copy
exit /b 0
