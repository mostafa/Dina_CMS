import codec
import os
import shutil


class RepositoryError (Exception):
    def __init__ (self , err):
        self.errstr = err
    def __unicode__ (self):
        return self.errstr
    def __str__ (self):
        return self.errstr
    


class Repository (object):
    """
    Dina Repository Class
    """

    def __init__ (self, url , cache ,codename="stable" , sections=["main",] ):
        self.protocol = url.split (':')[0]
        self.codec = codec.getCodec (self.protocol)
        if not self.codec :
            raise RepositoryError ("\"%s\" does not support by DPM at this time." % (self.protocol))
        self.codename = codename
        self.sections = sections
        if url[-1] == "/":
            url = url[:-1]
        self.url = url
        self.cache = cache
        self.name = url.replace (' ' , '_').replace ('/' , '_')
        
        

    def _setUrl (self , url):
        #+++ i should add here an url validation
        self.url = url
        

    def _getUrl (self):
        return self.url
    
    url = property (fget = _getUrl , fset= _setUrl)




    def _getFile (self , addr):
        """
        Download the given file.
        """
        if not addr:
            return -1
        filename = addr.split ('/')[-1]
        try:
            self.codec.getFile (self.url + addr , self.cache)
            
        except:
                #+++ here i should add better output
                raise RepositoryError ("codec.getFile : error")
        
        return self.cache + filename


    def update (self):
        """
        Update repository packages file.
        """

        self.CleanCache ()
        
        #+++ here i should add some scurity identification for repositories. something lik Release file in debian


        dirs = os.listdir (self.cache + "repo/")
        if not self.name in dirs:
            os.mkdir (self.cache + "repo/" + self.name)
        addr = list ()
        for i in self.sectiosn:
            
            addr.append ( {"url" :  self.url + "/dists/" + self.codename + "/" +  i  + "/Packages.json" , "cache_dir" : self.codename + "_" +  i})
        dirs = os.listdir (self.cache + "repo/" + self.name)
        for i in addr:
            if not i["cache_dir"] in dirs:
                os.mkdir (self.cache + "repo/" + self.name + "/" + i["cache_dir"])
            try:
                
                self.codec.getFile (i , self.cache + "repo/" + self.name + "/" + i["cache_dir"])
            except:
                raise RepositoryError ("codec.getFile : error")


    def CleanCache (self):
        """
        Clean the cache.
        """
        shutil.rmtree (self.cache + "repo/" + self.name)



