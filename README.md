# phage_plaque_count
Auto detection and count the phage plaque number in culture plate

# Introduction
Recently I'm studing openCV, consideing bacteriophage is one of interests of my lab, I write this script for training my skill.
This script only fit the circular plate, the square plate version will be developed in the next few days.

# Required Packages
openCV

imutils

# Usage
The using of this tool is very easy, put the script, a trainning file "risst.tr" and the reference file you want to use to the filefolder of your sequence.
For example, if the species of your genome dataset are *Sreptococcus suis*, you just need to put ```Streptococcus_suis_cps_locus_reference.gbk``` and ```risst.tr``` in the folder contain your genome sequence files, open a terminal and into the folder, get in the evironment if you create one by conda, and run like this:   
``` Python
python phage_plaque_count.py  *.jpg
```

* Not only .jpg, other format of picture is also available

# Example
Input

![KP831](https://user-images.githubusercontent.com/108860907/225705866-cfb25b82-ad90-4488-9251-9657d2a5e7c6.jpg)

Output

![plague_detection](https://user-images.githubusercontent.com/108860907/225705964-5a7c721f-b534-47eb-8447-f0dfa760fc5f.png)

A total number of 20 bacteriophage plaques were detected on the plate
