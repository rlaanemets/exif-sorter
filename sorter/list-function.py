# A program which makes a list containing
# paths to all jpg files in a given directory
def listjpg(usrpath):
    import glob
    usrpath = raw_input('input path:')
    jpgpath = usrpath + '*.jpg'
#    print 'the list of jpg files is: ', '\n', glob.glob(jpgpath)
