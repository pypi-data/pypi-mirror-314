(contributions)=

# How to contribute

Any development work takes place performing pull requests against the current `develop` branch.

## Prerequisites

1. Make sure you have an account on GitHub and that you have your public SSH key uploaded.

2. One of two things, either you need to clone the repository, or you need to make sure you
   have the recent changes in place.

   1. You have the [AiiDA-VASP] repository present in your local computer.
      Clone the upstream [AiiDA-VASP] repository by running:

      ```
      $ git clone git@github.com:aiida-vasp/aiida-vasp.git
      ```

   2. You already have the [AiiDA-VASP] repository present on your local computer.
      Check if you already have some changes. From the root folder of the repository run:

      ```
      $ git status
      ```

      If you have no changes, good, continue. If you have, try to remember what you have done
      and if it is worth saving. Issue for instance:

      ```
      $ git stash
      ```

      to store what you had changed. These can later be retrieved as long as you do not delete
      the repository and clone it again. Now, make sure you are on the `develop` branch, i.e.:

      ```
      $ git checkout develop
      ```

      Make sure you have the recent `develop` branch by running i.e.:

      ```
      $ git pull origin develop
      ```

      if the upstream [AiiDA-VASP] repository is stored as `origin` in your `git` setup.

3. Typically this upstream repository will be a `remote` called `origin`. Double check
   what it is called with `git remote -v`. In the following, we assume this is called
   `origin`.

4. Make sure your AiiDA-VASP Python virtual environment is enabled, consult [installation](#installation).

5. Make sure you are ready for development work on the plugin, meaning, you need to make
   sure you have installed everything you need. Make sure you have installed the plugin in
   edit mode and that you have enabled the extra `tests`, `docs` and `pre-commit` options when installing.
   Execute from the root folder of the clones source code for [AiiDA-VASP]:

   ```
   $ cd aiida-vasp
   $ pip install -e .[tests,pre-commit,docs]
   ```

6. Make sure `pre-commit` is enabled by running:

   ```
   $ pre-commit install
   ```

## Workflow for contributions

You should try to follow this workflow when submitting a contribution:

0. Open an [issue] describing as best you can the issue and how to fix it (if you know or have
   some suggestion).
1. Create a new branch for your suggested changes. Use a short, descriptive name (here, we
   use the example `my_changes`), i.e. `git checkout -b my_changes`
2. Edit/add files.
3. If you added new files, or renamed, make sure to add them back in (here, example
   file `new_documentation.rst`) with i.e. `git add new_documentation.rst`
4. Verify that you have not forgotten any files and that the changes are as expected
   with `git status` and `git diff`.
5. Commit the changes: `git commit -am 'My new additions'`. Make sure to give a proper and descriptive
   commit message. Sometimes it is better not to give the `-m` option and only do `git commit -a 'My new additions'`
   which will bring up your standard editor. There, in the first line you give a header which is the title of the
   commit. Following is a blank line and then a more extensive description of what is done. Notice that
   when you issue the commit, `pre-commit` will run different checks, in particular for linting. Most
   likely this will not pass. Please adjust and issue the commit command again until it passes. The same check
   is done after the code have been pushed.
6. Upload your changes to the main repository: `git push origin my_changes`
7. Create a new [pull request].
   Select your `my_changes` branch as the `compare` branch and `develop` as the `base` branch.
   Please [test the changes locally using pytest](#running-tests).
8. Describe the changes and optionally assign someone to review and approve the commits.

[aiida-vasp]: https://github.com/aiida-vasp/aiida-vasp
[issue]: https://github.com/aiida-vasp/aiida-vasp/issues
[pull request]: https://github.com/aiida-vasp/aiida-vasp/pulls
[tox]: https://tox.wiki/en/latest/
[vasp]: https://www.vasp.at
