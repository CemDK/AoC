from pathlib import Path
import subprocess

#data = Path('example.txt').read_text().strip().splitlines()
data = Path('input.txt').read_text().strip().splitlines()

PART_1 = """
seq(S) :- sequence(S,_,_).

% it can't be the case, that we have a rule(A,B) and a sequence where A follows B
notValid(S) :- sequence(S,X,A), sequence(S,Y,B), seq(S), rule(B,A), X<Y.

valid(S) :- not notValid(S), seq(S).

mid_index(S,I) :- M = #max{ P : sequence(S,P,_) }, seq(S), I = (M+1)/2.
mid_value(S,V) :- mid_index(S,I), sequence(S,I,V).

part1(T) :- T = #sum { V,S : mid_value(S,V), valid(S) }.

#show part1/1.
"""

PART_2 = """
seq(S) :- new_sequence(S,_,_).

seq_len(S,M) :- M = #max { P : new_sequence(S,P,_) }, seq(S).
seq_values(S,V) :- new_sequence(S,_,V).

mid_index(S,I) :- M = #max{ P : new_sequence(S,P,_) }, seq(S), I = (M+1)/2.
mid_value(S,V) :- mid_index(S,I), new_sequence(S,I,V).

part2(T) :- T = #sum { V,S : mid_value(S,V), seq(S) }.

#show part2/1.
"""

GENERATE_CORRECT_SEQ = """
seq(S) :- sequence(S,_,_).

notValid(S) :- sequence(S,X,A), sequence(S,Y,B), seq(S), rule(B,A), X<Y.

seq_len(S,M) :- M = #max { P : sequence(S,P,_) }, seq(S).
seq_values(S,V) :- sequence(S,_,V).

1 { new_sequence(S,1,V) : sequence(S,I,V) } 1  :- notValid(S).
1 { new_sequence(S,I+1,V) : seq_values(S,V) } 1 :- new_sequence(S,I,_), seq_len(S,M), I<M.

:- new_sequence(S,X,A), new_sequence(S,Y,B), rule(B,A), X<Y.
:- new_sequence(S,X,A), new_sequence(S,Y,B), X==Y, A!=B.
:- new_sequence(S,X,A), new_sequence(S,Y,A), X!=Y.

#show new_sequence/3.
"""


def convert_to_ASP(data):
    with open('instance.lp', 'w') as instance:
        sequence = 0
        for lineNumber, line in enumerate(data):
            if "|" in line:
                nums = line.split("|")
                instance.write(f"rule({nums[0]},{nums[1]}).\n")

            elif line != "":
                nums = line.split(",")
                for index, num in enumerate(nums):
                    instance.write(f"sequence({sequence+1},{index+1},{num}).\n")
                sequence += 1

def run_clingo_input(encoding, files):
    cmd = ['clingo'] + files + ['-', '0']
    result = subprocess.run(cmd, input=encoding, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)

def get_new_seq(encoding, instance):
    cmd = ['clingo', instance, '-', '0']
    result = subprocess.run(cmd, input=encoding, capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if "new_sequence" not in line:
            print(line)
    if result.stderr:
        print("Errors:", result.stderr)
    with open('new_sequence.lp', 'w') as f:
        for line in result.stdout.splitlines():
            if "new_sequence" in line:
                line = line.replace(" ", ".\n")
                f.write(line + ".\n")


convert_to_ASP(data)
print("----------------------------------------------------------------")
print("Part 1:")
run_clingo_input(PART_1, ['instance.lp'])
print("----------------------------------------------------------------")
print("Generating correct sequences...")
# this takes approx 7 seconds on my machine...
get_new_seq(GENERATE_CORRECT_SEQ, 'instance.lp')
print("")
print("Part 2:")
run_clingo_input(PART_2, ['instance.lp', 'new_sequence.lp'])
