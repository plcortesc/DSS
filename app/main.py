import os
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import memcache
from google.appengine.api import files
   
BUCKET_PATH = '/gs/cs553ape'
MEMCACHE = False

class FileKey(db.Model):
  blobinfokey = db.StringProperty()
  filelocation = db.StringProperty() 

def filelist_key():
  return  db.Key.from_path('Filelist', 'default_filelist')

class Main(webapp2.RequestHandler):
  def get(self):
    insert_url = blobstore.create_upload_url('/insert')
    self.response.out.write('<html><body>')
    

    self.response.out.write("<center><h3>INSERT</h3></center>")
    self.response.out.write("""<center><form action="%s" method="post" enctype="multipart/form-data"></center>""" % insert_url)
    self.response.out.write("""
          <center>
          <div style="color: Red"><p style="font-size:large;font-style: oblique;font-family: fantasy;font-weight: bold" align="center">Enter the new file key: </p><input type="text" name="filekey"></div>
          <div style="color: Red"><p style="font-size:large;font-style: oblique;font-family: fantasy;font-weight: bold" align="center">Select file to upload: </p><input type="file" multiple name="file"><br></div><div> <input type="submit"
          name="submit" value="INSERT"> </div></form></center><br>""")
    
  
    self.response.out.write("<center><h3>CHECK</h3></center>")
    self.response.out.write("""
          <center>
          <form action="/check" method="post">
            <div style="color: Red"><p style="font-size:large;font-style: oblique;font-family: fantasy;font-weight: bold" align="center">Enter the file key you want to check: </p><input type="text" name="filekey"></div>
            <div><input type="submit" value="CHECK"></div>
          </form>
          </center>
          <br>""")

    self.response.out.write("<center><h3>REMOVE</h3></center>")
    self.response.out.write("""
          <center>
          <form action="/remove" method="post">
            <div style="color: Red"><p style="font-size:large;font-style: oblique;font-family: fantasy;font-weight: bold" align="center">Enter the file key you want to remove: </p><input type="text" name="filekey"></div>
            <div><input type="submit" value="REMOVE"></div>
          </form>
          </center>
          <br>""")          
    
    self.response.out.write("<center><h3>FIND</h3></center>")
    self.response.out.write("""
          <center>
          <form action="/find" method="post">
            <div style="color: Red"><p style="font-size:large;font-style: oblique;font-family: fantasy;font-weight: bold" align="center">Enter the file key you want to find and see its content: </p><input type="text" name="filekey"></div>
            <div><input type="submit" value="FIND"></div>
          </form>
          </center>
          <br>""")

    self.response.out.write("<center><h3>LIST</h3></center>")
    self.response.out.write("""<center><a href="/list">Too see all the files in the LIST click on this link</a></center><br>""")
        
    self.response.out.write('</body></html>')

class Insert(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    fkstring = self.request.get("filekey")
    filekey = FileKey(key_name =fkstring, parent=filelist_key())
    self.response.out.write("File key: "+ filekey.key().id_or_name())         

    upload_files = self.get_uploads('file')
    blob_file = upload_files[0]
    filekey.blobinfokey = str(blob_file.key())

    if MEMCACHE and blob_file.size <= 102400:
      self.response.out.write("</br> Inserted in MEMCACHE")
      memcache.add(fkstring, blob_file)
      filekey.filelocation = "memcache"
      self.response.out.write("""<br><b><a href="/">RETURN TO HOME</a></b><br>""")
    else:
      self.response.out.write("</br> Inserted in GOOGLE CLOUD STORAGE")
      wr_path = files.gs.create(BUCKET_PATH+"/"+filekey.key().id_or_name(), mime_type='text/plain', acl='public-read')
      with files.open(wr_path, 'a') as filepath:
        start = 0
        fetchsz = blobstore.MAX_BLOB_FETCH_SIZE - 1
        filesize=blob_file.size
        while start < filesize:
          filepath.write( blobstore.fetch_data(blob_file, start, start+fetchsz))
          start = start + fetchsz
      files.finalize(wr_path)
      filekey.filelocation = "cloudstorage"
      self.response.out.write("""<br><b><a href="/">RETURN TO HOME</a></b><br>""")
    
    filekey.put()
 


class Remove(webapp2.RequestHandler):
  def post(self):
    fkstring = self.request.get("filekey")
    removeKey = db.Key.from_path("FileKey", fkstring, parent=filelist_key())
    allFileKeys = FileKey.all()
    allFileKeys.filter('__key__ =', removeKey)
    if allFileKeys.count() != 0:
      f = db.get(removeKey)
      if f.filelocation == "memcache":
        memcache.delete(f.key().id_or_name())
        self.response.out.write("<br>Deleted %s from MEMCACHE</br>" % fkstring)
      else:
        files.delete(BUCKET_PATH+"/"+f.key().id_or_name())
        self.response.out.write("<br>Deleted %s from GOOGLE CLOUD STORAGE</br>" % fkstring)
      db.delete(removeKey)
      self.response.out.write("""<br><br><b><a href="/">RETURN TO HOME</a></b>""")
    else:
      self.response.out.write("ERROR!!! The file key '%s' is not in the list." % fkstring)
      self.response.out.write("""<br><br><b><a href="/">RETURN TO HOME</a></b>""")


class Check(webapp2.RequestHandler):
  def post(self):
    fkstring = self.request.get("filekey")
    allFileKeys = FileKey.all()
    allFileKeys.filter('__key__ =', db.Key.from_path("FileKey", fkstring, parent=filelist_key()))
    if allFileKeys.count() != 0:
      self.response.out.write("SUCCESS!!! The file key '%s' is currently in the list." % fkstring)
      self.response.out.write("""<br><br><b><a href="/">RETURN TO HOME</a></b><br>""")
    else:
      self.response.out.write("ERROR!!! The file key '%s' is not in the list." % fkstring)
      self.response.out.write("""<br><b><a href="/">RETURN TO HOME</a></b><br>""")

   

class Find(blobstore_handlers.BlobstoreDownloadHandler):
  def post(self):
    fkstring = self.request.get("filekey")
    allFileKeys = FileKey.all()
    allFileKeys.filter('__key__ =', db.Key.from_path("FileKey", fkstring, parent=filelist_key()))
    if allFileKeys.count() == 0:
      self.response.out.write("ERROR!!! The file key '%s' is not in the list." % fkstring)
    else:
      for f in allFileKeys:
        if f.filelocation != "memcache":
          with files.open(BUCKET_PATH+"/"+f.key().id_or_name(), 'r') as filepath:
            bufRead = filepath.read(9999999)
            while bufRead:
              self.response.out.write(bufRead)
              bufRead = filepath.read(9999999)
        else:
          blob_file = memcache.get(f.key().id_or_name()) 
          self.send_blob(blob_file)
    self.response.out.write("""<br><br><b><a href="/">RETURN TO HOME</a></b>""")



class List(webapp2.RequestHandler):
  def get(self):
    allFileKeys = FileKey.all()
    self.response.out.write("<b>All files in the list</b>:</br></br>")
    for i in allFileKeys:
      self.response.out.write(i.key().id_or_name()+'</br>')
    self.response.out.write("""<br><b><a href="/">RETURN TO HOME</a></b><br><br>""")

class InsertURL(webapp2.RequestHandler):
  def get(self):
    insert_url=blobstore.create_upload_url('/insert')
    self.response.out.write(insert_url)

      
app = webapp2.WSGIApplication([('/', Main),
                               ('/insert', Insert),
                               ('/inserturl', InsertURL),
                               ('/remove', Remove),
                               ('/check', Check),
                               ('/find', Find),
                               ('/list', List)],
                              debug=True)
