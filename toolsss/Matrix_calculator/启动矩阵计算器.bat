@echo off
:: 强制让命令行支持中文，防止乱码
chcp 65001 > nul

:: 1. 切换到包含空格的完整文件夹目录（加双引号）
cd /d "C:\Users\lixiang\Desktop\toolsss\Matrix Calculator"

:: 2. 自动多路径探测 Anaconda 并引入
if exist "C:\ProgramData\Anaconda3\Scripts\activate.bat" (
    call "C:\ProgramData\Anaconda3\Scripts\activate.bat" "C:\ProgramData\Anaconda3"
) else if exist "C:\Users\%USERNAME%\anaconda3\Scripts\activate.bat" (
    call "C:\Users\%USERNAME%\anaconda3\Scripts\activate.bat" "C:\Users\%USERNAME%\anaconda3"
) else if exist "D:\Anaconda3\Scripts\activate.bat" (
    call "D:\Anaconda3\Scripts\activate.bat" "D:\Anaconda3"
) else (
    echo ❌ 未找到 Anaconda 安装路径，请检查是否安装成功！
    pause
    exit
)

:: 3. 激活虚拟环境
call conda activate matrix

:: 4. 自动生成依赖清单（加双引号防止空格报错）
pip freeze > "C:\Users\lixiang\Desktop\toolsss\Matrix Calculator\requirements.txt"

:: 5. 启动 Streamlit（加双引号强制锁定带空格的路径）
streamlit run "C:\Users\lixiang\Desktop\toolsss\Matrix Calculator\matrix_app.py"

pause