# 15-Minute Sprints: Learning Systems by Building Them

A public log of how I'm learning to think like an engineer: building real systems by hand, one small feature at a time, with no copy-pasted solutions.

## Why

LeetCode taught me how to make data structure and algorithm decisions. It didn't teach me how to decide how a _whole system_ should be built: how the pieces talk to each other, where state lives, what breaks under load.

AI coding tools can write most of this code for me. My goal is to understand what they're doing well enough to steer them, review their output, and know when they're wrong. The way to get there is to build the fundamentals myself first.

## The rules

1. **15-minute sprints.** Each sprint ships one small, working feature.
2. **One commit per sprint**, with a message that says what changed and why.
3. **No copy-pasted solutions.** Reading docs, specs, and API examples is fine. Copying someone's finished code or asking an AI to write the logic is not.
4. **AI as a reviewer, not an author.** I can ask conceptual questions or for a hint. After I finish a piece, I can paste it in for critique.
5. **Stuck rule.** If I'm stuck on the same thing for a full sprint, I ask for a hint: a nudge, not the answer.
6. **Primary sources first.** Docs, RFCs, and the library's source code before tutorials.
7. **Write down what I learned.** One sentence per sprint.

## Roadmap

| Phase | Project                                        | Why it matters                                    |
| ----- | ---------------------------------------------- | ------------------------------------------------- |
| 1     | [HTTP server from a raw socket](./http-server) | Sockets, ports, TCP vs HTTP, parsing, concurrency |
| 2     | Agent loop from scratch (no framework)         | What agent frameworks abstract away               |
| 3     | NAS agent (LangGraph + Postgres)               | Applying it all to a real project                 |

### Phase 2 backlog: agent loop

Python, raw model API, no framework.

- [ ] Send one message to the model and print the reply
- [ ] REPL loop that keeps conversation history
- [ ] Define one tool (`list_files(path)`) and detect when the model calls it
- [ ] Execute the tool and send the result back
- [ ] Loop until the model stops calling tools, with a max-iterations cap
- [ ] Add a second tool (`disk_usage`)
- [ ] Error handling: tool failures the model can recover from
- [ ] Log each step to a file
- [ ] Read-only mode: block any tool outside an allowlist
- [ ] Swap the hosted model for a local one behind a common interface

## Learning log

One line per sprint: what I learned, not just what I built.

- A socket is an OS object for network I/O, like a file handle; a port tells the OS which program incoming data belongs to.
- In HTTP the client always speaks first; a server that talks first breaks the protocol.
- HTTP headers can't start with whitespace, or clients treat them as a continuation of the previous line.
