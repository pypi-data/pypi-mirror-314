#!/usr/bin/env python
#===============================================================================
# gmme-pylib for Python
# Copyright (c) 2002 - 2023, GMM Enterprises, LLC.
# Licensed under the GMM Software License
# All rights reserved 
#===============================================================================
#	Author:	David Crickenberger
# ------------------------------------------------------------------------------
#	Packages:
#		Utils::CmdLine
#
# 	Description:
#		Command line processor module.
#
#===============================================================================
# $Log: $
#===============================================================================
from time import strftime

import datetime
import os
import socket
import sys
import time
import traceback

import gmmePylib.Utils.Object
import gmmePylib.Utils.Other


#-------------------------------------------------------------------------------
#-- Object manager routines for Global functions/objects
#-------------------------------------------------------------------------------
class LoggerObjs_() :
    m_objs = None
    
    def __init__(self) :
        self.m_objs = []

    def __del__(self) :
        self.m_objs = []
    
    def add(self, a_loggerObj) :
        self.m_objs.append(a_loggerObj)

    def remove(self, a_loggerObj) :
        l_id = id(a_loggerObj)
        for l_i in range(0, len(self.m_objs) - 1) :
            if l_id == id(self.m_objs[l_i]) :
                del self.m_objs[l_i]
                break


#-------------------------------------------------------------------------------
#-- Global functions/objects
#-------------------------------------------------------------------------------
g_loggerObj = None
g_loggerObjs_ = LoggerObjs_()

def Debug(a_msg) :
    if g_loggerObj is not None : g_loggerObj.LogDebug(a_msg, 1)
def Fatal(a_msg) :
    if g_loggerObj is not None : g_loggerObj.LogFatal(a_msg, 1)
def Info(a_msg) :
    if g_loggerObj is not None : g_loggerObj.LogInfo(a_msg, 1)
def Raw(a_msg) :
    if g_loggerObj is not None : g_loggerObj.LogRaw(a_msg, 1)
def Sql(a_msg) :
    if g_loggerObj is not None : g_loggerObj.LogSql(a_msg, 1)
def Warn(a_msg) :
    if g_loggerObj is not None : g_loggerObj.LogWarning(a_msg, 1)
def Warning(a_msg) :
    if g_loggerObj is not None : g_loggerObj.LogWarning(a_msg, 1)

def LogDebug(a_msg) :
    if g_loggerObj is not None : g_loggerObj.LogDebug(a_msg, 1)
def LogFatal(a_msg) :
    if g_loggerObj is not None : g_loggerObj.LogFatal(a_msg, 1)
def LogInfo(a_msg) :
    if g_loggerObj is not None : g_loggerObj.LogInfo(a_msg, 1)
#def LoggerGlobalFunctions():
#    global LogRaw
def LogRaw(a_msg) :
    if g_loggerObj is not None : g_loggerObj.LogRaw(a_msg, 1)
def LogSql(a_msg) :
    if g_loggerObj is not None : g_loggerObj.LogSql(a_msg, 1)
def LogWarn(a_msg) :
    if g_loggerObj is not None : g_loggerObj.LogWarning(a_msg, 1)
def LogWarning(a_msg) :
    if g_loggerObj is not None : g_loggerObj.LogWarning(a_msg, 1)


#-------------------------------------------------------------------------------
#-- Static functions/objects
#-------------------------------------------------------------------------------
def logObjectFuncsCreate_(a_obj):

    global g_loggerObj
    
    if g_loggerObj is None:
        g_loggerObj = a_obj


def logObjectFuncsRemove_(a_obj):

    global g_loggerObj

    if id(g_loggerObj) == id(a_obj):
        g_loggerObj = None

    g_loggerObjs_.remove(a_obj)
    

#-------------------------------------------------------------------------------
#-- Class LoggerException
#-------------------------------------------------------------------------------
class LoggerException():

    def __init__(self, a_msg):
        self.m_msg = a_msg

    
#-------------------------------------------------------------------------------
#-- Class Logger
#-------------------------------------------------------------------------------
class Logger() :

    #---------------------------------------------------------------------------
    #-- Members
    #---------------------------------------------------------------------------


    #---------------------------------------------------------------------------
    #-- ctor
    #---------------------------------------------------------------------------
    def __init__(self, **a_args):

        global g_loggerObjs_


        #-----------------------------------------------------------------------
        #-- initialize with default values
        self.m_hndl = None
        self.m_file = None
        self.m_logPath = None
        self.m_logFile = None
        self.m_logFull = None
        self.m_isOpen = False
        self.m_host = socket.gethostname().ljust(15)
        self.m_append = False
        self.m_stdout = True
        self.m_dtfmt = '%Y%m%d%H%M%S'
        self.m_pathsep = os.path.sep


        #-----------------------------------------------------------------------
        #-- see if any parameters was passed, and initialize some to a default
        #-- value if not passed
        if len(a_args) > 0: self.argsHelper_(a_args)

        if self.m_file is None: sys.argv[0]
        if self.m_logPath is None: self.m_logPath = os.path.dirname(self.m_file)
        if self.m_logFile is None: self.m_logFile = os.path.basename(self.m_file) + ".log"

        self.argsCheck_()

        g_loggerObjs_.add(self)


    #---------------------------------------------------------------------------
    #-- dtor
    #---------------------------------------------------------------------------
    def __del__(self):

        global g_loggerObjs_

        #-----------------------------------------------------------------------
        #-- close if open
        if self.m_isOpen: self.m_hndl.close()
        if g_loggerObjs_ is not None: g_loggerObjs_.remove(self)


    #---------------------------------------------------------------------------
    #-- argsCheck_
    #---------------------------------------------------------------------------
    def argsCheck_(self):
        if self.m_file is None: raise LoggerException("'file' not initialized")
        if self.m_logPath is None: raise LoggerException("'logPath' not initialized")
        if self.m_logFile is None: raise LoggerException("'logFile' not initialized")


    #---------------------------------------------------------------------------
    #-- argsHelper_
    #---------------------------------------------------------------------------
    def argsHelper_(self, a_args):

        #-----------------------------------------------------------------------
        #-- process args
        l_members = {
            'file': 'm_file',
            'logPath': 'm_logPath',
            'logFile': 'm_logFile',
            'append': 'm_tmpAppend',
            'stdout': 'm_tmpStdout',
            'dtfmt': 'm_dtfmt'
        }
        l_found = gmmePylib.Utils.Object.Init(self, l_members, a_args)


        #-----------------------------------------------------------------------
        #-- finish processing args and make sure require ones are set
        if l_found:
            if 'tmpAppend' in self.__dict__: self.m_append = gmmePylib.Utils.Other.IsYesOrNo(self.m_tmpAppend)
            if 'tmpStdout' in self.__dict__: self.m_stdout = gmmePylib.Utils.Other.IsYesOrNo(self.m_tmpStdout)


    #---------------------------------------------------------------------------
    #-- close
    #---------------------------------------------------------------------------
    def Close(self):
        
        self.m_hndl.close()
        
        self.m_file = None
        self.m_logPath = None
        self.m_logFile = None
        self.m_logFull = None
        self.m_isOpen = False
        self.m_append = False
        self.m_stdout = True
        self.m_dtfmt = "%Y%m%d%H%M%S"

        logObjectFuncsRemove_(self)


    #---------------------------------------------------------------------------
    #-- open
    #---------------------------------------------------------------------------
    def Open(self, **a_args):

        #-----------------------------------------------------------------------
        #-- we have no parameters, so make sure uid,pwd,sid were passed into
        #-- new.
        if len(a_args) > 0: self.argsHelper_(a_args)
        self.argsCheck_()


        #-----------------------------------------------------------------------
        #-- if log is currently open, then close
        #if self.m_isOpen : self.close()


        #-----------------------------------------------------------------------
        #-- initialize the following:
        #--   1: set date/time
        l_dttm = strftime(self.m_dtfmt)

        #--   2: filename
        self.m_file = os.path.basename(self.m_file)
        self.m_file.ljust(10, ' ')
        l_rc = 0


        #-----------------------------------------------------------------------
        #-- build full name for log file
        self.m_logPath.rstrip(os.path.sep)
        self.m_logFull = self.m_logPath
        if self.m_logPath != '':
            gmmePylib.Utils.Other.OSMakeFolder(self.m_logPath)
            self.m_logFull += os.path.sep
        self.m_logFull += self.m_logFile

        l_tmp = os.path.splitext(self.m_logFull)
        if l_tmp[1] == '': self.m_logFull += '_' + l_dttm + '.log'


        #-----------------------------------------------------------------------
        #-- open the log file or append to the log file
        l_otype = 'w'
        if self.m_append: l_otype = 'a'

        try :
            self.m_hndl = open(self.m_logFull, l_otype, 1)
            self.m_isOpen = True
        except IOError:
            self.m_isOpen = False
            #traceback.print_exc()

        if self.m_isOpen: logObjectFuncsCreate_(self)

        return self.m_isOpen


    #---------------------------------------------------------------------------
    #-- logRaw
    #---------------------------------------------------------------------------
    def LogRaw(self, a_msg):

        if self.m_isOpen:
            self.m_hndl.write(a_msg + '\n')
            self.m_hndl.flush()
        if self.m_stdout: print(a_msg)


    #---------------------------------------------------------------------------
    #-- msg_
    #---------------------------------------------------------------------------
    def msg_(self, a_type, a_msg, a_level = 0):

        #-----------------------------------------------------------------------
        #-- determine calling function
        l_level = a_level + 1
        
        l_curFrame = sys._getframe(l_level)
        l_file = l_curFrame.f_code.co_filename
        if l_file == '<string>': l_file = os.path.basename(sys.argv[0])
        l_line = l_curFrame.f_lineno
        #l_func = l_curFrame.f_code.co_name
        l_func = l_file


        #-----------------------------------------------------------------------
        #-- determine date/time
        l_time = time.time()
        l_timeSec, l_timeMsec = gmmePylib.Utils.Other.SplitTimeSeconds(l_time)


        #-----------------------------------------------------------------------
        #-- build message
        l_msg = gmmePylib.Utils.Other.FormatTime(l_time, '%m/%d/%Y %H:%M:%S.') + str(l_timeMsec)[0:3].zfill(3) + ' '
        l_msg += self.m_host + ' '
        l_msg += self.m_file + ' '
        l_msg += l_func.ljust(20) + ' '
        l_msg += str(l_line).rjust(5) + ' '
        l_msg += 'system   '
        l_msg += a_type.ljust(6) + ' '
        l_msg += a_msg

        if self.m_isOpen:
            self.m_hndl.write(l_msg + '\n')
            self.m_hndl.flush()
        if self.m_stdout: print(l_msg)


    #---------------------------------------------------------------------------
    #-- log functions
    #---------------------------------------------------------------------------
    def Debug(self, a_msg, a_level = 0): self.msg_('debug', a_msg, a_level + 1)
    def Fatal(self, a_msg, a_level = 0): self.msg_('fatal', a_msg, a_level + 1)
    def Info(self, a_msg, a_level = 0): self.msg_('info', a_msg, a_level + 1)
    def Sql(self, a_msg, a_level = 0): self.msg_('sql', a_msg, a_level + 1)
    def Warn(self, a_msg, a_level = 0): self.msg_('warn', a_msg, a_level + 1)
    def Warning(self, a_msg, a_level = 0): self.msg_('warn', a_msg, a_level + 1)

    def LogDebug(self, a_msg, a_level = 0): self.msg_('debug', a_msg, a_level + 1)
    def LogFatal(self, a_msg, a_level = 0): self.msg_('fatal', a_msg, a_level + 1)
    def LogInfo(self, a_msg, a_level = 0): self.msg_('info', a_msg, a_level + 1)
    def LogSql(self, a_msg, a_level = 0): self.msg_('sql', a_msg, a_level + 1)
    def LogWarn(self, a_msg, a_level = 0): self.msg_('warn', a_msg, a_level + 1)
    def LogWarning(self, a_msg, a_level = 0): self.msg_('warn', a_msg, a_level + 1)


    #---------------------------------------------------------------------------
    #-- member access functions
    #---------------------------------------------------------------------------
    def Append(self): return self.m_append
    def DateFormat(self): return self.m_dtfmt
    def Dtfmt(self): return self.m_dtfmt
    def File(self): return self.m_file
    def IsOpen(self): return self.m_isOpen
    def LogFile(self): return self.m_logFile
    def LogFull(self): return self.m_logFull
    def LogPath(self): return self.m_logPath
    def Stdout(self): return self.m_stdout


#-------------------------------------------------------------------------------
#-- Create wrapper functions
#-------------------------------------------------------------------------------
def CreateLogger(**a_argv):
    return Logger(**a_argv)


#-------------------------------------------------------------------------------
#-- Generate logfile name from appname
#-------------------------------------------------------------------------------
#def LogFileFromAppname():
#    l_appname = sys.argv[0]
#    l_appname = os.path.basename(sys.argv[0])
#    l_appname = os.path.splitext(l_appname)[0]

#    return l_appname
 

#===============================================================================
# Self test of module
#===============================================================================
'''
if __name__ == "__main__" :

    l_t1 = time.time()
    l_t2 = time.localtime(l_t1)
    l_ts = time.strftime('%Y%m%d%H%M%S', l_t2)

    l_appname = sys.argv[0]
    l_logger = Logger(file=l_appname, logpath='d:\\junk\\tlogs', logfile='test.log', append=True)
    l_logger.Open()
    l_logger.LogRaw('test message 1')
#    LogRaw('test message 2')
    l_rc = 0
'''