﻿# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from bs4 import BeautifulSoup
import requests

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'cimau'
SITE_NAME = 'Cimaau'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)


RAMADAN_SERIES = (URL_MAIN + '/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-7series/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b1%d9%85%d8%b6%d8%a7%d9%86-2023/', 'showSeries')
MOVIE_EN = (URL_MAIN + '/category/افلام-اجنبي-movies7-english/', 'showMovies')
MOVIE_AR = (URL_MAIN + '/category/افلام-عربي-arabic5-movies/', 'showMovies')
MOVIE_HI = (URL_MAIN + '/category/افلام-هندي-indian/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + '/category/افلام-اجنبي-movies7-english/افلام-asian-movies/', 'showMovies')
KID_MOVIES = (URL_MAIN + '/category/افلام-كرتون-movies5-anime/', 'showMovies')
MOVIE_NETFLIX = (URL_MAIN + '/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a-movies7-english/netflix-movie/', 'showMovies')

SERIE_TR = (URL_MAIN + '/category/مسلسلات-7series/مسلسلات-تركية-series1-turkish/', 'showSeries')
SERIE_EN = (URL_MAIN + '/category/مسلسلات-7series/مسلسلات-اجنبي-english/', 'showSeries')
SERIE_AR = (URL_MAIN + '/category/مسلسلات-7series/مسلسلات-عربية-arabic-series/', 'showSeries')
SERIE_ASIA = (URL_MAIN + '/category/مسلسلات-7series/مسلسلات-اسيوية-series1-asian/', 'showSeries')
SERIE_HEND = (URL_MAIN + '/category/مسلسلات-7series/مسلسلات-هندية-series-indian/', 'showSeries')
SERIE_LATIN = (URL_MAIN + '/category/مسلسلات-7series/latino-mexico/', 'showSeries')
SERIE_RAMADAN = (URL_MAIN + '/category/series/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b1%d9%85%d8%b6%d8%a7%d9%86-2023/', 'showSeries')
WWE = (URL_MAIN + '/category/%d8%a7%d8%ae%d8%b1%d9%89-1other/wwe/', 'showSeries')
SERIE_ANIME = (URL_MAIN + '/category/series/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%83%d8%b1%d8%aa%d9%88%d9%86-anime-series/', 'showSeries')
PROGRAMS = (URL_MAIN + '/category/series/%d8%a8%d8%b1%d8%a7%d9%85%d8%ac-%d8%aa%d9%84%d9%8a%d9%81%d8%b2%d9%8a%d9%88%d9%86%d9%8a%d8%a9-tv1-shows/', 'showSeries')
SERIE_NETFLIX = (URL_MAIN + '/category/series/series-netflix/', 'showSeries')

MOVIE_PACK = (URL_MAIN , '/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a-movies7-english/full-pack/')
URL_SEARCH = (URL_MAIN + '/?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/search/%D9%81%D9%8A%D9%84%D9%85+', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/search/%D9%85%D8%B3%D9%84%D8%B3%D9%84+', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
s = requests.Session()

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', icons + '/MoviesEnglish.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام Netflix', icons + '/MoviesEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', icons + '/Arabic.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', icons + '/Asian.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', icons + '/Hindi.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])

    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انمي', icons + '/Anime.png', oOutputParameterHandler)
 


    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انمي', icons + '/Anime.png', oOutputParameterHandler)
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', icons + '/TVShowsEnglish.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات Netflix', icons + '/TVShowsEnglish.png', oOutputParameterHandler)

    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', icons + '/Cartoon.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', icons + '/TVShowsEnglish.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات Netflix', icons + '/TVShowsEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', icons + '/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', icons + '/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', icons + '/Hindi.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', SERIE_LATIN[0])

    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات لاتيني', icons + '/TVShows.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANIME[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', icons + '/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_RAMADAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات رمضان', icons + '/Ramadan.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', PROGRAMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيون', icons + '/Programs.png', oOutputParameterHandler)

    
    oOutputParameterHandler.addParameter('siteUrl', WWE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مصارعة', icons + '/WWE.png', oOutputParameterHandler)
    
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_PACK[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showPack', 'سلاسل افلام', icons + '/pack.png', oOutputParameterHandler)

    
    oOutputParameterHandler.addParameter('siteUrl', WWE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مصارعة', icons + '/WWE.png', oOutputParameterHandler)
    
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_PACK[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showPack', 'سلاسل افلام', icons + '/pack.png', oOutputParameterHandler)
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مكسيكي', icons + '/TVShows.png', oOutputParameterHandler)  
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PACK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showPack', 'أقسام الموقع', icons + '/Icon.png', oOutputParameterHandler)

 
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search/+'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search/+'+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showPack():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
# ([^<]+) .+? 

    sPattern = '<a href="([^<]+)">([^<]+)</a>'


    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sTitle = aEntry[1].replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","") 
            sThumb = aEntry[1]
            siteUrl = aEntry[0]
            sDesc = ''
			

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            if 'series' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMovies', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showPack', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
			
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    soup = BeautifulSoup(sHtmlContent,"html.parser") 
    #VSlog(soup)
    sHtmlContent = soup.find("div",{"class":"PageContent"})
 # ([^<]+) .+?

    sPattern = '<li class="MovieBlock"><a href="([^<]+)"><div.+?image:url([^<]+);"></div>.+?</div></div>([^<]+)</div>'
		
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1].replace("(","").replace(")","")
            sDesc = ''
            sYear = ''
            
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
  # ([^<]+) .+?


    if not sSearch:
        sPattern = '<a class=\"next.page-numbers\" href=\"(.+?)\">'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        
        if aResult[0]:
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break
     
                siteUrl = aEntry.replace('"',"")
                #VSlog("Check for next Movies : " + siteUrl)
                sThumb = icons + '/Next.png'

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Next' , sThumb, oOutputParameterHandler)

        sPattern = '<a class=\"next.page-numbers\" href=\"(.+?)\">'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        
        if aResult[0]:
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break
     
                siteUrl = aEntry.replace('"',"")
                #VSlog("Check for next Movies : " + siteUrl)
                sThumb = icons + '/Next.png'

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]' , sThumb, oOutputParameterHandler)


                progress_.VSclose(progress_)
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
    soup = BeautifulSoup(sHtmlContent,"html.parser") 
    #VSlog(soup)
    sHtmlContent = soup.find("div",{"class":"PageContent"})
    #VSlog(sHtmlContent)
 
      # (.+?) ([^<]+) .+?
    sPattern = '<li class="MovieBlock"><a href="([^<]+)"><div.+?image:url([^<]+);"></div>.+?</div></div>([^<]+)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    itemList = []
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("&#8217;","'").replace("مشاهدة","").replace("مترجمة","").replace("مسلسل","").replace("انمي","").replace("أنمي","").replace("كاملة","").replace("كامل","").replace("مترجم","").replace("فيلم","").replace("برنامج","").replace("برنامج","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","")
            
            siteUrl = aEntry[0]
            sThumb = aEntry[1].replace("(","").replace(")","")
            sDesc = ""
            sDisplayTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S").replace("موسم","S").replace("S ","S").split('حلقة')[0].split('حلقه')[0]

            if sDisplayTitle not in itemList:
                itemList.append(sDisplayTitle)
                
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
  # ([^<]+) .+?




    if not sSearch:
        sPattern = '<a class=\"next.page-numbers\" href=\"(.+?)\">'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        #VSlog(aResult)
        
        if aResult[0]:
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break
     
                siteUrl = aEntry.replace('"',"")
                #VSlog("Check for next series : " + siteUrl)
                sThumb = icons + '/Next.png'

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sThumb',sThumb)
                #oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                
                
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]' , sThumb, oOutputParameterHandler)

            progress_.VSclose(progress_)
        sPattern = '<a class=\"next.page-numbers\" href=\"(.+?)\">'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        #VSlog(aResult)
        
        if aResult[0]:
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break
     
                siteUrl = aEntry.replace('"',"")
                #VSlog("Check for next series : " + siteUrl)
                sThumb = icons + '/Next.png'

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sThumb',sThumb)
                #oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                
                
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'Next' , sThumb, oOutputParameterHandler)

            progress_.VSclose(progress_)
        oGui.setEndOfDirectory()
	
def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    

    oParser = cParser()
            
    sPattern =  '<a href="([^<]+)"><div class="WatchingArea Hoverable">' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        m3url = aResult[1][0] 
        if 'Episode'  in m3url: 
            m3url = aResult[1][0] 
            oRequest = cRequestHandler(m3url)
            sHtmlContent = oRequest.request()
 # ([^<]+) .+?
            sPattern = '<a href="([^<]+)"><em>([^<]+)</em><span>([^<]+)</span></a></li>'

            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
	
	
            if aResult[0]:
               oOutputParameterHandler = cOutputParameterHandler()
               for aEntry in aResult[1]:
 
                  if "مدبلج" in sMovieTitle:
                     sMovieTitle = sMovieTitle.replace("مدبلج","")
                     sMovieTitle = "مدبلج"+sMovieTitle
                  sTitle = sMovieTitle+' E'+ aEntry[2]
                  sUrl = aEntry[0]
                  sThumb = sThumb
                  sDesc = ''
			
                  oOutputParameterHandler.addParameter('siteUrl',sUrl)
                  oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                  oOutputParameterHandler.addParameter('sThumb', sThumb)
                  oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        else:
            oRequest = cRequestHandler(m3url)
            sHtmlContent = oRequest.request()
 # ([^<]+) .+?
    sPattern = '<a href="" data-link="([^<]+)" class="sever_link"><img src="http://.+?/template/logo_server/1593281223_333.jpg" width="40" height="40" alt="" />([^<]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]: 
        oOutputParameterHandler = cOutputParameterHandler()             
        for aEntry in aResult[1]: 
            sTitle = aEntry[1]
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ""
			


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = ''
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    
    #Recuperation infos


    sIMDB = re.compile(r'httph|https:\/\/www.imdb.com\/title\/(.+?)\/',sHtmlContent)

    sIMDB = re.search(r'https://www.imdb.com/title/([^<]+)/',sHtmlContent)

    
    sPattern = '<h2>القصة</h2><p>([^<]+)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sDesc = aResult[1][0]
    
    # .+? ([^<]+)
    sPattern = '<a href="([^<]+)"><div class="WatchingArea Hoverable">'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        m3url = aResult[1][0]
        if '/tag/'  in m3url: 
            m3url = aResult[1][0] 
            oRequest = cRequestHandler(m3url)
            sData = oRequest.request()
 # ([^<]+) .+?
            sPattern = '<li class="MovieBlock"><a href="([^<]+)">.+?style="background-image:url([^<]+);"></div>.+?</div></div>([^<]+)</div>'

            oParser = cParser()
            aResult = oParser.parse(sData, sPattern)
	
	
            if aResult[0]:
               oOutputParameterHandler = cOutputParameterHandler()    
               for aEntry in aResult[1]:
 
                   sTitle = aEntry[2]
                   siteUrl = aEntry[0]
                   sThumb = aEntry[1].replace("(","").replace(")","")
                   sDesc = sDesc

                   sYear = ''
                   m = re.search('([0-9]{4})', sTitle)
                   if m:
                      sYear = str(m.group(0))
                      sTitle = sTitle.replace(sYear,'')
			


                   oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                   oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                   oOutputParameterHandler.addParameter('sThumb', sThumb)
                   oOutputParameterHandler.addParameter('sYear', sYear)
                   oOutputParameterHandler.addParameter('sDesc', sDesc)
                   oGui.addLink(SITE_IDENTIFIER, 'showLinks', sTitle, sThumb, sDesc, oOutputParameterHandler)
        
 
               sNextPage = __checkForNextPage(sHtmlContent2)
               if sNextPage:
                  oOutputParameterHandler = cOutputParameterHandler()
                  oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                  oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
        else:
               oRequest = cRequestHandler(m3url)
               sHtmlContent = oRequest.request()
				


            
    sPattern =  '<meta itemprop="embedURL" content="(.+?)" />' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        m3url = aResult[1][0] 
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()

    #print sUrl
    


    sPage='0'

    sPattern = 'data-link="([^<]+)" class=".+?"><img.+?/>(.+?)</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

   
    if aResult[0]:
        for aEntry in aResult[1]:
            sPage = aEntry[0]
            sTitle = 'server '+':'+ aEntry[1]
            siteUrl = 'https://tv.cimaaa4u.fun/structure/server.php?id='+sPage
            sDesc = sDesc

            oRequestHandler = cRequestHandler(siteUrl)
            sData = oRequestHandler.request();
    # (.+?)
               

            sPattern = '<iframe.+?src="(.+?)"'
            oParser = cParser()
            aResult = oParser.parse(sData, sPattern)



	
            if aResult[0]:
                for aEntry in aResult[1]:
        
                    url = aEntry
                    if url.startswith('//'):
                       url = 'http:' + url
            
                    sHosterUrl = url 
                    if 'userload' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                    if 'moshahda' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                    if 'streamtape' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
                    if 'mystream' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN                           
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    # (.+?) ([^<]+)

    sPattern = 'href="([^<]+)" target="_blank" class="download_link">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
        
            url = aEntry

            if url.startswith('//'):
               url = 'http:' + url
				
					
            
            sHosterUrl = url 
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'streamtape' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
     
    oGui.setEndOfDirectory()  

def __checkForNextPage(sHtmlContent):
    sPattern = '<a class=\"next.page-numbers\" href=\"(.+?)\">'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        #VSlog("Check for next func : " + aResult[1])
        return aResult[1]

    return False