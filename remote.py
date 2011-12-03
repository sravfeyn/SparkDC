#!/usr/bin/env python2

  ## Load the basic modules we want.
import re, os, sys, time, commands, getopt, types
  ## This is the Expect module.
import pexpect
import getpass

#-------------------------------------------
  ## Initialize the module.
class Ssh:
  def __init__(self):
      ## Three responses we might expect.
    self.Initial_Responses = ['Are you sure', 
      'password:', pexpect.EOF] 


#-------------------------------------------
  def Ssh_Method1(self, User="", Password="",
    Host="", Timeout=120, Response='', Command="", 
    Opposite_Match = 0):

    if Command == '': return (-1, '')
    elif Response == '': return (-2, '')

      ## Execute the command.
    child = pexpect.spawn(Command)

      ## Get the first response.
    i = child.expect (self.Initial_Responses, Timeout)
        ## The first reponse is to accept the key.
    if i==0:
      T = child.read(100)
      child.sendline("yes")
      child.expect('password:', Timeout)
      child.sendline(Password)
        ## The second response sends the password.
    elif i == 1:
      child.sendline(Password)
        ## Otherwise, there is an error.
    else:
      Str1 = str(child.before)
      return (-3, 'ERROR: Unknown1: ' + Str1)

      ## Get the next response.
    Possible_Responses = ['password:', pexpect.EOF]
    i = child.expect (Possible_Responses, Timeout)
      ## If it asks for a password, error.

    if i == 0:
      return (-4, 'ERROR: Incorrect password.')
      ## Otherwise we are okay.
    else:
        ## Get the output before the match.
      Output = str(child.before)

        ## Compile a regular expression.
      RE1 = re.compile(Response)

        ## If OM = 1, it means "don't match".
      OM = Opposite_Match
        ## If we detecting a positive match and
        ## it works, return good.
      if (OM == 0) and (RE1.search(Output)):
        return (0, Output)
        ## If we are trying not to detect a match
        ## and it doesn't match, return good.
      elif (OM != 0) and (not RE1.search(Output)):
        return (0, Output)
      else :
        ## Otherwise, there is an error.
        return (-6, str(child.after))

#-------------------------------------------- 
    ## This method detects if a file exists.
  def File_Test_Exist(self,Destination_File="", 
    User="", Password="", Host="", Timeout=120):

    Command = """ssh -l %s %s 'if test -e %s ;\
 then echo "GOOD: FILE EXISTS" ; fi'""" \
      %(User, Host, Destination_File)
    Response = 'GOOD: FILE EXISTS'

    (Error, Message) = self.Ssh_Method1(User=User,
      Password=Password, Host=Host, Timeout=Timeout
     , Response=Response, Command=Command)

    if Error == -5:
     Message ="ERROR: file doesn't exist. "+Message
    return (Error, Message)

#-------------------------------------------
    ## This transfers a file using rsync with ssh.
  def Script_Transfer(self, Destination_Script="",
    User="", Password="", Host="", Source_Script=""
    , Timeout=120):

    Command = """rsync -e ssh -av %s %s@%s:%s"""\
      %(Source_Script, User, Host, 
      Destination_Script)
    Response = 'rsync error:'

    (Error, Message) = self.Ssh_Method1(User=User,
      Password=Password, Host=Host, Timeout=Timeout
     , Response=Response, Command=Command, 
     Opposite_Match=1)

    return (Error, Message)

#---------------------------------------------
  def Script_Execute(self, Destination_Script="", 
    User="", Password="", Host="", Timeout=120):

      ## Use local python if available.
    Python_Command = "/usr/local/python/bin/python"
    (Test1,Output) = self.File_Test_Exist(
      Destination_File=Python_Command, User=User, 
      Password=Password, Host=Host)
    if Test1 != 0: Python_Command = "python"

    Command = """ssh -l %s %s '%s %s'""" %(User, 
      Host, Python_Command, Destination_Script)
    Response = 'GOOD:'

    (Error, Message) = self.Ssh_Method1(User=User,
      Password=Password, Host=Host, Timeout=Timeout
     , Response=Response, Command=Command)

    return (Error, Message)

#-------------------------------------------
  def Download_File(self, File_Client="", 
    File_Destination="", User="", Password="", 
    Host="", Timeout=3600):

    Command = """rsync -av -e ssh %s@%s:%s %s""" %(
      User, Host, File_Client, File_Destination)
    Response = 'rsync error:'

      ## We set Opposite_Match to 1 because
      ## we don't want to match the reposnse.
    (Error, Message) = self.Ssh_Method1( User=User,
      Password=Password, Host=Host, Timeout=Timeout
      , Response=Response, Command=Command, 
      Opposite_Match=1 )

    return (Error, Message)
#-------------------------------------------

