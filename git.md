# What is cherry-pick and how this created a new commit

git cherry-pick is a command used to apply a specific commit from one branch to another. Instead of merging or rebasing an entire branch, cherry-pick allows you to select a single commit and apply it.

When you run git cherry-pick <commit-hash>, Git takes the changes introduced by that commit and applies them to the current branch. This creates a new commit with a different hash, even though the changes are the same. The reason for the new commit hash is that Git considers the history of a commit, and since this commit is being applied in a different context (another branch), it is treated as a new entity.

Example:
```
    git checkout feature-branch
    git cherry-pick abc123  # Applies commit abc123 from another branch
```
# How to rebase to clean up commits before a PR

Rebasing before a pull request (PR) helps to squash, reorder, or edit commits to make the history cleaner and more meaningful.
To interactively rebase and clean up commits before pushing a PR:

* Identify how many commits you want to clean up:
```
    git log --oneline
```
* Start an interactive rebase for the last N commits:
```
    git rebase -i HEAD~N
```
* This opens an editor where you can:

- Pick: Keep a commit as is.
- Squash (s): Merge a commit with the one before it.
- Edit (e): Modify the commit message or changes.
- Drop (d): Remove a commit.

* After making the changes, save and close the editor.

If you modified commits, force push the branch:
```
    git push --force
```
# Bisecting

git bisect is a tool that helps find the commit that introduced a bug by using binary search.
Instead of manually checking each commit, git bisect automates the process:

1. Start bisecting
```
    git bisect start
```
2. Mark the bad commit (where the bug exists):
```
    git bisect bad
```
3. Mark the good commit (where things worked fine):
```
git bisect good abc123  # Use a known working commit hash
```
4. Git will now check out a commit in between. Test it and mark it as either:
```
    git bisect good  # If it works fine
    git bisect bad   # If the bug is present
```
5. Repeat until Git identifies the exact commit that introduced the bug.
6. Once done, exit bisect mode:
```
    git bisect reset
```
# Reflog
git reflog (reference log) tracks every action that moves the HEAD (like checkouts, rebases, commits, and resets). It is local-only and helps recover lost commits.

* To view recent changes:
```
    git reflog
```
* Each entry has an index like HEAD@{1}, HEAD@{2}, etc., allowing you to restore a lost commit:
```
    git checkout HEAD@{3}
```
* If you accidentally reset or delete a commit, you can restore it using:
```
    git reset --hard HEAD@{1}
```