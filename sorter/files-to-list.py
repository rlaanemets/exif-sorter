# A program which makes a list containing
# paths to all jpg files in a given directory
import glob
usrpath = raw_input('input path:')
filetype = raw_input('file type (extension):')
jpgpath = usrpath + '*.' + filetype
print 'the list of ', filetype, 'files is: ', '\n', glob.glob(jpgpath)

