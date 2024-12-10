from dataclasses import dataclass

@dataclass
class GitLabApplicationStats():
   forks: str
   issues: str
   merge_requests: str
   notes: str
   snippets: str
   ssh_keys: str
   milestones: str
   users: str
   groups: str
   projects: str
   active_users: str
