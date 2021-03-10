﻿#-*- coding: utf-8 -*-
#zombi
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import urllib2,urllib,re
import unicodedata
 
SITE_IDENTIFIER = 'animeblkom'
SITE_NAME = 'animeblkom'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://blkom.com'
ANIM_NEWS = ('https://blkom.com/anime-list', 'showSeries')

ANIM_MOVIES = ('https://blkom.com/movie-list', 'showMovies')
URL_SEARCH_SERIES = ('https://blkom.com/search?query=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://blkom.com/search?query='+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
     # (.+?) ([^<]+) .+?
    sPattern = '<img class="lazy" data-original="([^<]+)" alt.+?<div class="name"> <a href="([^<]+)">([^<]+)</a> </div> <div class="overlay">.+?<div class="story-text"> <p>([^<]+)</p>.+?<div class="badge red" title=.+?>(.+?)</'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[2]).decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            siteUrl = URL_MAIN+str(aEntry[1])
            sThumbnail = URL_MAIN+str(aEntry[0])
            sInfo = aEntry[3].decode("utf8")
            sInfo = cUtil().unescape(sInfo).encode("utf8")
            sYear = aEntry[4]
            sDisplayTitle = ('%s (%s)') % (sTitle, sYear)


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle',sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sInfo', aEntry[3])
            if '/watch/' in siteUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, sInfo, oOutputParameterHandler) 
            else:
				oGui.addMovie(SITE_IDENTIFIER, 'showEps', sDisplayTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
			
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
     # (.+?) ([^<]+) .+?
    sPattern = '<img class="lazy" data-original="([^<]+)" alt.+?<div class="name"> <a href="([^<]+)">([^<]+)</a> </div> <div class="overlay">.+?<div class="story-text"> <p>([^<]+)</p>.+?<div class="badge red" title=.+?>(.+?)</'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[2]).decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            siteUrl = URL_MAIN+str(aEntry[1])
            sThumbnail = URL_MAIN+str(aEntry[0])
            sInfo = aEntry[3].decode("utf8")
            sInfo = cUtil().unescape(sInfo).encode("utf8")
            sYear = aEntry[4]
            sDisplayTitle = ('%s (%s)') % (sTitle, sYear)


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle',sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sInfo', aEntry[3])
            if '/watch/' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, sInfo, oOutputParameterHandler) 
            else:
				oGui.addTV(SITE_IDENTIFIER, 'showEps', sDisplayTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sInfo = oInputParameterHandler.getValue('sInfo')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # (.+?) .+?
    sPattern = '<li class="episode-link.+?href="([^<]+)"> <span>الحلقة</span> <span class="separator">:</span> <span>([^<]+)<'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent.replace('\n',''))
    #fh.close()

    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = sMovieTitle+" E"+aEntry[1]
            siteUrl = URL_MAIN+str(aEntry[0])
            sThumbnail = str(sThumbnail)
            sInfo = sInfo.decode("utf8")
            sInfo = cUtil().unescape(sInfo).encode("utf8")
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            

 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory() 

 
def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="page-link" href="([^<]+)" rel="next" '
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # (.+?) .+? ([^<]+)
                

    sPattern = '<div class="item"> <span class="([^<]+)">'
    sPattern = sPattern + '|' + '<a data-src="([^<]+)">([^<]+)</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)


    #print aResult

	
    if (aResult[0] == True):
			total = len(aResult[1])
			progress_ = progress().VScreate(SITE_NAME)
			for aEntry in aResult[1]:
				progress_.VSupdate(progress_, total)
				if progress_.iscanceled():
					break


 


				sSub = aEntry[0].replace('active',"")
				sSub = sSub+' ترجمة'
            
				if aEntry[0]:
					oGui.addText(SITE_IDENTIFIER,'[COLOR coral]'+sSub+'[/COLOR]')
                   
        
				if aEntry[1]:
					url = str(aEntry[1])
					sTitle = str(aEntry[2]).decode("utf8").replace('"',"")
					sTitle = cUtil().unescape(sTitle).encode("utf8")
					sTitle = '[COLOR yellow]'+sTitle+'[/COLOR]'
					if url.startswith('//'):
						url = 'https:' + url
            
					sHosterUrl = url 
					oHoster = cHosterGui().checkHoster(sHosterUrl)
					if (oHoster != False):
						sDisplayTitle = sMovieTitle+sTitle
						oHoster.setDisplayName(sDisplayTitle)
						oHoster.setFileName(sMovieTitle)
						cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

			progress_.VSclose(progress_)

    # (.+?) .+? ([^<]+)
               

    sPattern = '<div class="col-xs-12 col-md-2 quality-icon ([^<]+)"'
    sPattern = sPattern + '|' + '<a href="([^<]+)" target="_blank"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)


    #print aResult

	
    if (aResult[0] == True):
			total = len(aResult[1])
			progress_ = progress().VScreate(SITE_NAME)
			for aEntry in aResult[1]:
				progress_.VSupdate(progress_, total)
				if progress_.iscanceled():
					break


 


				sSub = aEntry[0]
            
				if aEntry[0]:
					oGui.addText(SITE_IDENTIFIER,'[COLOR coral]'+sSub+'[/COLOR]')
                   
        
				if aEntry[1]:
					url = str(aEntry[1])
					sTitle = str(aEntry[0]).decode("utf8").replace('"',"")
					sTitle = cUtil().unescape(sTitle).encode("utf8")
					sTitle = '[COLOR yellow]'+sTitle+'[/COLOR]'
					if url.startswith('//'):
						url = 'https:' + url
            
					sHosterUrl = url 
					oHoster = cHosterGui().checkHoster(sHosterUrl)
					if (oHoster != False):
						sDisplayTitle = sMovieTitle+sTitle
						oHoster.setDisplayName(sDisplayTitle)
						oHoster.setFileName(sMovieTitle)
						cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

			progress_.VSclose(progress_)
    oGui.setEndOfDirectory()