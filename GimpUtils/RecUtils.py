#!/usr/bin/env python
from gimpfu import *
import csv

CSV_PATH = "C:\\Users\\Elisar\\Desktop\\temp2.csv"
MAIN_CSV_PATH = "C:\\Users\\Elisar\\Desktop\\temp.csv"


def get_rec_position_to_csv(image,drawable,page,stage):
    selection,x1,y1,x2,y2=pdb.gimp_selection_bounds(image)
    if not selection:
        pdb.gimp_message("No selection")
    else:
        gimp.message('L=%d\nU=%d\nR=%d\nD=%d' % (x1,y1,x2-x1,y2-y1))
        f = open(CSV_PATH, 'ab')
        writer = csv.writer(f)
        writer.writerow([page,stage,x1,y2,x2-x1,y2-y1])
        f.close()
        f = open(MAIN_CSV_PATH, 'ab')
        writer = csv.writer(f)
        writer.writerow(['END OF SAME PAGE'])
        f.close()

### Registration
desc='Show selection margins'
register(
    'selection-margins',desc,desc,'Elisar-Eisenbach','LEGO-AI-FUN','2022',"<Image>/Select/Step1",'*',
    [
        (PF_INT,"page","Page",1),
        (PF_INT,"stage","Stage",1)
    ],
    [],
    get_rec_position_to_csv
)

main()