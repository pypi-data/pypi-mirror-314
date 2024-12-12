import requests
from abc import ABC
import country_converter as coco
from .classes import *
from datetime import datetime
from typing import Union
from loguru import logger as loguru_logger
import sys
from fastapi import status
from geopy.geocoders import Nominatim

class Brexception(Exception):
    """A brewify exception, hahaha! (I should raise my child)"""
    pass

class Logger:
    def __init__(self, log_format: str = "<cyan>[+] brew | {message}</cyan>", level: str = "DEBUG"):
        loguru_logger.remove()
        
        
        loguru_logger.add(
            sink=sys.stdout,  
            format=log_format,
            level=level,
            colorize=True
        )
        
        self.logger = loguru_logger

    def debug(self, message: str, *args, **kwargs):
        self.logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        self.logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        self.logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        self.logger.critical(message, *args, **kwargs)

class Brewify(ABC):
    """Baseclass for the `brewify` library"""
    def __init__(
    self: "Brewify", 
    api_key: str = None, 
    proxy_username: str = None, 
    proxy_password: str = None, 
    proxy_ip: str = None, 
    proxy_port: int = None
    ):
        self.api_key = api_key
        self.session = requests.Session()
        self.base = "https://brew-api.vercel.app"
        self.geolocator = Nominatim(user_agent="geoapiExercises")
        self.logger = Logger(level="INFO")
        
        if all([proxy_username, proxy_password, proxy_ip, proxy_port]):
            self.proxy = f"http://{proxy_username}:{proxy_password}@{proxy_ip}:{proxy_port}"
            self.test_proxy(self.proxy)
        else:
            self.proxy = None  


    def test_proxy(self, proxy: str = None):
        """Test the proxy connection by making a simple request"""
        try:
            response = requests.get("http://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=5)
            response.raise_for_status()  
            self.logger.info(f"Proxy is working: {proxy}")
        except requests.RequestException as e:
            self.logger.error(f"Proxy test failed: {e}")
            raise Exception("Proxy is not working. Please check your proxy settings.")

    
    def request(self, endpoint: str, params: Union[str, dict]):
        """base `requester` method for this class"""
        try:
            df = params if params else ""
            pr = {
                "https": self.proxy,
                "http": self.proxy
            } if self.proxy else {}
            s = self.session.get(
                url=f"{self.base}/{endpoint}{df}".replace(" ", "%20"), 
                headers={'Authorization': self.api_key},
                timeout=120,
                proxies=pr
                )
            
        
            if s.status_code == status.HTTP_401_UNAUTHORIZED:
               raise Brexception("No such API key found in PostgreSQL database. Head to https://discord.gg/brew to obtain one.")
            
            s.raise_for_status()

            self.logger.info(f"Response Time: {s.headers['X-Process-Time']}s")
            return s

            
        except requests.HTTPError as e:
            raise Brexception(f"http error: {str(e.args[0])}")
        
    def get_google_image(self, query: str) -> ImageLinkResponse:
        """`smegsy`"""
        r = self.request(endpoint="google/search/images", params=f"?query={query}")
        return ImageLinkResponse(**r.json())
    
    def search_google(self, query: str) -> TextSearchResponse:
        """try to not do a different search frequently as it costs my `wallet` (please dont do it)"""
        r = self.request(endpoint="google/search/text", params=f"?query={query}")
        s: dict = r.json()
        return TextSearchResponse(**s)
    
    def imdb_search(self, query: str) -> ImdbSearchResponseModel:
        """idk for the `movieheads`"""
        r = self.request(endpoint="imdb/search", params=f"?query={query}")
        d: dict = r.json()
        return ImdbSearchResponseModel(**d)
    
    def discord_guild_search(self, invite_code: str = None) -> Model:
        """who the `freak` uses this (no diddy)"""
        r = self.request(endpoint="lookup/discord/guild", params=f"?invite_code={invite_code}")
        d: dict = r.json()
        return Model(**d)
    
    def discord_user_search(self, user_id: int = None) -> UserInfoResponse:
        """filthy discordians"""
        r = self.request(endpoint="lookup/discord/user", params=f"?user={user_id}")
        s: dict = r.json()
        return UserInfoResponse(**s)
    
    def sentiment_analysis(self, sentence: str = None) -> SentimentAnalysisResponses:
        """The model for this took atleast `two hours`"""
        r = self.request(endpoint="sentiment", params=f"?text={sentence}")
        s = r.json()
        if not s or not s[0]:  
           raise Brexception("No sentiment data returned")
        
        
        return SentimentAnalysisResponses(s[0])
    
    def chatbot(self, query: str = None) -> Ask:
        """THIS IS ONLY MADE FOR `CHATTING` PURPOSES DONT ASK IT FOR TUTORIALS"""
        r = self.request(endpoint="ask", params=f"?query={query}")
        s = r.json()
        return Ask(response=str(s[0]["generated_text"]))
    
    def joke(self) -> Joke:
        """tells a `joke` duh"""
        r = self.request(endpoint="joke", params=None)
        s: dict = r.json()
        return Joke(setup=s.get("setup"), punchline=s.get("punchline"))
    
    def uwuify(self, msg: str) -> Uwu:
        """Gimme nitro `d-d-daddy...`"""
        r = self.request(endpoint="uwuify", params=f"?msg={msg}")
        s: dict = r.json()
        return Uwu(text=s.get("text"))
    
    def github_profile(self, username: str) -> GitHubResponse:
        """really you need an `explanation`?"""
        r = self.request(endpoint="lookup/github/profile", params=f"?username={username}")
        return GitHubResponse(**r.json())
    
    def country(self, country_code: str):
        """
        Get info about a country.
        
        :param `country_code`: str - The ISO country code, location, or country name of the desired country you want to gain info for e.g, US, America, or Texas
        """
        if len(country_code) == 2 and country_code.isalpha():
            iso2_code = country_code.upper()  
        else:
            try:
                iso2_code = coco.convert(names=country_code, to='ISO2')
            except ValueError:
                location_info = self.geolocator.geocode(country_code)
                if location_info:
                    country = self.geolocator.reverse((location_info.latitude, location_info.longitude), exactly_one=True)
                    country_name = country.raw['address'].get('country', None)
                    if country_name:
                        iso2_code = coco.convert(names=country_name, to='ISO2')
                    else:
                        return None  
                else:
                    return None  

        
        r = self.request(endpoint="country", params=f"?country_code={iso2_code}")
        s = r.json()
        return CountryInfoResponse(
            country=s['country'],
            currency=s['currency'],
            population=s['population'],
            languages=s['languages']
        ) 
    
    def ipinfo(self, ip: str) -> IPGeolocationResponse:
        """im `tired` bruh"""
        r = self.request(endpoint="geo", params=f"?ip={ip}")
        return IPGeolocationResponse(**r.json())

    def countdown(self, year: int, month: int, day: int) -> Countdown:
        """
        Get the countdown to an event.

        :param year: int - The year of the event
        :param month: int - The month of the event (1-12)
        :param day: int - The day of the event (1-31)
        :return: Countdown - pydantic model
        """
        try:
            
            event_date = datetime(year, month, day).strftime("%Y-%m-%d")
            params = f'?event_date={event_date}'  
            response_json = self.request(endpoint="countdown", params=params)
            return Countdown(**response_json.json())
        except Exception as e: 
            raise Brexception(e)