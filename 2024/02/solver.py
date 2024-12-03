from pathlib import Path

data = Path("input.txt").read_text().splitlines()
matrix = [line.split(" ") for line in data if line.strip()]


def check_safety(level):
    if level[0] == level[1]:
        return False, 0, 1
    
    ascending = level[0] < level[1]
    for i in range(len(level)-1):
        left = level[i]
        right = level[i+1]
        if ascending:
            if left >= right or (abs(left - right) > 3) or (left == right):
                return False, i, i+1
        else:
            if left <= right or (abs(left - right) > 3) or (left == right):
                return False, i, i+1
    
    return True, 0, 0
    

safe_levels = 0
dampened_safety = 0
total_levels = 0
unsafe_levels = 0
for level in matrix:
    current = list(map(int, level))

    safe, left, right = check_safety(current)

    now_safe = False
    if not safe:
        if left > 0:
            copy = current.copy()
            del copy[left - 1]
            now_safe, _, _ = check_safety(copy)

        if not now_safe:
            copy = current.copy()
            del copy[left]

            now_safe, _, _ = check_safety(copy)
            if not now_safe:
                copy = current.copy()
                del copy[right]
                now_safe, wrong_left, wrong_right = check_safety(copy)
        
    
    if now_safe:
        dampened_safety += 1
    if safe:
        safe_levels += 1

    if not safe and not now_safe:
        unsafe_levels += 1

    total_levels += 1
    

print("")
print(f"Safe Levels: {safe_levels}")
print(f"Dampened Levels: {dampened_safety}")
print(f"Total Safe Levels: {safe_levels + dampened_safety}")
print(f"Unsafe Levels: {unsafe_levels}")
print(f"Total Levels: {total_levels}")

