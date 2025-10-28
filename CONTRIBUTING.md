# Contributing Guidelines

## Team Workflow

### Branching Strategy
- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/[name]` - Individual feature branches
- `hotfix/[name]` - Urgent fixes

### Commit Messages
Use clear, descriptive commit messages:
```
[TYPE] Brief description

Detailed explanation if needed

TYPE can be:
- FEAT: New feature
- FIX: Bug fix
- DOCS: Documentation changes
- REFACTOR: Code refactoring
- TEST: Adding tests
- STYLE: Code style changes
```

Example:
```
FEAT: Add moving average crossover strategy

Implemented SMA crossover strategy with configurable periods.
Includes backtesting results and parameter optimization.
```

### Code Review Process
1. Create feature branch
2. Implement changes
3. Test thoroughly
4. Create pull request
5. Team review
6. Merge to develop

### Documentation
- Update relevant .md files when adding features
- Document all strategy parameters
- Keep architecture diagrams updated
- Add inline comments for complex logic

## Development Standards

### Code Style
- Follow PEP 8 (Python)
- Use meaningful variable names
- Keep functions small and focused
- Write docstrings for all functions/classes

### Testing
- Write unit tests for new features
- Backtest strategies before deployment
- Paper trade before live trading
- Document test results

### Version Control
- Commit frequently with clear messages
- Don't commit sensitive data (API keys, credentials)
- Keep commits atomic (one logical change per commit)
- Pull latest changes before starting work

## Communication

### Daily Sync
- Quick status update
- Blockers or issues
- Plan for the day

### Decision Log
Document major decisions in the relevant .md files with:
- Date
- Decision made
- Rationale
- Participants

## Questions?
Discuss any uncertainties before implementing to ensure alignment.

