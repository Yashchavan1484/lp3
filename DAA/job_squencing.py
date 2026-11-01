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
