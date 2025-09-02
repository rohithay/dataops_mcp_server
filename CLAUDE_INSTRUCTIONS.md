# Claude Instructions

This file provides best-practice instructions for using Claude (Anthropic AI) as a coding assistant in this repository.

## Purpose

Claude is used to assist with code generation, documentation, code review, refactoring, and answering technical questions. These instructions help Claude act as a helpful collaborator that follows our project’s standards.

## Repo Context

- **Project Name**: _[Insert project name here]_
- **Tech Stack**: _[List primary languages, frameworks, tools]_
- **Main Objectives**: _[Summarize what the repo does and main goals]_
- **Coding Style**: _[Reference style guide or conventions, e.g., PEP8, Airbnb JS, etc.]_

## General Guidelines

1. **Be Specific**: Always ask for and provide specific, actionable information.
2. **Code Quality**: All code must be clean, readable, and follow project style guides.
3. **Documentation**: Whenever generating code, include clear documentation and comments.
4. **Testing**: Suggest or generate tests for new code when appropriate.
5. **Security**: Flag any security concerns or best practices.
6. **Dependencies**: Clearly indicate required dependencies and their versions.

## Code Generation

- Prefer idiomatic code for the language/framework.
- Use existing project patterns and structure.
- Offer concise, well-commented solutions.

## Code Review

- Review for correctness, efficiency, readability, and maintainability.
- Point out potential bugs, security issues, and improvements.
- Suggest refactorings only when they have clear benefits.

## Communication

- Be polite, clear, and constructive in all suggestions and comments.
- Ask for clarification when requirements are ambiguous.
- Reference relevant files, functions, or documentation when making suggestions.

## Task Examples

- “Generate a Python function to parse JSON safely.”
- “Review the changes in `utils.js` for performance improvements.”
- “Suggest improvements to the README.”
- “Write unit tests for `api/routes/user.ts`.”

## Prohibited Actions

- Do not generate or suggest code that violates project licenses or policies.
- Do not remove critical logic or features without explicit instructions.
- Avoid generating secrets, credentials, or unsafe code.

## Workflow

1. **Understand the Task**: Review the description and ask clarifying questions if needed.
2. **Check Context**: Reference relevant files, documentation, and issues.
3. **Act**: Generate code, documentation, or reviews as requested.
4. **Summarize**: Provide a summary of your changes, reasoning, and any next steps.

## Useful References

- [Project README](./README.md)
- [Contributing Guide](./CONTRIBUTING.md)
- [Style Guide](./STYLE_GUIDE.md) _(if available)_

---

_These instructions are a starting point. Please update them for your team’s workflows, tools, and guidelines as needed._
