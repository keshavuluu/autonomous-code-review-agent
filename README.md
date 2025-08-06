# Autonomous Code Review Agent 🤖

An intelligent, autonomous system that automatically reviews pull requests on GitHub, analyzing code against standard coding practices and providing feedback directly as comments within the GitHub interface.

## Features ✨

- **Autonomous Operation**: Runs automatically on every PR creation/update
- **Multi-AI Support**: Uses OpenAI GPT, Anthropic Claude, or Google Gemini
- **Traditional Linting**: Integrates ESLint, Pylint, Black, and other linters
- **GitHub Integration**: Posts comments directly to PRs via GitHub API
- **Multi-Language Support**: Python, JavaScript, TypeScript, and more
- **Cost-Effective**: Uses free tiers and affordable AI APIs

## How It Works 🔄

1. **Trigger**: GitHub Actions workflow triggers on PR events
2. **Analysis**: Code is analyzed using both traditional linters and AI models
3. **Feedback**: Results are posted as comments directly on the PR
4. **Summary**: A comprehensive review summary is provided

## Setup Instructions 🚀

### 1. Repository Setup

Copy the following files to your repository:

- `.github/workflows/code-review-agent.yml`
- `.github/scripts/code_review_agent.py`

### 2. GitHub Secrets Configuration

Add these secrets to your repository (Settings → Secrets and variables → Actions):

```
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key (optional)
```

**Note**: You only need one AI provider. The system will use whichever API key is available.

### 3. API Key Setup

#### OpenAI (Recommended for beginners)
1. Sign up at [OpenAI](https://platform.openai.com/)
2. Get $5 free credit for new users
3. Create an API key
4. Add to GitHub secrets as `OPENAI_API_KEY`

#### Anthropic Claude
1. Sign up at [Anthropic](https://console.anthropic.com/)
2. Get free tier with generous limits
3. Create an API key
4. Add to GitHub secrets as `ANTHROPIC_API_KEY`

#### Google Gemini (Optional)
1. Sign up at [Google AI Studio](https://makersuite.google.com/)
2. Get free tier
3. Create an API key
4. Add to GitHub secrets as `GOOGLE_API_KEY`

### 4. Permissions

The workflow automatically requests necessary permissions:
- `contents: read` - to read repository files
- `pull-requests: write` - to post comments
- `actions: read` - to access workflow context

## Usage 📝

Once set up, the agent will automatically:

1. **Trigger** on every PR creation, update, or reopen
2. **Analyze** all changed files using:
   - Traditional linters (ESLint, Pylint, Black, etc.)
   - AI code analysis (OpenAI/Claude/Gemini)
3. **Post Comments** directly on the PR with:
   - File-specific feedback
   - Line-by-line suggestions
   - Overall review summary

## Example Output 📋

### File-Specific Comment
```
## Code Review for src/main.py

**pylint**: Line 15: Variable 'x' is not used
**AI Review (OpenAI)**: Consider adding type hints to improve code readability and catch potential type-related bugs early in development.
```

### Summary Comment
```
## Code Review Summary

Found 5 issues across 3 files.

### Key Findings:
- Linter issues: 3
- AI analysis issues: 2

Please review the detailed comments above and address the identified issues.
```

## Supported Languages 🌐

- **Python**: Pylint, Flake8, Black, isort, MyPy
- **JavaScript/TypeScript**: ESLint, Prettier
- **Other**: Basic AI analysis for any text file

## Cost Analysis 💰

### Free Options (Recommended)
- **GitHub Actions**: 2,000 free minutes/month (private repos)
- **OpenAI**: $5 free credit for new users
- **Anthropic**: Generous free tier
- **Traditional Linters**: Completely free

### Estimated Monthly Costs
- **Small Project** (10 PRs/month): $0-5
- **Medium Project** (50 PRs/month): $5-15
- **Large Project** (200 PRs/month): $15-50

## Customization ⚙️

### Adding New Linters

Edit `.github/scripts/code_review_agent.py` and add to the `run_linters` method:

```python
elif file_path.endswith('.java'):
    linters = [
        ('checkstyle', ['checkstyle', file_path]),
        ('spotbugs', ['spotbugs', file_path])
    ]
```

### Customizing AI Prompts

Modify the `analyze_code_with_ai` method to change what the AI looks for:

```python
context = f"""
Please review this code for:
1. Security vulnerabilities
2. Performance bottlenecks
3. Code maintainability
4. Documentation quality
5. Test coverage suggestions
"""
```

### Language-Specific Rules

Add custom rules for different programming languages or frameworks:

```python
if 'react' in file_path.lower():
    context += "\n\nPay special attention to React best practices and hooks usage."
```

## Troubleshooting 🔧

### Common Issues

1. **"No API key found"**
   - Ensure you've added at least one AI API key to GitHub secrets
   - Check that the secret names match exactly

2. **"Permission denied"**
   - Verify the workflow has the correct permissions
   - Check that the GitHub token has PR write access

3. **"Linter not found"**
   - The system gracefully handles missing linters
   - Install linters in your repository if needed

4. **"Timeout errors"**
   - Large files may timeout
   - Consider splitting large files or increasing timeout limits

### Debug Mode

To debug issues, you can manually trigger the workflow:
1. Go to Actions tab in your repository
2. Select "Code Review Agent" workflow
3. Click "Run workflow"

## Security Considerations 🔒

- API keys are stored securely in GitHub secrets
- The agent only reads files in the PR
- Comments are posted with your repository's permissions
- No code is sent to external services unless you configure AI APIs

## Contributing 🤝

Feel free to submit issues and enhancement requests!

## License 📄

MIT License - feel free to use and modify as needed.

---

**Happy coding! 🎉**

This autonomous code review agent will help maintain code quality and catch issues early in your development process. 