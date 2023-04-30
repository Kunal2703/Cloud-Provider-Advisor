from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from .jobs import awsjob, azurejob, gcpjob
from jobs.updateTable import main as updateTable


scheduler= BackgroundScheduler()
awsflag=0
azureflag=0
gcpflag=0

def job_listener(event):
    global awsflag, azureflag, gcpflag
    if event.exception:
        print("Some error Occurred")
    else:
        job=scheduler.get_job(event.job_id)
        if job.name=='awsjob':
            awsflag=1
        if job.name=='azurejob':
            azureflag=1
        if job.name=='gcpjob':
            gcpflag=1
        if awsflag and azureflag and gcpflag:
            print("execute update job")
            updateTable()
            awsflag=0
            azureflag=0
            gcpflag=0   

def start():
    scheduler.add_job(awsjob, 'cron', hour='*/12', name='awsjob')
    scheduler.add_job(azurejob, 'cron',  hour='*/12', name='azurejob')
    scheduler.add_job(gcpjob, 'cron',  hour='*/12', name='gcpjob')
    #scheduler.add_job(updatejob, name='updatejob')
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()





