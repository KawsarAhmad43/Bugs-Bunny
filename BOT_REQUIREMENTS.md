# Coding Bot Requirements

## Overview

Build an autonomous coding bot that can identify and fix bugs in this Django/React todo application. The bot should demonstrate capabilities similar to what would be needed for the Exodus CRM project.

## Core Requirements

### 1. Multi-File Context Understanding
- Navigate between Django and React code
- Understand API contracts and data flow
- Track state management across components
- Follow import chains and dependencies

### 2. Bug Detection Capabilities
- Static code analysis to identify issues
- Pattern recognition for common antipatterns  
- Understanding of framework-specific best practices
- Ability to trace symptoms to root causes

### 3. Fix Generation
- Generate minimal, targeted fixes
- Maintain existing code style and patterns
- Preserve functionality while fixing issues
- Create atomic, well-scoped changes

### 4. Git Integration
- Analyze commit history
- Create meaningful commit messages
- Optional: Use git bisect to find regression points
- Understand diff context

### 5. Testing Awareness
- Run existing tests to verify bugs
- Ensure fixes don't break tests
- Optional: Generate tests for bug fixes
- Understand test frameworks (pytest, Jest)

## Technical Requirements

### Language Support
- Python (Django, Django REST Framework)
- TypeScript/JavaScript (React)
- Understanding of API patterns
- Session-based authentication

### Framework Knowledge
- Django models, views, serializers
- React hooks, state management
- Material-UI components
- REST API conventions

### Development Practices
- CSRF protection
- User permission isolation
- State synchronization
- Error handling

## Deliverables

### 1. Bot Implementation
- Source code for the bot
- Installation/setup instructions
- Configuration options
- Dependencies list

### 2. Demo Execution
- Video or log showing bot fixing all 5 bugs
- Step-by-step process documentation
- Time taken for each fix
- Any manual interventions required

### 3. Technical Documentation
- Architecture overview
- Decision-making process
- Limitations and assumptions
- Future improvement suggestions

### 4. Bug Fix Report
For each bug:
- How the bot identified it
- Root cause analysis
- Fix applied
- Verification method

## Evaluation Criteria

### Accuracy (40%)
- All bugs correctly identified
- Fixes resolve the issues
- No new bugs introduced
- Edge cases handled

### Code Quality (30%)  
- Clean, minimal fixes
- Follows project conventions
- Good commit hygiene
- Maintainable solutions

### Context Handling (20%)
- Cross-file understanding
- Full-stack awareness  
- Framework best practices
- API contract comprehension

### Communication (10%)
- Clear explanations
- Good documentation
- Helpful error messages
- Progress indicators

## Bonus Features

### Advanced Capabilities
- Suggest architectural improvements
- Add missing TypeScript types
- Improve error handling
- Add loading states
- Generate unit tests
- Performance optimizations

### Exodus-Specific Features
- Multi-tenant awareness
- Event-driven architecture understanding
- Complex state management
- Permission system comprehension

## Constraints

- Bot should work autonomously (minimal human intervention)
- Fixes should be reversible
- Must not break existing functionality
- Should complete within reasonable time (< 30 minutes)

## Success Metrics

A successful bot will:
1. Find and fix all 5 planted bugs
2. Explain its reasoning clearly
3. Generate production-ready fixes
4. Demonstrate understanding of full-stack relationships
5. Show potential for handling real-world Exodus CRM issues
