# atlas-man
A CLI to manage Trello and Jira projects.

This project is in very early, but very active stages of development.

## Development Status
- Trello:
  - ✅ List boards
  - ✅ List lists
  - ✅ List cards
  - ✅ Add board
  - ✅ Add list
  - ✅ Add card
  - ✅ Update board
  - ✅ Update list
  - ✅ Update card
  - ✅ Delete board
  - ✅ Delete list
  - ✅ Delete card
- Jira:
  - List issues
    - ✅ all issues
    - options for filtering by project, status, etc.
  - ✅ List projects
  - Add issue (default: task)
    - ✅ Add task (default option)
    - ✅ options for issue type
    - ✅ iterate through mandatory fields
    - add optional parameters for other fields
  - ✅ Add project
  - Update issue
  - Update project
    - title
  - ✅ Delete issue
  - ✅ Delete project
- General:
  - TUI (prompt_toolkit) to select boards, lists, cards, etc.
  - ✅ Config file to store API keys and other settings
  - ✅ Alias support for boards, lists, cards, etc.
  - ✅ Trello-specific and Jira-specific help text
  - Integration with [Cabinet](https://www.github.com/tylerjwoodfin/cabinet)
  - Full test coverage
  - `verbose` support from config file
  - `default_tool` support from config file
  - `output_format` support from config file
  - Export to CSV
- Future:
  - Confluence integration
  - Bitbucket integration

## Overview
`atlas-man` is a command-line interface (CLI) tool for managing tasks and projects in Trello and Jira. It allows you to interact with both platforms directly from your terminal, enabling streamlined project management without needing to open a web browser.

## Features
- List, add, and delete boards, lists, and cards on Trello.
- List, add, update, and delete issues and projects on Jira.
- Separate commands for Trello and Jira, so you can work with only the commands you need.
- Context-aware argument validation, ensuring commands are accurately targeted to Trello or Jira.

## Installation
```bash
pip install atlasman
```

or

```bash
curl -s https://api.github.com/repos/tylerjwoodfin/atlas-man/releases/latest \
| grep "browser_download_url" \
| cut -d '"' -f 4 \
| xargs curl -L -o atlas-man.pex

sudo mv atlas-man.pex /usr/local/bin/
```

Dependencies in `requirements.md` are installed automatically.

## Configuration
Before using `atlas-man`, you need to populate `~/.config/atlas-man/config.json` file with your Trello and Jira API keys.

### Trello Configuration
- Visit the [Trello Power-Ups Admin](https://trello.com/power-ups/admin/) page and create a new Power-Up.

```
New Power-Up Name: atlas-man <or anything else>
Workspace: <choose a workspace>
Iframe connector URL: <leave blank>
Email: <your email>
Support Contact: <your email>
Name: <your name>
```

- Once the Power-Up is created, go to the API Keys tab and `Generate a new API Key`.
- Copy the API Key and secret, then paste it into `~/.config/atlas-man/config.json` under the `trello` section.
- Run
```bash
export TRELLO_API_KEY=<your API key>
export TRELLO_API_SECRET=<your API secret>
```
- Visit [https://trello.com/1/authorize?expiration=never&scope=read,write&response_type=token&key=<YOUR_API_KEY>](https://trello.com/1/authorize?expiration=never&scope=read,write&response_type=token&key=<YOUR_API_KEY>).
  - Click `Allow`.
  - You will be redirected to a page with a token.
  - Copy the token from the URL into `oauth_token` in `~/.config/atlas-man/config.json`.
- Copy the token and paste it into `~/.config/atlas-man/config.json` under the `trello` section.
- Your config.json should look something like this:
```json
{
  "trello": {
    "api_key": "<your API key>",
    "api_secret": "<your API secret>",
    "oauth_token": "<your OAuth token>",
    "alias_ids": { // optional
        "shopping": {
          "board_id": "",
          "list_id": ""
        },
        "todo": {
          "board_id": "",
          "list_id": ""
        }
        // add more aliases as needed
    }
  },
}
```

### Jira Configuration

- Visit the [Jira API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens) page and create a new API token.
- Copy the token and paste it into `~/.config/atlas-man/config.json` under the `jira` section.
- Fill out other fields in `~/.config/atlas-man/config.json` as needed.
- Your config.json should look like this:
```json
{
  "jira": {
        "api_token": "",
        "base_url": "https://yourdomain.atlassian.net",
        "username": "",
        "default_project_key": "",
        "default_issue_type": "Task",
        "show_done_issues": False,
        "custom_status_order": { // optional
            "To Do": 1,
            "In Progress": 2,
            "Testing": 3,
            "Done": 4
        }
    },
}
```

## Usage
Run the CLI by executing the `main` script with the appropriate commands for Trello or Jira. You can access detailed help with the `--help` flag.

```bash
atlasman --help
```

### Trello Commands
#### Listing Commands
- **List all Trello boards**:
  ```bash
  atlasman --trello --boards
  ```
- **List all Trello lists**:
  ```bash
  atlasman --trello --lists
  ```
- **List all Trello cards**:
  ```bash
  atlasman --trello --cards
  ```

#### Add Commands
- **Add a new Trello board**:
  ```bash
  atlasman --trello --add-board "Board Name"
  ```
- **Add a new Trello list to an existing board**:
  ```bash
  atlasman --trello --add-list "Board ID" "List ID"
  ```
- **Add a new Trello card to an existing list**:
  ```bash
  atlasman --trello --add-card "List ID" "Card Title"
  ```

#### Delete Commands
- **Delete a Trello board**:
  ```bash
  atlasman --trello --delete-board "Board ID"
  ```
- **Delete a Trello list from a board**:
  ```bash
  atlasman --trello --delete-list "List ID"
  ```
- **Delete a Trello card from a list**:
  ```bash
  atlasman --trello --delete-card "Card ID"
  ```

### Jira Commands
#### Listing Commands
- **List all Jira issues**:
  ```bash
  atlasman --jira --issues
  ```
  - By default, this lists all issues not in the "Done" status.
    - Configure this under `jira` -> `show_done_issues` in `~/.config/atlas-man/config.json`.
  - You can also configure the sort order under `jira` -> `custom_status_order` in `~/.config/atlas-man/config.json`. See the example above. Add more statuses as needed.

- **List all Jira projects**:
  ```bash
  atlasman --jira --projects
  ```

#### Add Commands
- **Add a new Jira issue to a project**:
  ```bash
  atlasman --jira --add-issue "Project Key" "Issue Title" --type "<Issue Type, optional>"
  ```

- **Add a new Jira project**:
  ```bash
  atlasman --jira --add-project "Project Name"
  ```

#### Update Commands
- **Update an existing Jira issue's title**:
  ```bash
  atlasman --jira --update-issue "Issue ID" "New Title"
  ```

#### Delete Commands
- **Delete a Jira issue**:
  ```bash
  atlasman --jira --delete-issue "Issue ID"
  ```
- **Delete a Jira project**:
  ```bash
  atlasman --jira --delete-project "Project Key"
  ```

## Example Usages
Here are a few example commands you can try:

```bash
# List all Trello boards
atlasman --trello --boards

# Add a new list to the "Development" board
atlasman --trello --add-list "Development" "Backlog"

# List all issues in Jira
atlasman --jira --issues

# Add a new issue to the "WEB" project in Jira
atlasman --jira --add-issue "WEB" "Fix homepage bug"
```

## Contributing
We welcome contributions! Please fork the repository, make your changes, and submit a pull request. Before contributing, review the following guidelines:
1. Ensure code is clear, concise, and well-documented.
2. Include comments for any complex logic.
3. Test thoroughly before submitting your pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/tylerjwoodfin/atlas-man/blob/main/LICENSE) file for more information.

## Contact
This project was developed by [Tyler Woodfin](https://www.tyler.cloud/).
For any inquiries or issues, please open an issue on [GitHub](https://github.com/tylerjwoodfin/atlas-man/issues).

Happy tasking!