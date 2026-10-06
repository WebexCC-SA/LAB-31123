```mermaid
flowchart LR
    H[Human] <--> A[AI Agent]
    A <--> C[MCP Client]

    L[LLM] <--> A

    C <--> T[Tools]
    C <--> R[Resources]
    C <--> P[Prompts]
```
