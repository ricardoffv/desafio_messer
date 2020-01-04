from crontab import CronTab

USER='ricardoffv'

cron = CronTab(user=USER)
job = cron.new(command='python3 get_ipgm.py')
job.month.every(1)

cron.write()