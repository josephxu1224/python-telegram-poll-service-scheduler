Morning Service
START 4:00am
STOP 6:30am
REMIND|PIN 4:00am


Wednesday Serivce & Friday Prayer Meetting
START 5:00pm
STOP 8:30pm
REMIND|PIN 5:00pm


Sunday Serivce

START 8:00Am
STOP 11:30Am
REMIND|PIN  8:00Am


crontab -l


# Morning Service Monday to Friday
0,30 4 * * 1-5 python3 ~/ScheduleServicePollCN/poll_scheduler.py --group-id=542770295 --tag='send'
0 6 * * 1-5 python3 ~/ScheduleServicePollCN/poll_scheduler.py --group-id=542770295 --tag='remind'
30 6 * * 1-5 python3 ~/ScheduleServicePollCN/poll_scheduler.py --group-id=542770295 --tag='stop'
#
# Wednesday Service and Friday Prayer Meeting
0,30 17 * * 3,5 python3 ~/ScheduleServicePollCN/poll_scheduler.py --group-id=542770295 --tag='send'
0 20 * * 3,5 python3 ~/ScheduleServicePollCN/poll_scheduler.py --group-id=542770295 --tag='remind'
30 20 * * 3,5 python3 ~/ScheduleServicePollCN/poll_scheduler.py --group-id=542770295 --tag='stop'
#
# Sunday Service
0,30 8 * * 0 python3 ~/ScheduleServicePollCN/poll_scheduler.py --group-id=542770295 --tag='send'
0 11 * * 0 python3 ~/ScheduleServicePollCN/poll_scheduler.py --group-id=542770295 --tag='remind'
30 11 * * 0 python3 ~/ScheduleServicePollCN/poll_scheduler.py --group-id=542770295 --tag='stop'
