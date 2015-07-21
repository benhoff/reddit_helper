import praw
def get_most_recent_submission(user_name, password):
    user_agent = 'python:github_streamer_helper:v0.0.1 (by /u/beohoff)'
    r = praw.Reddit(user_agent=user_agent)
    r.login(user_name, password)
    me = r.user

    submissions = me.get_submitted(limit=1)
    most_recent_watchpeoplecode = next(submissions)

    if most_recent_watchpeoplecode.title != 'WatchPeopleCode':
        submissions = me.get_submitted()
        for thing in submissions:
            subreddit = thing.subreddit.display_name
            print(subreddit)
            # TODO: determine if need to call `.lower()` on submission
            if subreddit == 'WatchPeopleCode':
                most_recent_watchpeoplecode = thing
                break

    return most_recent_watchpeoplecode
