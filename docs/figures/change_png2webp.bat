 @echo off
:: change png files to webp files
setlocal
echo Searching for new .png files...
for %%F in (*.png) do (
    rem output file is input file name with extension .webp
    rem set outfile = %%~nF.webp
    rem echo %%~nF.webp
    rem echo %%F

    cwebp -q 50  %%F  -o %%~nF.webp

)