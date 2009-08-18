import os
import tarfile
import shutil
import random
from models import application 
from django.conf import settings
from django.core.management import call_command


class installer (object):
    """ Dina Installer main class """
    
    # this class will extract and install an application or a template package
    def __init__ (self , file_path):
        self.path = file_path
        


    def _extract (self):
        """ Extract the archive file in the same directory  """

        #!!! Here i should add error handling

        # Get the current working directory address
        pwd = os.getcwd ()
        self.return_path = pwd
        os.chdir ('/tmp/')
        # build a random unique name
        dirname = 'dina_' + str (random.randrange (1 , 1000))
        self.dirname = dirname

        # build a dir
        os.mkdir(dirname)

        # Copy archive and its meta data to /tmp
        shutil.copy2 (self.path , '/tmp/' + dirname + "/tmp_archive")

        # Change the current working directory to /tmp
        os.chdir ('/tmp/' + dirname)

        #extract the file name from path
        archive =  "tmp_archive"#self.path.split('/')[-1]
        
        # open archive file for extraction
        tar = tarfile.open (archive)

        # extract the archive file
        tar.extractall ()
        tar.close ()


    def _read_index (self):
        """ Read the package information file """
        
        # pars the information file to a python dictionary
        dic = self._parser ('package.info')
        

        #+++ here i should add an exception handler --------------

        if dic["type"].lower ()  == "application":

            self.obj = application (Name = dic["name"])

        elif dic["type"].lower () == "template":

            self.obj = template (Name = dic["name"])
            # here i should add the difference field
        
        self.obj.SHA1 = dic["sha1"]
        self.obj.Author = dic["author"]
        self.obj.Email = dic["email"]
        self.obj.Home = dic["home"]
        self.obj.url = dic["url"]
        self.obj.Description = dic["description"]
        self.dir = dic["directory"]
        self.obj.Publish = False
        #------------------------------------------------------

        return 0
    


    def install (self):
        """ install the package """

        self._extract ()
        self._read_index ()
        os.chdir ('/tmp/' + self.dirname)
        appdir = settings.APP_ROOT
        shutil.copytree (self.dir , appdir + "/" + self.dir)
        #os.rmdir ('/tmp/' + self.dirname)
        os.chdir (self.return_path)
                   
        return self.obj


    def _parser (self , file):
        """Parse the file to a python dictionary"""
        #+++ here i should add a conf validator
        try:
            fd = open (file , "r")
            lines = fd.readlines ()
            fd.close ()
        except:
            print "Error: The file %s does not exists or permission denid !" % (file)
            return -1
        dic = {}
        for i in lines:
            if i.strip ()[0] == '#':
                pass
            else:
                li = i.split ("=")
                dic[li[0].strip().lower()] = li[1].strip().lower()
                
        return dic


    