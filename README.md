# blender_Multiple-version-options
可讓用戶自行選擇所需要的Blender版本

推薦使用code模式觀看

#教學(ZH)

#-----Blender.param-----

#修改 0.0.0 為您所需要的版本 例如:4.2.0 / 3.6.7 / 4.0.0

#一定要使用3位數字否則會出錯！

#並且在Default的""內新增您的blender的路徑 例如:C:\Program Files\Blender Foundation\Blender\blender.exe

#-----可修改/複製參數-----

[Blender_0.0.0_RenderExecutable]
Type=multilinemultifilename
Label=Blender 0.0.0 Executable
Category=Render Executables
CategoryOrder=0
Default=""
Description=The path to the Blender executable file used for rendering. Enter alternative paths on separate lines.

#-------------------------

#-----BlenderSubmission.py-----

#修改或新增()內的數字即可

#-----可修改/複製參數-----

scriptDialog.AddComboControlToGrid("BlenderVersion", "ComboControl","0.0.0", ("4.2.0", "4.0.0", "3.6.7", "3.6.2"), 7, 1, expand=False)

#-------------------------

Tutorial (EN)

----- Blender.param -----

Modify 0.0.0 to the version you need, e.g.: 4.2.0 / 3.6.7 / 4.0.0

You must use three-digit version numbers, or errors will occur!

Also, add your Blender path inside the Default quotes, e.g.: C:\Program Files\Blender Foundation\Blender\blender.exe

----- Editable/Copyable Parameters -----

[Blender_0.0.0_RenderExecutable]
Type=multilinemultifilename
Label=Blender 0.0.0 Executable
Category=Render Executables
CategoryOrder=0
Default=""
Description=The path to the Blender executable file used for rendering. Enter alternative paths on separate lines.

-------------------------

----- BlenderSubmission.py -----

Modify or add numbers within the parentheses ()

----- Editable/Copyable Parameters -----

scriptDialog.AddComboControlToGrid("BlenderVersion", "ComboControl", "0.0.0", ("4.2.0", "4.0.0", "3.6.7", "3.6.2"), 7, 1, expand=False)

-------------------------

教程 (JP)
----- Blender.param -----

0.0.0 を必要なバージョンに変更してください。例：4.2.0 / 3.6.7 / 4.0.0

必ず3桁の数字を使用してください。さもなければエラーが発生します！

さらに、Defaultの "" 内にBlenderのパスを追加してください。例：C:\Program Files\Blender Foundation\Blender\blender.exe

----- 編集可能/コピー可能なパラメータ -----

[Blender_0.0.0_RenderExecutable]
Type=multilinemultifilename
Label=Blender 0.0.0 Executable
Category=Render Executables
CategoryOrder=0
Default=""
Description=The path to the Blender executable file used for rendering. Enter alternative paths on separate lines.

-------------------------

----- BlenderSubmission.py -----

() 内の数字を変更または追加してください

----- 編集可能/コピー可能なパラメータ -----

scriptDialog.AddComboControlToGrid("BlenderVersion", "ComboControl", "0.0.0", ("4.2.0", "4.0.0", "3.6.7", "3.6.2"), 7, 1, expand=False)

-------------------------
