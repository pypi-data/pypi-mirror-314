import os
import rich_click as click
import tempfile
import git as GitPython
import hashlib
import json
import datetime
import requests
import coloredlogs
import logging

coloredlogs.install(level='INFO')

coloredlogs.install(
    level='INFO',
    fmt='%(asctime)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S.%f'
)

help_config = click.RichHelpConfiguration(
    text_markup="rich",
    show_arguments=True,
)
help_config.dump_to_globals()

def serialize_date_time(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


class GitRepoManager:
    def __init__(self, repo_url, clone_dir):
        self.repo_url = repo_url
        self.clone_dir = clone_dir

    def clone_repo(self):
        if os.path.exists(self.clone_dir):
            logging.info(f'Directory {self.clone_dir} already exists. Skipping clone.')
            return
        try:
            # logging.info(f'Repository beign cloned to {self.clone_dir}')
            GitPython.Repo.clone_from(self.repo_url, self.clone_dir)
            logging.info(f'Repository cloned to {self.clone_dir}')
        except Exception as e:
            logging.info(f'Error cloning repository: {e}')

    def get_commit_counts_by_date(self, author=None):
        if not os.path.exists(self.clone_dir):
            logging.info(f'Directory {self.clone_dir} does not exist. Cannot get commit counts.')
            return {}

        try:
            repo = GitPython.Repo(self.clone_dir)
            commits = list(repo.iter_commits())
            commit_counts = {}
            for commit in commits:
                if author and commit.author.email != author:
                    continue
                commit_date = commit.committed_datetime.date().isoformat()
                if commit_date in commit_counts:
                    commit_counts[commit_date] += 1
                else:
                    commit_counts[commit_date] = 1
            total_days_with_commits = len(commit_counts)
            total_commits = sum(commit_counts.values())
            logging.info(f'Total days with commits: {total_days_with_commits}')
            logging.info(f'Total number of commits: {total_commits}')
            return commit_counts
        except Exception as e:
            logging.info(f'Error getting commit counts: {e}')
            return {}

@click.group()
def skyline():
    """Skyline CLI"""
    pass

@skyline.command()
@click.option('--author', '-a', help='Filter commits by author email')
@click.argument('repository')
def git(repository, author):
    """
    Perform git operations on the specified repository
    """
    repo_hash = hashlib.md5(repository.encode()).hexdigest()
    temp_dir = os.path.join(tempfile.gettempdir(), f"skyline_{repo_hash}")
    logging.info(f'Cloninng {repository} to {temp_dir}')
    manager = GitRepoManager(repository, temp_dir)
    manager.clone_repo()
    commits = manager.get_commit_counts_by_date()
    # logging.info(f"Commits by date: {commits}")
    commits_json = json.dumps(commits, indent=4)
    # logging.info(f"Commits JSON: {commits_json}")
    try:
        response = requests.post(
            'https://api.skyline.partcad.org/timeline',
            headers={'Content-Type': 'application/json'},
            data=commits_json
        )
        if response.status_code == 200:
            logging.info('Commits successfully sent to the API.')
        else:
            logging.info(f'Failed to send commits to the API. Status code: {response.status_code}')
    except Exception as e:
        raise click.UsageError(f'Error sending commits to the API: {e}')

@skyline.command()
def clean():
    """
    Clean up temporary directories
    """
    temp_dir = tempfile.gettempdir()
    for item in os.listdir(temp_dir):
        if item.startswith('skyline_'):
            item_path = os.path.join(temp_dir, item)
            if not click.confirm(f"Do you want to remove {item_path}?"):
                continue
            item_path = os.path.join(temp_dir, item)
            logging.info(f'Removing {item_path}')
            os.system(f'rm -rf {item_path}')

if __name__ == '__main__':
    skyline()
