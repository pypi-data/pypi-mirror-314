import zipfile
from io import BytesIO, TextIOWrapper
from typing import Any, TextIO, Iterable, Optional, Union
from xml.etree.ElementTree import Element, ElementTree
from feasytools import TimeFunc, SegFunc, ConstFunc, makeFunc
from copy import deepcopy

FloatVar = Optional[float]
FloatLike = Union[int, float, TimeFunc, 'list[tuple[int, float]]']
FloatVals = Union[int, float]


def _float2func(v: FloatLike) -> TimeFunc:
    if isinstance(v, (float, int)):
        return ConstFunc(v)
    elif isinstance(v, TimeFunc):
        return v
    else:
        return SegFunc(v)


def _tfv(s: FloatVar): return "<unsolved>" if s is None else str(s)

def _readVal(s: str) -> 'tuple[float, str]':
    if s.endswith("pu"):
        return float(s[:-2]), "pu"
    elif s.endswith("kVA"):
        return float(s[:-3]), "kVA"
    elif s.endswith("kvar"):
        return float(s[:-4]), "kvar"
    elif s.endswith("kW"):
        return float(s[:-2]), "kW"
    elif s.endswith("MVA"):
        return float(s[:-3]), "MVA"
    elif s.endswith("Mvar"):
        return float(s[:-4]), "Mvar"
    elif s.endswith("MW"):
        return float(s[:-2]), "MW"
    elif s.endswith("kV"):
        return float(s[:-2]), "kV"
    elif s.endswith("V"):
        return float(s[:-1]), "V"
    elif s.endswith("kA"):
        return float(s[:-2]), "kA"
    elif s.endswith("ohm"):
        return float(s[:-3]), "ohm"
    elif s.endswith("kWh"):
        return float(s[:-3]), "kWh"
    else:
        return float(s), ""
    

def _readFloatLike(e: Optional[Element], sb_mva:float, ub_kv:float) -> FloatLike:
    assert e is not None
    def _valconv(v:FloatVals, u:str) -> FloatVals:
        if u == "pu":
            return v
        elif u == "kVA":
            return v / (sb_mva * 1000)
        elif u == "kvar":
            return v / (sb_mva * 1000)
        elif u == "kW":
            return v / (sb_mva * 1000)
        elif u == "MVA":
            return v / sb_mva
        elif u == "Mvar":
            return v / sb_mva
        elif u == "MW":
            return v / sb_mva
        elif u == "kV":
            return v / ub_kv
        elif u == "V":
            return v / (ub_kv * 1000)
        elif u == "kA":
            return v / (sb_mva / (ub_kv * 3 ** 0.5))
        elif u == "ohm":
            return v * ub_kv ** 2 / sb_mva
        elif u == "$/puh" or u == "$/puh2" or u == "$":
            return v
        elif u == "$/kWh":
            return v * (sb_mva * 1000)
        elif u == "$/MWh":
            return v * sb_mva
        elif u == "$/kWh2":
            return v * (sb_mva * 1000 * sb_mva * 1000)
        elif u == "$/MWh2":
            return v * (sb_mva * sb_mva)
        else:
            return v
    if "const" in e.attrib:
        v, u = _readVal(e.attrib["const"])
        if u == "": u = e.attrib.get("unit","")
        return _valconv(v, u)
    else:
        repeat = int(e.attrib.get("repeat", "1"))
        period = int(e.attrib.get("period", "0"))
        sf = SegFunc()
        for itm in e:
            time = int(itm.attrib["time"])
            v, u = _readVal(itm.attrib["value"])
            sf.add(time, _valconv(v, u))
        return sf.repeat(repeat, period)


class Bus:
    ID: str
    V: FloatVar  # pu
    Pd: TimeFunc  # pu
    Qd: TimeFunc  # pu
    ShadowPrice: FloatVar  # Shadow price of generators on this bus，$/pu power
    Lat: Optional[float]
    Lon: Optional[float]

    def __init__(self, id: str, pd_pu: FloatLike, qd_pu: FloatLike, 
                 lat: Optional[float] = None, lon: Optional[float] = None, v_pu: Optional[float] = None):
        self.ID = id
        self.V = v_pu
        self.Pd = _float2func(pd_pu)
        self.Qd = _float2func(qd_pu)
        self.ShadowPrice = None
        self.Lat = lat
        self.Lon = lon

    def __repr__(self):
        return f"Bus(id='{self.ID}', v_pu={self.V}, pd_pu={self.Pd}, qd_pu={self.Qd}, lat={self.Lat}, lon={self.Lon})"

    def __str__(self):
        return repr(self)
    
    def str_t(self, _t: int, /):
        return f"Bus(id='{self.ID}', v_pu={_tfv(self.V)}, pd_pu={self.Pd(_t)}, qd_pu={self.Qd(_t)}, lat={self.Lat}, lon={self.Lon})"

    @property
    def position(self) -> 'tuple[Optional[float], Optional[float]]':
        '''Return the position of the bus, (lat, lon)'''
        return self.Lat, self.Lon
    
    @staticmethod
    def fromXML(node: 'Element', Sb_MVA: float, Ub_kV: float):
        id = node.attrib["ID"]
        p = _readFloatLike(node.find("Pd"), Sb_MVA, Ub_kV)
        q = _readFloatLike(node.find("Qd"), Sb_MVA, Ub_kV)
        lat = node.attrib.get("Lat", None)
        if lat is not None: lat = float(lat)
        lon = node.attrib.get("Lon", None)
        if lon is not None: lon = float(lon)
        return Bus(id, p, q, lat, lon)
    
    @staticmethod
    def load(fp: TextIO, Sb_MVA: float, loop: str = "0,0"):
        ret = loop.split(",")
        assert len(ret) == 2
        loop_period = int(ret[0])
        loop_times = int(ret[1])
        data = fp.readlines()
        hl = data[0].split(',')
        if hl[0].strip() != "time": raise ValueError("Bad format of bus CSV file")
        tl = [int(x.strip()) for x in hl[1:]]
        if loop_period > 0 and loop_times > 0:
            tl_old = tl.copy()
            for i in range(loop_times - 1):
                tl.extend([x + loop_period * (i + 1) for x in tl_old])
        else:
            tl_old = tl

        def parseline(ln: str,i:int):
            ret = ln.split(',')
            if len(ret) != len(tl_old) + 1: raise ValueError(f"Bad line length at line {i} in bus CSV file")
            p: 'list[float]' = []
            q: 'list[float]' = []
            for x in ret[1:]:
                p0, q0 = x.strip().split('|')
                p.append(float(p0) / Sb_MVA)
                q.append(float(q0) / Sb_MVA)
            if loop_period > 0 and loop_times > 0:
                p = p * loop_times
                q = q * loop_times
            bn = ret[0].strip().split('|')
            if len(bn) == 1:
                return bn[0], makeFunc(tl, p), makeFunc(tl, q), None, None
            elif len(bn) == 3:
                return bn[0], makeFunc(tl, p), makeFunc(tl, q), float(bn[1]), float(bn[2])
            else:
                raise ValueError(f"Bad bus name format at line {i} in bus CSV file, should be 'name' or 'name|lat|lon'")
        
        return [Bus(*parseline(ln,i)) for i,ln in enumerate(data[1:],start=1)]


class Line:
    ID: str
    fBus: str
    tBus: str
    R: float  # pu
    X: float  # pu
    P: FloatVar  # pu
    Q: FloatVar  # pu
    I: FloatVar  # pu

    def __init__(self, id: str, fbus: str, tbus: str, r_pu: float, x_pu: float, 
                 i_pu: Optional[float] = None, p_pu: Optional[float] = None, q_pu: Optional[float] = None):
        '''
        Initialize
            id: Line ID
            fbus: ID of start bus
            tbus: ID of end bus
            r_pu: Resistance, pu
            x_pu: Reactance, pu
        '''
        self.ID = id
        self.fBus = fbus
        self.tBus = tbus
        self.R = r_pu
        self.X = x_pu
        self.I = i_pu
        self.P = p_pu
        self.Q = q_pu

    @property
    def pair(self):
        '''Syntax candy of (self.fBus, self.tBus)'''
        return (self.fBus, self.tBus)

    def __repr__(self) -> str:
        return (f"Line(id='{self.ID}', fbus='{self.fBus}', tbus='{self.tBus}', r_pu={self.R}, " + 
                f"x_pu={self.X}, i_pu={self.I}, p_pu={self.P}, q_pu={self.Q})")

    def __str__(self) -> str:
        return repr(self)
    
    def str_t(self, _t: int, /) -> str:
        return self.__str__()

    @staticmethod
    def load(fp: TextIO, Zb_Ohm: float = 1.0):
        data = fp.readlines()
        head = [x.strip() for x in data[0].split(',')]
        if head != ["id", "fBus", "tBus", "R", "X"]:
            raise ValueError("Bad line CSV format: Columns must be 'id,fBus,tBus,R,X' (case sensitive). ")

        def parseline(ln: str):
            (id, f, t, r, x) = (x.strip() for x in ln.split(','))
            return id, f, t, float(r) / Zb_Ohm, float(x) / Zb_Ohm

        return [Line(*parseline(ln)) for ln in data[1:]]

    @staticmethod
    def fromXML(node: 'Element', Zb_Ohm: float):
        id = node.attrib["ID"]
        f = node.attrib["From"]
        t = node.attrib["To"]
        r = float(node.attrib["R"]) / Zb_Ohm
        x = float(node.attrib["X"]) / Zb_Ohm
        return Line(id, f, t, r, x)
    
    def toXMLNode(self) -> 'Element':
        return Element("line", {
            "ID": self.ID,
            "From": self.fBus,
            "To": self.tBus,
            "R": str(self.R),
            "X": str(self.X),
        })

class GeneratorModel:
    Pmin: TimeFunc  #pu
    Pmax: TimeFunc  #pu
    Qmin: TimeFunc  #pu
    Qmax: TimeFunc  #pu
    CostA: TimeFunc  #$/(pu Power·h)**2
    CostB: TimeFunc  #$/pu Power·h
    CostC: TimeFunc  #$
    def __init__(self, pmin_pu: FloatLike, pmax_pu: FloatLike, qmin_pu: FloatLike, qmax_pu: FloatLike,
                 costA: FloatLike, costB: FloatLike, costC: FloatLike):
        '''
        Initialize
            pmin_pu: Minimal active power output, pu
            pmax_pu: Maximal active power output, pu
            qmin_pu: Minimal reactive power output, pu
            qmax_pu: Maximal reactive power output, pu
            costA: Secondary cost, $/(pu Power·h)**2
            costB: Primary cost, $/pu Power·h
            costC: Fixed cost, $
        '''
        self.Pmin = _float2func(pmin_pu)
        self.Pmax = _float2func(pmax_pu)
        self.Qmin = _float2func(qmin_pu)
        self.Qmax = _float2func(qmax_pu)
        self.CostA = _float2func(costA)
        self.CostB = _float2func(costB)
        self.CostC = _float2func(costC)
    
    def toGenerator(self, id:str, busid:str):
        return Generator(id, busid, 
            deepcopy(self.Pmin), deepcopy(self.Pmax), 
            deepcopy(self.Qmin), deepcopy(self.Qmax), 
            deepcopy(self.CostA), deepcopy(self.CostB), 
            deepcopy(self.CostC)
        )
    
    @staticmethod
    def fromXML(node: 'Element', Sb_MVA: float, Ub_kV: float):
        pmin = _readFloatLike(node.find("Pmin"), Sb_MVA, Ub_kV)
        pmax = _readFloatLike(node.find("Pmax"), Sb_MVA, Ub_kV)
        qmin = _readFloatLike(node.find("Qmin"), Sb_MVA, Ub_kV)
        qmax = _readFloatLike(node.find("Qmax"), Sb_MVA, Ub_kV)
        ca = _readFloatLike(node.find("CostA"), Sb_MVA, Ub_kV)
        cb = _readFloatLike(node.find("CostB"), Sb_MVA, Ub_kV)
        cc = _readFloatLike(node.find("CostC"), Sb_MVA, Ub_kV)
        return GeneratorModel(pmin, pmax, qmin, qmax, ca, cb, cc)


class Generator:
    ID: str
    BusID: str
    Pmin: TimeFunc  #pu
    Pmax: TimeFunc  #pu
    P: FloatVar  #pu
    Qmin: TimeFunc  #pu
    Qmax: TimeFunc  #pu
    Q: FloatVar  #pu
    CostA: TimeFunc  #$/(pu Power·h)**2
    CostB: TimeFunc  #$/pu Power·h
    CostC: TimeFunc  #$

    def __init__(self, id: str, busid: str, pmin_pu: FloatLike, pmax_pu: FloatLike, qmin_pu: FloatLike, qmax_pu: FloatLike,
                 costA: FloatLike, costB: FloatLike, costC: FloatLike, P: Optional[float] = None, Q: Optional[float] = None):
        '''
        Initialize
            id: Generator ID
            busid: ID of the bus where the generator is located
            pmin_pu: Minimal active power output, pu
            pmax_pu: Maximal active power output, pu
            qmin_pu: Minimal reactive power output, pu
            qmax_pu: Maximal reactive power output, pu
            costA: Secondary cost, $/(pu Power·h)**2
            costB: Primary cost, $/pu Power·h
            costC: Fixed cost, $
        '''
        self.ID = id
        self.BusID = busid
        self.P = P
        self.Q = Q
        self.Pmin = _float2func(pmin_pu)
        self.Pmax = _float2func(pmax_pu)
        self.Qmin = _float2func(qmin_pu)
        self.Qmax = _float2func(qmax_pu)
        self.CostA = _float2func(costA)
        self.CostB = _float2func(costB)
        self.CostC = _float2func(costC)
        self.CostShadow = None

    def __repr__(self) -> str:
        return (f"Generator(id='{self.ID}', busid='{self.BusID}', P={self.P}, Q={self.Q}, " +
                f"pmin_pu={self.Pmin}, pmax_pu={self.Pmax}, qmin_pu={self.Qmin}, qmax_pu={self.Qmax}, " + 
                f"costA={self.CostA}, costB={self.CostB}, costC={self.CostC})")

    def __str__(self) -> str:
        return repr(self)

    def str_t(self, _t: int, /) -> str:
        return (f"Generator(id='{self.ID}', busid='{self.BusID}', P={_tfv(self.P)}, Q={_tfv(self.Q)}, " + 
                f"pmin_pu={self.Pmin(_t)}, pmax_pu={self.Pmax(_t)}, qmin_pu={self.Qmin(_t)}, qmax_pu={self.Qmax(_t)}, " + 
                f"costA={self.CostA(_t)}, costB={self.CostB(_t)}, costC={self.CostC(_t)})")

    def Cost(self, _t: int, /, secondary: bool = True) -> FloatVar:
        '''
        Get the cost of the generator at time _t, $/h
            _t: time
            secondary: whether to use the secondary cost model, False for the primary cost model
        '''
        if self.P is None: return None
        ret = self.CostB(_t) * self.P + self.CostC(_t)
        if secondary: ret += self.CostA(_t) * self.P ** 2
        return ret

    def CostPerPUPower(self, _t: int, /, secondary: bool = True) -> FloatVar:
        '''
        Get the cost of the generator per pu power at time _t, $/pu Power·h
            _t: time
            secondary: whether to use the secondary cost model, False for the primary cost model
        '''
        if self.P is None or self.P == 0: return None
        ret = self.CostB(_t) * self.P + self.CostC(_t)
        if secondary: ret += self.CostA(_t) * self.P ** 2
        return ret / self.P

    @staticmethod
    def load(fp: TextIO, SbkW: float, Sb: float = 1.0):
        '''
        Load generators from a CSV file
            fp: file pointer
            SbkW: base power for electricity cost conversion, kW: $/kWh->$/pu Power·h
            Sb: base power, unit determined by 'info.txt': powers in the file / Sb == pu values
        '''
        data = fp.readlines()
        hl = data[0].split(',')
        if hl[0].strip() != "time": raise ValueError("Bad generator CSV file")
        tl = [int(x.strip()) for x in hl[1:]]

        def parseline(ln: str):
            ret = ln.split(',')
            if len(ret) != len(tl) + 1: raise ValueError("Bad generator CSV file: line length error")
            pmin: 'list[float]' = []
            qmin: 'list[float]' = []
            pmax: 'list[float]' = []
            qmax: 'list[float]' = []
            for x in ret[1:]:
                pmin0, pmax0, qmin0, qmax0 = x.strip().split('|')
                pmin.append(float(pmin0) / Sb)
                pmax.append(float(pmax0) / Sb)
                qmin.append(float(qmin0) / Sb)
                qmax.append(float(qmax0) / Sb)
            (id, busid, ca, cb, cc) = (x.strip() for x in ret[0].strip().split("|"))
            #ca:$/(kWh)**2；cb:$/kWh；cc:$
            return (id, busid, makeFunc(tl, pmin), makeFunc(tl, pmax),
                    makeFunc(tl, qmin), makeFunc(tl, qmax), float(ca) * SbkW * SbkW, float(cb) * SbkW, float(cc))

        return [Generator(*parseline(ln)) for ln in data[1:]]

    @staticmethod
    def fromXML(node: 'Element', Sb_MVA: float, Ub_kV: float):
        id = node.attrib["ID"]
        busid = node.attrib["Bus"]
        pmin = _readFloatLike(node.find("Pmin"), Sb_MVA, Ub_kV)
        pmax = _readFloatLike(node.find("Pmax"), Sb_MVA, Ub_kV)
        qmin = _readFloatLike(node.find("Qmin"), Sb_MVA, Ub_kV)
        qmax = _readFloatLike(node.find("Qmax"), Sb_MVA, Ub_kV)
        ca = _readFloatLike(node.find("CostA"), Sb_MVA, Ub_kV)
        cb = _readFloatLike(node.find("CostB"), Sb_MVA, Ub_kV)
        cc = _readFloatLike(node.find("CostC"), Sb_MVA, Ub_kV)
        return Generator(id, busid, pmin, pmax, qmin, qmax, ca, cb, cc)
    

BusID = str
LineID = str

class Grid:
    Sb: float  #MVA
    Ub: float  #kV

    @property
    def Sb_MVA(self) -> float:
        return self.Sb

    @property
    def Sb_kVA(self) -> float:
        return self.Sb * 1000

    @property
    def Zb(self) -> float:
        '''Zb, unit = Ohm'''
        return self.Ub ** 2 / self.Sb

    @property
    def Ib(self) -> float:
        '''Ib, unit = kA'''
        return self.Sb / (self.Ub * (3 ** 0.5))

    def __init__(self, Sb_MVA: float, Ub_kV: float, buses: 'Iterable[Bus]',
                 lines: 'Iterable[Line]', gens: 'Iterable[Generator]', holdShadowPrice: bool = False):
        '''
        Initialize
            Sb_MVA: base power, MVA
            Ub_kV: base voltage, kV
            buses: list of buses
            lines: list of lines
            gens: list of generators
            holdShadowPrice: whether to hold the shadow price of the buses of the last time when failed to solve this time
        '''
        self.Sb = Sb_MVA
        self.Ub = Ub_kV
        self._buses = {bus.ID: bus for bus in buses}
        self._lines = {line.ID: line for line in lines}
        self._ladjfb: 'dict[str, list[Line]]' = {bus.ID: [] for bus in buses}
        self._ladjtb: 'dict[str, list[Line]]' = {bus.ID: [] for bus in buses}
        self._bnames = list(self._buses.keys())
        self._gens = {gen.ID: gen for gen in gens}
        self._gatb: 'dict[str, list[Generator]]' = {bus.ID: [] for bus in buses}
        for line in self._lines.values():
            if not line.fBus in self._bnames: raise ValueError(f"Bus {line.fBus} undefined")
            if not line.tBus in self._bnames: raise ValueError(f"Bus {line.tBus} undefined")
            self._ladjfb[line.fBus].append(line)
            self._ladjtb[line.tBus].append(line)
        for gen in self._gens.values():
            assert gen.BusID in self._bnames
            self._gatb[gen.BusID].append(gen)
        self._holdShadowPrice = holdShadowPrice
   

    def AddGen(self, g: Generator):
        self._gens[g.ID] = g
        self._gatb[g.BusID].append(g)

    @property
    def BusNames(self) -> 'list[str]':
        return self._bnames

    def Bus(self, id: str) -> 'Bus':
        return self._buses[id]

    @property
    def Buses(self):
        return self._buses.values()

    def LinesOfFBus(self, busid: str) -> 'list[Line]':
        return self._ladjfb[busid]

    def LinesOfTBus(self, busid: str) -> 'list[Line]':
        return self._ladjtb[busid]

    def Line(self, id: str) -> 'Line':
        return self._lines[id]

    @property
    def Lines(self):
        return self._lines.values()

    def Gen(self, id: str) -> 'Generator':
        return self._gens[id]

    @property
    def GenNames(self) -> 'list[str]':
        return list(self._gens.keys())

    @property
    def Gens(self):
        return self._gens.values()

    def GensAtBus(self, busid: str) -> 'list[Generator]':
        return self._gatb[busid]

    def __repr__(self):
        b = '\n  '.join(map(str, self._buses.values()))
        l = '\n  '.join(map(str, self._lines.values()))
        g = '\n  '.join(map(str, self._gens.values()))
        return f"Ub={self.Ub}kV, Sb={self.Sb_MVA}MVA\nBuses:\n  {b}\nLines:\n  {l}\nGenerators:\n  {g}"

    def __str__(self):
        return repr(self)
    
    def str_t(self, _t: int):
        b = '\n  '.join(v.str_t(_t) for v in self._buses.values())
        l = '\n  '.join(v.str_t(_t) for v in self._lines.values())
        g = '\n  '.join(v.str_t(_t) for v in self._gens.values())
        return f"Ub={self.Ub}kV, Sb={self.Sb_MVA}MVA\nAt time {_t}:\nBuses:\n  {b}\nLines:\n  {l}\nGenerators:\n  {g}"

    @staticmethod
    def fromFile(file_name:str, holdShadowPrice: bool = False):
        if file_name.lower().endswith(".zip"):
            return Grid.fromFileZIP(file_name, holdShadowPrice)
        elif file_name.lower().endswith(".xml"):
            return Grid.fromFileXML(file_name)
        else:
            raise ValueError("Unsupported file type")
        
    @staticmethod
    def fromFileXML(xml_name: str, holdShadowPrice: bool = False):
        rt = ElementTree(file=xml_name).getroot()
        # Read base values
        Sb, unit = _readVal(rt.attrib["Sb"])
        if unit == "MVA": pass
        elif unit == "kVA": Sb /= 1000
        else: raise ValueError(f"Invalid base value unit: {unit}")
        Ub, unit = _readVal(rt.attrib["Ub"])
        if unit == "kV": pass
        else: raise ValueError(f"Invalid base value unit: {unit}")
        #Read grid model
        bm = rt.attrib.get("model","")
        if bm != "": # No base model
            try:
                grpt = int(rt.attrib.get("grid-repeat","1"))
                lrpt = int(rt.attrib.get("load-repeat","1"))
                fixed = rt.attrib.get("fixed-load","") == "true"
            except:
                raise ValueError("Invalid grid-repeat or load-repeat or fixed-load")
            from .cases import _get_buses, _get_lines, _get_gens, _DEFAULT_LOAD_SCALE, _DEFAULT_GENERATOR, _DEFAULT_GEN_POS
            if bm.lower() == "ieee33":
                from .cases import _IEEE33_LOAD, _IEEE33_LINE
                buses:list[Bus] = _get_buses(Sb * 1000, grpt, _IEEE33_LOAD, not fixed, _DEFAULT_LOAD_SCALE, lrpt, 86400)
                lines:list[Line] = _get_lines(Ub * Ub / Sb, _IEEE33_LINE, grpt)
                gens:list[Generator] = _get_gens(_DEFAULT_GENERATOR, _DEFAULT_GEN_POS, grpt)
            elif bm.lower() == "ieee69":
                from .cases import _IEEE69_LOAD, _IEEE69_LINE
                buses:list[Bus] = _get_buses(Sb * 1000, grpt, _IEEE69_LOAD, not fixed, _DEFAULT_LOAD_SCALE, lrpt, 86400)
                lines:list[Line] = _get_lines(Ub * Ub / Sb, _IEEE69_LINE, grpt)
                gens:list[Generator] = _get_gens(_DEFAULT_GENERATOR, _DEFAULT_GEN_POS, grpt)
            else:
                raise ValueError(f"Undefined base model: {bm}")
        else:
            buses:list[Bus] = []
            lines:list[Line] = []
            gens:list[Generator] = []
        #Read buses, lines and generators

        gen_models:dict[str, GeneratorModel] = {}
        for e in rt:
            if e.tag == "bus":
                buses.append(Bus.fromXML(e, Sb, Ub))
            elif e.tag == "line":
                lines.append(Line.fromXML(e, Ub * Ub / Sb))
            elif e.tag == "gen" or e.tag == "generator":
                bm = e.attrib.get("model","")
                if bm == "": # No base model
                    gens.append(Generator.fromXML(e, Sb, Ub))
                else:
                    if bm not in gen_models: raise ValueError(f"Undefined generator model: {bm}")
                    gens.append(gen_models[bm].toGenerator(e.attrib["ID"], e.attrib["Bus"]))
            elif e.tag == "genmodel" or e.tag == "generatormodel":
                gen_models[e.attrib["name"]] = GeneratorModel.fromXML(e, Sb, Ub)
            else:
                raise ValueError(f"Unknown XML node: {e.tag}")
        return Grid(Sb, Ub, buses, lines, gens, holdShadowPrice)

    @staticmethod
    def fromFileZIP(zip_name: str, holdShadowPrice: bool = False):
        zf = zipfile.ZipFile(zip_name, "r")
        with TextIOWrapper(BytesIO(zf.read("info.txt"))) as fp:
            info: dict[str, Any] = {}
            for item in [x.split(':') for x in fp.readlines()]:
                if len(item) != 2: raise ValueError("Bad grid info file")
                info[item[0].strip()] = item[1].strip()
        Sb = float(info.pop("S_base_MVA"))
        Ub = float(info.pop("U_base_kV"))
        Zb = Ub * Ub / Sb
        with TextIOWrapper(BytesIO(zf.read("buses.csv"))) as fp:
            buses_unit = info.pop("buses_unit")
            buses_loop = info.pop("buses_loop", "0,0")
            if buses_unit == "pu":
                buses = Bus.load(fp, 1, buses_loop)
            elif buses_unit in ["kVA", "kvar", "kW"]:
                buses = Bus.load(fp, Sb * 1000, buses_loop)
            elif buses_unit in ["MVA", "Mvar", "MW"]:
                buses = Bus.load(fp, Sb, buses_loop)
            else:
                raise ValueError(f"Invalid power unit: {buses_unit}")
        with TextIOWrapper(BytesIO(zf.read("lines.csv"))) as fp:
            lines_unit = info.pop("lines_unit")
            if lines_unit == "pu":
                lines = Line.load(fp)
            elif lines_unit == "ohm":
                lines = Line.load(fp, Zb)
            else:
                raise ValueError(f"Invalid resistance unit: {lines_unit}")
        with TextIOWrapper(BytesIO(zf.read("gens.csv"))) as fp:
            gens_unit = info.pop("gens_unit")
            if gens_unit == "pu":
                gens = Generator.load(fp, Sb * 1000)
            elif gens_unit in ["kVA", "kvar", "kW"]:
                gens = Generator.load(fp, Sb * 1000, Sb * 1000)
            elif gens_unit in ["MVA", "Mvar", "MW"]:
                gens = Generator.load(fp, Sb * 1000, Sb)
            else:
                raise ValueError(f"Invalid power unit: {gens_unit}")
        return Grid(Sb, Ub, buses, lines, gens, holdShadowPrice)

    def savePQofBus(self, file_name: str, t:int):
        with open(file_name, "w") as fp:
            fp.write("Bus,Pd,Qd\n")
            for bus in self.Buses:
                fp.write(f"{bus.ID},{bus.Pd(t)},{bus.Qd(t)}\n")
    
    def loadPQofBus(self, file_name: str):
        with open(file_name) as fp:
            for ln in fp.readlines()[1:]:
                bn, p, q = ln.strip().split(',')
                self.Bus(bn).Pd = ConstFunc(float(p) / self.Sb)
                self.Bus(bn).Qd = ConstFunc(float(q) / self.Sb)
