from pathlib import Path
import subprocess

data = Path('input.txt').read_text().splitlines()

PROBLEM_ENCODING = """
col(N) :- cell(N,1,_).
row(N) :- cell(1,N,_).

% part 1
% straight
valid(X,Y,"D") :- cell(X,Y,"X"), cell(X,Y+1,"M"), cell(X,Y+2,"A"), cell(X,Y+3,"S"), col(X), row(Y).
valid(X,Y,"U") :- cell(X,Y,"X"), cell(X,Y-1,"M"), cell(X,Y-2,"A"), cell(X,Y-3,"S"), col(X), row(Y).
valid(X,Y,"R") :- cell(X,Y,"X"), cell(X+1,Y,"M"), cell(X+2,Y,"A"), cell(X+3,Y,"S"), col(X), row(Y).
valid(X,Y,"L") :- cell(X,Y,"X"), cell(X-1,Y,"M"), cell(X-2,Y,"A"), cell(X-3,Y,"S"), col(X), row(Y).

% diagonals
valid(X,Y, "RD") :- cell(X,Y,"X"), cell(X+1,Y+1, "M"), cell(X+2,Y+2,"A"), cell(X+3,Y+3,"S"), col(X), row(Y).
valid(X,Y, "LU") :- cell(X,Y,"X"), cell(X-1,Y-1, "M"), cell(X-2,Y-2,"A"), cell(X-3,Y-3,"S"), col(X), row(Y).
valid(X,Y, "RU") :- cell(X,Y,"X"), cell(X+1,Y-1, "M"), cell(X+2,Y-2,"A"), cell(X+3,Y-3,"S"), col(X), row(Y).
valid(X,Y, "LD") :- cell(X,Y,"X"), cell(X-1,Y+1, "M"), cell(X-2,Y+2,"A"), cell(X-3,Y+3,"S"), col(X), row(Y).

% part 2
valid2(X,Y, "MAS") :- cell(X,Y,"A"), cell(X-1,Y+1, "M"), cell(X+1,Y-1,"S"), cell(X-1,Y-1,"M"), cell(X+1,Y+1,"S"),col(X), row(Y).
valid2(X,Y, "MAS") :- cell(X,Y,"A"), cell(X-1,Y+1, "S"), cell(X+1,Y-1,"M"), cell(X-1,Y-1,"M"), cell(X+1,Y+1,"S"),col(X), row(Y).
valid2(X,Y, "MAS") :- cell(X,Y,"A"), cell(X-1,Y+1, "M"), cell(X+1,Y-1,"S"), cell(X-1,Y-1,"S"), cell(X+1,Y+1,"M"),col(X), row(Y).
valid2(X,Y, "MAS") :- cell(X,Y,"A"), cell(X-1,Y+1, "S"), cell(X+1,Y-1,"M"), cell(X-1,Y-1,"S"), cell(X+1,Y+1,"M"),col(X), row(Y).

%#show valid/3.
%#show valid2/3.
part1(C) :- C = #count { X,Y,D : valid(X,Y,D), col(X), row(Y) }.
part2(C) :- C = #count { X,Y,D : valid2(X,Y,D), col(X), row(Y) }.

#show part1/1.
#show part2/1.
"""

def convertToASPEncoding(data):
    with open('instance.lp', 'w') as instance:
        for lineNumber, line in enumerate(data):
            for index, character in enumerate(line):
                instance.write(f"cell({index+1},{lineNumber+1},\"{character}\").\n")

def run_clingo_input(encoding, instance):
    cmd = ['clingo', instance, '-']
    result = subprocess.run(cmd, input=encoding, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)


convertToASPEncoding(data)
run_clingo_input(PROBLEM_ENCODING, 'instance.lp')
