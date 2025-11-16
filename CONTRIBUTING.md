# Contributing to GNN-TEC-Network

Thank you for your interest in contributing to GNN-TEC-Network! This document provides guidelines for contributing to the project.

## 🎯 Ways to Contribute

### 1. Report Bugs
- Use GitHub Issues to report bugs
- Include detailed description and steps to reproduce
- Provide system information (OS, Python version, dependencies)

### 2. Suggest Enhancements
- Open an issue with the "enhancement" label
- Clearly describe the proposed feature
- Explain why it would be useful

### 3. Submit Pull Requests
- Fork the repository
- Create a feature branch
- Make your changes
- Submit a pull request

### 4. Improve Documentation
- Fix typos or clarify explanations
- Add examples or tutorials
- Improve code comments

### 5. Share Results
- Apply the method to new datasets
- Share interesting findings
- Contribute analysis notebooks

## 🔧 Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/GNN-TEC-Network.git
cd GNN-TEC-Network

# Create development environment
conda create -n gnn-tec-dev python=3.8
conda activate gnn-tec-dev

# Install in development mode
pip install -e .
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

## 📝 Code Style

### Python Code
- Follow PEP 8 style guide
- Use Black for code formatting: `black .`
- Use flake8 for linting: `flake8 .`
- Add type hints where appropriate

### Documentation
- Use clear, concise language
- Include code examples
- Add docstrings to all functions

### Example Function

```python
def compute_similarity(embeddings: np.ndarray, metric: str = 'cosine') -> np.ndarray:
    """
    Compute pairwise similarity between node embeddings.
    
    Args:
        embeddings: Node embeddings array of shape (n_nodes, embedding_dim)
        metric: Similarity metric ('cosine', 'euclidean', 'manhattan')
    
    Returns:
        Similarity matrix of shape (n_nodes, n_nodes)
    
    Example:
        >>> embeddings = model.get_embeddings()
        >>> similarity = compute_similarity(embeddings, metric='cosine')
    """
    # Implementation
    pass
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_gnn_model.py

# Run with coverage
pytest --cov=gnn_tec_network
```

### Write Tests
- Add tests for new features
- Ensure existing tests pass
- Aim for >80% code coverage

## 📋 Pull Request Process

### 1. Before Submitting
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Commit messages are clear

### 2. Commit Messages
Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```
feat(gnn): add multi-head attention mechanism
fix(data): correct edge index computation
docs(readme): update installation instructions
```

### 3. Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## 🌟 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Acknowledged in release notes
- Credited in publications (for significant contributions)

## 📧 Questions?

- Open a discussion on GitHub
- Email: your.email@institution.edu

Thank you for contributing! 🎉
