# Easy-Git CLI Tool

**Easy-Git** is a command-line tool designed to simplify and streamline common Git workflows, making it easier and faster to interact with Git repositories. This tool is particularly useful for developers who want to automate repetitive tasks like staging files, committing changes, and pushing to remote repositories.

Currently, **Easy-Git** includes the following features:
- **Quick Commit**: A streamlined process for staging, committing, and pushing changes to the repository.
- **Shortcuts for Commands**: You can use both `quick-commit` and `c` to trigger the same functionality.
- More features coming soon!

> **Note**: This project is a work in progress and will be extended with more tools and functionalities over time. Stay tuned for more features!


## 🚀 Installation

### Prerequisites
Ensure that you have **Python** installed.

### Install the Tool

The tool is available on PyPI, so you can install it using `pip`:

```bash
pip install easy-git
```
Or `poetry`:

```bash
poetry add easy-git
```

## ⚙️ Usage

Once installed, you can use the tool directly from the command line.

### Available Commands

- **`quick-commit`**: Perform the add-commit-push cycle.
- **`c`**: Alias for the `quick-commit` command.

### Example Usage

1. **Stage and commit files**:

   ```bash
   easy-git quick-commit
   ```

   Or use the shortcut:

   ```bash
   easy-git c
   ```


## 🚧 Work in Progress

This project is still in progress, and new features will be added over time. Current functionalities include the `quick-commit` cycle, but more tools and features will be added in the future.

Stay tuned for updates!


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
