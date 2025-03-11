from pathlib import Path
import subprocess

data = Path('example.txt').read_text().strip().splitlines()
#data = Path('input.txt').read_text().strip().splitlines()

PART_1 = """
#program base.
dir(0,1). dir(1,0). dir(0,-1). dir(-1,0).
rule(dir(0,-1),dir(1,0)).  % up goes right
rule(dir(1,0),dir(0,1)).  % right goes down
rule(dir(0,1),dir(-1,0)).  % down goes left
rule(dir(-1,0),dir(0,-1)).  % left goes up

max(X,Y) :- X = #max { V : field(V,_) }, Y = #max { V : field(_,V) }.

at(0,X,Y,dir(0,-1)) :- start(X,Y).
at(T+1,X+A,Y+B,dir(A,B)) :- not obstacle(X+A,Y+B), at(T,X,Y,dir(A,B)), max(X_MAX,Y_MAX), X<=X_MAX; Y<=Y_MAX.
at(T,X,Y,dir(A2,B2)) :- obstacle(X+A1,Y+B1), at(T,X,Y,dir(A1,B1)), rule(dir(A1,B1),dir(A2,B2)).

part1(T-1) :- T = #count { X,Y : at(_,X,Y,_) }.

% ----------------------------------------------------------------
new_obstacles(X,Y) :- obstacle(X,Y).
%0 { new_start(X,Y,dir(A,B)) : at(_,X,Y,dir(A,B)) } 1.
new_obstacles(X+A,Y+B) :- new_start(X,Y,dir(A,B)), not obstacle(X+A,Y+B), not escaped(X+A,Y+B).
step(0,X,Y,D) :- new_start(X,Y,D).

#program check(t).
:- step(T1,X,Y,D), step(T2,X,Y,D), T1 < T2.

#program step(t).
1 { step(T+1,X+A,Y+B,dir(A,B)) } 1 :- not new_obstacles(X+A,Y+B), step(T,X,Y,dir(A,B)), not escaped(X+A,Y+B).
step(T,X,Y,dir(A2,B2)) :- new_obstacles(X+A1,Y+B1), step(T,X,Y,dir(A1,B1)), rule(dir(A1,B1),dir(A2,B2)), T < maxsteps. 

visited(X,Y,D) :- step(_,X,Y,D).

escaped(X+1,1..Y) :- max(X,Y).
escaped(1..X,Y+1) :- max(X,Y).
escaped(-1,1..Y) :- max(X,Y).
escaped(1..X,-1) :- max(X,Y).


escape :- step(T,X,Y,dir(A,B)), escaped(X+A,Y+B).
loop :- step(T,_,_,_), T >= maxsteps.

% ----------------------------------------------------------------
% Constraints
% ----------------------------------------------------------------
% do not allow an obstacle to be placed on the start position
:- new_obstacles(X,Y), start(X,Y).

% do not allow the route to escape the field
:- escape.

% do not allow the route to loop
%:- new_obstacles, step(T1,X,Y,H), step(T2,X,Y,H), T1!=T2.

% uncomment once the program halts
%:- new_obstacles, not loop.

% do not allow the route to loop
%:- step(T1,X,Y,H), step(T2,X,Y,H), T1!=T2.


#show part1/1.
%#show at/4.
#show step/4.
#show loop/0.
#show escape/0.
%#show no_new_obstacles/0.
%#show new_obstacles/0.
"""

PART_2 = """
"""

def convert_to_ASP(data):
    with open('instance.lp', 'w') as instance:
        for lineNumber, line in enumerate(data):
            for index, character in enumerate(line):
                if "#" in character:
                    instance.write(f"obstacle({index+1},{lineNumber+1}).\n")

                if "^" in character:
                    instance.write(f"start({index+1},{lineNumber+1}).\n")
        instance.write(f"field(1..{index+1},1..{lineNumber+1}).\n")

                

def run_clingo_input(encoding, files):
    cmd = ['clingo'] + files + ['-', '0']
    result = subprocess.run(cmd, input=encoding, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)


convert_to_ASP(data)
print("----------------------------------------------------------------")
print("Part 1:")
run_clingo_input(PART_1, ['instance.lp'])
print("----------------------------------------------------------------")
print("Part 2:")
#run_clingo_input(PART_2, ['instance.lp', 'new_sequence.lp'])
