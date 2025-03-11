import sys
from clingo.application import Application, clingo_main
from clingo.control import Control
from clingo.symbol import Function, Number, parse_term, String, Symbol, SymbolType

PART1 = """
    rule(0,-1,1,0).  % up goes right
    rule(1,0,0,1).  % right goes down
    rule(0,1,-1,0).  % down goes left
    rule(-1,0,0,-1).  % left goes up

    max(X,Y) :- X = #max { V : field(V,_) }, Y = #max { V : field(_,V) }.

    at(0,X,Y,0,-1) :- start(X,Y).
    at(T+1,X+A,Y+B,A,B) :- not obstacle(X+A,Y+B), at(T,X,Y,A,B), max(X_MAX,Y_MAX), X<=X_MAX; Y<=Y_MAX.
    at(T,X,Y,A2,B2) :- obstacle(X+A1,Y+B1), at(T,X,Y,A1,B1), rule(A1,B1,A2,B2).

    part1(T-1) :- T = #count { X,Y : at(_,X,Y,_,_) }.
    #show part1/1.
"""


PART2 = """
%0 { new_start(X,Y,A,B) : at(_,X,Y,A,B) } 1.
0 { new_start(5,7,0,-1) } 1.

new_obstacles(X,Y) :- obstacle(X,Y).
new_obstacles(X+A,Y+B) :- new_start(X,Y,A,B), not obstacle(X+A,Y+B), not escaped(X+A,Y+B).
newest_obstacle(X,Y) :- new_obstacles(X,Y), not obstacle(X,Y).

step(0,X,Y,A,B) :- new_start(X,Y,A,B), newest_obstacle(_,_).
step(T,X,Y,A2,B2) :- new_obstacles(X+A1,Y+B1), step(T,X,Y,A1,B1), rule(A1,B1,A2,B2).

escaped(X+1,1..Y) :- max(X,Y).
escaped(1..X,Y+1) :- max(X,Y).
escaped(-1,1..Y) :- max(X,Y).
escaped(1..X,-1) :- max(X,Y).

:- step(T,X,Y,A,B), escaped(X+A,Y+B).


#show newest_obstacle/2.
#show step/4.
"""

SHOWS = """
#show new_start/4.
#show new_obstacle/2.
"""

class AoC6(Application):
    program_name = "AoC Day 6"
    version = "1.0"
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AoC6, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._ctl = None
        self._current_model = []
        self._models = []
        self._new_starts = []
        self._new_obstacles = []

    def on_model(self, model):
        print(f"Answer: {len(self._models) + 1}")
        print(model)

        
        if len(self._models) == 0:
            visited = []
            new_obstacle = []
            for atom in model.symbols(atoms=True ):
                if atom.match("at", 5):
                    x = atom.arguments[1].number
                    y = atom.arguments[2].number
                    a = atom.arguments[3].number
                    b = atom.arguments[4].number
                    new_start = (x, y, a, b)
                    visited.append(new_start)
                    new_obstacle.append((x+a,y+b))

            self._new_starts = visited
            self._new_obstacles = new_obstacle
            print(f"New Starts: {self._new_starts}")
            print(f"New Obstacles: {self._new_obstacles}")

        self._models.append(model)    

    def main(self, ctl, files):
        self._ctl = Control()
        self._ctl.configuration.solve.models = 0
        for file in files:
            self._ctl.load(file)
        if not files:
            self._ctl.load("-")
            
            
        self._ctl.add("part1", [], PART1)
        self._ctl.add("part2", [], PART2)
        self._ctl.add("step", ["m1", "m2"], "step(m2,X,Y,A,B) :- not new_obstacles(X+A,Y+B), step(m1,X,Y,A,B), not escaped(X+A,Y+B).")
        self._ctl.add("loop", [], ":- step(T1,X,Y,A,B), step(T2,X,Y,A,B), T1!=T2.")

        self._ctl.add("shows", [], "#show new_start/4. #show part1/1. #show newest_obs/2. #show step/4.")


        self._ctl.ground([("base", []), ("part1", []), ("shows", [])], context=self)
        self._ctl.solve(on_model=self.on_model)
        self._ctl.ground([("part2", [])], context=self)

        step = 0
        while True:
            programs = [("step", [Number(step), Number(step+1)]),
                        ("loop", [])]
            self._ctl.ground(programs, context=self)
            ret = self._ctl.solve(on_model=self.on_model)

            if ret.satisfiable:
                step += 1
            else:
                break

        #for new_start, new_obstacle in zip(self._new_starts, self._new_obstacles):
            #print("-" * 120)
            #print(f"New Start: {new_start}")
            #print(f"New Obstacle: {new_obstacle}")
            #programs = [("flag", [Number(step)]),
                        #("shows", []),
                        #("newest_obs", [])]
            #self._ctl.ground(programs, context=self)

            #for flag in flags:
                #self._ctl.assign_external(parse_term(flag), False)
            
            #self._ctl.assign_external(parse_term(f"flag({step})"), True)
            #flags.append(f"flag({step})")

            ## solve
            #self._ctl.solve(on_model=self.on_model)

            #step += 1


if __name__ == "__main__":
    app = AoC6()
    clingo_main(app, sys.argv[1:])