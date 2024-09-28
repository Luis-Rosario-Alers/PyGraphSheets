# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.
Please note we have a [code of conduct](CODE_OF_CONDUCT.md), please follow it in all your interactions with the project.


## Development Environment Setup
1. **Clone the repository**:
   ```sh
   git clone https://github.com/Luis-Rosario-Alers/PyGraphSheets
   cd PyGraphSheets
2. **Create and activate a virtual environment**:
    ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
3. **Install the dependencies**:
    ```sh
   pip install -r requirements.txt
4. **Set up environment variables**:
    Create a `.env` file in the root directory and add the necessary environment variables:
    ```sh
   FILE_PATH=path/to/your/credentials.json
   SHEET_ID=your_google_sheet_id
5. **Run the application**:
    ```sh
   python PyGraphSheets/main.py
## Issues and feature requests

You've found a bug in the source code, a mistake in the documentation or maybe you'd like a new feature?Take a look at [GitHub Discussions](https://github.com/Luis-Rosario-Alers/PyGraphSheets/discussions) to see if it's already being discussed.  You can help us by [submitting an issue on GitHub](https://github.com/Luis-Rosario-Alers/PyGraphSheets/issues). Before you create an issue, make sure to search the issue archive -- your issue may have already been addressed!

Please try to create bug reports that are:

- _Reproducible._ Include steps to reproduce the problem.
- _Specific._ Include as much detail as possible: which version, what environment, etc.
- _Unique._ Do not duplicate existing opened issues.
- _Scoped to a Single Bug._ One bug per report.

**Even better: Submit a pull request with a fix or new feature!**

### How to submit a Pull Request

1. Search our repository for open or closed
   [Pull Requests](https://github.com/Luis-Rosario-Alers/PyGraphSheets/pulls)
   that relate to your submission. You don't want to duplicate effort.
2. Fork the project
3. Create your feature branch (`git checkout -b feat/amazing_feature`)
4. Commit your changes (`git commit -m 'feat: add amazing_feature'`) PyGraphSheets uses [conventional commits](https://www.conventionalcommits.org), so please follow the specification in your commit messages.
5. Push to the branch (`git push origin feat/amazing_feature`)
6. [Open a Pull Request](https://github.com/Luis-Rosario-Alers/PyGraphSheets/compare?expand=1)
