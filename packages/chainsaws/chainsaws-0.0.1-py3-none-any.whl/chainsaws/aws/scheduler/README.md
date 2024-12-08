# AWS EventBridge Scheduler

AWS EventBridge Scheduler를 쉽게 사용할 수 있는 high-level 인터페이스를 제공합니다.

## Installation

pip install chainsaws

## Quick Start

### 1. Configure Scheduler

```python
from chainsaws.aws.scheduler import (
  SchedulerAPI,
  SchedulerAPIConfig,
  ScheduleRate,
  ScheduleCron
)

# initialize with default settings
scheduler = SchedulerAPI()

# Create schedule for Lambda function (runs every minute in default)
scheduler.create_schedule(
  lambda_function_arn="arn:aws:lambda:ap-northeast-2:123456789012:function:my-scheduler"
)

# Or use specific rate
scheduler.create_schedule(
  lambda_function_arn="arn:aws:lambda:ap-northeast-2:123456789012:function:my-scheduler",
  rate=ScheduleRate.EVERY_15_MINUTES
)

# Or use cron expression
scheduler.create_schedule(
  lambda_function_arn="arn:aws:lambda:ap-northeast-2:123456789012:function:my-scheduler",
  schedule_expression=ScheduleCron.daily(hour=0, minute=0) # Daily at midnight
)
```

### 2. Implement Lambda Handler

```python
from chainsaws.aws.scheduler import ScheduledTask, josin

def handler(event, context):
    """Lambda handler for scheduled tasks
    Note:
    This handler is triggered every minute, but each task
    only runs according to its schedule.
    """
    # Tasks to run daily at midnight
    with ScheduledTask('0 0 * * *') as do:
        def daily_cleanup():
            print("Running daily cleanup")

        def generate_daily_report():
            print("Generating daily report")

    do(daily_cleanup)
    do(generate_daily_report)

    # Tasks to run every 15 minutes
    with ScheduledTask('*/15 * * * *') as do:
        def check_metrics():
            print("Checking metrics")

        def update_cache():
            print("Updating cache")

        do(check_metrics)
        do(update_cache)

    # Tasks to run hourly
    with ScheduledTask('0 * * * *') as do:
        def hourly_backup():
            print("Running hourly backup")

        do(hourly_backup)

    # Wait for all tasks to complete
    join()
```

## Features

### Schedule Rates

Pre-defined common execution intervals:

```python
ScheduleRate.EVERY_MINUTE # rate(1 minute)
ScheduleRate.EVERY_5_MINUTES # rate(5 minutes)
ScheduleRate.EVERY_15_MINUTES # rate(15 minutes)
ScheduleRate.EVERY_30_MINUTES # rate(30 minutes)
ScheduleRate.EVERY_HOUR # rate(1 hour)
ScheduleRate.EVERY_3_HOURS # rate(3 hours)
ScheduleRate.EVERY_6_HOURS # rate(6 hours)
ScheduleRate.EVERY_12_HOURS # rate(12 hours)
ScheduleRate.EVERY_DAY # rate(1 day)
```

### Cron Expression Helper

Easy creation of complex cron expressions:

```python
# Daily at specific time
ScheduleCron.daily(hour=9, minute=0) # Every day at 9 AM

# Weekly at specific day/time
# ex) Every Monday at 9 AM
ScheduleCron.weekly(
  day_of_week=1, # 1=Monday
  hour=9,
  minute=0
)

# Monthly at specific day/time
# ex) First day of every month at midnight
ScheduleCron.monthly(
  day_of_month=1,
  hour=0,
  minute=0
)
```

## How It Works

1. EventBridge Scheduler triggers Lambda function every minute
2. Each ScheduledTask block in Lambda function checks current time against its schedule
3. Only tasks matching the schedule are executed
4. All tasks run asynchronously and complete at join()

## Important Notes

- Set Lambda function timeout considering task execution times
- Configure memory based on number of concurrent tasks
