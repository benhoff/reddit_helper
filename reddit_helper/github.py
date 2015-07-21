import requests
import datetime

def get_most_recent_commits(github_name):
    url = 'https://api.github.com/users/{}/events'.format(github_name)
    r = requests.get(url)
    events = r.json()
    push_events = []

    for event in events:
        if event['type'] == u'PushEvent':
            push_events.append(event)

    most_recent_commits = {}

    current_time = datetime.datetime.utcnow()
    tweleve_hour_delta = datetime.timedelta(hours=48)

    for push_event in push_events:
        push_time = datetime.datetime.strptime(push_event['created_at'], 
                                               '%Y-%m-%dT%H:%M:%SZ')

        delta_push_time =  current_time - push_time

        if delta_push_time < tweleve_hour_delta:
            repo_name = push_event['repo']['name']
            if repo_name in most_recent_commits:
                break
            else:
                latest_commit = push_event['payload']['commits'][0]
                most_recent_commits[repo_name] = latest_commit

    return most_recent_commits
