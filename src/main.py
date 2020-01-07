from indeed import get_jobs as get_indeed_jobs
from stackoverflow import get_jobs as get_stackoverflo_jobs
from extract_to_file import save_to_file

indeed_jobs = get_indeed_jobs()
stackoverflow_jobs = get_stackoverflo_jobs()

jobs = indeed_jobs + stackoverflow_jobs

save_to_file(jobs)