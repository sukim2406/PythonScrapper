from indeed import get_jobs as get_indeed_jobs
from stackoverflow import get_jobs as get_stackoverflo_jobs

indeed_jobs = get_indeed_jobs()
stackoverflow_jobs = get_stackoverflo_jobs()

jobs = indeed_jobs + stackoverflow_jobs

print(jobs)