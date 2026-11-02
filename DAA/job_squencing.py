def job_sequencing(jobs):               # jobs = [(id, deadline, profit)]
    jobs = sorted(jobs, key=lambda j: j[2], reverse=True)   # highest profit first
    max_d = max(j[1] for j in jobs)
    slot = [None] * (max_d + 1)         # slot[1..max_d]
    total = 0
    for jid, d, p in jobs:
        for t in range(min(d, max_d), 0, -1):   # latest free slot <= deadline
            if slot[t] is None:
                slot[t] = jid
                total += p
                break
    return [s for s in slot[1:] if s], total

jobs = [('a',2,100),('b',1,19),('c',2,27),('d',1,25),('e',3,15)]
print(job_sequencing(jobs))   # (['c','a','e'], 142)


# Aim
# To schedule jobs, each taking 1 unit of time and having a deadline and a profit, so that the total profit is maximum using the greedy method.

# Theory
# Each job takes 1 unit of time, has a deadline and a profit. A job earns its profit only if it finishes on or before its deadline.
# Only one job can run at a time, so each time slot holds at most one job.
# Greedy strategy: consider jobs in decreasing order of profit, and put each job in the latest free slot on or before its deadline.
# Choosing the latest free slot keeps the earlier slots open for jobs with tighter deadlines.
# If no slot is free, the job is rejected.
    
# Algorithm
# Sort the jobs by profit in descending order.
# Find the maximum deadline and create that many empty slots (1 to max_d).
# For each job, scan slots from its deadline down to 1.
# At the first empty slot, place the job, add its profit to the total, and move to the next job.
# If no empty slot is found, skip the job.
# Return the scheduled jobs (in slot order) and the total profit.

# Dry run

# Jobs: a(2,100), b(1,19), c(2,27), d(1,25), e(3,15). After sorting by profit: a(100), c(27), d(25), b(19), e(15). Max deadline = 3.

# markdown
# | Step | Job | Deadline | Profit | Slots checked      | Action               | Slot 1 | Slot 2 | Slot 3 | Total |
# |------|-----|----------|--------|--------------------|----------------------|--------|--------|--------|-------|
# | 1    | a   | 2        | 100    | 2                  | Placed in slot 2     | -      | a      | -      | 100   |
# | 2    | c   | 2        | 27     | 2 (full), 1        | Placed in slot 1     | c      | a      | -      | 127   |
# | 3    | d   | 1        | 25     | 1 (full)           | Rejected             | c      | a      | -      | 127   |
# | 4    | b   | 1        | 19     | 1 (full)           | Rejected             | c      | a      | -      | 127   |
# | 5    | e   | 3        | 15     | 3                  | Placed in slot 3     | c      | a      | e      | 142   |

# Schedule: c → a → e, Maximum profit = 142. Jobs b and d are rejected.

# Complexity

# Let n = number of jobs and D = maximum deadline.

# markdown
# | Step                         | Time Complexity | Reason                                         |
# |------------------------------|-----------------|------------------------------------------------|
# | Sorting jobs by profit       | O(n log n)      | Standard comparison sort                       |
# | Finding max deadline         | O(n)            | One pass                                       |
# | Placing jobs (slot search)   | O(n × D)        | Each job may scan up to D slots                |
# | **Total**                    | **O(n log n + n × D)** | Worst case O(n²) when D is about n      |

# | Space Complexity | Value | Reason                                         |
# |------------------|-------|------------------------------------------------|
# | Slot array       | O(D)  | One entry per time slot                        |
# | Sorted copy      | O(n)  | `sorted()` creates a new list                  |
# | **Total**        | **O(n + D)** |                                         |
# Comparison with other approaches
# markdown
# | Point              | Brute Force                      | Greedy (this code)                 | Greedy + Union-Find (optimized)     |
# |--------------------|----------------------------------|------------------------------------|-------------------------------------|
# | Idea               | Try all subsets and orderings    | Highest profit first, latest free slot | Same, but find free slot faster |
# | Time               | O(n! ) or O(2^n × n)             | O(n log n + n × D)                 | O(n log n) almost                   |
# | Space              | O(n)                             | O(n + D)                           | O(n + D)                            |
# | Optimal?           | Yes                              | Yes                                | Yes                                 |
# | Practical?         | Only for tiny n                  | Yes                                | Best for large inputs               |
# | Slot search        | Not applicable                   | Linear scan backwards              | Near O(1) using disjoint sets       |

# Why greedy is better here: brute force checks every possible selection and order, 
# which grows exponentially. Greedy needs only one sort and one pass, and still gives the optimal answer because 
# the feasible job sets form a structure (a matroid) where taking the best available choice is always safe.

# # Why the latest free slot? It leaves earlier slots free for jobs with earlier deadlines. 
# Placing job a in slot 2 instead of slot 1 left slot 1 open for c.

# # Easy example

# # Think of an exam week where you have several assignments, each needing one day, 
# each with a last date and marks. You first take the one with the most marks, and do 
# it on its last possible day, so earlier days stay free for tighter deadlines. 
# If a task’s deadline days are all full, you skip it. That is job sequencing.

