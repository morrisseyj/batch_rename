import os
import re
from PIL import Image
import datetime
import shutil
import pickle
import sys

#Function that takes the absolute photo path - should be generated from the tknter app
def photo_batch_cleaner(raw_photo_directory):

    #Then set the location of the organized photos
    organized_photos_directory = os.path.join(raw_photo_directory + '_organized_files' + '-' + str(datetime.date.today()))

    #Now check if the organized photos directory exists
    #If so do nothing otherwise make the directory
    if os.path.exists(organized_photos_directory):
        pass
    else:
        os.mkdir(organized_photos_directory)

    #Now create a dictionary as such - filename: year_mon
    #First get the contents of the raw photo directory
    contents = os.listdir(raw_photo_directory)

    #Now get all the files in that directory - i.e. ignore folders
    files = [i for i in contents if os.path.isfile(os.path.join(raw_photo_directory, i))]
    
    with open(os.path.join(organized_photos_directory, 'file_list'), 'wb') as f:
        pickle.dump(files, f)
        
    sys.exit()
