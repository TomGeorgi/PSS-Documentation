# PSS-Documentation Template
## How to set up your CI

If you want to use [Travis-CI](https://travis-ci.org/) as your Continuous Integration please follow this few steps:

1. Visit [Travis-CI](https://travis-ci.org/) and Sign In with youru GitHub Account
2. Go to your Profile settings ![](https://github.com/TomGeorgi/PSS-Documentation/blob/template/graphics/readme_graphics/github_settings.png)
3. Enable Travis for your forked repository ![](https://github.com/TomGeorgi/PSS-Documentation/blob/template/graphics/readme_graphics/enable_travis.png)
4. Go to your [GitHub Token Settings](https://github.com/settings/tokens) and generate a new token which includes the same access rights like the example picture below and copy this token. ![](https://github.com/TomGeorgi/PSS-Documentation/blob/template/graphics/readme_graphics/token_settings.png)
5. Visit [Travis-CI](https://travis-ci.org/) again and go to your activate repository
6.  Click on the repository settings ![](https://github.com/TomGeorgi/PSS-Documentation/blob/template/graphics/readme_graphics/travis_repo_settings.png).
7. Generate a new Environment Variable named **GH_TOKEN** and insert your token as value.
8. That's all.

## Create a Release
```bash
git add files/ you want/ to/commit
git commit -m "Message"
git tag tag-name
git push -u origin master --tags
```




