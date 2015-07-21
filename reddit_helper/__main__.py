
import sys 
import os
import tempfile
import json

from subprocess import call

import github
import reddit

def _get_settings():
    main_dir = os.path.dirname(os.path.realpath(__file__))
    settings = None
    settings_filename= os.path.join(main_dir, 'settings.json')
    if os.path.exists(settings_filename):
        with open(settings_filename) as settings_file:
            settings = json.load(settings_file)
    else:
        print('Fill out your `settings.json` file!')
        sys.exit(0)
    return settings

def main():
    settings = _get_settings()
    reddit_username = settings['reddit_username']
    github_username = settings['github_username']

    latest_commits = github.get_most_recent_commits(github_username)

    EDITOR = os.environ.get('EDITOR','vim') #that easy!

    initial_message = 'So during this stream I\n\n'
    and_message = 'Also,\n\n'

    num_of_repos_changed = len(latest_commits)

    for index, (repo_name, commit) in enumerate(latest_commits.items()):
        github_link= "https://github.com/{}".format(repo_name)

        s = "[here's the directroy at the end of this stream]({github_link}/tree/{commit})\n\n[and here's just the repo]({github_link})\n\n".format(github_link=github_link,
                commit = commit['sha'])

        initial_message += s
        if index < num_of_repos_changed:
            initial_message += and_message

    comment = ''
    with tempfile.NamedTemporaryFile('w+', suffix=".tmp") as tempfile_:
        tempfile_.write(initial_message)
        tempfile_.flush()
        call([EDITOR, tempfile_.name])
        tempfile_.seek(0)
        comment = tempfile_.read()
    
    _ = os.system('clear')
    user_prompt = input('Submit? (Y/N): ')
    if user_prompt.lower() in ['yes', 'y', 'yeppers']:
        reddit_submission = reddit.get_most_recent_submission(reddit_username,
                settings['reddit_password'])
        
        reddit_submission.add_comment(comment)
        print('Commented!')

if __name__ == '__main__':
    main()
