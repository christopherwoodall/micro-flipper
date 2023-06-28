#!/usr/bin/env python

import yaml
import tempfile
from git import Repo
from subprocess import run
from pathlib import Path
import logging
import json

class RepoManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.manifest_file = 'manifest.micro'
        self.setup_logging()
        self.manifest = self.load_manifest()

    def setup_logging(self):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # File handler
        file_handler = logging.FileHandler('output.log')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(console_handler)

    def load_manifest(self):
        if Path(self.manifest_file).exists():
            with open(self.manifest_file, 'r') as file:
                return json.load(file)
        else:
            return {}

    def save_manifest(self):
        with open(self.manifest_file, 'w') as file:
            json.dump(self.manifest, file)

    def read_yaml_file(self):
        try:
            with open(self.config_file, 'r') as file:
                self.config = yaml.safe_load(file)
                logging.info(f'Read configuration file {self.config_file}')
                return True
        except Exception as e:
            logging.error(f'Failed to read configuration file {self.config_file}: {str(e)}')
            return False

    def clone_repo(self, repo_url, output_path):
        try:
            if Path(output_path).exists() and repo_url in self.manifest:
                repo = Repo(output_path)
                if repo.head.object.hexsha == self.manifest[repo_url]:
                    logging.info(f'Repository {repo_url} in {output_path} is up to date')
                    return True, False, False
                else:
                    before_pull = repo.head.object.hexsha
                    origin = repo.remotes.origin
                    origin.pull()
                    after_pull = repo.head.object.hexsha
                    was_updated = before_pull != after_pull
                    self.manifest[repo_url] = after_pull
                    logging.info(f'Updated repository {repo_url} in existing directory {output_path}')
                    return True, False, was_updated
            else:
                repo = Repo.clone_from(repo_url, output_path)
                self.manifest[repo_url] = repo.head.object.hexsha
                logging.info(f'Cloned repository {repo_url} into {output_path}')
                return True, True, False
        except Exception as e:
            logging.error(f'Failed to clone or update repository {repo_url}: {str(e)}')
            return False, False, False

    def run_commands(self, commands):
        try:
            if self.config.get('single_shell', False):
                command = ' && '.join(commands)
                run(command, shell=True)
                logging.info(f'Executed commands in a single shell: {command}')
            else:
                for command in commands:
                    run(command, shell=True)
                    logging.info(f'Executed command: {command}')
            return True
        except Exception as e:
            logging.error(f'Failed to execute command {command}: {str(e)}')
            return False

    def manage_repos(self):
        if not self.read_yaml_file():
            return

        for path in self.config['paths']:
            Path(path).mkdir(parents=True, exist_ok=True)

        for repo in self.config['repos']:
            success, is_new_install, was_updated = self.clone_repo(repo['repo'], repo['path'])
            if not success:
                continue

            if 'post_install' in repo:
                if is_new_install:
                    if not self.run_commands(repo['post_install']):
                        logging.error(f'Failed to execute post-install commands for repository: {repo["repo"]}')
                else:
                    logging.info(f'Skipped post-install commands for existing repository: {repo["repo"]}')

            if 'post_update' in repo:
                if was_updated:
                    if not self.run_commands(repo['post_update']):
                        logging.error(f'Failed to execute post-update commands for repository: {repo["repo"]}')
                else:
                    logging.info(f'Skipped post-update commands for repository that was not updated: {repo["repo"]}')

        self.save_manifest()


if __name__ == "__main__":
    manager = RepoManager('config.yaml')
    manager.manage_repos()
