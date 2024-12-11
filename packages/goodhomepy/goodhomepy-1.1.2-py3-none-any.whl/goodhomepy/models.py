from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Device(BaseModel):
    id: Optional[str] = Field(..., alias='_id')
    name: Optional[str]
    type: Optional[int]
    model: Optional[str]
    reference: Optional[str]
    client: Optional[str]
    linked_at: Optional[str]
    last_connection: Optional[str]
    home: Optional[str]
    owner: Optional[str]
    manufacturer: Optional[str]
    profile_name: Optional[str]
    timezone: Optional[str]
    serial_number: Optional[str]
    program: Optional[Dict[str, Any]]
    state: Optional[Dict[str, Any]]


class Home(BaseModel):
    id: Optional[str] = Field(..., alias='_id')
    street: Optional[str]
    zipcode: Optional[str]
    city: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]
    timezone: Optional[str]
    name: Optional[str]


class User(BaseModel):
    id: Optional[str] = Field(..., alias='_id')
    email: Optional[str]
    firstname: Optional[str]
    lastname: Optional[str]
    status: Optional[str]
    role: Optional[str]
    homes: Optional[List[str]]
    devices: Optional[List[str]]


class AuthResponse(BaseModel):
    token: Optional[str]
    id: Optional[str]
    role: Optional[str]
    refresh_token: Optional[str]


class VerifyTokenResponse(BaseModel):
    expire: Optional[int]


class RefreshTokenResponse(BaseModel):
    token: Optional[str]
