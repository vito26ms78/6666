@echo off

title Anber Translator Build System

echo ==========================================
echo Anber Translator Build System
echo ==========================================
echo.

echo Cleaning old build...
echo.

if exist build (
rmdir /s /q build
)

if exist dist (
rmdir /s /q dist
)

rem if exist AnberTranslator.spec (
rem del /q AnberTranslator.spec
rem )

echo.
if not exist dictionary (
    echo.
    echo ERROR: dictionary folder not found
    echo.
    pause
    exit /b
)
echo Build Start...
echo.

py -3.11 -m PyInstaller ^
--noconfirm ^
--clean ^
--onedir ^
--console ^
--name AnberTranslator ^
--hidden-import=capture ^
--hidden-import=capture.dxgi_capture ^
--hidden-import=ocr ^
--hidden-import=ocr.easyocr_engine ^
--hidden-import=translator ^
--hidden-import=translator.translator_engine ^
--hidden-import=overlay ^
--hidden-import=overlay.overlay_window ^
--hidden-import=overlay.overlay_renderer ^
--hidden-import=overlay.text_renderer ^
--hidden-import=core ^
--hidden-import=core.translation_loop ^
--hidden-import=window ^
--hidden-import=window.window_detector ^
--hidden-import=dictionary ^
--hidden-import=dictionary.dictionary_corrector ^
--hidden-import=deep_translator ^
--hidden-import=dxcam ^
--hidden-import=mss ^
--hidden-import=torch ^
--hidden-import=torchvision ^
--hidden-import=numpy ^
--hidden-import=cv2 ^
--hidden-import=PyQt6 ^
--collect-all=cv2 ^
--collect-all=easyocr ^
--collect-all=PyQt6 ^
--collect-all=torch ^
--collect-all=torchvision ^
--add-data "dictionary;dictionary" ^
--collect-all=skimage ^
--collect-all=scipy ^
--collect-all=shapely ^
main.py

echo.
echo ==========================================
echo Build Finished
echo ==========================================
echo.

if exist dist\AnberTranslator (
echo Build Success
echo.
echo Output:
echo dist\AnberTranslator
) else (
echo Build Failed
)

echo.
pause
