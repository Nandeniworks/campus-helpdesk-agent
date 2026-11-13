# Part F: Architectural Reflection

Each architectural component in the modern AI-agent toolchain addresses a fundamentally distinct layer of the problem space:

* **Skills** solve the problem of **procedural guidance and domain methodology**. They teach an agent *how* to approach specialized tasks through instructions and progressive disclosure without bloating baseline context.
* **Plugins** solve the problem of **distribution, lifecycle management, and policy enforcement**. They bundle skills, custom commands, hooks, and configs into a single installable unit governed by security boundaries.
* **MCP (Model Context Protocol)** solves the problem of **dynamic data connectivity and real-time execution**. It provides a standardized client-server protocol over stdio/SSE, giving agents access to live external databases and enterprise resources without hardcoded integrations.
* **Git Worktrees** solve the problem of **isolated, parallel developer collaboration**. They allow multiple concurrent development branches to share a single repository object database without filesystem collisions or switching overhead.

### When to Choose a Skill over an MCP Tool
I would choose an **Agent Skill** over an MCP tool when the objective is to teach the agent **reasoning strategies, runbooks, anti-hallucination policies, or multi-step analysis workflows** that operate on files already accessible in the repository. Skills excel at explaining *how* to think and format responses. Conversely, an **MCP tool** is essential when the agent requires real-time access to live data stored behind an authenticated API, transactional mutation capabilities (such as updating a student ledger), or when exposing capabilities across multiple agent platforms. A Skill defines policy; an MCP tool executes remote capabilities.

### What Would Never Be Delegated to an Agent Without Review
I would never delegate **destructive schema migrations, access control policy changes, production deployment pipelines, or autonomous merge conflict resolution** without human review. While agents can accurately generate resolutions, they lack situational awareness regarding business consequences. An automated merge can produce syntactically valid code that silently breaks security invariants. Human oversight remains mandatory for state mutations that are irreversible or security-critical.
