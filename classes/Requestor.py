import requests
from abc import ABC,abstractmethod
import logging
from datetime import datetime
import time
from random import randint
import emoji
import json

#Logging
logger = logging.getLogger(__name__)


#Method for making requests
class RequestorBase(ABC):
    
    @abstractmethod
    def __init__(self,session, allowed_requests,interval,padding_factor):
        raise NotImplementedError
    
    #Makes requests to links and returns list of response dicts: 
    # [{'link': link, 'status_code':status_code, 'content': content},...]
    @abstractmethod
    def makeRequests(cls,links):
        raise NotImplementedError
    
    #Makes requests to links and returns list of response dict: 
    #Delay (ms) is used for delays if making multiple requests
    # {'link': link, 'status_code':status_code, 'content': content}
    @abstractmethod
    def makeRequest(cls,link,delay):
        raise NotImplementedError
    
#------------------Implementation Classes------------------------------------------#


#Method for making requests
class Requestor(RequestorBase):
    
    
    def __init__(self,session=None, allowed_requests=1000,interval_ms=2500,padding_factor=5):
        self.__allowed_requests = allowed_requests
        self.__interval_ms = interval_ms
        self.__padding_factor= padding_factor
        self.__session = session
        self.__default_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0',
        } 
        
        if self.__session is None:
            self.__session = requests.sessions.Session()
            self.__session.headers.update(self.__default_headers)
            
        
        
    #Requests pages and returns list of dicts with link, status, and content
    #Uses set interval with padding factor in form of interval/padfactor for delaying commands
    #Returns list of dicts in form {'link':link, 'status_code':status_code,'content':content}
    def makeRequests(self,links):
        
        response_list = []

        num_links = len(links)
    
        index = 0

        while(index < num_links and self.__allowed_requests > 0):
            
            logger.debug(f'link[{index}] request to {links[index]}')

            content = self.__getContent(links[index])
            
            logger.debug(f'Response code: {content['status_code']}')

            response_list.append(content)
        
            if index != num_links-1:
                
                rand_delay = self.__getRandDelayInSeconds(self.__interval_ms,self.__padding_factor)
                time.sleep(rand_delay)
            
            self.__allowed_requests -= 1
            index+=1
    
        return response_list
    
    #Makes single request and returns html page content
    #Returns dict in form {'link':link, 'status_code':status_code,'content':content}
    def makeRequest(self,link,delay=0,params=None):
        logger.debug(f'Sending request to {link}')

        if(delay > 0):
            
            rand_delay = self.__getRandDelayInSeconds(delay,self.__padding_factor)
            time.sleep(rand_delay)

        content = self.__getContent(link,params)
            
        logger.debug(f'Response code: {content['status_code']}')

        self.__allowed_requests -= 1
        return content
    

    #Returns html page or None
    def __getContent(self,link,params=None):
        req = self.__session.get(link,params=params)
        dict = {}
        dict['link'] = link
        dict['status_code'] = req.status_code
        dict['content'] = req.text
        if dict['content']:
            dict['content'] = emoji.replace_emoji(dict['content'],'')
        return dict
    
    def __getRandDelayInSeconds(self,duration_ms,padding_factor):
        padding_ms = round(duration_ms/padding_factor)
        return (duration_ms + randint(-1*padding_ms, padding_ms))/1000
    
    def setSession(self,session):
        self.__session = session
    
    def getSession(self):
        return self.__session
        
    def setAllowedRequests(self,allowed_requests):
        self.__allowed_requests = allowed_requests
    
    def getAllowedRequests(self):
        return self.__allowed_requests
    
    def setInterval(self,interval_ms):
        self.__interval_ms = interval_ms
    
    def getInterval(self):
        return self.__interval_ms
    
    def setPadding(self,padding_factor):
        self.__padding = padding_factor
    
    def getPadding(self):
        return self.__padding
    



    
class WeatherRequestor(Requestor):

    __URL = 'https://archive-api.open-meteo.com/v1/archive'
    __DEF_LAT = 40.507999747027796 
    __DEF_LON = -88.99071849002091
    __DEF_TZ = '-05:00'

    METEO_WEATHER_CODES = {
	"0":{
		"day":{
			"description":"Sunny",
			"image":"http://openweathermap.org/img/wn/01d@2x.png"
		},
		"night":{
			"description":"Clear",
			"image":"http://openweathermap.org/img/wn/01n@2x.png"
		}
	},
	"1":{
		"day":{
			"description":"Mainly Sunny",
			"image":"http://openweathermap.org/img/wn/01d@2x.png"
		},
		"night":{
			"description":"Mainly Clear",
			"image":"http://openweathermap.org/img/wn/01n@2x.png"
		}
	},
	"2":{
		"day":{
			"description":"Partly Cloudy",
			"image":"http://openweathermap.org/img/wn/02d@2x.png"
		},
		"night":{
			"description":"Partly Cloudy",
			"image":"http://openweathermap.org/img/wn/02n@2x.png"
		}
	},
	"3":{
		"day":{
			"description":"Cloudy",
			"image":"http://openweathermap.org/img/wn/03d@2x.png"
		},
		"night":{
			"description":"Cloudy",
			"image":"http://openweathermap.org/img/wn/03n@2x.png"
		}
	},
	"45":{
		"day":{
			"description":"Foggy",
			"image":"http://openweathermap.org/img/wn/50d@2x.png"
		},
		"night":{
			"description":"Foggy",
			"image":"http://openweathermap.org/img/wn/50n@2x.png"
		}
	},
	"48":{
		"day":{
			"description":"Rime Fog",
			"image":"http://openweathermap.org/img/wn/50d@2x.png"
		},
		"night":{
			"description":"Rime Fog",
			"image":"http://openweathermap.org/img/wn/50n@2x.png"
		}
	},
	"51":{
		"day":{
			"description":"Light Drizzle",
			"image":"http://openweathermap.org/img/wn/09d@2x.png"
		},
		"night":{
			"description":"Light Drizzle",
			"image":"http://openweathermap.org/img/wn/09n@2x.png"
		}
	},
	"53":{
		"day":{
			"description":"Drizzle",
			"image":"http://openweathermap.org/img/wn/09d@2x.png"
		},
		"night":{
			"description":"Drizzle",
			"image":"http://openweathermap.org/img/wn/09n@2x.png"
		}
	},
	"55":{
		"day":{
			"description":"Heavy Drizzle",
			"image":"http://openweathermap.org/img/wn/09d@2x.png"
		},
		"night":{
			"description":"Heavy Drizzle",
			"image":"http://openweathermap.org/img/wn/09n@2x.png"
		}
	},
	"56":{
		"day":{
			"description":"Light Freezing Drizzle",
			"image":"http://openweathermap.org/img/wn/09d@2x.png"
		},
		"night":{
			"description":"Light Freezing Drizzle",
			"image":"http://openweathermap.org/img/wn/09n@2x.png"
		}
	},
	"57":{
		"day":{
			"description":"Freezing Drizzle",
			"image":"http://openweathermap.org/img/wn/09d@2x.png"
		},
		"night":{
			"description":"Freezing Drizzle",
			"image":"http://openweathermap.org/img/wn/09n@2x.png"
		}
	},
	"61":{
		"day":{
			"description":"Light Rain",
			"image":"http://openweathermap.org/img/wn/10d@2x.png"
		},
		"night":{
			"description":"Light Rain",
			"image":"http://openweathermap.org/img/wn/10n@2x.png"
		}
	},
	"63":{
		"day":{
			"description":"Rain",
			"image":"http://openweathermap.org/img/wn/10d@2x.png"
		},
		"night":{
			"description":"Rain",
			"image":"http://openweathermap.org/img/wn/10n@2x.png"
		}
	},
	"65":{
		"day":{
			"description":"Heavy Rain",
			"image":"http://openweathermap.org/img/wn/10d@2x.png"
		},
		"night":{
			"description":"Heavy Rain",
			"image":"http://openweathermap.org/img/wn/10n@2x.png"
		}
	},
	"66":{
		"day":{
			"description":"Light Freezing Rain",
			"image":"http://openweathermap.org/img/wn/10d@2x.png"
		},
		"night":{
			"description":"Light Freezing Rain",
			"image":"http://openweathermap.org/img/wn/10n@2x.png"
		}
	},
	"67":{
		"day":{
			"description":"Freezing Rain",
			"image":"http://openweathermap.org/img/wn/10d@2x.png"
		},
		"night":{
			"description":"Freezing Rain",
			"image":"http://openweathermap.org/img/wn/10n@2x.png"
		}
	},
	"71":{
		"day":{
			"description":"Light Snow",
			"image":"http://openweathermap.org/img/wn/13d@2x.png"
		},
		"night":{
			"description":"Light Snow",
			"image":"http://openweathermap.org/img/wn/13n@2x.png"
		}
	},
	"73":{
		"day":{
			"description":"Snow",
			"image":"http://openweathermap.org/img/wn/13d@2x.png"
		},
		"night":{
			"description":"Snow",
			"image":"http://openweathermap.org/img/wn/13n@2x.png"
		}
	},
	"75":{
		"day":{
			"description":"Heavy Snow",
			"image":"http://openweathermap.org/img/wn/13d@2x.png"
		},
		"night":{
			"description":"Heavy Snow",
			"image":"http://openweathermap.org/img/wn/13n@2x.png"
		}
	},
	"77":{
		"day":{
			"description":"Snow Grains",
			"image":"http://openweathermap.org/img/wn/13d@2x.png"
		},
		"night":{
			"description":"Snow Grains",
			"image":"http://openweathermap.org/img/wn/13n@2x.png"
		}
	},
	"80":{
		"day":{
			"description":"Light Showers",
			"image":"http://openweathermap.org/img/wn/09d@2x.png"
		},
		"night":{
			"description":"Light Showers",
			"image":"http://openweathermap.org/img/wn/09n@2x.png"
		}
	},
	"81":{
		"day":{
			"description":"Showers",
			"image":"http://openweathermap.org/img/wn/09d@2x.png"
		},
		"night":{
			"description":"Showers",
			"image":"http://openweathermap.org/img/wn/09n@2x.png"
		}
	},
	"82":{
		"day":{
			"description":"Heavy Showers",
			"image":"http://openweathermap.org/img/wn/09d@2x.png"
		},
		"night":{
			"description":"Heavy Showers",
			"image":"http://openweathermap.org/img/wn/09n@2x.png"
		}
	},
	"85":{
		"day":{
			"description":"Light Snow Showers",
			"image":"http://openweathermap.org/img/wn/13d@2x.png"
		},
		"night":{
			"description":"Light Snow Showers",
			"image":"http://openweathermap.org/img/wn/13n@2x.png"
		}
	},
	"86":{
		"day":{
			"description":"Snow Showers",
			"image":"http://openweathermap.org/img/wn/13d@2x.png"
		},
		"night":{
			"description":"Snow Showers",
			"image":"http://openweathermap.org/img/wn/13n@2x.png"
		}
	},
	"95":{
		"day":{
			"description":"Thunderstorm",
			"image":"http://openweathermap.org/img/wn/11d@2x.png"
		},
		"night":{
			"description":"Thunderstorm",
			"image":"http://openweathermap.org/img/wn/11n@2x.png"
		}
	},
	"96":{
		"day":{
			"description":"Light Thunderstorms With Hail",
			"image":"http://openweathermap.org/img/wn/11d@2x.png"
		},
		"night":{
			"description":"Light Thunderstorms With Hail",
			"image":"http://openweathermap.org/img/wn/11n@2x.png"
		}
	},
	"99":{
		"day":{
			"description":"Thunderstorm With Hail",
			"image":"http://openweathermap.org/img/wn/11d@2x.png"
		},
		"night":{
			"description":"Thunderstorm With Hail",
			"image":"http://openweathermap.org/img/wn/11n@2x.png"
		}
	}
}

    def __init__(self,apikey, session=None, allowed_requests=1000, interval_ms=2500, padding_factor=5):
        super().__init__(session, allowed_requests, interval_ms, padding_factor)
        
        if apikey:
            self.__apikey = apikey
        else:
            raise ValueError('Api key needed')
       

    #Gets weather data for requested parameters
    #Datetime must be in YYYY-MM-DD
    def getWeatherJsonFromDate(self,datetime,lat=__DEF_LAT,lon=__DEF_LON,tz=__DEF_TZ,delay=0):

        args = {'latitude':lat,
                 'longitude':lon,
                 'start_date': datetime,
                 'end_date': datetime,
                 'daily': 'temperature_2m_max,temperature_2m_min,wind_direction_10m_dominant,wind_speed_10m_mean,weather_code,precipitation_sum,precipitation_hours,pressure_msl_mean'.split(','),
                 'temperature_unit':'fahrenheit',
                 'wind_speed_unit':'mph',
                 'precipitation_unit':'inch',
                 'tz': 'America%2FChicago',
        }
        
        logger.info(f'Making weather api call with args {args}')

        
        
        response = super().makeRequest(self.__URL,params=args,delay=delay)

        logger.debug(f'API call returned {response}')


        return response['content'] if response['status_code'] == 200 else None
        
        
    def getWeatherExpandedJsonWithWMOCodeInfo(self,datetime,lat=__DEF_LAT,lon=__DEF_LON,tz=__DEF_TZ,delay=0):
        response = self.getWeatherJsonFromDate(datetime,lat,lon,tz,delay)

        if not response:
            return None
        
        json_dict = json.loads(response)
        
        daily_weather = json_dict.get('daily') 
        
        wmo_code = str(daily_weather.get('weather_code')[0])

        if self.METEO_WEATHER_CODES.get(wmo_code):
            json_dict['daily']['weather_visual'] = self.METEO_WEATHER_CODES[wmo_code]
        else:
            logger.warning(f'Found wmo_code {wmo_code} not in WeatherRequestor\'s dict')

        return json.dumps(json_dict)
            


