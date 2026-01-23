---
description: Sync local changes to GitHub with detailed commit messages (GitOps)
---

1.  **Check Status**: Verify exactly what has changed.
    ```bash
    git status
    ```

2.  **Stage Changes**: Add new and modified files.
    ```bash
    git add .
    ```

3.  **Commit with Detail**: Create a commit message that explains *what* and *why*.
    *   Format: `Category: Short summary` followed by a bulleted list of details if necessary.
    *   *Example:* `Refactor: Moved media stacks to /media. updated docker-compose paths.`
    ```bash
    git commit -m "Type: Detailed summary of changes"
    ```

4.  **Push and Verify**: Push to main and check the status.
    ```bash
    git push
    // turbo
    git status
    ```
