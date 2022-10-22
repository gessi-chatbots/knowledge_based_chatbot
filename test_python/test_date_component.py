import datetime

test_dates = [
    'August 25th',
    'August 25th at 15:00',
    '25/09/2022',
    'today',
    'tomorrow',
    '2022/09/24',
    '2022-09-04',
    '24th September 1999',
    '20220904'
]

tests = "stories:\n"

for date in test_dates:
    tests += f"""
    - story: test date num. 3
      steps:
        - user: |
          [{date}](information_calendar)
        intent: inform
        - entities: 
            - information_calendar: {datetime(date)}
        - action: action_request_information
    """