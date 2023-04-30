from django.conf import settings

from jobs.awsInstPrice import main as awsmain
from jobs.azureInstPrice import main as azuremain
from jobs.gcpInstPrice import main as gcpmain


def awsjob():
    awsmain()

def azurejob():
    azuremain()

def gcpjob():
    gcpmain()

