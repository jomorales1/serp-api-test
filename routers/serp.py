from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Union
from configparser import ConfigParser
from serpapi import GoogleSearch

import os

cd = os.path.dirname(os.path.abspath(__file__))
config = ConfigParser()
config.read(cd + '/../config.cfg')
api_key = config.get('SerpAPI', 'api_key')


class RequestData(BaseModel):
    engine: str
    query: str
    location: Union[str, None] = None
    num: int
    as_ylo: Union[int, None] = None
    as_yhi: Union[int, None] = None
    hl: str

router = APIRouter()

@router.post('/search', tags=['search'], status_code=200)
async def get_report(request_data: RequestData):
    params = {'engine': request_data.engine, 'q': request_data.query, 'num': request_data.num, 'hl': request_data.hl, 'api_key': api_key}
    if request_data.as_ylo:
        params['as_ylo'] = request_data.as_ylo
    if request_data.as_yhi:
        params['as_yhi'] = request_data.as_yhi
    if request_data.location:
        params['location'] = request_data.location
    results = {}
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
    except Exception as error:
        raise HTTPException(status_code=500, detail=f'Error while retrieving search results\n{error}')
    return results
