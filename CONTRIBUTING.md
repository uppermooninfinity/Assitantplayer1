# Contributing to Telegram Music Bot

Thank you for considering contributing to Telegram Music Bot! We welcome contributions from everyone.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Detailed steps to reproduce the bug
- Expected behavior vs actual behavior
- Your environment (OS, Python version, etc.)
- Any relevant logs or screenshots

### Suggesting Features

Feature suggestions are welcome! Please create an issue with:
- A clear, descriptive title
- Detailed description of the feature
- Why this feature would be useful
- Any implementation ideas you might have

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature-name`)
7. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused
- Write docstrings for classes and functions

### Testing

- Test your changes before submitting a PR
- Ensure the bot starts without errors
- Test all affected commands
- Verify voice chat functionality works

### Commit Messages

- Use clear and meaningful commit messages
- Start with a verb in present tense (Add, Fix, Update, etc.)
- Keep the first line under 50 characters
- Add detailed description if needed

Example:
```
Add Spotify playlist support

- Implement playlist parsing
- Add queue management
- Update documentation
```

## Development Setup

1. Clone your fork:
```bash
git clone https://github.com/yourusername/telegram-music-bot.git
cd telegram-music-bot
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your `.env` file with test credentials

5. Run the bot:
```bash
python bot.py
```

## Areas for Contribution

- Bug fixes
- New music platform support (Apple Music, Deezer, etc.)
- UI/UX improvements
- Documentation improvements
- Performance optimizations
- Test coverage
- Localization/translations

## Questions?

Feel free to create an issue with the `question` label if you have any questions about contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

Thank you for contributing!
