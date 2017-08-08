#!/usr/bin/python


import os
import Cookie
import datetime
import random
import time
import sys
import cgitb
import cgi
import zipfile
import shutil
from urlparse import urlparse

cgitb.enable()


# WFM PASSWORD - CHANGE BEFORE USE ONLINE !!!
#wfmpwd = "adminpassword"
wfmpwd = ''

# attributes
hostName = cgi.escape(os.environ["HTTP_HOST"])
scriptname = cgi.escape(os.environ["SCRIPT_NAME"])
uri = scriptname + "?" + cgi.escape(os.environ["QUERY_STRING"])
"""
if os.environ.has_key("REQUEST_URI"):
  # Linux OS
  uri = cgi.escape(os.environ["REQUEST_URI"])
  
else:
  # Windows OS
  uri = scriptname + "?" + cgi.escape(os.environ["QUERY_STRING"])
"""
  

(rootpos, pyname) = os.path.split(scriptname)

qsList = dict(cgi.parse_qsl(urlparse(uri)[4]))


vfolder = ""
editFile = ""
uploadReq = ""
rfolder = ""
mainrfolder = ""
action = "list"
addprev = False
localpwd = ""




"""
### HTML TEMPLATES ###########################################################
"""

htmlfooter = """
"""

htmlMoveToLogin = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <body>
    <script language="JavaScript">
      window.location.href = '<!-- SCRIPTNAME -->';
    </script>
  </body>
</html>
"""

htmlTemplateLogin = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
  
  <meta content="text/html; charset=ISO-8859-1" http-equiv="content-type">
  <title>-- title --</title>

<style>
	body {
	font-family: Helvetica;	 
	}
	
     .footercode {
     color: #AAAAAA;
     	cursor: default;
	font-size: 11px;
     }
 
     .titlefile {
	vertical-align: middle; 
	text-align: left;
	color: rgb(44, 89, 224); 
	cursor: default;
	font-size:large;
	font-weight: bold;
     }
     
    .txtlabel {
    color: rgb(44, 89, 224); 
    cursor: default;
    font-size:large;
    font-weight: bold;
    }
    
</style>
  <script language='JavaScript'>
    var virfolder = "<!-- virtualfolder -->";
    
    function loginaction()
    {
      document.getElementById("loginform").submit();
    }
    
    
  </script>
</head>
<body>
<table style="text-align: left; width: 100%;" border="0" cellpadding="2" cellspacing="2">

  <tbody>
    <tr>
      <td>
        <form id="loginform" name="loginform" action="<!-- SCRIPTNAME -->?f=<!-- virtualfolder -->&wa=access" method="post">
          <span class="txtlabel">insert password here: </span><input type="password" name="pwd" id="pwd" class="textzone" />
        </form>
      </td>
    </tr>
    <tr>
      <td>
        <input type="button" onclick="javascript:loginaction();" value="login" />
      </td>
    </tr>
  </tbody>
</table>

<br>

<br>
""" + htmlfooter + """
</body></html>
"""



htmlTemplateUpload = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
  
  <meta content="text/html; charset=ISO-8859-1" http-equiv="content-type">
  <title>-- title --</title>

<style>
	body {
	font-family: Helvetica;	 
	}
	
     .footercode {
     color: #AAAAAA;
     	cursor: default;
	font-size: 11px;
     }
 
     .titlefile {
	vertical-align: middle; 
	text-align: left;
	color: rgb(44, 89, 224); 
	cursor: default;
	font-size:large;
	font-weight: bold;
     }
     
    .txtlabel {
    color: rgb(44, 89, 224); 
    cursor: default;
    font-size:large;
    font-weight: bold;
    }
    
</style>
  <script language='JavaScript'>
    var virfolder = "<!-- virtualfolder -->";
    
    function cancelaction()
    {
      window.location.href='<!-- SCRIPTNAME -->?f=' + escape(virfolder);
    }
    
    function uploadaction()
    {
      document.getElementById("uploadform").submit();
    }
    
    
  </script>
</head>
<body>
<table style="text-align: left; width: 100%;" border="0" cellpadding="2" cellspacing="2">

  <tbody>
    <tr>
      <td>
        <span class="titlefile"><!-- FILEPATH --></span>
      </td>
    </tr>  
    <tr>
      <td>
        <form id="uploadform" name="uploadform" action="<!-- SCRIPTNAME -->?f=<!-- virtualfolder -->&saveupload=true" method="post" enctype="multipart/form-data">
          <span class="txtlabel">select file to upload:</span>&nbsp;&nbsp;<input type="file" name="fileformobj" id="fileformobj" class="textzone" />
        </form>
      </td>
    </tr>
    <tr>
      <td>
        <input type="button" onclick="javascript:uploadaction();" value="Upload file" />&nbsp;&nbsp;&nbsp;
        <input type="button" onclick="javascript:cancelaction();" value="Cancel"/>&nbsp;
      </td>
    </tr>
  </tbody>
</table>

<br>

<br>
""" + htmlfooter + """
</body></html>
"""



htmlTemplateEdit = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
  
  <meta content="text/html; charset=ISO-8859-1" http-equiv="content-type">
  <title>-- title --</title>

<style>
	body {
	font-family: Helvetica;	 
	}
	
     .titlefile {
	vertical-align: middle; 
	text-align: left;
	color: rgb(44, 89, 224); 
	cursor: default;
	font-size:large;
	font-weight: bold;
     }
     
     .footercode {
     color: #AAAAAA;
     	cursor: default;
	font-size: 11px;
     }     
     
	.textzone {
     font-family: Courier;
     font-size: 14px;
     color: #006600;
     }
    
    
</style>
  <script language='JavaScript'>
    var virfolder = "<!-- virtualfolder -->";
    
    function cancelaction()
    {
      window.location.href='<!-- SCRIPTNAME -->?f=' + virfolder;
    }
    
    function savefile()
    {
      document.getElementById("editform").submit();
    }
    
    
  </script>
</head>
<body>
<table style="text-align: left; width: 100%;" border="0" cellpadding="2" cellspacing="2">

  <tbody>
    <tr>
      <td>
        <span class="titlefile"><!-- FILEPATH --></span>
      </td>
    </tr>  
    <tr>
      <td>
        <form id="editform" name="editform" action="<!-- SCRIPTNAME -->?f=<!-- virtualfolder -->&savefile=<!-- FILENAME -->" method="post">
          <textarea wrap="off" cols="125" rows="28" name="filecontent" id="filecontent" class="textzone"><!-- FILECONTENT --></textarea>
        </form>
      </td>
    </tr>
    <tr>
      <td>
        <input type="button" onclick="javascript:savefile();" value="Save file" />&nbsp;&nbsp;&nbsp;
        <input type="button" onclick="javascript:cancelaction();" value="Cancel"/>&nbsp;
      </td>
    </tr>
  </tbody>
</table>

<br>

<br>
""" + htmlfooter + """
</body></html>
"""




htmlTemplate = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
  
  <meta content="text/html; charset=ISO-8859-1" http-equiv="content-type">
  <title>-- title --</title>

<style>
	body {
	font-family: Helvetica;	 
	}
	
	.topdomain {
			vertical-align: top; 
			text-align: right; 
			color: rgb(44, 89, 224); 
			cursor: default;
			font-size:large;
			font-weight: bold;
	}
	
     .footercode {
     color: #AAAAAA;
     	cursor: default;
	font-size: 11px;
     }
     
    .dirstyle {
	color:#0000FF;
	text-decoration: none;        
    }

    .dirlink {
	color:#0000FF;
	text-decoration: none;
    }

    .dirlink:hover {
	text-decoration:underline;        
    }

    .filestyle {
	color:#006600;
	text-decoration: none;
    }
    
    .filelink {
	color:blue;
	text-decoration: none;	
    }

    .filelink:hover {
	text-decoration:underline;        
    }
    
    .headFiles {
	background-color: black;
	color: white;
    }

    .headrowfolder {
	background-color: #4444ff;
	width: 16px;
	height: 16px;
    }

    .headrowfile {
	background-color: #006600;
	width: 16px;
	height: 16px;	
    }
    
    .headrowzip {
	background-color: #ffcd00;
	width: 16px;
	height: 16px;	
    }
    
    .headrowempty {
	width: 16px;
	height: 16px;	
    }    
    
    .headdelfile {
	background-color: #e7261c;
	width: 16px;
	height: 16px;
    }

    .headmovefile {
	background-color: #969696;
	width: 16px;
	height: 16px;
    }

    .rowfile:hover {
	background-color: #999999;
    }
    
    .rowfolder:hover {
	background-color: #999999;
    }
    
    
</style>
  <script language='JavaScript'>
    var virfolder = "<!-- virtualfolder -->";
    
    function delfile(pathfile)
    {
      var answer = confirm("Are you sure to delete file " + pathfile + " ?")
      if (answer)
      {
        window.location.href = href='""" + pyname + """?f=' + (virfolder) + '&df=' + pathfile;
      }
    }
    
    function createfolder()
    {
      var foldername = prompt("write name of new folder", "new_folder");
      
      if (foldername.replace(' ', '') != '')
      {
        window.location.href = '""" + pyname + """?f=' + (virfolder) + '&newf=' + foldername;
      }      
    }
    
    function createzip()
    {
      var zfpath = prompt("write zip file path", "tmpfolder/website.zip");
      
      if (zfpath.replace(' ', '') != '')
      {
        window.location.href = '""" + pyname + """?f=' + virfolder + '&createzip=' + zfpath;
      }      
    
        
    }

    function createfile()
    {
      var newfilename = prompt("write name of new file", "new_file.txt");
      
      if (newfilename.replace(' ', '') != '')
      {
        window.location.href = '""" + pyname + """?f=' + (virfolder) + '&newfile=' + newfilename;
      }      
    }
    
    function movepath(frompath)
    {
      var msgout = 'move from: ' + frompath + ' to:';
      var topath = prompt(msgout, '');
      
      if (topath.replace(' ', '') != '')
      {
        window.location.href = '""" + pyname + """?f=' + (virfolder) + '&movefrom=' + frompath + '&moveto=' + topath;
      }      
    }
        
    
    function uploadfile()
    {
      window.location.href = '""" + pyname + """?f=' + (virfolder) + '&wa=upload';
    }
    
    
    function logout()
    {
      window.location.href = '""" + pyname + """?f=' + (virfolder) + '&wa=logout';
    }    
    
  </script>
</head>
<body>
<table style="text-align: left; width: 100%;" border="0" cellpadding="2" cellspacing="2">

  <tbody>
    <tr>
      <td>Server => <!-- domain --></td>
    </tr>
    <tr>
      <td>Last synced at: </td>
    </tr>
    <tr style ="background-color: black; color: white">
      <td><!-- realfolder --></td>
    </tr>
    <tr>
      <td style="vertical-align: top;"><!-- subfolders --><br>
      </td>
    </tr>
    <tr>
      <td style="vertical-align: top;">
      <hr><br>
      </td>
    </tr>
    <tr>
      <td style="vertical-align: top;"><!-- files --><br>
      </td>
    </tr>
  </tbody>
</table>

<br>

<br>
""" + htmlfooter + """
</body></html>
""" 



"""
### HTML TABLES FOR FILES AND FOLDERS #######################################
"""


# html objects
strFolders = "<table cellpadding='2' cellspacing='2' border='0'>\r\n"
strFiles = "<table cellpadding='2' cellspacing='2' border='0'>\r\n" + \
           "  <tr class='rowfile'>\r\n" + \
           "    <td colspan='6' align='right'>" + \
             "<a class='filelink' href='javascript:uploadfile();'>upload file</a>&nbsp;&nbsp;&nbsp;&nbsp;\r\n" + \
             "<a class='filelink' href='javascript:createfile();'>create empty file</a></td>\r\n" + \
           "  </tr>\r\n" + \
           "  <tr>\r\n" + \
           "    <td></td>\r\n" + \
           "    <td></td>\r\n" + \
           "    <td></td>\r\n" + \
           "    <td class='headFiles' width='59%'>Document name</td>\r\n" + \
           "    <td class='headFiles' width='20%'>Last update</td>\r\n" + \
           "    <td class='headFiles' width='20%'>File size</td>\r\n" + \
           "  </tr>\r\n"





"""
### APP FUNCTIONS #######################################
"""


# put error in output using text plain format
def writeError(section, msg):
  print "Content-type: text/plain"
  print 
  print "SECTION: " + section
  print "MESSAGE: " + msg


# join 2 path using backslash for separator
def joinPath(path1, path2):
  path1 = path1.strip()
  path2 = path2.strip()
  if len(path1) == 0:
    return path2
  
  if path2[0:1] == "/":
    path2 = path2[1:len(path2)]
  
  if path1[len(path1)-1] == "/":
    return path1 + path2
  else:
    return path1 + "/" + path2

# get wfm key stored in cookie
def getCookieKey():
  try:
    if os.environ.has_key('HTTP_COOKIE'):
      cookie = Cookie.SimpleCookie(os.environ['HTTP_COOKIE'])
    else:
      cookie = Cookie.SimpleCookie()
    
    if cookie.has_key("wfmkey") != True:
      return ""
    else:
      return cookie["wfmkey"].value
  except Cookie.CookieError, e:
    writeError('getCookieKey', "error detected")
    sys.exit()


# set wfm key stored in cookie
def setCookieKey(wfmkey):
  try:
    expiration = datetime.datetime.now() + datetime.timedelta(days=2)
    cookie = Cookie.SimpleCookie()
    cookie["wfmkey"] = wfmkey
    cookie["wfmkey"]["domain"] = hostName
    cookie["wfmkey"]["path"] = "/"
    cookie["wfmkey"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
    print cookie
  except Exception, e:
    writeError('setCookieKey', e.strerror)
    sys.exit()


# delete folder, subfolders and files by path
def deletePath(pathToDelete):
    global rfolder
    for root, dirs, files in os.walk(os.path.join(rfolder, pathToDelete), topdown=False):
      for name in files:
        try:
          os.remove(os.path.join(root, name))
        except Exception,e:
          writeError('deletePath', e.strerror)
          sys.exit()
    
      for name in dirs:
        try:
          os.rmdir(os.path.join(root, name))
        except Exception,e:
          writeError('deletePath::rmdir', e.strerror)
          sys.exit()
    
    if os.path.isdir(os.path.join(rfolder, pathToDelete)) == True:        
        os.rmdir(os.path.join(rfolder, pathToDelete))
    
    if os.path.isfile(os.path.join(rfolder, pathToDelete)) == True:        
        os.remove(os.path.join(rfolder, pathToDelete))


# get list of files and folders path to compress
def dirEntries(dir_name, subdir, notInclude):

  fileList = []
  
  # loop for each file in <dir_name>
  for file in os.listdir(dir_name):        
    # create dir full path
    dirfile = os.path.join(dir_name, file)        
    # check for file
    if os.path.isfile(dirfile):            
      # check for file filter
      if len(notInclude) == 0:                
        # add file to list
        fileList.append(dirfile)
          
      else:                
        # check for file to exclude
        if file != notInclude:                    
          # append file to list
          fileList.append(dirfile)
                
    # recursively access file names in subdirectories
    elif os.path.isdir(dirfile) and subdir:
      fileList.extend(dirEntries(dirfile, subdir, notInclude))
          
  return fileList


# extract folders and files from zip file    
def extractFiles(filepath):
    global rfolder
    global vfolder

    zfile = zipfile.ZipFile(os.path.join(rfolder,filepath))

    for name in zfile.namelist():
      
      (dirname, filename) = os.path.split(name)
      if dirname != "":
        if not os.path.exists(os.path.join(rfolder,dirname)):	
          try:
            os.mkdir(os.path.join(rfolder,dirname))
          except Exception,e:
            writeError('extractFiles::mkdir ' + os.path.join(rfolder,dirname), e.strerror)
            sys.exit()
            
      if filename != "":
        try:          
          fd = open(os.path.join(rfolder, name), "w")
          fd.write(zfile.read(name))
          fd.close()

        except Exception,e:
          writeError('extractFiles ' + os.path.join(rfolder, name), e.strerror)
          sys.exit()


# create zip file 
def compressFiles(folderpath, outzipfile):
  global rfolder
  global vfolder
  
  # remove old temp zip file
  if os.path.exists(outzipfile + ".tmp") == True:
    os.remove(outzipfile + ".tmp")
  
  try:
    # generate files and folders list
    zipFilesList = dirEntries(folderpath, True, "")
    
    # create zip file manager
    zipMan = zipfile.ZipFile(outzipfile + ".tmp", 'w', zipfile.ZIP_DEFLATED)
    
    # loop for each file in folder
    for f in zipFilesList:
      # add file to zip
      zipMan.write(f)
    
    # close zip file
    zipMan.close()
    
    # rename file
    os.rename(outzipfile + ".tmp", outzipfile)
    
  except Exception,e:
    writeError('compressFiles ' + folderpath, e.strerror)
    sys.exit()
  

# upload from local file
def uploadFile():
  global rfolder
  global vfolder
    
  try: # Windows needs stdio set for binary mode.
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
  except ImportError:
    pass
  
  try:
    form = cgi.FieldStorage()
    if not form.has_key("fileformobj"): 
      return
    fileitem = form["fileformobj"]
    if not fileitem.file:
      return
    fout = file (os.path.join(rfolder, fileitem.filename), 'wb')
    while 1:
      chunk = fileitem.file.read(1000)
      if not chunk: 
        break
      fout.write (chunk)
      
    fout.close()  
      
  except Exception,e:
    writeError('uploadFile ' + os.path.join(rfolder, fileitem.filename), e.strerror)
    sys.exit()
  

# detect if file is binary or not
def is_binary(filename):
    fin = open(filename, 'rb')
    try:
        CHUNKSIZE = 1024
        chunk = fin.read(CHUNKSIZE)
        if '\0' in chunk: # found null byte
          return True
        else:
          return False

    except Exception,e:
      writeError('is_binary', e.strerror)
      sys.exit()





def addFolder(name):
    global strFolders
    global vfolder
    
    strFolders += "  <tr class='rowfolder'>\r\n" + \
                  "    <td><div class='headrowempty'></div></td>\r\n" + \
                """    <td><a href="javascript:movepath('""" + joinPath(vfolder,name) + """');" title="move folder"><div class="headmovefile"></div></a></td>\r\n""" + \
                """    <td><a href="javascript:delfile('""" + name + """');" title='delete folder'><div class='headdelfile'></div></a></td>\r\n""" + \
                  "    <td width='99%'><a class='dirlink' " + \
                  "        href='" + pyname + "?f=" + joinPath(vfolder, name) + "'>" + (name) + "</a></td>\r\n" + \
                  "  </tr>\r\n"
    



def addFile(name):
    global strFiles
    global vfolder
    global rfolder
    global rootpos
    global pyname

    statinfo = os.stat(os.path.join(rfolder, name))
    file_ext = os.path.splitext(name)[1]
    
    isBinary = is_binary(os.path.join(rfolder, name))
    
    # verify for binary file
    if isBinary != True:
      # plain text
      editCode  =   "    <td><a href='" + pyname + "?f=" + vfolder + "&edit=" + name + "&wa=edit' title='edit file'><div class='headrowfile'></div></a></td>\r\n"
      editCode += """    <td><a href="javascript:movepath('""" + joinPath(vfolder,name) + """');" title="move file"><div class="headmovefile"></div></a></td>\r\n"""
    
    else:
      # binary
      editCode  =   "    <td><div class='headrowempty'></div></td>\r\n"
      editCode += """    <td><a href="javascript:movepath('""" + joinPath(vfolder,name) + """');" title="move file"><div class="headmovefile"></div></a></td>\r\n"""
    
    if file_ext.lower() != ".zip":    
      # NOT zip file
      strFiles += "  <tr class='rowfile'>\r\n" + \
                  editCode + \
                """    <td><a href="javascript:delfile('""" + name + """');" title='delete file'><div class='headdelfile'></div></a></td>\r\n""" + \
                  "    <td width='59%'>" + name + "</td>\r\n" + \
                  "    <td class='filestyle' width='20%'>" + time.strftime("%Y-%m-%d %H:%M", time.localtime(statinfo.st_mtime)) + "</td>\r\n" + \
                  "    <td class='filestyle' width='20%'>" + str(statinfo.st_size / 1024) + " Kb</td>\r\n" + \
                  "  </tr>\r\n"
    else:
      # zip file
      strFiles += "  <tr class='rowfile'>\r\n" + \
                  "    <td><a href='" + pyname + "?f=" + vfolder + "&unzip=" + name + "' title='extract file'><div class='headrowzip'></div></a></td>\r\n" + \
                """    <td><a href="javascript:movepath('""" + joinPath(vfolder,name) + """');" title="move file"><div class="headmovefile"></div></a></td>\r\n""" + \
                """    <td><a href="javascript:delfile('""" + name + """');" title='delete zip'><div class='headdelfile'></div></a></td>\r\n""" + \
                  "    <td width='59%'>" + name + "</td>\r\n" + \
                  "    <td class='filestyle' width='20%'>" + time.strftime("%Y-%m-%d %H:%M", time.localtime(statinfo.st_mtime)) + "</td>\r\n" + \
                  "    <td class='filestyle' width='20%'>" + str(statinfo.st_size / 1024) + " Kb</td>\r\n" + \
                  "  </tr>\r\n"


                
"""
### READ ACTION ###########################################################
"""

if qsList.has_key("wa"):
    # web action
    action = qsList["wa"]


if action == "logout":
  # log out
  setCookieKey("")
  htmlMoveToLogin = htmlMoveToLogin.replace("<!-- SCRIPTNAME -->", pyname)
  print "Content-type: text/html"
  print  
  print htmlMoveToLogin
  sys.exit()


if action == "login":
  # login page request
  # update informations
  htmlTemplateLogin = htmlTemplateLogin.replace("-- title --", "Pulp Server 2.13")
  htmlTemplateLogin = htmlTemplateLogin.replace("<!-- SCRIPTNAME -->", pyname)
  print "Content-type: text/html"
  print
  print htmlTemplateLogin
  sys.exit()

if action == "access":
  # check for password
  form = cgi.FieldStorage()
  if not form.has_key("pwd"):
    # not autorized
    htmlMoveToLogin = htmlMoveToLogin.replace("<!-- SCRIPTNAME -->", pyname + "?wa=login&msg=nopwd")
    print "Content-type: text/html"
    print
    print htmlMoveToLogin
    sys.exit()
    
  sendkey = form["pwd"].value
  
  if sendkey != wfmpwd:
    # not autorized
    htmlMoveToLogin = htmlMoveToLogin.replace("<!-- SCRIPTNAME -->", pyname + "?wa=login&msg=pwdnotequal")
    print "Content-type: text/html"
    print
    print htmlMoveToLogin
    sys.exit()
  
  setCookieKey(sendkey)
  
  htmlMoveToLogin = htmlMoveToLogin.replace("<!-- SCRIPTNAME -->", pyname)
  print "Content-type: text/html"
  print  
  print htmlMoveToLogin
  sys.exit()


"""
### CHECK FOR PERMISSION ###########################################################
"""
# get stored password
localpwd = getCookieKey()


# check for same authorized password
if localpwd != wfmpwd:
  # not autorized
  htmlMoveToLogin = htmlMoveToLogin.replace("<!-- SCRIPTNAME -->", pyname + "?wa=login")
  print "Content-type: text/html"
  print
  print htmlMoveToLogin
  sys.exit()





"""
### READ QUERYSTRING ###########################################################
"""

# check virtual path presence

if qsList.has_key("f"):
    # update virtual path
    vfolder = qsList["f"]


if qsList.has_key("edit"):
    # file name to edit
    editFile = qsList["edit"]

if qsList.has_key("uploadreq"):
    # upload file request
    uploadReq = qsList["uploadreq"]


# update real folder path
rfolder = os.path.abspath("./" + vfolder)
mainrfolder = os.path.abspath("./") 
vfolder = rfolder.replace(mainrfolder, "")
vfolder = vfolder.replace("\\", "/")


if rfolder != mainrfolder:
    addprev = True


# verify for upload file
if qsList.has_key("saveupload"):
    # verify for save upload file
    if qsList["saveupload"] == "true":
      uploadFile()

# verify for delete request    
if qsList.has_key("df"):
    # delete file or folder
    deletePath(qsList["df"])

# verify for unzip request    
if qsList.has_key("unzip"):
    # unzip files
    extractFiles(qsList["unzip"])

# verify for zip request    
if qsList.has_key("createzip"):
    # zip files
    compressFiles(rfolder, os.path.abspath("./" + qsList["createzip"]))


# verify for new folder
if qsList.has_key("newf"):
    # create new folder
    try:
      os.mkdir(os.path.join(rfolder, qsList["newf"]))
    except Exception,e:
      writeError('newf::mkdir ' + os.path.join(rfolder, qsList["newf"]), e.strerror)
      sys.exit()

# verify for new file
if qsList.has_key("newfile"):
    # create new file
    try:
      fd = open(os.path.join(rfolder, qsList["newfile"]), "w")
      fd.write('')
      fd.close()
    except Exception,e:
      writeError('newfile ' + os.path.join(rfolder, qsList["newfile"]), e.strerror)
      sys.exit()

# verify for file to save
if qsList.has_key("savefile"):  
  try:
    # Create instance of FieldStorage 
    form = cgi.FieldStorage()
    textcontent = form.getvalue('filecontent')
    fd = open(os.path.join(rfolder, qsList["savefile"]), "w")
    fd.write(textcontent)
    fd.close()
  except Exception,e:
    writeError('savefile ' + os.path.join(rfolder, qsList["savefile"]), e.strerror)
    sys.exit()




# verify for file to save
if qsList.has_key("movefrom"):
  if qsList.has_key("moveto"):
    try:
      shutil.move(os.path.abspath("./" + qsList["movefrom"]), os.path.abspath("./" + qsList["moveto"]))
    except Exception,e:
      writeError('movefrom-to ' + qsList["movefrom"] + " - " + qsList["moveto"], e.strerror)
      sys.exit()






"""
### UPDATE TEMPLATES ###########################################################
"""


# add html header
print "Content-type: text/html"
print

# check for requested action
if action == "list":
  ### Folders and files list ############################## 
  strFolders += "  <tr class='rowfolder'>\r\n" + \
                "    <td colspan='4' align='right'>" + \
                "        <a class='dirlink' href='javascript:logout();'>Home</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + \
                "        <a class='dirlink' href='javascript:createzip();'>zip folder</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + \
                "        <a class='dirlink' href='javascript:createfolder();'>create empty folder</a>" + \
                "    </td>\r\n" + \
                "  </tr>\r\n"
  
  
  if addprev == True:
      strFolders += "  <tr class='rowfolder'>\r\n" + \
                    "    <td><div class='headrowempty'></div></td>\r\n" + \
                    "    <td><div class='headrowempty'></div></td>\r\n" + \
                    "    <td><div class='headrowempty'></div></td>\r\n" + \
                    "    <td width='99%'><a class='dirlink' " + \
                    "        href='" + pyname + "?f=" + vfolder + "/..'>" + cgi.escape("..") + "</a></td>\r\n" + \
                    "  </tr>\r\n"
  
  
  # update informations
  htmlTemplate = htmlTemplate.replace("<!-- virtualfolder -->", cgi.escape(vfolder.replace("\\", "/")))
  htmlTemplate = htmlTemplate.replace("<!-- domain -->", cgi.escape(hostName))
  htmlTemplate = htmlTemplate.replace("<!-- folder -->", cgi.escape(vfolder))
  htmlTemplate = htmlTemplate.replace("<!-- realfolder -->", cgi.escape(rfolder))
  htmlTemplate = htmlTemplate.replace("-- title --", "Pulp Server 2.13")
  
  # retrieve folder items list
  folderfile = os.listdir(rfolder)
  folderfile.sort()
  
  # update created lists
  for sf in folderfile:
      if os.path.isdir(os.path.join(rfolder, sf)) == True:
          addFolder(sf)
      #if os.path.isdir(sf):
      else:
          addFile(sf)
  
  
  strFolders += "</table>\r\n"
  strFiles += "</table>\r\n"
  
  # update html code
  htmlTemplate = htmlTemplate.replace("<!-- subfolders -->", strFolders)
  htmlTemplate = htmlTemplate.replace("<!-- files -->", strFiles)
  
  print htmlTemplate  + "<!-- hostname = " + hostName + " -->\r\n" + \
    "<!-- rootpos = " + rootpos + " -->\r\n" + \
    "<!-- scriptname = " + scriptname + " -->\r\n" + \
    "<!-- uri = " + uri + " -->\r\n"


elif action == "upload":
  ### Upload file ##############################
  
  # update informations
  htmlTemplateUpload = htmlTemplateUpload.replace("<!-- virtualfolder -->", vfolder)
  htmlTemplateUpload = htmlTemplateUpload.replace("-- title --", "Pulp Server 2.13")
  htmlTemplateUpload = htmlTemplateUpload.replace("<!-- SCRIPTNAME -->", pyname)

  print htmlTemplateUpload



elif action == "edit":
  ### Edit file ##############################
  
  # update informations
  htmlTemplateEdit = htmlTemplateEdit.replace("<!-- virtualfolder -->", vfolder)
  htmlTemplateEdit = htmlTemplateEdit.replace("<!-- FILEPATH -->", "Edit " + vfolder + "/" + editFile)
  htmlTemplateEdit = htmlTemplateEdit.replace("<!-- FILENAME -->", editFile)
  htmlTemplateEdit = htmlTemplateEdit.replace("-- title --", "Pulp Server 2.13")
  htmlTemplateEdit = htmlTemplateEdit.replace("<!-- SCRIPTNAME -->", pyname)
  
  fd = open(os.path.join(rfolder, editFile), "r")
  filecontent = ""
  fline = fd.readline()
  while fline != "":
    filecontent += fline
    fline = fd.readline()
    
  fd.close()
  htmlTemplateEdit = htmlTemplateEdit.replace("<!-- FILECONTENT -->", filecontent)
  
  print htmlTemplateEdit




