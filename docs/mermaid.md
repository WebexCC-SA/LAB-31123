```mermaid
block-beta
    columns 7

    space space L["LLM"] space space space T["Tools"]
    H["Human"] space A["AI Agent"] space C["MCP Client"] space R["Resources"]
    space space space space space space P["Prompts"]

    H <--> A
    L <--> A
    A <--> C
    C <--> T
    C <--> R
    C <--> P
```
