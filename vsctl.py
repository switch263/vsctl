#!/usr/bin/env python
"""
        File name: vsctl.py
        Author: Max Forma
        Description: Simpler control over VSFTPD daemon utilizing MySQL for user database.
        Date created: 7/28/2016
        Date last modified: 7/28/2016
        Python Version: 2.7
"""

from config import *
import sys
import os
import random
import string
import MySQLdb


def helptxt():
    print "Usage: vsctl <command> <args>"
    print "Commands:"
    print "adduser <username> - New user will be added with a randomly generated password, and their home folder " \
          "created in /srv/ftp/ftpusers/virtual/. User/pass will display if successful."
    print "chpass <username> - Change an existing user's password"
    print "deluser <username> -  Delete a user (DOES NOT REMOVE USER FTP DIRECTORY)"
    print "diskuse <username> - Get disk usage for specified user"
    print ""
    print "See source code for further documentation."
    print ftphome
    print mysqlhost
    print mysqluser
    print mysqlpass
    print mysqldb
    print passlen
    exit()


if len(sys.argv) < 2:
    helptxt()

randpass = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(passlen)])
username = None
command = sys.argv[1]
if sys.argv[2]:
    username = sys.argv[2]


def createuser(user):
    try:
        con = MySQLdb.connect(mysqlhost, mysqluser, mysqlpass, mysqldb)
        con.query("INSERT INTO accounts (username, pass) VALUES ('" + user + "', md5('" + randpass + "'))")
        result = con.use_result()
    except Exception as e:
        print "Error: %s" % e.args[0]
        sys.exit(1)
    os.system("mkdir " + ftphome + "/" + username)
    os.system("chown vsftpd.users " + ftphome + "/" + username)
    print "User successfully created and now able to access ftp.zenoss.com."
    print "user: " + username + ""
    print "pass: " + randpass + ""
    return


def deluser(user):
    sql = "SELECT id,username FROM accounts WHERE username LIKE '%" + user + "%';"
    sql2 = "SELECT id,username FROM accounts WHERE username LIKE '%{}%';".format(user)
    print sql2
    try:
        con = MySQLdb.connect(mysqlhost, mysqluser, mysqlpass, mysqldb)
        con.query(sql2)
        result = con.use_result()
        if result.num_rows() > 1:
            print "too many results, try harder"
        else:
            try:
                user = dict(result)['username']
                delid = dict(result)['id']
                print user
                print delid
            except KeyError:
                print "unexpected result."
            try:
                print "Doing deletion stuffs (not actually, yet)"
            except:
                print "oh no mysql broke"
    except Exception as e:
        print "TOTALLY SIDEWAYS"
        print "Error %s" % e.args[0]


if command == "adduser" and username is not None:
    print "You want to make a new user %s." % username
    createuser(username)
elif command == "deluser" and username is not None:
    print "You want to delete a user %s." % username
    deluser(username)
elif command == "diskuse" and username is not None:
    os.system("du -hs " + ftphome + "/" + username)
else:
    helptxt()
