# learning-the-ropes-together-
This is where we’ll practice our standard GitHub workflows
KB inserted text here!

Hi this is Gina :) 
This is an edit by Hannah.
hi! 
This is an update! -Mark


For an all-purpose tutorial, check out this [Github 'hello world' tutorial](https://docs.github.com/en/get-started/start-your-journey/hello-world)


### Some helpful git commands:

`git status`: shows you what branch you are on and if there are any file changes that have yet to be staged or committed; also tells you if there are commits that haven't been pushed yet

`git add fname`: adds the file fname to the staging area

`git commit -m 'message'`: commits all files in the staging area to the current working branch and attaches the message to the commit

`git push`: pushes the commits to your GitHub repository


### A workflow that creates a new branch

`git checkout -b branch-name` : checks out a new branch named "branch-name"; if you create a new branch, it's usually a good idea to start from the main branch.

`git add fname1 fname2` : adds two updated files to the staging area

`git commit -m 'updated two files to do XX and YY' : commits the staged files

`git push` : pushes the commits to the GitHub; if you don't have commits on that branch on your github yet, there will be a response from git that says you need to specify which branch to push to. It will give you a line to copy and paste -- copy and paste that line :-) It should look like: `git push --set-upstream origin branch-name`


### A workflow that updates your local and origin repository to incorporate changes from the upstream repo

First, you should make sure you have an "upstream" repository set. For this repo in the CMU-COSMIC organization, you can create an upstream by typing:

`git remote add upstream git@github.com:CMU-COSMIC/learning-the-ropes-together.git`

Then we can fetch the changes:

`git fetch upstream`

then merge them into our local repo main branch:

`git merge upstream/main main`

and push to the origin repo:

`git push` 
