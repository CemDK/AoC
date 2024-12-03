from pathlib import Path
import re

teststring1 = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
teststring2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

data = Path("input.txt").read_text().strip()
data = "".join(line.strip() for line in data)

reNaiveMuls = re.compile('mul\(\d+\,\d+\)')
reDigits = re.compile('(\d+)\,(\d+)')
reMultest0 = re.compile(r"^(.*?mul\(\d+,\d+\).*?)don't\(\)")                                    # find first muls until first dont
reMultest1 = re.compile(r"don't\(\)(.*?mul\(\d+,\d+\).*?)do\(\)")                               # find muls between donts and dos
reMultest2 = re.compile(   r"do\(\)(.*?mul\(\d+,\d+\).*?)don't\(\)")                            # find muls between dos and donts
reMultest3 = re.compile(   r"do\(\)(?!.*don't\(\))(?!.*do\(\))(.*?mul\(\d+,\d+\).*?)$")         # find muls after last do if no last dont
reMultest4 = re.compile(r"don't\(\)(?!.*don't\(\))(.*?mul\(\d+,\d+\).*?)$")                     # find muls after last dont 

dos = []
donts = []
naiveMatches = []
for match in reNaiveMuls.findall(data):
    naiveMatches.append(match)

for match in reMultest0.findall(data):
    for mul in reNaiveMuls.findall(match):
        dos.append(mul)

for match in reMultest1.findall(data):
    for mul in reNaiveMuls.findall(match):
        donts.append(mul)

for match in reMultest2.findall(data):
    for mul in reNaiveMuls.findall(match):
        dos.append(mul)

for match in reMultest3.findall(data):
    print(match)
    for mul in reNaiveMuls.findall(match):
        dos.append(mul)

for match in reMultest4.findall(data):
    for mul in reNaiveMuls.findall(match):
        donts.append(mul)

# -------------------------------------------------

naiveSum = 0
for match in naiveMatches:
    for num in reDigits.findall(match):
        multiplicand = int(num[0])
        multiplier = int(num[1])
        naiveSum += multiplicand * multiplier

sumOfDos = 0
for match in dos:
    for num in reDigits.findall(match):
        multiplicand = int(num[0])
        multiplier = int(num[1])
        sumOfDos += multiplicand * multiplier

sumOfDonts = 0
for match in donts:
    for num in reDigits.findall(match):
        multiplicand = int(num[0])
        multiplier = int(num[1])
        sumOfDonts += multiplicand * multiplier

print("")
print(f"Naive Count: {len(naiveMatches)}")
print(f"Do Count: {len(dos)}")
print(f"Dont Count: {len(donts)}")
print(f"Dos and Donts Count: {len(donts) + len(dos)}")
print("")
print(f"Naive Sum: {naiveSum}")
print(f"Sum of Dos: {sumOfDos}")
print(f"Sum of Donts: {sumOfDonts}")
print(f"Sum of Dos and Donts: {sumOfDos + sumOfDonts}")
print(f"Sum: {naiveSum - sumOfDonts}")
