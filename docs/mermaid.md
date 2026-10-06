```mermaid
block-beta
    columns 5

    space L["LLM"] space space space

    H["Human"]
    block:host:2
        columns 3
        A["AI Agent"] space C["MCP Client"]
        space HL["MCP Host"] space
    end
    block:server:2
        columns 1
        T["Tools"]
        R["Resources"]
        P["Prompts"]
        SL["MCP Server"]
    end

    H <--> A
    L <--> A
    A <--> C
    C <--> server

    style host fill:#ffffff,stroke:#333333,stroke-width:2px
    style server fill:#ffffff,stroke:#333333,stroke-width:2px
    style HL fill:none,stroke:none,color:#1496d4
    style SL fill:none,stroke:none,color:#159947
```
