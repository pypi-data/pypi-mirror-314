"""Main module."""

# library modules
import asyncio
import random
import re
import sys
import traceback
import functools
from typing import Callable, List, Dict, Any, Union
from datetime import datetime
from pprint import pformat
from pydantic import BaseModel
import itertools
import functools

from jinja2 import Template, StrictUndefined

from geomdl import BSpline, utilities, fitting

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from agptools.helpers import (
    build_uri,
    DATE,
    TO_NS,
    NOW,
    parse_uri,
    build_uri,
)
from agptools.containers import walk, soft
from agptools.logs import logger
from agptools.progress import Progress
from agptools.crontab import Crontab

from syncmodels.crud import parse_duri
from syncmodels.storage import (
    Storage,
    WaveStorage,
    tf,
    REG_SPLIT_PATH,
    SurrealConnectionPool,
)
from syncmodels.definitions import (
    URI,
    JSON,
    UID,
    WAVE,
    ORG_KEY,
    ID_KEY,
    REG_SPLIT_ID,
    extract_wave,
    DATETIME_KEY,
    REG_PRIVATE_KEY,
)
from syncmodels.wave import TUBE_SNAPSHOT
from syncmodels.model.geojson import to_geojson

from smartmodels.tokens import NAMESPACES, LOCATION, TYPES, ASPECT

# ---------------------------------------------------------
# local imports
# ---------------------------------------------------------
from ..definitions import MONOTONIC_KEY

WAVE_FACTOR = 10**9

# ---------------------------------------------------------
# models / mappers
# ---------------------------------------------------------
# from ..models.swarmtube import SwarmtubeApp
# from .. import mappers
# from ..models.enums import *
# from ..definitions import TAG_KEY

# ---------------------------------------------------------
# Loggers
# ---------------------------------------------------------

log = logger(__name__)


class Event(BaseModel):
    "TBD"
    wave: WAVE
    uid: UID
    payload: Any = None


class Broker:
    "Basic Broker capabilities"

    def __init__(self):
        self.subscriptions: Dict[UID, List[Callable]] = {}

    async def start(self):
        "any action related to start broker operations"

    async def stop(self):
        "any action related to stop broker operations"

    async def subscribe(self, uid: UID, callback: Callable):
        "TBD"
        inventory = self.subscriptions.setdefault(uid, [])
        if callback not in inventory:
            inventory.append(callback)

    async def unsubscribe(self, uid: UID, callback: Callable):
        "TBD"
        inventory = self.subscriptions.setdefault(uid, [])
        if callback in inventory:
            inventory.remove(callback)

    async def is_connected(self):
        return True


# TODO: agp: unify with syncmodels.iAgent/iRunner?
class iAgent:  # TODO: agp: is the same as syncmodels.iAgent/iRunner?
    IDLE_SLEEP = 5

    def __init__(
        self,
        uid,
        broker: Broker,
        storage: Union[WaveStorage, Storage],
        meta=None,
        prefix="",
        target="",
        *args,
        **kw,
    ):
        if not prefix:
            prefix = uid
        self.uid = uid
        self.broker = broker
        self.storage = storage

        self.state = ST_INIT
        self.meta = {} if meta is None else meta

        # prefix template
        # TODO: agp: have the same capabilities as syncmodels.iAgent
        self.prefix = prefix
        if prefix:
            if isinstance(prefix, str):
                _uri = parse_duri(prefix)
                if not _uri["_path"] and (
                    m := re.match(r"/?(?P<prefix>.*?)/?$", prefix)
                ):
                    d = m.groupdict()
                    if d["prefix"]:
                        prefix = "/{{{prefix}}}".format_map(d)
                prefix_template = Template(prefix)
                assert isinstance(prefix_template, Template)
            else:
                prefix_template = prefix

            self.prefix_template = prefix_template
            self.prefix = prefix

        # super().__init__(*args, **kw)

    def render(self, template=None, **kw):
        template = template or self.prefix_template
        soft(kw, self.__dict__)

        result = template.render(kw)
        return result

    async def main(self):
        "main loop"
        # await super().main()
        await self._start_live()
        while self.state < ST_STOPPED:
            await self._idle()
        await self._stop_live()

    async def _start_live(self):
        log.info("[%s] _start_live", self.uid)

    async def _stop_live(self):
        log.info("[%s] _stop_live", self.uid)

    async def _idle(self):
        # log.debug("[%s] alive", self.uid)
        await asyncio.sleep(self.IDLE_SLEEP)


class Tube(iAgent):
    """Represents the concept of a stream of events that
    can be located by a UID or searching metadata
    """

    uid: UID

    def __init__(
        self,
        uid: UID,
        sources: List[UID],
        broker: Broker,
        storage: Storage,
        meta=None,
        **kw,
    ):
        super().__init__(uid=uid, broker=broker, storage=storage, meta=meta, **kw)
        self.sources = sources
        assert isinstance(self.storage, WaveStorage), "needed for subscriptions"
        # TODO: use regexp and instrospection to subcribe multiples
        # TODO: sources


class App(iAgent):
    "TBD"
    TIME_TO_LIVE = sys.float_info.max

    def __init__(self, uid="app", *args, **kw):
        super().__init__(uid=uid, *args, **kw)
        self.tubes = {}
        self.tasks = {}
        self.loop = None
        self.t0 = 0

    async def _start_live(self):
        assert self.loop is None
        self.loop = asyncio.get_running_loop()
        self.t0 = self.loop.time()

        # start broker and storage
        await self.storage.start()
        await self.broker.start()

        # start tubes
        for uid, tube in self.tubes.items():
            log.info("- starting: [%s]", uid)
            self.tasks[uid] = self.loop.create_task(tube.main(), name=uid)

    async def _stop_live(self):
        # requests fibers to TERM
        for uid, tube in self.tubes.items():
            log.info("- term: [%s]", uid)
            tube.state = ST_STOPPED

        # wait and clear stopped for 5 secs
        t0 = self.loop.time()
        while self.tasks and self.loop.time() - t0 < 5:
            for uid, task in list(self.tasks.items()):
                if task.done():
                    self.tasks.pop(uid)
                    log.info("- end: [%s]", uid)
            await asyncio.sleep(0.5)

        # kill remaining
        for uid, task in self.tasks.items():
            log.info("- kill: [%s]", uid)
            task.cancel()

        # wait and clear stopped for 5 secs
        t0 = self.loop.time()
        while self.tasks and self.loop.time() - t0 < 5:
            for uid, task in list(self.tasks.items()):
                if task.done():
                    self.tasks.pop(uid)
                    log.info("- finished: [%s]", uid)
            await asyncio.sleep(0.5)

        # stop broker and storage
        await self.storage.stop()
        await self.broker.stop()

    def must_stop(self):
        return len(self.tubes) < 1

    def add(self, *tubes):
        for tube in tubes:
            self.tubes[tube.uid] = tube

    def run(self):
        asyncio.run(self.main())

    async def _idle(self):
        await super()._idle()
        if self.must_stop():
            self.state = ST_STOPPED
            log.info("[%s] want stop", self.uid)


ST_INIT = 0
ST_HISTORICAL = 1
ST_SWITCHING = 2
ST_LIVE = 3
ST_STOPPED = 4


class Clock(Tube):
    "A tube that emit a clock tick"
    counter: int

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.counter = 0

    async def _start_live(self):
        await super()._start_live()

    async def _stop_live(self):
        await super()._stop_live()

    async def _idle(self):
        await super()._idle()
        self.counter += 1
        edge = {
            # MONOTONIC_KEY: time.time(),  # TODO: let the storage set this value?
            #'uid': uid,
            "payload": self.counter,
        }
        await self.storage.put(self.uid, edge)


class SwarmTubeException(Exception):
    "base for all SwarmTube Exceptions"


class SkipWave(SwarmTubeException):
    """the item can't be processed but we
    need to advance the Wave to the next one
    """


class RetryWave(SwarmTubeException):
    """the item can't be processed but we
    need to retry later on, so the Wave
    doesn't jump to the next one
    """


class Particle(Tube):
    "TBD"
    MAX_EVENTS = 1024
    _live = Dict[UID, List[Event]] | None
    _historical = Dict[UID, List[Event]] | None

    RETRY_DELAY = 15
    LIVE_WAITING = 10

    def __init__(
        self,
        uid: UID,
        sources: List[UID],
        broker: Broker,
        storage: Storage,
        since=None,
        specs=None,
        **kw,
    ):
        super().__init__(uid, sources=sources, broker=broker, storage=storage, **kw)
        self.since = since
        self.specs = specs or {}
        self._wave = {}
        self._live = {}
        self._historical = {}
        self._live_activity = asyncio.Queue()
        self._need_resync = False

        self._milk = set()
        self._wip_edge = {}

        self._wip_uncompleted = set()

        self.context = {}

        self.metrics = Progress()

    async def main(self):
        "TBD"
        self._need_resync = True
        # self.metrics.start()
        while self._need_resync:
            self._need_resync = False
            await self._find_sources()

            await self._start_live()
            await self._start_historical()

        log.info("=" * 70)
        log.info("[%s] >> Idle", self.uid)
        log.info("=" * 70)

        context = self.context
        while self.state < ST_STOPPED:
            try:
                # live processing must be based on analyzing
                # the while buffer, not just reacting to a single event
                # (as if we're processing historical data) because
                # it's safer (race-conditions)
                event = await asyncio.wait_for(
                    self._live_activity.get(),
                    timeout=self.LIVE_WAITING,
                )
                edge = await self.pop_edge(self._live, context)
                if edge:
                    await self.dispatch(edge)
                    # self._wave[_uid] = _wave
            except asyncio.TimeoutError:
                # we only can sent datetime event when live connection
                #  is active, in order not to move forward the crontab
                # cursors and have problems when connection comes back again
                if await self.broker.is_connected():
                    context[DATETIME_KEY] = NOW()
                    self._live_activity.put_nowait(True)
                    # self._milk.clear()
                pass  #  No live data has been received
            except Exception as why:
                log.error(why)
                log.error("".join(traceback.format_exception(*sys.exc_info())))

            # self._live_activity.clear()

            self.metrics.update(n=0)

        await self._stop_live()

    async def _find_sources(self):
        """find and expand sources as patterns, allowing regexp
        instead defining each of them
        """
        storage = self.storage.storage

        sources = []
        for uri in self.sources:
            _uri = parse_duri(uri)
            nsdb = "{fscheme}://{host}".format_map(_uri)
            info = await storage.info(nsdb)
            pattern = _uri["_path"]
            # pattern = tf(pattern) # don't use tr() will alter regexp
            pattern = pattern.replace("/", "_")

            for table in info["tables"]:
                if re.match(f"{pattern}$", table):
                    _uri["path"] = f"/{table}"
                    fquid = build_uri(**_uri)
                    sources.append(fquid)

        if sources:
            log.info("source pattern: %s", self.sources)
            log.info("found [%s] sources", len(sources))
            for idx, tubename in enumerate(sources):
                log.info("[%s]: %s", idx, tubename)
        else:
            log.error(
                "can't find any source using these patterns: %s",
                self.sources,
            )
            log.error("exiting, particle will not start")

        self.sources = sources
        for uri in self.sources:
            # TODO: use faster dqueue?
            self._live[uri] = []
            self._historical[uri] = []

    async def _start_live(self):
        "TBD"
        log.info("[%s] ++ Requesting LIVE STREAMING", self.uid)

        for uid in self.sources:
            await self.broker.subscribe(uid, self.live)

    async def _stop_live(self):
        "TBD"
        for uid in self.sources:
            await self.broker.unsubscribe(uid, self.live)

    def _new_wip(self):
        self._wip_edge = {_: [] for _ in self.sources}
        self._wip_uncompleted = set(self.sources)

    async def _start_historical(self):
        "TBD"
        self.state = ST_HISTORICAL
        self._wave = await self.storage.last_waves(self.prefix, self.sources, self.uid)
        if self.since is not None:
            wave__ = TO_NS(self.since.timestamp())
            for key in list(self._wave):
                self._wave[key] = wave__

        assert isinstance(self._wave, Dict), "missing await?"

        # self._wave = {uid: _wave for uid in self.sources}

        log.info("-" * 80)
        log.info("[%s] -- Switching to HISTORICAL", self.uid)
        log.info("-" * 80)

        # init feeding variables
        buffer = self._historical
        self._milk.update(self.sources)

        # reset WIP edge variables
        self._new_wip()

        context = self.context

        while self.state < ST_LIVE:
            # for each input source, feed the historical with ALL
            # available data as we can't switch to LIVE streaming
            # until all historical data has been moved to 'live'
            # buffers when WIP edge can't be completed because
            # some sources are missing.

            # the number of data included from storage
            n = 0

            for uid in self._milk:
                stream = await self.storage.storage.since(
                    uid, self._wave[uid], max_results=self.MAX_EVENTS
                )
                if stream:  # is ordeder by MONOTONIC_KEY
                    buffer[uid].extend(stream)
                    n += len(stream)
                    self._wave[uid] = extract_wave(stream[-1])
            self._milk.clear()

            if n == 0:  # no more historical data
                # move live data to historical and try to continue until
                # we get a state with no more historical data and no more live data
                self.state = ST_SWITCHING
                # time.sleep(0.9)
                assert id(buffer) != id(self._live)
                for uid, _buff in self._live.items():
                    _hist = self._historical[uid]
                    while True:
                        try:
                            candidate = _buff.pop(0)
                            if candidate[MONOTONIC_KEY] > self._wave[uid]:
                                _hist.append(candidate)
                                n += 1
                            else:
                                # this live event has been captured by historical polling
                                # so is already processed
                                # print(f"*** already processed: --> {candidate}")
                                pass
                        except IndexError:
                            break
                if n == 0:
                    log.info("*" * 80)
                    log.info("[%s] ** Switching to LIVE STREAMING **", self.uid)
                    log.info("*" * 80)
                    self.metrics.update(n=0, force=True)
                    self.state = ST_LIVE

            # try to process buffer
            while self.state < ST_LIVE:
                # TODO: remove DEBUG
                if not all(buffer.values()):
                    foo = 1  # must milk!!
                # TODO: HERE: if milked, cut_wave really necesary? <-------------
                n_edges = 0
                async for edge in self.pop_edge(buffer, context):
                    await self.dispatch(edge)
                    n_edges += 1

                if not n_edges:
                    if self.state == ST_SWITCHING:
                        break
                    elif self._milk:
                        break  # continue loading more historical
                    else:
                        # edge can be generate but buffer maybe has data
                        # so we need to continue feeding wip_edge
                        # until an edge can be generated
                        for uid, _ in buffer.items():
                            # check that we have data to process
                            if not _:
                                self._milk.add(uid)
                        if self._milk:
                            break  # continue loading more historical


                # edge = await self.pop_edge(buffer, context)
                # if edge:
                #     await self.dispatch(edge)
                # elif self.state == ST_SWITCHING:
                #     break
                # elif self._milk:
                #     break  # continue loading more historical
                # else:
                #     # edge can be generate but buffer maybe has data
                #     # so we need to continue feeding wip_edge
                #     # until an edge can be generated
                #     for uid, _ in buffer.items():
                #         # check that we have data to process
                #         if not _:
                #             self._milk.add(uid)
                #     if self._milk:
                #         break  # continue loading more historical

            # check if we have an overflow while processing historical data
            if self._need_resync:
                log.info(
                    "[%s] *** ---> Request Stopping Streaming due OVERFLOW",
                    self.uid,
                )
                await self._stop_live()

    def live(self, _uri: UID, event: Dict):
        "TBD"
        uri = _uri["uri"]
        # TODO: REVIEW it looks like is handled at the end as well ...
        if len(self._live[uri]) >= self.MAX_EVENTS:
            self._need_resync = True
            return

        # wave_uri = parse_duri(event['id'])
        if MONOTONIC_KEY not in event:
            m = REG_SPLIT_PATH.match(event["id"])
            if m:
                event[MONOTONIC_KEY] = m.groupdict()["id"]

        self._live[uri].append(event)
        # self._live_activity.put_nowait(event)
        self._live_activity.put_nowait(False)

        if self.state == ST_LIVE:
            pass
        elif len(self._live[uri]) >= self.MAX_EVENTS:
            # request stop streaming and a new re-sync process
            # TODO: REVIEW it looks like is handled at the beginning as well ...
            self._need_resync = True

    async def pop_edge_old(self, buffer, context):
        """Analyze buffer and return an edge if all data
        is available for processing the next step"""
        # TODO: implement a policy delegation criteria to know when edge is ready to be processed

        await self._wip_feed(buffer, context)
        # check if we must send the WIP edge
        if self._wip_uncompleted:
            pass
        else:
            # WIP edge is completed, so return it back and
            # reset WIP place holders for the next edge
            edge = self._wip_edge  # get a reference
            self._new_wip()  # that will be lost here

            # avoid sending empty edges
            if all(edge.values()):
                if MONOTONIC_KEY not in edge:
                    # we need to provide a MONOTONIC_KEY to the edge
                    # try to get the minimal wave value from returned
                    # egde
                    waves = set()
                    for key, value in walk(edge):
                        if key and key[-1] in (MONOTONIC_KEY,):
                            waves.add(value)
                    if waves:
                        edge[MONOTONIC_KEY] = max(waves)
                    else:
                        # error
                        log.error("can't find any %s in the edge!", MONOTONIC_KEY)
                        log.error("%s", edge)

                return edge


    async def pop_edge(self, buffer, context):
        """Analyze buffer and return an edge if all data
        is available for processing the next step"""
        # TODO: implement a policy delegation criteria to know when edge is ready to be processed

        # await self._wip_feed(buffer, context)

        async for edge in  self._wip_feed(buffer, context):
            self._new_wip()  # that will be lost here

            # avoid sending empty edges
            if all(edge.values()):
                if MONOTONIC_KEY not in edge:
                    # we need to provide a MONOTONIC_KEY to the edge
                    # try to get the minimal wave value from returned
                    # egde
                    waves = set()
                    for key, value in walk(edge):
                        if key and key[-1] in (MONOTONIC_KEY,):
                            waves.add(value)
                    if waves:
                        edge[MONOTONIC_KEY] = max(waves)
                    else:
                        # error
                        log.error("can't find any %s in the edge!", MONOTONIC_KEY)
                        log.error("%s", edge)

                yield edge

        yield None
        # check if we must send the WIP edge
        if self._wip_uncompleted:
            pass
        else:
            # WIP edge is completed, so return it back and
            # reset WIP place holders for the next edge
            edge = self._wip_edge  # get a reference
            self._new_wip()  # that will be lost here

            # avoid sending empty edges
            if all(edge.values()):
                if MONOTONIC_KEY not in edge:
                    # we need to provide a MONOTONIC_KEY to the edge
                    # try to get the minimal wave value from returned
                    # egde
                    waves = set()
                    for key, value in walk(edge):
                        if key and key[-1] in (MONOTONIC_KEY,):
                            waves.add(value)
                    if waves:
                        edge[MONOTONIC_KEY] = max(waves)
                    else:
                        # error
                        log.error("can't find any %s in the edge!", MONOTONIC_KEY)
                        log.error("%s", edge)

                yield edge


    def _ordered_streaming(self, buffer):
        unified = []
        for uid, stream in buffer.items():
            for data in stream:
                wave__ = data.get(MONOTONIC_KEY)
                assert wave__
                unified.append((wave__, uid, data))

        unified.sort()
        return unified

    async def _wip_feed(self, buffer, context):
        """
        Extract the current `edge` if it's ready for processing
        and move forward the stream for the next step
        dropping all values that are going to be used


        Default policy is to do the minimal step for computation.
        - get the minimal wave
        - drop the input related with the minimal wave
        - return a custom `edge` for computation
        """
        for wave__, uid, data in self._ordered_streaming(buffer):
            stream = buffer[uid]
            _data = stream.pop(0)
            assert id(data) == id(_data)  # TODO: REMOVE check

            self._wip_edge[uid].append(data)
            if uid in self._wip_uncompleted:
                self._wip_uncompleted.remove(uid)
            if not self._wip_uncompleted:
                ts = extract_wave(data) or data.get(MONOTONIC_KEY)
                self._wip_edge[MONOTONIC_KEY] = TO_NS(ts)
                break  # generate a edge

    def _cut_edge(self, buffer, cut_wave):
        # TODO: delete, not used
        edge = {}
        milked = []

        for uid, stream in buffer.items():
            item = stream[0]
            item_wave = extract_wave(item)
            if item_wave <= cut_wave:
                # extract from buffer
                stream.pop(0)
                milked.append(uid)
            edge[uid] = item

        return milked, edge

    async def dispatch(self, edge):
        "TBD"
        # build the data to be processed
        # split metadata (".*__" fields by now) and each
        # input stream
        # TODO: review the criteria for keywords filtering
        ikeys = set([k for k in edge if k.endswith("__")])
        ekeys = ikeys.symmetric_difference(edge)
        assert ekeys, "no payload in the edge?"

        # set found metadata
        data = {k: edge[k] for k in ikeys}
        uid_template = Template(self.uid)
        while self.state < ST_STOPPED:
            log.info("[%s] -> dispatch", self.uid)
            log.info("%s", pformat(edge))
            try:
                # do the computation
                # compute must yield data (async and yield)
                async for payload in self._compute(edge, ekeys):
                    # update
                    if payload:
                        data[MONOTONIC_KEY] = data.get(MONOTONIC_KEY) + 1
                        data.update(payload)
                        # store results
                        # and shift sync / waves info
                        uid = uid_template.render(**data, **self.__dict__)
                        await self.storage.put(uid, data)

                    N = sum([len(_) for _ in self._live.values()])
                    self.metrics.update(buffer=N)
                    log.info("[%s] <- dispatch:", self.uid)
                    log.info("%s", pformat(data))

                wave = data.get(MONOTONIC_KEY)  # Must exist!
                if wave:
                    await self.storage.update_sync_wave(
                        self.prefix,
                        self.sources,
                        self.uid,
                        wave,
                    )
                else:
                    log.error("data %s has no %s key", data, MONOTONIC_KEY)
                break  #  let continue with next wave
            except SkipWave as why:
                # some error is produced, but we want to jump to the next wave
                wave = data.get(MONOTONIC_KEY)  # Must exist!
                if wave:
                    log.info("Skip wave [%s], reason: %s", wave, why)

                    await self.storage.update_sync_wave(
                        self.prefix,
                        self.sources,
                        self.uid,
                        wave,
                    )
                else:
                    log.error("data %s has no %s key!", data, MONOTONIC_KEY)
                break  #  let continue with next wave
            except RetryWave as why:
                delay = self.RETRY_DELAY
                for msg in why.args:
                    log.info("Retry wave, reason: %s", msg)
                    if isinstance(msg, dict):
                        delay = msg.get("delay", self.RETRY_DELAY)
                log.warning(
                    "%s._compute() has failed but is needed a retry (%s secs)",
                    str(self),
                    delay,
                )
                await asyncio.sleep(delay)
            except Exception as why:
                log.error(why)
                log.error("".join(traceback.format_exception(*sys.exc_info())))
                delay = self.RETRY_DELAY * 10
                log.warning(
                    "%s._compute() has failed for an UNEXPECTED reason. "
                    "Wave edge can't be moved forward, retry in (%s secs)",
                    str(self),
                    delay,
                )
                await asyncio.sleep(delay)

    async def _compute(self, edge, ekeys):
        """
        Return None if we don't want to store info
        """
        raise NotImplementedError()


class iGeo:
    GEO_CACHE = {}
    MAX_GEO_CACHE = 1000

    storage: WaveStorage = None

    GEO_URI_TEMPLATE = f"{NAMESPACES.INFRASTRUCTURE.value}://centesimal/{TUBE_SNAPSHOT}"

    def __init__(self, uid, sources, broker, storage, **kw):
        kw.setdefault("geo_uri_template", self.GEO_URI_TEMPLATE),
        soft(
            kw.setdefault("specs", {}),
            {
                "__default__": 5,  # None means Default
            },
        )
        super().__init__(uid, sources, broker, storage, **kw)
        self.geo_uri_template = kw["geo_uri_template"]
        self._cached_M = {}

    async def _get_geolocation(self, data):

        geo_hash__ = []
        geo_keys__ = set(
            [
                "ubication",
            ]
        ).intersection(data)
        geo_keys__ = list(geo_keys__)
        geo_keys__.sort()

        if not geo_keys__:
            log.error("can't find geolocation in [%s]", data)
        geo_params = {}

        for key in geo_keys__:
            value = data.get(key)
            geo_params[key] = value
            geo_hash__.append(value)

        geo_hash__ = tuple(geo_hash__)
        if not (geo_point := self.GEO_CACHE.get(geo_hash__)):
            # get the last one
            try:
                for geo_location in await self.storage.query(
                    self.geo_uri_template, **geo_params
                ):
                    geo_data = geo_location["geometry"]
                    geo_point = to_geojson(geo_data)
                    if len(self.GEO_CACHE) > self.MAX_GEO_CACHE:
                        self._free_geo_cache()
                    self.GEO_CACHE[geo_hash__] = geo_point

            except Exception as why:
                foo = 1
            pass

        data["geo_point__"] = geo_point
        data["geo_keys__"] = geo_keys__
        data["geo_hash__"] = geo_hash__

        return geo_keys__, geo_hash__, geo_point

    def _free_geo_cache(self):
        keys = list(self.GEO_CACHE)
        random.shuffle(keys)
        for key in list(keys[: self.MAX_GEO_CACHE // 3]):
            self.GEO_CACHE.pop(key)


class XParticle(iGeo, Particle):
    "TBD: extended particle"
    EXCLUDE = f"id$|{REG_PRIVATE_KEY}"
    FULL_EXCLUDE = f"{EXCLUDE}|datetime"
    IDS_KEYS = set([ID_KEY, ORG_KEY])
    DATETIME = ["datetime", MONOTONIC_KEY]

    DEFAULT_TARGET = "{{ uid }}:{{ name }}"

    def __init__(self, uid, sources, broker, storage, **kw):
        soft(
            kw.setdefault("specs", {}),
            {
                "__default__": 5,  # means Default
                "second": 0,
            },
        )
        soft(
            kw,
            {
                "target": self.DEFAULT_TARGET,
            },
        )
        kw.setdefault("group_by", [])
        super().__init__(uid, sources, broker, storage, **kw)

        self.group_by = kw.get("group_by")
        self.cron = {_: Crontab(**self.specs) for _ in sources}
        self._wip_cursor = {_: None for _ in sources}
        self._wip_tmp_edge = {_: {} for _ in sources}
        self._wip_known_keys = {_: set() for _ in sources}

    async def _wip_feed(self, buffer, context):
        """
        We can process buffers in the same way for historical
        data or streaming data as wip internal structure must
        be filled in any order.

        Particle need to wait until some criteria is reached
        and we can compute all defined stats and interpolate
        values in the time-mark defined by "cron" specs, etc
        depending on the XParticle sub-classing.

        What is true, is every data used must be retired from
        buffers, but we can process buffers in any "uid" order.

        Then, cleaning process due by "_new_wip" may keep some
        data for the next cycle, but it's depends on what type
        of interpolation methods are we using.

        - explore _wip_uncompleted signals
        - reach a point where we can stop getting more data from this signal
        - this depends on the interpolation method that we're using
        - remove from _wip_uncompleted
        - continue until all signal are ready (not _wip_uncompleted)
        - do the stats computation within the period t0->t1
        - compute interpolated values in t1
        - clean and do a step forward (_new_wip)

        """
        for wave__, uid, data in self._ordered_streaming(buffer):
            # TODO: remove stream.pop() if we process all the buffers
            # TODO: it'll be faster
            stream = buffer[uid]
            _data = stream.pop(0)
            assert id(data) == id(_data)  # TODO: REMOVE check

            point = await self._wip_build_point(data)
            self._wip_add_point(uid, point)
            # TODO: debug, simulate live streaming
            # if False and random.random() < 0.10:
            #     break
        else:
            # milk?
            pass

        # we've classify all data to determine the logic of
        # the particle, so let's try to update the wip edge
        # with this new data, whatever this means for the subclass
        for ready in self._is_wip_edge_completed(buffer, context):
            yield ready
            # self._push_wip_edge(ready)

    async def _wip_get_data_keys(self, data):
        """"""
        keys = [_ for _ in data if not re.match(self.FULL_EXCLUDE, _)]
        keys = self.group_by + keys
        data_keys = set([_ for _ in keys if isinstance(data[_], (int, float))])

        return set(keys), data_keys

    async def _wip_build_point(self, data):
        await self._get_geolocation(data)

        keys, data_keys = await self._wip_get_data_keys(data)

        point = {}
        point["keys"] = keys
        point["value_keys"] = data_keys

        structure_keys = list(keys.difference(data_keys))
        structure_keys.sort()
        structure_values = tuple([data[_] for _ in structure_keys])
        data_values = {_: data[_] for _ in data_keys}

        point["structure_keys"] = structure_keys
        point["structure_values"] = structure_values
        point["value_values"] = data_values
        point["org"] = data
        point["group_by__"] = data.pop("group_by__", None)

        # TODO: use cache
        for k in self.DATETIME:
            if k in data:
                # use a coherent datetime no matter the source
                point["datetime"] = DATE(data[k])
                break
        else:
            log.error("can't find a datetime key from %s candidates", self.DATETIME)

        return point

    def _wip_add_point(self, uid, point):

        # find interpolation datetime
        dt = point["datetime"]
        # place the data point in its structural value
        holder_key = point["structure_values"]
        self._wip_known_keys[uid].add(holder_key)

        # find the holder for this uid and iterpolation time
        # we allocate all related data with its interpolation slot
        uid_holder = self._wip_tmp_edge[uid]
        # if group_by := point.get("group_by__"):
        #     uid_holder = uid_holder.setdefault(group_by, {})

        interpolation_holder = uid_holder.setdefault(dt, {})
        # use a list to sort the signals point received
        last_holder = interpolation_holder.setdefault(holder_key, [])
        # insert backwards
        for idx in range(len(last_holder), 0, -1):
            if last_holder[idx - 1]["datetime"] < dt:
                last_holder.insert(idx, point)
                break
        else:
            last_holder.append(point)
            idx = 0

    def _is_wip_edge_completed(self, buffer, context) -> bool:
        raise NotImplementedError()

    def _push_wip_edge(self, ready):
        raise NotImplementedError()

    def _find_1st_cursor(self, uid):
        uid_holder = self._wip_tmp_edge[uid]
        known_idt = list(uid_holder)
        known_idt.sort()
        idt0 = known_idt[0]

        cron = self.cron[uid]
        t0 = cron.next_ts(idt0)
        self._wip_cursor[uid] = t0
        return t0

    def _new_wip(self):
        super()._new_wip()
        for _ in self.sources:
            self._wip_tmp_edge.setdefault(_, {})
            # self._wip_edge.setdefault(_, {})
            # self._wip_nurbs.setdefault(_, {})

        # self._wip_uncompleted = set(self.sources)

    def _find_M(self, key):
        for pattern, M in self.specs.items():
            if pattern:
                if re.match(pattern, key):
                    self._cached_M[key] = M
                    break
        else:
            # get default value (key = "")
            self._cached_M[key] = M = self.specs.get("__default__")

        return M

    def _calc(self, old_values, new_values):
        raise RuntimeError("you need to implement this incremental compute")

class XInterpolate(XParticle):
    """A particle that condense and interpolate information before
    generate a new edge

    Some operations may be executed in cascade using subclassing
    """

    def __init__(self, uid, sources, broker, storage, **kw):

        super().__init__(uid, sources, broker, storage, **kw)

        self._wip_pending_edge = {_: set() for _ in sources}
        self._wip_idt_found = {_: {} for _ in sources}
        self._wip_nurbs = {}
        self._wip_result = {_: {} for _ in sources}

        self._wip_known_idt = {_: [] for _ in sources}
        self._cached_M = {}

    def _new_wip(self):
        super()._new_wip()
        # XInterpolate never cleans its historical by default
        # so don't do something like:
        # self._wip_edge = {_: {} for _ in self.sources}
        # but
        for _ in self.sources:
            self._wip_tmp_edge.setdefault(_, {})
            # self._wip_edge.setdefault(_, {})
            self._wip_nurbs.setdefault(_, {})

        # self._wip_uncompleted = set(self.sources)

    def _wip_add_point(self, uid, point):
        # find interpolation datetime
        dt = point["datetime"]
        # place the data point in its structural value
        holder_key = point["structure_values"]
        self._wip_known_keys[uid].add(holder_key)

        # find the holder for this uid and iterpolation time
        # we allocate all related data with its interpolation slot
        uid_holder = self._wip_tmp_edge[uid]
        interpolation_holder = uid_holder.setdefault(dt, {})
        # use a list to sort the signals point received
        last_holder = interpolation_holder.setdefault(holder_key, [])
        # insert backwards
        for idx in range(len(last_holder), 0, -1):
            if last_holder[idx - 1]["datetime"] < dt:
                last_holder.insert(idx, point)
                break
        else:
            last_holder.append(point)
            idx = 0

        # add nurbs info
        tid = dt.timestamp() + dt.microsecond
        uid_nurbs = self._wip_nurbs[uid]
        nurbs_interpolation_holder = uid_nurbs.setdefault(holder_key, {})
        for key, value in point["value_values"].items():
            nurbs_data = nurbs_interpolation_holder.setdefault(key, [])
            nurbs_data.append([tid, value])
            # nurbs_data.insert(idx, [tid, value])

    def _is_wip_edge_completed(self, buffer, context) -> bool:
        """
        1. find tge next time mark (t0) from the 1st data received
        2. t0 > datetime of 1st data point
        3. create a record for each different data point in order to check:
        4. add this signal to pending ones
        5. update lower bound_t0, t0, upper bound_t1
         . loop for geting more data
         . update the record
        6. check if record has cross t0 limit
        7. is eligible for interpolating in t0
        8. remove this signal from pending
        9. when no more pending signals are waiting to complete, we can generate an edge
        10. if we receive a point over t1, the we force all pending singals to be part
            of the edge despite we've no data that have crossed the t0 line

        """
        result = {}
        try:

            for uid, uid_holder in self._wip_tmp_edge.items():
                # 2. t0 > datetime of 1st data point
                known_idt = list(uid_holder)
                known_idt.sort()

                # 1. find tge next time mark (t0) from the 1st data received
                if t0 := self._wip_cursor.get(uid):
                    t1 = self.cron[uid].next_ts(t0)
                else:
                    t0 = self._find_1st_cursor(uid)
                    t1 = self.cron[uid].next_ts(t0)
                    delta = t1 - t0
                    t1 = t0
                    t0 = t0 - delta
                    assert t1 > known_idt[0]

                if not known_idt or (idt1 := known_idt[-1]) < t1:
                    # we've not crossed t1 boundary yet
                    continue

                # recollect all keys that can be interpolated
                idt_found = self._wip_idt_found[uid]
                pending = self._wip_pending_edge[uid]
                # _result = self._wip_result[uid]

                # TODO: agp: can we drop values that have been used?
                # TODO: in that case, t1 will be automatically computed
                for idt in known_idt:  # sorted
                    for key, data in uid_holder.get(idt, {}).items():

                        # 3. create a record for each different data point
                        if not (record := idt_found.get(key)):
                            if idt <= t1:
                                record = idt_found[key] = [idt1, idt, t1]
                                # 4. add this signal to pending ones
                                pending.add(key)
                            else:
                                # ignore creation of a unseen record because
                                # it starts in a future interval
                                continue

                        # 5. update lower bound_t1, t1, upper bound_t1
                        record[0] = min(record[0], idt)
                        record[1] = max(record[1], idt)

                        # 6. check if record has cross t1 limit
                        if record[0] < t1 and record[1] > record[-1]:
                            # 7. is eligible for interpolating in t1
                            # _result.setdefault(uid, {})[key] = record

                            # 8. remove this signal from pending
                            if key in pending:
                                pending.remove(key)
                                if not pending:
                                    break

                    # 10. if we receive a point over t1, the we force edge
                    if not pending or idt == idt1:
                        pending.clear()
                        break
                # 9. when no more pending signals are waiting
                # to complete, we can generate an edge
                if not pending:
                    self._wip_cursor[uid] = t1
                    result[uid] = idt_found.copy()
                    # cleanning
                    idt_found.clear()
                    break

        except Exception as why:
            log.error(why)
            log.error("".join(traceback.format_exception(*sys.exc_info())))
            print(why)

        return result

    def _update_wip_edge(self, buffer, context):
        assert False
        delta = context.setdefault("delta", {})

        for uid, info in delta.items():
            holder_key = info["structure_values"]
            new_values = info["value_values"]

            uid_holder = self._wip_tmp_edge[uid]
            last_holder = uid_holder.setdefault(holder_key, {})
            last_holder["org"] = info["org"]
            old_values = last_holder.setdefault("last", new_values)

            self._calc(old_values, new_values)

    async def _compute(self, edge, ekeys):
        raise NotImplementedError()

    def _push_wip_edge(self, ready):
        try:
            for uid, info in ready.items():
                nurbs_data = self._wip_nurbs[uid]
                tmp_holder = self._wip_tmp_edge[uid]
                interpolated = self._wip_edge
                for key, known_idts in info.items():
                    data = nurbs_data[key]
                    _info = info[key]
                    for parameter, data_points in data.items():
                        # TODO: remove
                        interval = [_.timestamp() for _ in _info]
                        bt0, bt1, t0 = interval
                        if (r := bt1 - bt0) > 0:
                            # we have more than 1 point
                            x = (t0 - bt0) / r
                        else:
                            x = 2.0  # > 1.0

                        if x < 1.0:
                            # use NURBS for interpolating, but we need to find the real `x`
                            assert 0.0 <= x <= 1.0
                            assert bt0 < t0 < bt1

                            # points = []
                            # for p in data_points:
                            #     p = p.copy()
                            #     p[0] -= bt0
                            #     points.append(p)

                            points = data_points

                            # calc value
                            p0, p1 = None, None
                            N = len(points)
                            for idx, p in enumerate(points):
                                p0 = p1
                                p1 = p
                                if p1[0] > t0:
                                    # estimate the real value of x € [0,1]
                                    # x = float(idx) / N
                                    # use a lineal interpolation
                                    f = (t0 - p0[0]) / (p1[0] - p0[0])
                                    x += f / N
                                    v = p0[1] + (p1[1] - p0[1]) * f
                                    value = [t0, v]
                                    break
                            else:
                                raise RuntimeError()
                            foo = 1

                            # using interpolation?
                            # value0 = curve.evaluate_single(x)

                            debug = False
                            if debug:
                                # degree = 1 if len(points) <= 10 else 2
                                degree = 1
                                curve = fitting.interpolate_curve(points, degree)
                                self._plot(curve, points, value, key)
                        else:
                            # we can't extrapolate, so the the lastest value
                            for value in data_points:
                                if value[0] >= bt1:
                                    value = [t0, value[1]]
                                    break
                            else:
                                log.error(
                                    "can't find  the lastest value from signal, using 1st one!"
                                )
                                value = [t0, data_points[-1][1]]

                        assert len(value) == 2

                        error = value[0] - t0
                        if error > 60:
                            log.warning(
                                "interpolated date and real one differs: %s sec (> 60 secs)",
                                error,
                            )
                        # tsample = datetime.fromtimestamp(value[0])
                        dt = value[0] = _info[2]

                        # we can remove from _wip_tmp_edge
                        # but preserve _wip_nurbs as it's been computed by timestamp
                        # and may be usefull for better interpolation (higher degree)
                        # we can drop some values from _wip_nurbs as we want if we
                        # keep the necessary points

                        # drop the data that has been used somehow
                        received = {}

                        # must be sorted to get the last received!
                        all_idts = list(tmp_holder)
                        all_idts.sort()
                        for bdt in all_idts:
                            if bdt > dt:
                                break
                            dated_key_items = tmp_holder[bdt]
                            if key in dated_key_items:
                                received = dated_key_items.pop(key)
                                if not dated_key_items:
                                    # cleaning data
                                    tmp_holder.pop(bdt)
                                # received = dated_key_items[key]
                                received = received[0]  # we've only one!

                        if received:  # use the last found
                            # we don't need to make a copy, it will be drop forever
                            if "org" in received:
                                # TODO: clone same strategy and use always "org" and other fields?
                                new = received.get("org") or received
                                assert parameter in received["value_keys"]
                            else:
                                new = received

                            new[parameter] = value[1]
                            new["datetime"] = dt
                            new[MONOTONIC_KEY] = int(dt.timestamp() * WAVE_FACTOR)
                            interpolated.setdefault(uid, {})[key] = new

            self._wip_uncompleted.difference_update(ready)
            # finally we put back the interpolated values into the
            # `_wip_tmp_edge` simulatig a fresh data in order to be
            # to do further interpolation with unseen "future" data
            for uid, uid_holder in interpolated.items():
                if re.match(self.EXCLUDE, uid):
                    continue
                holder = self._wip_tmp_edge.setdefault(uid, {})

                for key, data in uid_holder.items():
                    data["datetime"] = dt
                    dt_holder = holder.setdefault(dt, {})
                    dt_holder.setdefault(key, []).append(data)

        except Exception as why:
            print(why)
            log.error(why)
            log.error("".join(traceback.format_exception(*sys.exc_info())))
            foo = 1

        return interpolated

    def _plot(self, curve, data_points, value, label):
        #         from geomdl.visualization import VisMPL
        #
        #         vis_comp = VisMPL.VisCurve2D()
        #         curve.vis = vis_comp
        #         curve.render()
        # Plot the curves using Matplotlib
        plt.figure(figsize=(8, 6))

        # Optionally, plot the control points
        data_points_x, data_points_y = zip(*[(pt[0], pt[1]) for pt in data_points])

        data_points_x = [datetime.fromtimestamp(_) for _ in data_points_x]

        plt.scatter(
            data_points_x,
            data_points_y,
            color="blue",
            marker="o",
            label="Control Points Curve 1",
        )

        point = (datetime.fromtimestamp(value[0]), value[1])
        plt.scatter(
            point[0],
            point[1],
            color="red",
            marker="o",
            label="interpolation",
        )
        # Split the evaluated points into x and y coordinates for plotting
        curve.delta = 0.001
        curve1_points = curve.evalpts

        curve1_x, curve1_y = zip(*[(pt[0], pt[1]) for pt in curve1_points])
        curve1_x = [datetime.fromtimestamp(_) for _ in curve1_x]

        plt.plot(
            curve1_x,
            curve1_y,
            label=f"Curve 1 (Degree {curve.degree})",
            # color="blue",
        )
        # plt.plot(
        #     curve2_x,
        #     curve2_y,
        #     label=f"Curve 2 (Degree {degree_curve2})",
        #     color="green",
        # )

        # plt.scatter(
        #     ctrlpts_curve2_x,
        #     ctrlpts_curve2_y,
        #     color="green",
        #     marker="o",
        #     label="Control Points Curve 2",
        # )

        # Customize the plot
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.title(f"NURBS Curve: {label}")
        plt.grid(True)

        # Format the X-axis to display dates
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        # Adjust the interval as needed

        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        # plt.axis("equal")

        # Show plot
        plt.xticks(rotation=45)  # Rotate date labels for readability

        plt.show()
        foo = 1


    def _wip_next_ts(self, uid, dt):
        if dt:
            dt = DATE(dt)
            if ts := self.cron[uid].check(dt):
                return ts

    def _find_M(self, key):
        for pattern, M in self.specs.items():
            if pattern:
                if re.match(pattern, key):
                    self._cached_M[key] = M
                    break
        else:
            # get default value (key = "")
            self._cached_M[key] = M = self.specs.get("__default__")

        return M


class HIDE_XParticle(Particle):  # TODO: delete
    """Particle that compute rolling averages
#
    You may use in combination with other iTimedParticle instances
#
    """
#
    EXCLUDE = f"id$|{REG_PRIVATE_KEY}|datetime"
    IDS_KEYS = set([ID_KEY, ORG_KEY])
#
    def __init__(self, uid, sources, broker, storage, since=None, **kw):
        soft(
            kw.setdefault("specs", {}),
            {
                "__default__": 5,  # None means Default
            },
        )
        super().__init__(uid, sources, broker, storage, since=None, **kw)
        self.last = {}
        self._cached_M = {}

        self._duri = parse_duri(uid)

    def _find_M(self, key):
        for pattern, M in self.specs.items():
            if pattern:
                if re.match(pattern, key):
                    self._cached_M[key] = M
                    break
        else:
            # get default value (key = "")
            self._cached_M[key] = M = self.specs.get("__default__")

        return M

    def _calc(self, key, old_value, new_value):
        raise NotImplementedError()

    async def _compute(self, edge, ekeys):
        """
        Return None if we don't want to store info
        """
        # TODO: use different periods for each found key
        old = {}
        used = set()  # just double check, remove later on
        for src, stream in edge.items():
            # TODO: agp REVIEW (exclude keywords with uri names?)
            if re.match(self.EXCLUDE, src):
                continue

            for data in stream:
                keys = [_ for _ in data if not re.match(self.EXCLUDE, _)]
                _oid = parse_duri(data[ORG_KEY])
                oid = _oid[ID_KEY]
                if oid not in self.last:
                    self.last[oid] = {key: data[key] for key in keys}

                old = self.last[oid]
                old_keys = set(old)
                keys = old_keys.intersection(data)
                for key in keys:
                    old_value = old[key]  # always exists
                    new_value = data[key]  # always exists
                    # TODO: cache int/float values?
                    if isinstance(new_value, (int, float)):
                        # M = self._cached_M.get(key) or self._find_M(key)
                        # value = old_value + (new_value - old_value) / M
                        value = self._calc(key, old_value, new_value)
                        old[key] = value
                        used.add(oid)

                # propagate other values or new ones that appears later on
                missing_keys = keys.symmetric_difference(data)

                regular_keys = self.IDS_KEYS.symmetric_difference(missing_keys)
                for key in regular_keys:
                    old[key] = data[key]
                # ids
                for key in self.IDS_KEYS.intersection(data):
                    _duri = parse_duri(data[key])
                    self._duri[ID_KEY] = _duri[ID_KEY]
                    uri = build_uri(**self._duri)
                    old[key] = uri

                foo = 1

        # replace in result
        assert (
            len(used) == 1
        ), "can't mix more than one (:small) id in the same wave/edge"
        return old


class XMAParticle(HIDE_XParticle):  # TODO: delete
    def _calc(self, key, old_value, new_value):
        M = self._cached_M.get(key) or self._find_M(key)
        value = old_value + (new_value - old_value) / M
        return value


class MAXParticle(HIDE_XParticle):  # TODO: delete
    """Particle that compute the max of some values

    You may use in combination with other iTimedParticle instances

    # TODO: Create additional KPI for Stochastic, BB and MACD?
    """

    EXCLUDE = f"id$|{REG_PRIVATE_KEY}"
    IDS_KEYS = set([ID_KEY, ORG_KEY])

    def __init__(self, uid, sources, broker, storage, since=None, specs=None, **kw):
        kw.setdefault(
            "specs",
            {
                None: 5,  # None means Default
            },
        )
        super().__init__(uid, sources, broker, storage, since=None, **kw)

        self.stats = {}

    def _calc(self, key, old_value, new_value):
        M = self._cached_M.get(key) or self._find_M(key)
        value = old_value + (new_value - old_value) / M
        return value


class iTimedParticle(Particle):
    """Particle that compute data when at certains moments, similar to crontab

    2024-09-24 11:56:05.231292

    - take 1st date
    - if base mark doesn't exits, set to this value
    - as a base mark
    - iterate over *contab* alike expansion
    - date.replace() and check if

    """

    TIME_REGEXP = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}).*?(?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2})"

    def __init__(self, uid, sources, broker, storage, **kw):
        specs = soft(
            kw.setdefault("specs", {}),
            {
                "second": 0,
            },
        )
        super().__init__(uid, sources, broker, storage, **kw)

        self.cron = {_: Crontab(**specs) for _ in sources}

    def _is_wip_edge_completed(self, buffer, context):
        # we need to make the smaller step possible
        # as its happens in a live streaming
        for uid in list(self._wip_uncompleted):
            # we need to use a datetime from data, not wave
            # as the iTimedParticle are based on data
            # stream = buffer[uid]
            delta = context.setdefault("delta", {})
            info = delta.setdefault(uid, {})
            data = info.get("org", {})
            # dt = [
            #     _
            #     for _ in [
            #         DATE(data.get(DATETIME_KEY)),
            #         DATE(extract_wave(data)),
            #         DATE(context.get(DATETIME_KEY)),
            #     ]
            #     if _
            # ]
            # dt = dt and max(dt)
            dt = (
                data.get(DATETIME_KEY)
                or extract_wave(data)
                or context.get(DATETIME_KEY)
            )

            def check(dt):
                if dt:
                    dt = DATE(dt)
                    if ts := self.cron[uid].check(dt):
                        # this uid has reach the timed boundary
                        # so we can pause *milking* this source
                        # until the other ones reach the same boundary
                        # as well
                        self._wip_uncompleted.remove(uid)
                        self._wip_edge[MONOTONIC_KEY] = TO_NS(ts)
                        return ts

            if check(dt):
                pass
            elif buffer[uid]:
                pass  # continue processing buffer
            else:
                # source stream is empty, we need to wait for completion
                self._milk.add(uid)


class EODParticle(iTimedParticle):
    """Particle that compute data at the end of the day"""

    def __init__(self, uid, sources, broker, storage, **kw):
        soft(
            kw.setdefault("specs", {}),
            {
                "second": 0,
                "minute": 0,
                "hour": 0,
            },
        )
        super().__init__(uid, sources, broker, storage, **kw)


class HourParticle(iTimedParticle):
    """Particle that extract data from stream to compute result every 1 hour"""

    def __init__(self, uid, sources, broker, storage, **kw):
        soft(
            kw.setdefault("specs", {}),
            {
                "second": 0,
                "minute": 0,
            },
        )
        super().__init__(uid, sources, broker, storage, **kw)


class MinuteParticle(iTimedParticle):
    """Particle that extract data from stream to compute result every 1min"""

    def __init__(self, uid, sources, broker, storage, **kw):
        soft(
            kw.setdefault("specs", {}),
            {
                "second": 0,
            },
        )
        super().__init__(uid, sources, broker, storage, **kw)


class Minute5Particle(iTimedParticle):
    """Particle that extract data from stream to compute result every 5min"""

    def __init__(self, uid, sources, broker, storage, **kw):

        soft(
            kw.setdefault("specs", {}),
            {
                "second": 0,
                "minute": "|".join([str(_) for _ in range(0, 60, 5)]),
            },
        )
        super().__init__(uid, sources, broker, storage, **kw)


class Minute15Particle(iTimedParticle):
    """Particle that extract data from stream to compute result every 15min"""

    def __init__(self, uid, sources, broker, storage, **kw):
        soft(
            kw.setdefault("specs", {}),
            {
                "second": 0,
                "minute": "|".join([str(_) for _ in range(0, 60, 15)]),
            },
        )
        super().__init__(uid, sources, broker, storage, **kw)


class iXSMAParticle(XInterpolate):
    def _calc(self, old_values, new_values):
        for key, new_value in new_values.items():
            old_value = old_values.get(key, new_value)
            M = self._cached_M.get(key) or self._find_M(key)
            old_values[key] = old_value + (new_value - old_value) / M

        foo = 1


class iCollector:
    TRANSLATE = [["measure", "value"]]
    COPY = "|".join(["id.*", "datetime", "name", "ubication", MONOTONIC_KEY])

    CONVERT = {
        "datetime": str,
    }

    async def _compute(self, edge, ekeys):

        result = {}
        for uid, uid_holder in edge.items():
            if re.match(REG_PRIVATE_KEY, uid):
                continue
            aggregated = result.setdefault(
                uid,
                {
                    MONOTONIC_KEY: 0,
                },
            )

            for holder_key, org in uid_holder.items():
                push = False

                for pair in self.TRANSLATE:
                    if all([_ and _ in org for _ in pair]):
                        # use org[name], but last[value]

                        key = org.get(pair[0])
                        value = org.get(pair[1])
                        aggregated[key] = value
                        push = True

                # copy other structural values
                # TODO: don't include data that has been overbound in time
                for key in org:
                    if re.match(self.EXCLUDE, key):
                        continue
                    if re.match(self.COPY, key):
                        aggregated[key] = org[key]

                if dt := org.get("datetime"):
                    wave = int(dt.timestamp() * WAVE_FACTOR)
                    aggregated[MONOTONIC_KEY] = max(
                        aggregated[MONOTONIC_KEY],
                        wave,
                    )
            if push:
                # force datetime to be str
                for key, func in self.CONVERT.items():
                    if value := aggregated.get(key):
                        aggregated[key] = func(value)

                aggregated[ID_KEY] = self.render(**aggregated)

                yield aggregated
            else:
                foo = 1
            foo = 1

        # return result


class XSMAParticle(iCollector, XInterpolate):
    "example of SMA + iTimedParticle"


class XSMAParticle(iCollector, XInterpolate):
    "example of SMA + iTimedParticle"


# class ConfortParticle(XSMAParticle):
#     "example of SMA + iTimedParticle"


# ---------------------------------------------------------
# Surreal Implementation
# ---------------------------------------------------------
# from surrealist import Surreal


class Subscription(BaseModel):
    "live queries callbacks to be fired"
    lq_uid: UID
    callbacks: List[Callable]


class SurrealBroker(Broker):
    "pub / sub broker based on surreal"

    def __init__(self, url):
        super().__init__()
        self.url = url
        # TODO: missing surreal credentials
        self.connection_pool = SurrealConnectionPool(url)
        self._live_queries = {}
        log.info("broker will use [%s]", self.url)

    async def subscribe(self, uri: URI, callback: Callable):
        "TBD"
        await super().subscribe(uri, callback)

        _uri = parse_duri(uri)
        _sub_uri = dict(_uri)
        _sub_uri["path"] = f"/{_sub_uri['_path']}"
        # sub_uri = build_uri(**_sub_uri)

        table = tf(_sub_uri["_path"])
        if not (lq := self._live_queries.get(table)):
            # TODO: table or uri (fquid)?
            handler = functools.partial(self.dispatch, table)

            key = (_uri["fscheme"], _uri["host"])
            pool = self.connection_pool
            connection = pool.connections.get(key) or await pool._connect(*key)
            assert connection, "surreal connection has failed"

            # TODO: I think this is unnecessary
            info = connection.session_info().result
            namespace, database = _uri["fscheme"], _uri["host"]
            if info["ns"] != namespace or info["db"] != database:
                connection.use(namespace, database)

            res = connection.live(table, callback=handler)
            lq_uid = res.result

            lq = self._live_queries[table] = Subscription(lq_uid=lq_uid, callbacks=[])

        lq.callbacks.append((callback, _uri))

    async def unsubscribe(self, uri: URI, callback: Callable):
        "TBD"
        await super().unsubscribe(uri, callback)

        _uri = parse_duri(uri)
        _sub_uri = dict(_uri)
        _sub_uri["path"] = f"/{_sub_uri['_path']}"
        # sub_uri = build_uri(**_sub_uri)

        table = tf(_sub_uri["_path"])
        if lq := self._live_queries.get(table):
            lq.callbacks.remove((callback, _uri))
            if not lq.callbacks:

                key = (_uri["fscheme"], _uri["host"])
                pool = self.connection_pool
                connection = pool.connections.get(key) or await pool._connect(*key)
                assert connection, "surreal connection has failed"

                # TODO: I think this is unnecessary
                info = connection.session_info().result
                namespace, database = _uri["fscheme"], _uri["host"]
                if info["ns"] != namespace or info["db"] != database:
                    connection.use(namespace, database)

                connection.kill(lq.lq_uid)
                self._live_queries.pop(table)
        else:
            pass

    def dispatch(self, uid: str, res):
        "process an event from broker"
        result = res["result"]
        assert result["action"] in (
            "CREATE",
            "UPDATE",
        )
        # event = Event(uid=uid, **result['result'])
        event = result["result"]
        for callback, _uri in self._live_queries[uid].callbacks:
            if _uri.get("id") in (event.get(ORG_KEY), None):
                callback(_uri, event)

    async def is_connected(self):
        connections = [
            con.is_connected() for con in self.connection_pool.connections.values()
        ]
        return all(connections)


# ---------------------------------------------------------
# Example of a Particle Implementation
# ---------------------------------------------------------
class PlusOne(Particle):
    "Example of a Particle Implementation that adds 1 to the payload"

    async def _compute(self, edge, ekeys):
        s = 0
        for k in ekeys:
            s += edge[k]["payload"]

        s /= len(ekeys)
        s += random.random()
        data = {
            self.uid: s,
        }
        return data


class TempDiff(Particle):
    """Example of a Particle Implementation that computes
    the difference between the first and the last value"""

    async def _compute(self, edge, ekeys):
        X = [edge[k]["payload"] for k in ekeys]
        y = X[0] - X[-1]
        return y


# ---------------------------------------------------------
class TubeSync(Particle):
    """Do nothing special, but synchronize data"""
