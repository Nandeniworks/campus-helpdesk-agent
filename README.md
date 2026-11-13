# Campus Helpdesk Agent

A project for Assignment 8 – AI Tools and Prompt Engineering.

## Project Overview

This project focuses on building and auditing an AI-agent toolchain for a university campus helpdesk scenario.

It demonstrates the use of Agent Skills, plugins, the Model Context Protocol (MCP), and Git worktrees.

## Project Structure

```text
campus-helpdesk-agent/
├── campus-helpdesk/
│   ├── data/
│   │   └── mock/
│   ├── skills/
│   │   └── timetable-helper/
│   │       ├── references/
│   │       └── scripts/
│   ├── plugin/
│   │   └── campus-helpdesk/
│   │       ├── commands/
│   │       └── hooks/
│   └── mcp-server/
│       └── tests/
├── tests/
├── evidence/
│   ├── skill/
│   ├── plugin/
│   ├── mcp/
│   └── worktrees/
├── prompt-log/
├── README.md
└── .gitignore
```

## Main Components

- Agent Skills
- Campus Helpdesk Plugin
- Model Context Protocol (MCP) Server
- Git Worktrees

## Data and Security

This project uses mock campus data only. No real student information, passwords, or API keys are included.

## Evidence and Testing

Test results, screenshots, and implementation evidence will be maintained in the `evidence/` and `tests/` directories.

## Project Status

Repository structure established. Implementation: Part B skills verified and automated test suite active.