# Blender data genrationd for lego-ai-fun project
The pything script ./GenerateLegoData.py generates and renders scense with lego parts agains varioues backgrounds.
## How it works
We generate a random number of lego bricks. We drop them with a phisics simulation to create a pile. We position a camera at a random location facing the bricks and use the compositing to generate the output.
## output
Output is a folder for each generated image, inclusing the image and the masks assiciated with the it
## Prerequisits
To run this file you would need:
* Belnder (build and tested with version 3.00)
* Lego parts designs are taken from the [lDraw](https://www.ldraw.org/) parts library and they are imported using the [ImportLDraw](https://github.com/TobyLobster/ImportLDraw) Belnder plug-in.
## Control
You can control the following properties by adjusting the constants in the script:
* Number of images (scenes) generated
* Number of bricks in each image
* What bricks would be included
* What colors would the bricks be
* Target folder for generated data