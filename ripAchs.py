#! /usr/bin/python

# ripAchs.py - a rewrite of my Perl script for parsing out achievements from xbox.com pages
#    I did this as an exercise in learning Python.
#
# TODO: 
#    - currently times are read from Xbox.com pages in UTC time, and not
#        converted to localtime like in my Perl script.  This is due
#        to the fact I haven't yet been able to find a Python equivalent 
#        to the DateTime module in Perl.  As a result, toDateTimeObj
#        is currently unimplemented

import sys
import re
import glob
import pprint
import datetime
import urllib

# "Constants"

# name of the file to read game icon images from
GAMESFILE = "games.html"

# URL to the icon for the little GS logo
GICONURL = "http://live.xbox.com/xweb/lib/images/G_Icon_External.gif"

# Global variables used by printIndent()
g_indent = 0 
g_verbose = True 

#
# genKeyFromGameTitle (title) - generates a hash key from the game title stored in title
#    Note: this hashing function can most definitely cause collisions to occur
#
def genKeyFromGameTitle (title):
    # just keep spaces, letters, and numbers
    return re.sub (r'[^a-zA-Z \d]+', '',
        re.sub (r'&#\d+;', '', title));

#
# commify (num) - puts commas into the string num.  Taken from:
#    http://docstore.mik.ua/orelly/perl/cookbook/ch02_18.htm 
#    and converted to Python by Adam Parkin
#
def commify (num): 
    """return the given string num with commas inserted every 3 characters"""

    reversedStr = ''.join([char for char in reversed(num)])

    s = re.sub (r'(\d\d\d)(?=\d)(?!\d*\.)', r'\1,', reversedStr)
    return ''.join([char for char in reversed(s)])

#
# getHTML (fileName) - returns the contents of the HTML file fileName as one big
#    string.  If there is an error opening the file, this routine causes the
#    script to die. 
#
def getHTML (filename):
    """ returns the contents of the HTML file as one big string """
    f = open (filename, 'r')
    return f.read()

#
# stripExtraASCII (str) - removes all characters from str that are not in
#    the ASCII range of 26 through 126 (inclusive)
#
def stripExtraASCII (s):
    """ removes all characters from the supplied string that are not in the ASCII range 26-126 (inclusive)"""
    # functional programming is beautiful
    return reduce (lambda x,y: x + y, 
        filter (lambda x: ord(x) >= 26 and ord(x) <= 126, list (s)))

    # alternatively could've done a list comprehension:
    # return "".join ([c for c in list(s) if ord(c) >= 26 and ord(c) <= 126])

def getGameImgs():
    gameDataRegex = r'<tbody id=".{2}_.{8}"><tr onclick="XbcGetFirstChildHref\(this\);" onMouseOver="XbcNav_swapclass\(this, \'XbcProfileHighlight\', \'\'\);" onMouseOut="XbcNav_swapclass\(this,\'XbcProfileHighlight\',\'\'\);"><td class="XbcAchGameCell"><div class="XbcProfileImageDescCell"><img class="AchievementsGameIcon" src="(http://tiles.xbox.com/tiles/.*.jpg)" alt=".*" /><p><a href="http://live.xbox.com/en-../profile/Achievements/ViewAchievementDetails.aspx\?tid=.*"><strong class="XbcAchievementsTitle">(.*)</strong></a><br /><strong>Last Played Online:'

    games = {}
    for match in re.findall (gameDataRegex, getHTML (GAMESFILE)):
        games[genKeyFromGameTitle(match[1])] = match[0]

    return games 
    
#
# printIndent (msg) - prints msg to STDOUT, prepending the message with
#    an indent based upon the global g_indent variable if g_verbose
#    is True.  If verbose is False, then nothing is output to STDOUT 
#
def printIndent (msg):
    if g_verbose :
        s_indent = ""
        for dummy in range(g_indent * 4):
            s_indent = s_indent + "."
        s_indent = s_indent + msg
        print s_indent 

#
# replaceHTML (str) - replaces all HTML character codes (such as &amp; or 
#    &38;) found in str with ASCII character code equivalents.  For named
#    character codes, all standard codes in the standard ASCII range are 
#    recognized.  For numeric codes, the numeric value is parsed and passed
#    as an argument to Python's chr() routine.  NO CHECKS ARE DONE TO ENSURE
#    that numeric values are sensible (thus an HTML code of &9999999999; 
#    would result in a call to chr(9999999999))
#
#    Codes were taken from:
#    http://www.ascii.cl/htmlcodes.htm
# 
def replaceHTML (str):
    # HTML character codes to replace
    codes = {'quot' : '"', 'amp' : chr(38), 'lt' : chr(60), 'gt' : chr(62), 'nbsp' : ' ', 
        'copy' : chr(169), 'reg' : chr(174), 'iexcl' : chr(161), 'cent' : chr(162),
        'pound' : chr(163), 'curren' : chr(164), 'yen' : chr(165), 'brvbar' : chr(166), 
        'sect' : chr(167), 'uml' : chr(168), 'ordf' : chr(170), 'laquo' : chr(171), 
        'not' : chr(172), 'shy' : chr(173), 'macr' : chr(175), 'deg' : chr(176),  
        'plusmn' : chr(177), 'sup2' : chr(178), 'sup3' : chr(179), 'acute' : chr(180), 
        'micro' : chr(181), 'para' : chr(182), 'middot' : chr(183), 'cedil' : chr(184), 
        'sup1' : chr(185), 'ordm' : chr(186), 'raquo' : chr(187), 'frac14' : chr(188), 
        'frac12' : chr(189), 'frac34' : chr(190), 'iquest' : chr(191), 'Agrave' : chr(192),
        'Aacute' : chr(193), 'Acirc' : chr(194), 'Atilde' : chr(195), 'Auml' : chr(196),
        'Aring' : chr(197), 'AElig' : chr(198), 'Ccedil' : chr(199), 'Egrave' : chr(200),
        'Eacute' : chr(201), 'Ecirc' : chr(202), 'Euml' : chr(203), 'Igrave' : chr(204),
        'Iacute' : chr(205), 'Icirc' : chr(206), 'Iuml' : chr(207), 'ETH' : chr(208),
        'Ntilde' : chr(209), 'Ograve' : chr(210), 'Oacute' : chr(211), 'Ocirc' : chr(212),
        'Otilde' : chr(213), 'Ouml' : chr(214), 'times' : chr(215), 'Oslash' : chr(216),
        'Ugrave' : chr(217), 'Uacute' : chr(218), 'Ucirc' : chr(219), 'Uuml' : chr(220),
        'Yacute' : chr(221), 'THORN' : chr(222), 'szlig' : chr(223), 'agrave' : chr(224),
        'aacute' : chr(225), 'acirc' : chr(226), 'atilde' : chr(227), 'auml' : chr(228),
        'aring' : chr(229), 'aelig' : chr(230), 'ccedil' : chr(231), 'egrave' : chr(232),
        'eacute' : chr(233), 'ecirc' : chr(234), 'euml' : chr(235), 'igrave' : chr(236),
        'iacute' : chr(237), 'icirc' : chr(238), 'iuml' : chr(239), 'eth' : chr(240),
        'ntilde' : chr(241), 'ograve' : chr(242), 'oacute' : chr(243), 'ocirc' : chr(244),
        'otilde' : chr(245), 'ouml' : chr(246), 'divide' : chr(247), 'oslash' : chr(248),
        'ugrave' : chr(249), 'uacute' : chr(250), 'ucirc' : chr(251), 'uuml' : chr(252),
        'yacute' : chr(253), 'thorn' : chr(254), 'yuml' : chr(255)}

    for (code, val) in codes.iteritems():
        str = re.sub ('&' + code + ';', val, str)

    # replace all &#1234; style codes, and return the result
    return re.sub (r'&#(?P<numId>\d+);', lambda matchobj: chr(matchobj.group('numId')), str) 

#
# toDateTimeObj (day, month, year, hour, minute) - converts the supplied UTC timezone 
#    values into a datetime object in the local timezone. 
#
def toDateTimeObj (day, month, year, hour, minute): 
#    dtobj = datetime.datetime (year, month, day, hour, minute)
    return "42"

#
# padZero (n) - pads the string n with a 0 to make it a 2 character string.
#    If n is longer than 2 chars, returns the string unchanged.  Intended
#    as being a method that can pad an hour/minute/month numeric value
#    with a 0 to make it a 2 digit numeric string
#
def padZero (n) :
    return n.rjust (2, "0") 

#
# doFile (filename) - parses the achievements out of the supplied xbox.com 
#    formatted HTML file named filename.  Returns a hash that contains:
#
#    title => the game's title
#    percent => the current gs completion percentage
#    gs => current gamerscore earned for the game
#    gstotal => total possible gamerscore for the game (incl DLC)
#    achCount => current number of earned achievements for the game
#    achTotal => total possible achievements for the game (incl DLC) 
#
#    Also returns a list of hashes, with each hash 
#    representing a single achievement with:
#
#    name => The achievement name
#    desc => the achievement description
#    tcount => an integer indicating an order for the achievements
#        for the game (lower means earlier)
#    gs => gamerscore value of the achievement
#    date => a prettified string indicating the date the achievement
#        was unlocked
#    month => the 2-digit UTC month the achievement was unlocked
#    day => the 2-digit UTC day the achievement was unlocked
#    year => the 4-digit UTC year the achievement was unlocked
#    hour => the 24-hour clock UTC hour the achievement was unlocked
#    min => the 2-digit UTC minute the achievement was unlocked
#    img => a URL to the icon image associated with the achievement
#
def doFile (file):
    # RegEx for matching an individual achievement
    achRegex = r'<tbody\sid="ad_.?.?"><tr><td class="XbcAchDescription"><div class="XbcProfileImageDescCell"><img src="(http://tiles.xbox.com/tiles/.*.jpg)" /><p><strong class="XbcAchievementsTitle">(.*?)\n?</strong><br />(.*?)\n?</p></div></td><td class="XbcAchGamerData"><strong>(\d+) <img src="/xweb/lib/images/G_Icon_External.gif" /></strong><br /><strong>Acquired <script type="text/javascript">\n\s+<!--\n\s+_xbcDisplayDate\((\d+),\s(\d+),\s(\d+),\s(\d+),\s(\d+)\);\n\s+--></script><noscript>\d\d?/\d\d?/\d\d\d\d</noscript></strong></td></tr></tbody>'

    # RegEx for matching the header/game info
    titleRegex = r'.*<span class="XbcLiveText">(?P<title>.*?)</span>.*Achievements</h2></div><div class="XbcAchPercentageBar"><div><div style="width:\d+%;"></div></div><p>(?P<percent>\d+)% Unlocked</p></div></div><div class="XbcProfileSubHead"><p class="XbcFloatLeft"><strong>(?P<gs>\d+) of (?P<gstotal>\d+)\s<img src="/xweb/lib/images/G_Icon_External.gif" /></strong><br /><strong>(?P<achCount>\d+) of (?P<achTotal>\d+) Achievements</strong></p><div class="XbcFloatClear"></div></div><div class="XbcProfileTableContainer"><table class="XbcProfileTable XbcAchievementsDetailsTable" cellpadding="0" cellspacing="0"><thead><tr class="XbcTableColumns"><th class="XbcAchCol1"><span class="XbcDisplayNone">Achievements </span></th><th class="XbcAchCol2"><span class="XbcDisplayNone">Gamerscore </span></th></tr></thead>'

    html = getHTML(file)
    achList = []
    gameData = {}

    # read general game data
    match = re.search (titleRegex, html)
    if match : 
        gameData["title"] = stripExtraASCII (match.group('title'))
        gameData["percent"] = match.group ('percent') 
        gameData["gs"] = match.group ('gs')
        gameData["gstotal"] = match.group ('gstotal')
        gameData["achCount"] = match.group ('achCount')
        gameData["achTotal"] = match.group ('achTotal')
        gameData["key"] = genKeyFromGameTitle(match.group('title'))
        
        tcount = 999    # for in case there are achs with same date/time
        for (img, name, desc, gs, month, day, year, hour, min) in re.findall (achRegex, html):
            tcount = tcount - 1

            ach = {'name' : replaceHTML (name), 
                'img' : img,
                'desc' : replaceHTML (desc),
                'gs' : gs,
                'tcount' : tcount, 
                'month' : padZero(str(int(month) + 1)),
                'day' : padZero(day),
                'year' : year,
                'hour' : padZero(hour),
                'min' : padZero(min)
            }
            ach['date'] = ach["year"] + " " + ach["month"] + \
                " " + ach["day"] + " " + ach["hour"] + \
                ":" + ach["min"] + ":00"

            achList.append (ach)
            
    return (gameData, achList)

#
# readGameData () - looks in the current directory for HTML files (files with
#    an .html extension), and parses out all game data from them.  Returns
#    a hash mapping game titles to hashes which contain:
#
#    gameInfo => a hash containing information about a game
#    achList => a list of achievements for the game
#
def readGameData ():
    games = {}
    for file in glob.glob ('*.html'):
        printIndent ('readGameData: processing ' + file + '...')

        (gameData, achList) = doFile(file)
        if gameData:
            games[gameData["key"]] = {"gameInfo" : gameData, "achList" : achList}

    return games

#
# doCSVFile (games) - takes a reference to a hash containing information about
#    games, and processes it into the local file "out.csv"
# 
def doCSVFile (games):
    global g_indent

    lines = []
    gameDayTotals = {}

    g_indent += 1

    for (title, gameData) in games.iteritems():
        printIndent ("CSV: Processing " + title + "...")
        g_indent += 1

        achList = gameData["achList"]
        for ach in achList :
            printIndent ("CSV: processing " + ach["name"])
            lines.append (ach["date"] + "--" + str(ach["tcount"]) + ";" + \
                title + ";" + ach["name"] + ";" + \
                ach["desc"] + ";" + str(ach["gs"]) + "\n")

            key = "--".join ([ach["year"], ach["month"], ach["day"], title])

            # python dictionaries suck, this is 1 line in Perl
            if key in gameDayTotals :
                gameDayTotals[key] += int(ach["gs"])
            else:
                gameDayTotals[key] = int(ach["gs"])

        g_indent -= 1

    lines.sort()

    lines.append("\n")
    lines.append("\n")

    printIndent ("CSV: Processing daily totals")
    for k in sorted(gameDayTotals.keys()):
        lines.append (k + ";" + str(gameDayTotals[k]) + "\n")

    printIndent ("CSV: writing CSV file")
    f = open ('out.csv', 'w')
    f.writelines(lines)
    f.close()
    printIndent ("CSV: completed....")
    g_indent -= 1
    

#
# headerInfo (title, percent, gamerscore, gamerscoreTotal, achievementCount, achievementTotal
#    gameIconURL) - formats the supplied parameters into a single pretty string using BBC
#    forum markup. 
#
def headerInfo (title, percent, gs, gstotal, ach, achtotal, gameIcon) : 

    # a little defensive programming never hurts
    if gstotal == 0:
        gstotal = 1

    return '[CENTER][IMG]' + gameIcon + '[/IMG]\n[SIZE="3"][b]' + \
        title + '[/b][/SIZE]\n' + ach + ' / ' + achtotal + ' (' + \
        percent + '%) achievements for ' + gs + ' / ' + gstotal + \
        '[IMG]' + GICONURL + '[/IMG] (' + \
        str(round(float(gs) / float(gstotal) * 100.0, 1)) + '%)[/CENTER]' 

#
# formatDate (day, month, year, hour, min) - formats the supplied date/time
#    value into a string in the format:
#
#    MMMM DD, YYYY at H:MM AMPM
#
def formatDate (day, month, year, hour, min):
    return datetime.datetime(int(year), int(month), int(day), int(hour), \
        int(min)).strftime("%B %d, %Y at %I:%M%p")

def doForums (games, gameImages, gs):
    global g_indent
    g_indent += 1

    postIncrease = 0
    gameCount = len (games)

    f = open ('out.txt', 'w')
    
    for (title, gameData) in games.iteritems():
        printIndent ("ForumPost: Processing " + title + "...");
        achList = gameData["achList"]
        gameInfo = gameData["gameInfo"]
        gameTile = gameImages[gameData["gameInfo"]["key"]]
    
        f.write (headerInfo (gameInfo["title"], gameInfo["percent"], \
            gameInfo["gs"], gameInfo["gstotal"], \
            gameInfo["achCount"], gameInfo["achTotal"], \
            gameTile))

        f.write ('\n\n')
        printIndent ("ForumPost: sorting achievements...");

        # now we want a list of all achieements earned on the most recent
        # day an achievement was earned, and sorted by tcount.  So we sort
        # the achs by tcount, get the most recent ach, and filter out achs
        # that do not occur on the same day
 
        achList.sort (key=lambda x: x["tcount"], reverse=True)
        mostRecentAch = achList[0]
        todaysAchs = filter (lambda x: x["month"] == mostRecentAch["month"] and \
            x["day"] == mostRecentAch["day"] and \
            x["year"] == mostRecentAch["year"], achList)

        g_indent += 1

        total = 0
        for ach in todaysAchs:
            printIndent ("ForumPost: processing " + ach["name"])
            f.write('[IMG]' + ach["img"] + '[/IMG]\n[b]' + \
                ach["name"] + '[/b] - ' + ach["desc"] + \
                ' (' + str(ach["gs"]) + ' [IMG]' + \
                GICONURL + '[/IMG]) (Acquired ' + \
                formatDate (ach["day"], ach["month"], ach["year"], ach["hour"], ach["min"]) + \
                ')\n\n')
            total += int(ach["gs"])
        
        if gameCount > 1:
            f.write('[SIZE="2"][CENTER]Total GS for day in ' + \
                gameInfo["title"] + ': ' + str(total) + ' [IMG]' + \
                GICONURL + '[/IMG][/CENTER][/SIZE]\n\n')

        f.write ('[CENTER]------------------------------------[/CENTER]\n\n')

        g_indent -= 1
        postIncrease = postIncrease + total

    f.write ('[SIZE="3"][CENTER]Total increase in GS in this update: ' + \
        str(postIncrease) + ' [IMG]' + GICONURL + '[/IMG]\nNew Total GS: ' + \
        commify(str(gs)) + ' [IMG]' +  GICONURL + '[/IMG][/CENTER][/SIZE]\n\n')

    f.close()
    printIndent ("ForumPost: completed...."); 
    g_indent -= 1
    return "42"

#
# spacesToPlus (s) - replaces all occurences of spaces in the string s with plus signs (+) 
#
def spacesToPlus (s):
    return "+".join (s.split(' '))


#
# getGamerScore (gamertag) - returns the current gamerscore for
#    the supplied gamertag, or "-1" if the gamerscore could not
#    be determined
#
def getGamerScore (gamer):
    f = urllib.urlopen ("http://gamercard.xbox.com/" + spacesToPlus(gamer) + ".card")
    html = f.read()
    f.close()

    m = re.search (r'<span class="XbcFRAR">(?P<gs>\d+)<\/span>', html)
    if m :
        return m.group('gs')
    else:
        return "-1"

# the main entry point to the script
if __name__ == "__main__":
    gameImages = getGameImgs()
    games = readGameData()

    #pp = pprint.PrettyPrinter (4)
    #pp.pprint (games)

    printIndent ("Creating CSV File...")
    doCSVFile (games)
    printIndent ("Creating forum post...")
    doForums (games, gameImages, getGamerScore("Pedle Zelnip"));

