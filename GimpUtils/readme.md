# Automation for getting the Rectangle selection tool position

## Prerequisits
  To run this file you would need:
  * Gimp (I used 2.10.30, but I think it should work on more versions)

## How to use
  ### Gimp Part
  1. copy the .py file to the gimp plugin folder (Edit -> Preferences -> Folders -> Plug-ins)
  2. Reopen Gimp, the plug-in is now in the toolbar (select -> step1 / step2)
  3. In order to add the automation as a shortcut, hover your mouse on the automation button, and press your desirable shortcut
  ### Script part
  1. Select the Rectangle of the white border
  ![image](https://user-images.githubusercontent.com/62891625/156514956-f3daa015-92ec-4c5b-bec0-582b63fb8be5.png)
  2. Click 'step1', enter the stage and the page numbers and click OK
  3. Select Rectangle of each Lego part
  ![image](https://user-images.githubusercontent.com/62891625/156515273-b903a897-d4e0-43bc-82cf-d86236f1d9d6.png)
  4. Click 'step2', enter the partID and the quantity, and click OK
  5. In one file of csv you will have the border margin, the stage number and the page number,
     In the second CSV you will have the partID, quantity and the part margin, and empty space in the start,
     when you move to next stage, it will creates an empty line in the file, so you can see which row to copy from the first csv
  6. Just copy from the first csv to the second 
  

  
  

## Controls
  you can control the following properties by adjusting the constants in the script:
  * two output csv files 
