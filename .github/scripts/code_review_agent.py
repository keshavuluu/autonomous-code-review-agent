#!/usr/bin/env python3
"""
Autonomous Code Review Agent
Automatically reviews pull requests and provides feedback via GitHub comments.
"""

import os
import sys
import json
import subprocess
import requests
from typing import List, Dict, Any, Optional
import openai
import anthropic
import google.generativeai as genai
from pathlib import Path

class CodeReviewAgent:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        
        # GitHub context
        self.repo = os.getenv('GITHUB_REPOSITORY')
        self.pr_number = os.getenv('GITHUB_EVENT_PATH')
        
        # Initialize AI clients
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        if self.anthropic_api_key:
            self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_api_key)
        if os.getenv('GOOGLE_API_KEY'):
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    
    def get_pr_details(self) -> Dict[str, Any]:
        """Get PR details from GitHub API"""
        with open(self.pr_number, 'r') as f:
            event_data = json.load(f)
        
        pr_data = event_data['pull_request']
        return {
            'number': pr_data['number'],
            'title': pr_data['title'],
            'body': pr_data['body'],
            'head_sha': pr_data['head']['sha'],
            'base_sha': pr_data['base']['sha'],
            'files': pr_data['files']
        }
    
    def get_changed_files(self) -> List[str]:
        """Get list of changed files in the PR"""
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
            capture_output=True, text=True
        )
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    
    def run_linters(self, file_path: str) -> List[str]:
        """Run traditional linters on the file"""
        issues = []
        
        # Determine file type and run appropriate linters
        if file_path.endswith('.py'):
            # Python linters
            linters = [
                ('pylint', ['pylint', file_path]),
                ('flake8', ['flake8', file_path]),
                ('black', ['black', '--check', file_path]),
                ('isort', ['isort', '--check-only', file_path])
            ]
        elif file_path.endswith(('.js', '.ts', '.jsx', '.tsx')):
            # JavaScript/TypeScript linters
            linters = [
                ('eslint', ['npx', 'eslint', file_path]),
                ('prettier', ['npx', 'prettier', '--check', file_path])
            ]
        else:
            return issues
        
        for linter_name, command in linters:
            try:
                result = subprocess.run(command, capture_output=True, text=True, timeout=30)
                if result.returncode != 0:
                    issues.append(f"**{linter_name}**: {result.stderr or result.stdout}")
            except subprocess.TimeoutExpired:
                issues.append(f"**{linter_name}**: Timeout")
            except FileNotFoundError:
                continue
        
        return issues
    
    def analyze_code_with_ai(self, file_path: str, file_content: str) -> List[str]:
        """Analyze code using AI models"""
        issues = []
        
        # Prepare context for AI analysis
        context = f"""
        Please review this code file: {file_path}
        
        Code:
        ```{self.get_file_extension(file_path)}
        {file_content}
        ```
        
        Please analyze this code for:
        1. Code quality and best practices
        2. Potential bugs or issues
        3. Security vulnerabilities
        4. Performance improvements
        5. Maintainability concerns
        
        Provide specific, actionable feedback in a clear, professional tone.
        Focus on the most important issues first.
        """
        
        # Try different AI providers
        if self.openai_api_key:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert code reviewer. Provide clear, actionable feedback."},
                        {"role": "user", "content": context}
                    ],
                    max_tokens=1000,
                    temperature=0.3
                )
                ai_feedback = response.choices[0].message.content
                if ai_feedback.strip():
                    issues.append(f"**AI Review (OpenAI)**: {ai_feedback}")
            except Exception as e:
                issues.append(f"**AI Review Error**: {str(e)}")
        
        elif self.anthropic_api_key:
            try:
                response = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1000,
                    messages=[
                        {"role": "user", "content": context}
                    ]
                )
                ai_feedback = response.content[0].text
                if ai_feedback.strip():
                    issues.append(f"**AI Review (Claude)**: {ai_feedback}")
            except Exception as e:
                issues.append(f"**AI Review Error**: {str(e)}")
        
        return issues
    
    def get_file_extension(self, file_path: str) -> str:
        """Get file extension for syntax highlighting"""
        return Path(file_path).suffix.lstrip('.') or 'text'
    
    def read_file_content(self, file_path: str) -> str:
        """Read file content safely"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def post_comment(self, file_path: str, line_number: int, comment: str):
        """Post a comment to the GitHub PR"""
        pr_details = self.get_pr_details()
        
        url = f"https://api.github.com/repos/{self.repo}/pulls/{pr_details['number']}/comments"
        
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        data = {
            'body': comment,
            'path': file_path,
            'line': line_number,
            'commit_id': pr_details['head_sha']
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            print(f"Posted comment on {file_path}:{line_number}")
        except Exception as e:
            print(f"Error posting comment: {str(e)}")
    
    def post_review_comment(self, comment: str):
        """Post a general review comment"""
        pr_details = self.get_pr_details()
        
        url = f"https://api.github.com/repos/{self.repo}/pulls/{pr_details['number']}/reviews"
        
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        data = {
            'body': comment,
            'event': 'COMMENT'
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            print("Posted review comment")
        except Exception as e:
            print(f"Error posting review comment: {str(e)}")
    
    def run_review(self):
        """Main review process"""
        print("Starting code review...")
        
        changed_files = self.get_changed_files()
        if not changed_files:
            print("No changed files found")
            return
        
        all_issues = []
        
        for file_path in changed_files:
            if not os.path.exists(file_path):
                continue
                
            print(f"Reviewing {file_path}...")
            file_content = self.read_file_content(file_path)
            
            # Run traditional linters
            linter_issues = self.run_linters(file_path)
            
            # Run AI analysis
            ai_issues = self.analyze_code_with_ai(file_path, file_content)
            
            # Combine issues
            file_issues = linter_issues + ai_issues
            
            if file_issues:
                # Post file-specific comments
                comment = f"## Code Review for {file_path}\n\n" + "\n\n".join(file_issues)
                self.post_comment(file_path, 1, comment)
                all_issues.extend(file_issues)
        
        # Post summary comment
        if all_issues:
            summary = f"""
## Code Review Summary

Found {len(all_issues)} issues across {len(changed_files)} files.

### Key Findings:
- Linter issues: {len([i for i in all_issues if 'linter' in i.lower()])}
- AI analysis issues: {len([i for i in all_issues if 'ai review' in i.lower()])}

Please review the detailed comments above and address the identified issues.
            """
            self.post_review_comment(summary)
        else:
            self.post_review_comment("✅ Code review completed - no issues found!")

def main():
    agent = CodeReviewAgent()
    agent.run_review()

if __name__ == "__main__":
    main() 