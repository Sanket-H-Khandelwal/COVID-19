# COVID-19

# setting up the cron job

In order to set the cron job type command

> crontab -e

In the file go to the end and type

> 0 10 * * * python <directory_path>/cron_task.py

the first number is minute, second is hr, then day of month, then month and then day of week. 

In this case the code will run at 10 am every day

For example go to https://crontab.guru/#0_15_*_*_*

To view the sqlite db you can go to https://inloop.github.io/sqlite-viewer/

# Running

In order to check if code is working install requirement.txt and run
> python cron_task.py

