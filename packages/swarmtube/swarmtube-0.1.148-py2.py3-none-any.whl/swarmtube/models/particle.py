import random
from typing import List, Dict, Any
from enum import Enum

from pydantic import BaseModel, Field

from syncmodels.definitions import UID, URI, TAG, REGEXP
from syncmodels.model import Datetime


# Particle Tags
PARTICLE_PRIMARY = "primary"
PARTICLE_DERIVED = "derived"
PARTICLE_FLUSH = "flush"

PARTICLE_TAGS = [
    PARTICLE_PRIMARY,
    PARTICLE_DERIVED,
    PARTICLE_FLUSH,
]

# class ParticleKindEnum(Enum):
#     """TBD
#     Type of Particles"""
#
#     FINAL = 1

PARTICLE_NS = "particle"
PARTICLE_DB = "particle"


class ParticleDefinition(BaseModel):
    id: UID = Field(
        description="the unique identifier of particle",
        examples=["".join([random.choice("0123456789abcdef") for _ in range(40)])],
    )
    target: URI = Field(
        description="the target uri as holder of KPI",
        examples=[
            "test://test/mypki",
        ],
    )
    sources: List[URI] = Field(
        [],
        description="all the source uris that particle needs for computing",
        examples=[
            [
                "test://test/source_a",
                "test://test/source_b",
            ],
        ],
    )
    kind: str = Field(
        description="the king (class) of the particle that must be used",
        examples=[
            "XMAParticle",
            # "test://particle/sma",
        ],
    )
    specs: Dict[str, Any] = Field(
        {},
        description="the specs that overrides the default ones for the particle construction",
        examples=[
            {
                "__default__": 20,  # default
                "free": 4,
            },
        ],
    )
    tags: List[TAG] = Field(
        [],
        description="",
        examples=[
            PARTICLE_TAGS,
        ],
    )
    description: str = Field(
        "",
        description="the particle configuration description or purpose",
        examples=[
            "this particle computes the Simple Median Average of two inputs sources"
        ],
    )
    updated: Datetime = Field(None)


class ParticleRuntime(ParticleDefinition):
    hearbeat: Datetime | None = Field(None)


# ---------------------------------------------------------
# Request
# ---------------------------------------------------------
# TODO: MOVE this class to `syncmodels` as foundations


class Request(BaseModel):
    """A Kraken request to task manager.
    Contains all query data and search parameters.
    """

    filter: Dict[REGEXP, REGEXP] = Field(
        {},
        description="""
        {key: value} inventory filter (both can be regular expressions).
        Multiples values are allowed using AND operator.
        """,
        examples=[
            {
                "fquid": "foo.*bar.*",
            },
            {"name(s)?": r"foo-\d+", "bar": r".*blah$"},
            {"name|path": r".*flow.*"},
        ],
    )


class ParticleRequest(Request):
    """A particle request message information"""


# ---------------------------------------------------------
# Response
# ---------------------------------------------------------
# TODO: MOVE this class to `syncmodels` as foundations


class Response(BaseModel):
    """A Kraken response to task manager.
    Contains the search results given by a request.
    """

    num_items: int = 0
    elapsed: float = 0.0
    # result: Dict[UID_TYPE, Item] = {}


class ParticleResponse(Response):
    """A Kraken response to task manager.
    Contains the search results given by a request.
    """

    data: Dict[URI, ParticleRuntime] = {}
