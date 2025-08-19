import subprocess
import os
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

class GitRepo:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self._ensure_git_repo()
    
    def _ensure_git_repo(self):
        """Initialize git repository if it doesn't exist"""
        git_dir = self.repo_path / ".git"
        if not git_dir.exists():
            try:
                subprocess.run(["git", "init"], cwd=self.repo_path, check=True, 
                             capture_output=True, text=True)
                
                # Set initial config if not set
                try:
                    subprocess.run(["git", "config", "user.name", "CMS User"], 
                                 cwd=self.repo_path, check=True)
                    subprocess.run(["git", "config", "user.email", "cms@localhost"], 
                                 cwd=self.repo_path, check=True)
                except subprocess.CalledProcessError:
                    pass  # Config might already be set
                    
            except subprocess.CalledProcessError as e:
                print(f"Failed to initialize git repository: {e}")
    
    def add_file(self, file_path: str):
        """Add file to git staging area"""
        try:
            subprocess.run(["git", "add", file_path], 
                         cwd=self.repo_path, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to add file to git: {e}")
            # Continue without git operations
    
    def commit(self, message: str, author_name: str = None, author_email: str = None):
        """Commit changes with message and optional author"""
        try:
            cmd = ["git", "commit", "-m", message]
            
            if author_name and author_email:
                cmd.extend(["--author", f"{author_name} <{author_email}>"])
            
            result = subprocess.run(cmd, cwd=self.repo_path, check=True, 
                                  capture_output=True, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            if "nothing to commit" in str(e.stdout):
                return "No changes to commit"
            print(f"Warning: Failed to commit to git: {e}")
            return "File saved (git commit failed)"
    
    def get_file_diff(self, file_path: str, revision: str = "HEAD~1") -> str:
        """Get diff for a specific file"""
        try:
            result = subprocess.run([
                "git", "diff", revision, "HEAD", "--", file_path
            ], cwd=self.repo_path, capture_output=True, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error getting diff: {e}"
    
    def get_commit_history(self, file_path: str = None, limit: int = 10) -> list:
        """Get commit history, optionally for a specific file"""
        try:
            cmd = ["git", "log", "--oneline", f"-{limit}"]
            if file_path:
                cmd.extend(["--", file_path])
            
            result = subprocess.run(cmd, cwd=self.repo_path, 
                                  capture_output=True, text=True, check=True)
            
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split(' ', 1)
                    if len(parts) >= 2:
                        commits.append({
                            'hash': parts[0],
                            'message': parts[1]
                        })
            return commits
        except subprocess.CalledProcessError:
            return []
    
    def get_status(self) -> Dict[str, Any]:
        """Get repository status"""
        try:
            # Get status
            result = subprocess.run(["git", "status", "--porcelain"], 
                                  cwd=self.repo_path, capture_output=True, text=True)
            
            changes = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    status = line[:2]
                    file_path = line[3:]
                    changes.append({
                        'status': status.strip(),
                        'file': file_path
                    })
            
            # Get current branch
            branch_result = subprocess.run(["git", "branch", "--show-current"], 
                                         cwd=self.repo_path, capture_output=True, text=True)
            current_branch = branch_result.stdout.strip()
            
            return {
                'changes': changes,
                'current_branch': current_branch,
                'has_changes': bool(changes)
            }
        except subprocess.CalledProcessError:
            return {'changes': [], 'current_branch': 'main', 'has_changes': False}
    
    def remove_file(self, file_path: str):
        """Remove file from git and filesystem"""
        try:
            subprocess.run(["git", "rm", file_path], 
                         cwd=self.repo_path, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to remove file from git: {e}")
