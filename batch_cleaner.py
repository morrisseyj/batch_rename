import os
import re
from PIL import Image
import datetime
import shutil

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

    #List all the files that will not be changed as they are not jpeg
    not_changed = [i for i in files if not bool(re.search('\.JPG|\.jpg', os.path.splitext(i)[1]))]

    #Check all files are JPG if not i have to change the code
    #for i in files:
    #    if not bool(re.search('\.JPG|\.jpg', os.path.splitext(i)[1])):
    #        print(i)
    #        print('You are trying to organize some files that do not have the ".JPG" extension. This might break the code and cause a loss of data. Other filetypes can be accomodated, but please call James') 
    #        quit()

    #Get all the jpg (or whatever extensions) from the list of files (i.e. address that other files may be in the folder)
    pictures = [i for i in files if re.search('\.JPG|\.jpg', i)]

    #Make sure that all the valid file types have valid names - i.e. don't include brackets
    for i in pictures:
        if bool(re.search('\(|\)', i)):
            print('Some of the files have bracket symbols in the names. This may break the code and cause a loss of data. Please address filename issues or call James')
            quit()

    #Get jpg image objects - to get the meta-data (i want the dates) 
    images = [Image.open(os.path.join(raw_photo_directory, i)) for i in pictures]
    #Get exif data tag no 36867 which is the date, for every image
    dates_str = [i._getexif()[36867] for i in images]
    #Create date objects from the list of dates
    #dates_object = [datetime.datetime.strptime(i, "%Y:%m:%d %H:%M:%S") for i in dates_str]
    for i in dates_str:
        try:
            datetime.datetime.strptime(i, "%Y:%m:%d %H:%M:%S")
        except:
            print(i)
    #Get the YYYY_mmm string from the date object
    year_month_str = [str(i.year) + '_' + i.strftime('%b') for i in dates_object]
    #Create the eventual dictionary by linking the pictures list and date list
    filename_date_dict = {pictures[i]: year_month_str[i] for i in range(len(pictures))}

    #Now do the ordering of the photos
    #Iterate over the dictionary 
    #Copying the file to the relevant folder if it exists
    #Or creating the folder and copy the file if the folder does not exist
    counter = 1
    copy_counter = 1
    copy_errors = {}
    for i in filename_date_dict:
        print('Processing image', counter, 'of:', len(pictures))
        #create easily identifiable sources and destinations for readability
        dest_folder = os.path.join(organized_photos_directory, filename_date_dict[i])
        dest_file = os.path.join(organized_photos_directory, filename_date_dict[i], i)
        source_file = os.path.join(raw_photo_directory, i)
        
        #Check if the destination folder exists
        #If not create the folder and copy the file to it
        if not os.path.exists(dest_folder):
            os.mkdir(dest_folder)
            shutil.copy(source_file, dest_folder)
        else: #If the destination folder does not exist 
            if os.path.exists(dest_file): #First check if there won't be a file name clash
                while os.path.exists(dest_file): #If there is a clash
                    if bool(re.search('\(', dest_file)): #check whether the file has already had brackets added to its name
                        dest_file = dest_file[:-3] #If it has remove those brackets
                    dest_file += '(' + str(copy_counter) + ')' #Then add brackets around a number which is counting up   
                    copy_counter += 1 #The increment the counter of copies
                copy_errors.update({source_file: dest_file}) #start a dictionary containing any copy errors that can be printed at the end
                os.mkdir(os.path.join(raw_photo_directory, 'temp')) #Make a temp directory for renaming
                temp_rename_dir = os.path.join(raw_photo_directory, 'temp') #Create an object with temp directory path
                shutil.copy(source_file, temp_rename_dir) #copy the source file to the temp directory
                os.rename(os.path.join(temp_rename_dir, re.findall('[A-Za-z]+_\d+\.[A-Za-z]+', source_file)[0]), os.path.join(temp_rename_dir, re.findall('[A-Za-z]+_\d+\.[A-Za-z]+\(\d\)$', dest_file)[0])) #rename the source file in the temp directory to the updated dest_file name
                source_file = os.path.join(temp_rename_dir, re.findall('[A-Za-z]+_\d+\.[A-Za-z]+\(\d\)$', dest_file)[0]) #create an updated source_file path
                shutil.copy(source_file, dest_folder) #Copy the renamed source_file to the dest_folder
                shutil.rmtree(temp_rename_dir) #clean up by deleting the temp directory
            else:
                shutil.copy(source_file, dest_folder) #If dest folder already exists and the dest file does not exist, just copy
        copy_counter = 1 #reset the copy counter
        counter += 1 #Increment the counter

    if len(copy_errors) > 0:
        print('There were filename conflicts. Data has been kept but files have been renamed. The following filenames experienced errors:')
        for i in copy_errors:
            print('oldname: {}, newname: {}'.format(i, copy_errors[i]))

    print('The following files were not organized as they are not jpeg format')
    for i in not_changed:
        print(i)
        
    print('Done')