##let's try sorting

#import modules
import glob, sys, os, shutil

from PIL import Image
from PIL.ExifTags import TAGS

#ask for info 

usrpath = raw_input('input path:')
if usrpath == '':
    usrpath = '/home/swc/drop/'    
#print 'the usrpath string: ', usrpath

#screw the filetypes jpg only
filetype = raw_input('file type (extension) (default scans directory for \'JPG\' and \'jpg\' files) :')
if filetype == '':
    filetype = ['JPG', 'jpg']


# define attibutes
attributes = ['aperture', 'shutterspeed', 'isospeed', 'focallength', 'date', 'cameramodel']
sorttype = raw_input('which attrbute?')

if sorttype == '':
    sorttype = 'aperture'
    
if sorttype not in attributes:
    raise NameError('not a valid attribute, the list of supported commands is: \'aperture\', \'suhtterspeed\', \'isospeed\', \'focallength\', \'date\' and \'cameramodel\'')

#if sorttype is date, ask where to divide the time
if sorttype == 'date':
    dateprecision = raw_input('specify time dividers - years, months, days, hours, minutes or seconds: ')
    dividers = {'years' : 4, 'months' : 7, 'days' : 10, 'hours' : 13, 'minutes' : 16, 'seconds' : 19}
    if not dateprecision in dividers:
        raise NameError('not a valid divider')
        
outpath = raw_input('output path:')

if outpath == '':
    outpath = '/home/swc/w1'

#assemble a command for glob
##orig## jpgpath = usrpath + '*.' + filetype

filelist = []
for value in filetype:
    globpath = usrpath + '*.' + value
    filelist += (glob.glob(globpath))



print 'filelist: ', filelist


print 'making an output directory, if it doesnt exist'
if os.path.isdir(outpath) == False:      
    os.mkdir(outpath)

print 'beginning the cycle'
while filelist != []:
    #print 'the filelist that made into the cycle', filelist
    fpath = filelist[0]
    print 'current file is: ', fpath
    #get the exif data from the file
    exifdictionary = {}
    i = Image.open(fpath)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        exifdictionary[decoded] = value
            #return exifdictionary
    #print 'whole exifdict: ', exifdictionary                   
   
 
   
    # define attributes
    if sorttype == 'aperture':
        try:     
            outstr = 'F' + str(exifdictionary['FNumber'][0] / float(exifdictionary['FNumber'][1]))           
        except KeyError:
            print 'no parsable info found'
            outstr = 'noexif'
            sys.exc_clear()
        if '.0' in outstr:
            outstr = outstr.replace('.0', '')        
            
    elif sorttype == 'shutterspeed':
        try:
            if exifdictionary['ExposureTime'][0] == exifdictionary['ExposureTime'][1]:
                outstr = '1s'
            elif exifdictionary['ExposureTime'][0] == 1:
                outstr =  str(exifdictionary['ExposureTime'][0]) + ':' + str(exifdictionary['ExposureTime'][1]) + 's'
            elif exifdictionary['ExposureTime'][1] == 1:
                outstr = str(exifdictionary['ExposureTime'][0]) + 's'
            else:
                outstr =  str((exifdictionary['ExposureTime'][0]) / float((exifdictionary['ExposureTime'][1]))) + 's'    
        except KeyError:
            print 'no parsable info found'
            outstr = 'noexif'
            sys.exc_clear()
        
    elif sorttype == 'isospeed':
        try:
            outstr = 'ISO ' + str(exifdictionary['ISOSpeedRatings'])
        except KeyError:
            print 'no parsable info found'
            outstr = 'noexif'
            sys.exc_clear()   
           
    elif sorttype == 'focallength':
        try:
            outstr = str(exifdictionary['FocalLength'][0]) + 'mm'  
        except KeyError:
            print 'no parsable info found'
            outstr = 'noexif'
            sys.exc_clear()      
        
    elif sorttype == 'date':
        try:
            outstr = exifdictionary['DateTimeDigitized'][0: dividers[dateprecision]]
        except KeyError:
            print 'no parsable info found'
            outstr = 'noexif'
            sys.exc_clear()
    
    elif sorttype == 'cameramodel':
        try:
            outstr = exifdictionary['Model']
        except KeyError:
            print 'no parsable info found'
            outstr = 'noexif'
            sys.exc_clear()
    
    
    # make a folder for the file  
    print 'output folder name: ', outstr 
    newdir = outpath+'/'+outstr 
    if not os.path.exists(newdir):        
        os.mkdir(newdir)
        
        
    #copy the file to the folder
    shutil.copy2(filelist[0], newdir)
    
    #delete the file from filelist
    del filelist[0]
    #print 'removed!'

