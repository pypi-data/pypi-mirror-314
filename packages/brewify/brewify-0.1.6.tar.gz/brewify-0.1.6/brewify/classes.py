from typing import Optional, Dict, List, Any, Union
from pydantic import BaseModel, HttpUrl

class Ask(BaseModel):
    """`chatbot` response model"""
    response: str

class SentimentAnalysisResponse:
    """Class to represent a single sentiment analysis response."""
    
    def __init__(self, label: str, score: float):
        self.label = label
        self.score = score

    @classmethod
    def from_dict(cls, data: dict):
        """Create an instance from a dictionary."""
        return cls(label=data.get("label"), score=data.get("score"))

class SentimentAnalysisResponses:
    """Class to handle multiple `sentiment analysis` responses."""
    
    def __init__(self, responses: list):
        self.responses = [SentimentAnalysisResponse.from_dict(item) for item in responses]
        
        
        self.negative = self.get_sentiment_score("negative")
        self.neutral = self.get_sentiment_score("neutral")
        self.positive = self.get_sentiment_score("positive")

    def get_sentiment_score(self, sentiment_label: str):
        """Get the score for a specific sentiment label."""
        for resp in self.responses:
            if resp.label == sentiment_label:
                return resp.score
        return 0  

    def __str__(self):
        return "\n".join(f"Label: {resp.label}, Score: {resp.score}" for resp in self.responses)

class Guild(BaseModel):
    id: str
    name: str
    splash: Optional[str]
    banner: Optional[str]
    description: Optional[str]
    icon: Optional[str]
    features: List[str]
    verification_level: int
    vanity_url_code: Optional[str]
    nsfw_level: int
    nsfw: bool
    premium_subscription_count: Optional[int]


class Channel(BaseModel):
    id: str
    type: int
    name: str

class Model(BaseModel):
    """`discord guild` response model"""
    type: int
    code: str
    expires_at: Optional[str]
    guild: Guild
    guild_id: str
    channel: Optional[Channel]

class AvatarDecorationData(BaseModel):
    asset: Optional[str]  
    sku_id: Optional[str]  
    expires_at: Optional[Any] 

class UserInfoResponse(BaseModel):
    """`discord user` response model"""
    id: str
    username: str
    discriminator: str
    public_flags: int
    flags: int
    accent_color: int
    global_name: Optional[str]
    avatar_decoration_data: Optional[AvatarDecorationData]  
    banner_color: str
    clan: Optional[str]
    avatar: HttpUrl

class Joke(BaseModel):
    """`joke` response model"""
    setup: str
    punchline: str

class Uwu(BaseModel):
    """`uwu` response model"""
    text: str

class Repository(BaseModel):
    url: HttpUrl
    name: str
    description: Optional[str] = None
    language: Optional[str] = None
    created: str  


class Location(BaseModel):
    name: Optional[str] = None
    url: Optional[HttpUrl] = None

class Connections(BaseModel):
    email: Optional[str] = None
    twitter: Optional[str] = None
    website: Optional[HttpUrl] = None

class UserProfile(BaseModel):
    id: int
    url: HttpUrl
    name: str
    username: Optional[str] = None
    avatar: HttpUrl
    bio: Optional[str] = None
    created: str  
    location: Optional[Location] = None
    company: Optional[str] = None
    connections: Connections


class GitHubResponse(BaseModel):
    user: UserProfile
    repositories: List[Repository]

class ImageLinkResponse(BaseModel):
    """`google image` response model"""
    link: Optional[str]

class TextSearchResponse(BaseModel):
    """`google text` response model"""
    title: Optional[str]
    link: Optional[str]
    snippet: Optional[str]

class CreditsModel(BaseModel):
    director: Optional[str]
    writer: Optional[str]
    cast: Optional[List[str]]

class InformationModel(BaseModel):
    country: Optional[str]
    released: Optional[str]
    runtime: Optional[str]
    rated: Optional[str]
    genre: Optional[str]
    series: Optional[Union[Dict[str, Any], bool]]

class ImdbSearchResponseModel(BaseModel):
    """`imdb` response model"""
    url: Optional[str]
    title: Optional[str]
    plot: Optional[str]
    poster: Optional[str]
    credits: CreditsModel
    information: InformationModel
    rating: Optional[float]
    ratings: Optional[List[Dict[str, Any]]]

class CountryInfoResponse(BaseModel):
    country: str
    currency: str
    population: int
    languages: List[str]

class IPGeolocationResponse(BaseModel):
    ip: str
    network: str
    version: str
    city: str
    region: str
    region_code: str
    country: str
    country_name: str
    country_code: str
    country_code_iso3: str
    country_capital: str
    country_tld: str
    continent_code: str
    in_eu: bool
    postal: str
    latitude: float
    longitude: float
    timezone: str
    utc_offset: str
    country_calling_code: str
    currency: str
    currency_name: str
    languages: str
    country_area: float
    country_population: int
    asn: str
    org: str

class Countdown(BaseModel):
    days: int
    hours: int
    minutes: int