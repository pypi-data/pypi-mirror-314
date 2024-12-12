# Stacky

Stacky is a minimal Git extension providing a [stack-like](https://www.stacking.dev/) workflow with one PR per stack, rather than one PR per commit. This allows for easier integration with GitHub's current PR workflow.

Since GitHub doesn't natively support stacked PRs, [workarounds](https://github.com/gitext-rs/git-stack/blob/main/docs/comparison.md) fall into one of three categories: serial PRs (simple but slow), parallel PRs (fast but complex and requiring permissions), or single PRs with multiple commits (fast but less flexible to review). Stacky implements the latter, with a simple and intuitive interface.

## Concept

The main idea is every *stack* is just a branch `FEATURE` with linear history rooted at its base branch `FEATURE_base`

```bash
(main)(FEATURE_base) > commit1 > commit2 > ... > commitN (FEATURE)
```

Successive commits move the stack's top branch, and rebases move the top-to-bottom stack of changes onto a new location.

One PR is created per stack, allowing reviewers to go through changes one commit at a time, while still testing and merging the stack as a single change.

Stacky is small and easy to understand, integrates natively with GitHub, and requires zero repo or org-level admin permissions or changes.

## Install

```bash
brew install git-absorb  # optional
pip install git_stacky
```

## Usage

Stacky provides four commands to manage stacks:
- `hack FEATURE` create a new stack named `FEATURE`
- `rebase TARGET` rebase the current stack onto `TARGET`
- `stacks` list all stacks, optionally as a `--graph`
- `absorb` [absorb](https://github.com/tummychow/git-absorb) changes into the current stack

Here's an example workflow:

```bash
# Help text
(main)   git stack -h

# 1. New stack (apple, apple_base branches rooted at main)
(main)   git stack hack apple
(apple)  touch apple1 && git add -A && git commit -m 'apple1'
(apple)  touch apple2 && git add -A && git commit -m 'apple2'

# 2. New stack (banana, banana_base branches rooted at main)
(apple)  git stack hack banana
(banana) touch banana1 && git add -A && git commit -m 'banana1'

# 3. Rebase banana onto apple
(banana) git stack rebase apple

# 4. Rebase banana implicitly back onto main
(banana) git stack rebase

# 5. Force-delete banana stack
(banana) git checkout apple
(apple)  git stack stacks -D banana

# History evolution
# 1. (main)(apple_base) > apple1 > apple2 (apple)
# 2. (main)(apple_base)(banana_base) > apple1 > apple2 (apple)
#                                    > banana1 (banana)
# 3. (main)(apple_base) > apple1 > apple2 (apple)(banana_base) > banana1 (banana)
# 4. (main)(apple_base)(banana_base) > apple1 > apple2 (apple)
#                                    > banana1 (banana)
# 5. (main)(apple_base) > apple1 > apple2 (apple)
```
