#!/usr/bin/env python3
"""
Dynamic GitHub Profile README Updater
Automatically updates GitHub profile README with dynamic content
"""

import os
import re
import requests
import json
from datetime import datetime, timezone
import pytz

class GitHubProfileUpdater:
    def __init__(self, username="Skyy_07", github_token=None):
        self.username = username
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.headers = {
            'Authorization': f'token {self.github_token}' if self.github_token else None,
            'Accept': 'application/vnd.github.v3+json'
        }
        
    def get_current_timestamp(self):
        """Generate current timestamp in IST"""
        ist = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(ist)
        return current_time.strftime("%B %d, %Y at %I:%M %p IST")
    
    def get_github_activity(self):
        """Fetch recent GitHub activity"""
        try:
            url = f"https://api.github.com/users/{self.username}/events/public"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                events = response.json()[:5]  # Get last 5 events
                activity_lines = []
                
                for event in events:
                    event_type = event['type']
                    repo_name = event['repo']['name']
                    created_at = datetime.fromisoformat(event['created_at'].replace('Z', '+00:00'))
                    
                    if event_type == 'PushEvent':
                        commits = len(event['payload'].get('commits', []))
                        activity_lines.append(f"🔨 Pushed {commits} commit(s) to **{repo_name}**")
                    elif event_type == 'CreateEvent':
                        ref_type = event['payload'].get('ref_type', 'repository')
                        activity_lines.append(f"✨ Created {ref_type} in **{repo_name}**")
                    elif event_type == 'IssuesEvent':
                        action = event['payload']['action']
                        activity_lines.append(f"📝 {action.capitalize()} issue in **{repo_name}**")
                    elif event_type == 'PullRequestEvent':
                        action = event['payload']['action']
                        activity_lines.append(f"🔀 {action.capitalize()} pull request in **{repo_name}**")
                    elif event_type == 'WatchEvent':
                        activity_lines.append(f"⭐ Starred **{repo_name}**")
                
                return '\n'.join([f"- {line}" for line in activity_lines]) if activity_lines else "- 🚀 Building awesome projects!"
            
        except Exception as e:
            print(f"Error fetching GitHub activity: {e}")
        
        return "- 🚀 Building awesome projects!"
    
    def get_featured_projects(self):
        """Fetch featured repositories"""
        try:
            url = f"https://api.github.com/users/{self.username}/repos"
            params = {'sort': 'updated', 'per_page': 6}
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                repos = response.json()
                project_lines = []
                
                for repo in repos:
                    if not repo['fork'] and repo['description']:
                        name = repo['name']
                        description = repo['description'][:80] + "..." if len(repo['description']) > 80 else repo['description']
                        language = repo['language'] or 'Code'
                        stars = repo['stargazers_count']
                        url = repo['html_url']
                        
                        project_lines.append(
                            f"### [{name}]({url})\n"
                            f"**{description}**\n"
                            f"🔧 Built with {language} | ⭐ {stars} stars\n"
                        )
                
                return '\n'.join(project_lines[:3]) if project_lines else "🚧 Exciting projects coming soon!"
            
        except Exception as e:
            print(f"Error fetching projects: {e}")
        
        return "🚧 Exciting projects coming soon!"
    
    def get_leetcode_stats(self):
        """Generate LeetCode stats placeholder"""
        return """
<div align="center">
  <img src="https://leetcard.jacoblin.cool/Skyy_07?theme=dark&font=Fira%20Code&ext=contest" alt="LeetCode Stats"/>
</div>

**Recent Submissions:**
- 🟢 Easy: 50+ problems solved
- 🟡 Medium: 30+ problems solved  
- 🔴 Hard: 10+ problems solved
"""
    
    def get_codeforces_stats(self):
        """Generate Codeforces stats placeholder"""
        return """
<div align="center">
  <img src="https://codeforces-readme-stats.vercel.app/api/card?username=Skyy_07&theme=github_dark" alt="Codeforces Stats"/>
</div>

**Contest Performance:**
- 📊 Current Rating: Expert
- 🏆 Max Rating: 1800+
- 🎯 Problems Solved: 200+
"""
    
    def get_blog_posts(self):
        """Generate blog posts placeholder"""
        return """
- 🤖 [Getting Started with Machine Learning in Flutter](https://your-blog.com/ml-flutter)
- 🚀 [Building Responsive Web Apps with React.js](https://your-blog.com/react-responsive)
- 📱 [Mobile App Performance Optimization Tips](https://your-blog.com/mobile-performance)
- 🎨 [The Art of Clean Code: Best Practices](https://your-blog.com/clean-code)
"""
    
    def update_readme(self):
        """Update the README.md file with dynamic content"""
        try:
            # Read current README
            readme_path = 'README.md'
            if not os.path.exists(readme_path):
                print("README.md not found!")
                return False
            
            with open(readme_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Update timestamp
            timestamp_pattern = r'<!--START_SECTION:timestamp-->.*?<!--END_SECTION:timestamp-->'
            timestamp_replacement = f'<!--START_SECTION:timestamp-->\n**{self.get_current_timestamp()}**\n<!--END_SECTION:timestamp-->'
            content = re.sub(timestamp_pattern, timestamp_replacement, content, flags=re.DOTALL)
            
            # Update activity
            activity_pattern = r'<!--START_SECTION:activity-->.*?<!--END_SECTION:activity-->'
            activity_replacement = f'<!--START_SECTION:activity-->\n{self.get_github_activity()}\n<!--END_SECTION:activity-->'
            content = re.sub(activity_pattern, activity_replacement, content, flags=re.DOTALL)
            
            # Update projects
            projects_pattern = r'<!--START_SECTION:projects-->.*?<!--END_SECTION:projects-->'
            projects_replacement = f'<!--START_SECTION:projects-->\n{self.get_featured_projects()}\n<!--END_SECTION:projects-->'
            content = re.sub(projects_pattern, projects_replacement, content, flags=re.DOTALL)
            
            # Update LeetCode stats
            leetcode_pattern = r'<!--START_SECTION:leetcode-->.*?<!--END_SECTION:leetcode-->'
            leetcode_replacement = f'<!--START_SECTION:leetcode-->\n{self.get_leetcode_stats()}\n<!--END_SECTION:leetcode-->'
            content = re.sub(leetcode_pattern, leetcode_replacement, content, flags=re.DOTALL)
            
            # Update Codeforces stats
            codeforces_pattern = r'<!--START_SECTION:codeforces-->.*?<!--END_SECTION:codeforces-->'
            codeforces_replacement = f'<!--START_SECTION:codeforces-->\n{self.get_codeforces_stats()}\n<!--END_SECTION:codeforces-->'
            content = re.sub(codeforces_pattern, codeforces_replacement, content, flags=re.DOTALL)
            
            # Update blog posts
            blog_pattern = r'<!--START_SECTION:blog-->.*?<!--END_SECTION:blog-->'
            blog_replacement = f'<!--START_SECTION:blog-->\n{self.get_blog_posts()}\n<!--END_SECTION:blog-->'
            content = re.sub(blog_pattern, blog_replacement, content, flags=re.DOTALL)
            
            # Write updated content
            with open(readme_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            print(f"✅ README.md updated successfully at {self.get_current_timestamp()}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating README: {e}")
            return False

def main():
    """Main function to run the updater"""
    print("🚀 Starting GitHub Profile README Update...")
    
    updater = GitHubProfileUpdater()
    success = updater.update_readme()
    
    if success:
        print("🎉 Profile update completed successfully!")
    else:
        print("⚠️  Profile update failed. Check the logs above.")

if __name__ == "__main__":
    main()
