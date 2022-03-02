#!/usr/bin/env python
from gimpfu import *
import csv

CSV_PATH = "C:\\Users\\Elisar\\Desktop\\temp.csv"
MAIN_CSV_PATH = "C:\\Users\\Elisar\\Desktop\\temp2.csv"


def get_rec_position_to_csv2(image,drawable,legoID, quantity):
    selection,x1,y1,x2,y2=pdb.gimp_selection_bounds(image)
    if not selection:
        pdb.gimp_message("No selection")
    else:
        gimp.message('L=%d\nU=%d\nR=%d\nD=%d' % (x1,y1,x2-x1,y2-y1))
        f = open(CSV_PATH, 'ab')
        writer = csv.writer(f)
        writer.writerow(['','','','','','',quantity,legoID,x1,y2,x2-x1,y2-y1])
        f.close()
        f = open(MAIN_CSV_PATH, 'ab')
        writer = csv.writer(f)
        writer.writerow(['EMPTY'])
        f.close()

### Registration
desc='Show selection margins of brick'
register(
    'selection-margins-bricks',desc,desc,'Elisar-Eisenbach','LEGO-AI-FUN','2022',"<Image>/Select/Step2",'*',
    [
        (PF_INT,"legoID","LegoID",1),
        (PF_INT,"quantity","Quantity",1)
    ],
    [],
    get_rec_position_to_csv2
)

main()