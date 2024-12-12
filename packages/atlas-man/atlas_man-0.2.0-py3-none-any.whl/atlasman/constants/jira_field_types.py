"""
all known issue types within Jira and their expected type.
"""

JIRA_FIELD_TYPES = {
    # Standard Fields
    "summary": str,
    "description": str,
    "issuetype": dict,  # Complex type with id, name, etc.
    "project": dict,    # Complex type with id, key, name
    "priority": dict,   # Complex type with id, name
    "status": dict,     # Complex type with id, name, statusCategory
    "resolution": dict, # Complex type with id, name
    "assignee": dict,   # Complex type with accountId, displayName, emailAddress
    "reporter": dict,   # Complex type with accountId, displayName, emailAddress
    "created": str,     # ISO 8601 datetime
    "updated": str,     # ISO 8601 datetime
    "resolutiondate": str,  # ISO 8601 datetime
    "duedate": str,     # Format: YYYY-MM-DD
    "components": list, # List of component dicts
    "labels": list,     # List of strings
    "fixVersions": list,  # List of version dicts
    "versions": list,   # List of version dicts
    "watches": dict,    # Complex type with self, watchCount, isWatching
    "worklog": dict,    # Complex type with worklogs array
    "timeestimate": int,  # Seconds
    "timeoriginalestimate": int,  # Seconds
    "timespent": int,   # Seconds
    "aggregatetimespent": int,  # Seconds
    "aggregatetimeestimate": int,  # Seconds
    "aggregateprogress": dict,  # Complex type with progress, total
    "progress": dict,   # Complex type with progress, total
    "environment": str,
    "security": dict,   # Complex type with id, name

    # Common Custom Fields
    "customfield_10016": int,    # Story Points
    "customfield_10033": dict,    # Project
    "customfield_10014": list,   # Sprint (List of sprint objects)
    "customfield_10020": list,   # Epic Link
    "customfield_10015": str,    # Epic Name
    "customfield_10011": dict,   # Epic Status
    "customfield_10010": dict,   # Account/Customer
    "customfield_10013": str,    # Original Story Points
    "customfield_10007": dict,   # Team
    "customfield_10008": dict,   # Department
    "customfield_10009": list,   # Dependencies
    "customfield_10018": dict,   # Parent Link
    "customfield_10019": float,  # Time Tracking
    "customfield_10021": str,    # Release Version
    "customfield_10022": dict,   # Risk Assessment
    "customfield_10023": list,   # Attachments
    "customfield_10024": dict,   # Business Value
    "customfield_10025": str,    # Implementation Notes
    "customfield_10026": dict,   # Test Coverage
    "customfield_10027": list,   # Affected Users
    "customfield_10028": dict,   # Root Cause
    "customfield_10029": str,    # Solution
    "customfield_10030": dict,   # Impact Assessment
    "customfield_10031": list,   # Stakeholders
    "customfield_10032": dict,   # Cost Center

    # Complex Field Structures
    "comment": {
        "comments": list,        # List of comment objects
        "maxResults": int,
        "total": int,
        "startAt": int
    },

    # Changelog Fields
    "changelog": {
        "histories": list,       # List of change objects
        "maxResults": int,
        "total": int,
        "startAt": int
    },

    # Subtask Related
    "subtasks": list,           # List of subtask objects
    "parent": dict,             # Parent issue reference
    "issuelinks": list,         # List of issue link objects
}
