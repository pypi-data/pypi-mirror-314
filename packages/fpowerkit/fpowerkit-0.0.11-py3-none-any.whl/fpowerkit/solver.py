from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import IntEnum
import math
from pathlib import Path
from typing import Optional
from gurobipy import GRB, Constr, LinExpr, Model, Var
from gurobipy import quicksum as Qs
from .grid import Grid, BusID, FloatVar, TimeFunc

DEFAULT_SAVETO = "./fpowerkit_logs/"

class GridSolveResult(IntEnum):
    '''Result of grid solving'''
    Failed = 0
    OK = 1
    OKwithoutVICons = 2
    SubOKwithoutVICons = 3


class SolverBase(ABC):
    def __init__(self, grid:Grid, default_saveto:str = DEFAULT_SAVETO):
        self.grid = grid
        self.saveto = default_saveto
    
    def SetErrorSaveTo(self, path:str = DEFAULT_SAVETO):
        self.saveto = path

    @abstractmethod
    def solve(self, grid:Grid, _t:int, /, **kwargs):
        raise NotImplementedError

@dataclass
class LoadReduceModule:
    '''Load Reduce module'''
    Bus:BusID
    Limit:TimeFunc
    Reduction:FloatVar = None

class DistFlowSolver(SolverBase):
    '''DistFlow solver'''
    def __init__(self, grid:Grid, default_saveto:str = DEFAULT_SAVETO, /, *,
            source_buses:'Optional[list[BusID]]' = None, source_bus_V_pu:float = 1.0,
            max_v_pu:float = 1.1, min_v_pu:float = 0.9, max_I_kA:float = 0.866,
            max_load_reduction_proportion:float = 0.5):
        super().__init__(grid, default_saveto)
        self.source_buses = source_buses if source_buses is not None else []
        self.source_bus_V_pu = source_bus_V_pu
        self.max_v_pu = max_v_pu
        self.min_v_pu = min_v_pu
        self.max_I_kA = max_I_kA
        self.dec_buses:dict[BusID, LoadReduceModule] = {}
        self.C = 1e9
        self.max_load_reduction_proportion = max_load_reduction_proportion
        self.real_max_v_pu:FloatVar = None
        self.real_min_v_pu:FloatVar = None
        self.real_max_I_kA:FloatVar = None
    
    def solve(self, _t: int, /, *, timeout_s:float = 1) -> 'tuple[GridSolveResult, float]':
        '''Get the best result at time _t, return a tuple: (result status, optimal objective value)'''
        ok, val = self.__solve(_t, False, False, timeout_s)
        if ok == GRB.Status.OPTIMAL:
            return GridSolveResult.OK, val
        else:
            ok, val = self.__solve(_t, True, True, timeout_s)
            if ok == GRB.Status.OPTIMAL:
                return GridSolveResult.OKwithoutVICons, val
            elif ok == GRB.Status.SUBOPTIMAL:
                return GridSolveResult.SubOKwithoutVICons, val
            else:
                print(f"Failed to solve at time {_t}: {ok}")
                if self.saveto != "":
                    p = Path(self.saveto)
                    p.mkdir(parents=True, exist_ok=True)
                    self.grid.savePQofBus(str(p/f"{_t}_load.csv"), _t)
                return GridSolveResult.Failed, val            
        
    def __solve(self, _t: int, relax_V: bool, relax_I: bool, timeout_s:float) -> 'tuple[int, float]':
        model = Model("model")
        
        # ---------Variables----------
        # pg0[k]: Generator active power
        # qg0[k]: Generator reactive power
        # --> pg[j]: Active power of all generators at the bus
        # --> qg[j]: Reactive power of all generators at the bus
        # v[j]: Bus voltage ** 2
        # l[i,j]: Line current ** 2
        # P[i,j]: Line active power
        # Q[i,j]: Line reactive power
        pg0: dict[str, Var] = {g.ID: model.addVar(name=f"pg_{g.ID}", vtype='C', lb=g.Pmin(_t), ub=g.Pmax(_t)) for g in
                               self.grid.Gens}
        qg0: dict[str, Var] = {g.ID: model.addVar(name=f"qg_{g.ID}", vtype='C', lb=g.Qmin(_t), ub=g.Qmax(_t)) for g in
                               self.grid.Gens}
        pg: dict[str, list[Var]] = {bus.ID: [] for bus in self.grid.Buses}
        qg: dict[str, list[Var]] = {bus.ID: [] for bus in self.grid.Buses}
        for g in self.grid.Gens:
            pg[g.BusID].append(pg0[g.ID])
            qg[g.BusID].append(qg0[g.ID])
        if relax_V:
            vmax_rel = model.addVar(name="vmax_rel", vtype='C', lb=0, ub=1)
            vmin_rel = model.addVar(name="vmin_rel", vtype='C', lb=0, ub=1)
            max_v = self.max_v_pu ** 2 + vmax_rel
            min_v = self.min_v_pu ** 2 - vmin_rel
            v = {bus.ID: model.addVar(name=f"v_{bus.ID}", vtype='C') for bus in self.grid.Buses}
            model.update()
            model.addConstrs(min_v <= v0 for v0 in v.values())
            model.addConstrs(v0 <= max_v for v0 in v.values())
        else:
            vmax_rel = vmin_rel = 0
            max_v = self.max_v_pu ** 2
            min_v = self.min_v_pu ** 2
            v = {bus.ID: model.addVar(name=f"v_{bus.ID}", vtype='C', lb=min_v, ub=max_v) for bus in self.grid.Buses}
        if relax_I:
            l_rel = model.addVar(name="l_rel", vtype='C')
            max_l = (self.max_I_kA  / self.grid.Ib) ** 2 + l_rel
            l = {line.ID: model.addVar(name=f"l_{line.ID}", vtype='C', lb=0) for line in self.grid.Lines}
            model.update()
            model.addConstrs(l0 <= max_l for l0 in l.values())
        else:
            l_rel = 0
            max_l = (self.max_I_kA / self.grid.Ib) ** 2
            l = {line.ID: model.addVar(name=f"l_{line.ID}", vtype='C', lb=0, ub=max_l) for line in self.grid.Lines}
        P = {line.ID: model.addVar(name=f"P_{line.ID}", vtype='C', lb=-GRB.INFINITY, ub=GRB.INFINITY) for line in
             self.grid.Lines}
        Q = {line.ID: model.addVar(name=f"Q_{line.ID}", vtype='C', lb=-GRB.INFINITY, ub=GRB.INFINITY) for line in
             self.grid.Lines}
        
        Pdec = {bus: model.addVar(name=f"Pdec_{bus}", vtype='C', 
            lb=0, ub=lim.Limit(_t) * self.max_load_reduction_proportion) for bus,lim in self.dec_buses.items()}
        
        # ----------Constraints-----------
        Pcons: dict[str, Constr] = {}
        Qcons: dict[str, Constr] = {}

        for bus in self.grid.Buses:
            j = bus.ID
            flow_in = self.grid.LinesOfTBus(j)
            flow_out = self.grid.LinesOfFBus(j)
            dec = Pdec[j] if j in self.dec_buses else 0
            Pcons[j] = model.addConstr(Qs(P[ln.ID] - ln.R * l[ln.ID] for ln in flow_in) + Qs(pg[j]) == Qs(
                P[ln.ID] for ln in flow_out) + bus.Pd(_t) - dec, f"Pcons_{j}")
            Qcons[j] = model.addConstr(Qs(Q[ln.ID] - ln.X * l[ln.ID] for ln in flow_in) + Qs(qg[j]) == Qs(
                Q[ln.ID] for ln in flow_out) + bus.Qd(_t), f"Qcons_{j}")

        for line in self.grid.Lines:
            i, j = line.pair
            lid = line.ID
            model.addConstr(
                v[j] == v[i] - 2 * (line.R * P[lid] + line.X * Q[lid]) + (line.R ** 2 + line.X ** 2) * l[lid],
                f"ΔU2_cons_{lid}")
            model.addConstr(P[lid] ** 2 + Q[lid] ** 2 <= l[lid] * v[i], f"SoC_cons_{lid}")

        assert len(self.source_buses) > 0, "No source bus specified"
        for b in self.source_buses:
            model.addConstr(v[b] == self.source_bus_V_pu ** 2, f"src_{b}")

        decs = self.C * (Qs(Pdec.values()) + vmax_rel + vmin_rel + l_rel)
        goal = Qs(g.CostA(_t) * pg0[g.ID] ** 2 + g.CostB(_t) * pg0[g.ID] + g.CostC(_t) for g in self.grid.Gens)

        model.setObjective(decs + goal, GRB.MINIMIZE)
        model.setParam(GRB.Param.OutputFlag, 0)
        model.setParam(GRB.Param.QCPDual, 1)
        model.setParam(GRB.Param.TimeLimit, timeout_s)
        #if relax_I or relax_V: model.setParam(GRB.Param.NonConvex, 2)
        model.update()
        model.optimize()
        if model.Status != GRB.Status.OPTIMAL:
            return model.Status, -1

        for bus in self.grid.Buses:
            j = bus.ID
            bus.V = v[j].X ** 0.5
            try:
                sp = Pcons[j].Pi
            except:
                sp = None if not self.grid._holdShadowPrice else bus.ShadowPrice
            bus.ShadowPrice = sp

        for line in self.grid.Lines:
            lid = line.ID
            line.I = l[lid].X ** 0.5
            line.P = P[lid].X
            line.Q = Q[lid].X

        for gen in self.grid.Gens:
            j = gen.ID
            gen.P = pg0[j].X
            gen.Q = qg0[j].X
        
        for bus,lim in self.dec_buses.items():
            lim.Reduction = Pdec[bus].X
            if lim.Reduction < 1e-8: lim.Reduction = 0
        
        self.real_min_v_pu = math.sqrt(min_v.getValue()) if isinstance(min_v, LinExpr) else self.min_v_pu
        self.real_max_v_pu = math.sqrt(max_v.getValue()) if isinstance(max_v, LinExpr) else self.max_v_pu
        self.real_max_I_kA = math.sqrt(max_l.getValue()) if isinstance(max_l, LinExpr) else self.max_I_kA

        return model.Status, goal.getValue()