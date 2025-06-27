# Eeredivisie Fantasy Football - Agentic Way

### Name

The name of this system from now on in the document will be **Poly**.

### Goal
1. Every week produce a team of 15 players.
2. Team should be complete(4-3-3) with a goalkeeper.

### Requirements
1. Onboarding portal registers new users and provides user management.
2. New users needs to be onboarded/registered.
3. User should select a package/subscription.
4. Package/Subscrption defines which tools, APIs, rate-limit applies to an user.
5. Should be accessible via MCP-client(s).


### User registration flow

```mermaid

 sequenceDiagram
    User->>Onboard Portal: registration request
    Onboard Portal->>User: registration options
    User->>Onboard Portal: Choose options
    Onboard Portal->>Onboard Service: user details + registration choice
    Onboard Service->>IDP: create user + assign role
    IDP-->>Onboard Service: return
    Onboard Service-->>Onboard Portal: return
    Onboard Portal-->>User: return 

```

Subscription models would look like >>
![subscription models in Poly](./code/frontend/public/subscriptions.png)


### MCP client interaction flow

```mermaid

sequenceDiagram
    participant MCP_Client as MCP Client
    box Azure AWS/Azure/GCP
        participant APIM
        participant Init-Agent as Init Agent
        participant Sub_Agents as Sub Agents
        participant IDP
    end

    MCP_Client->>APIM: request
    APIM->>IDP: login + authenticate
    IDP-->>MCP_Client: oauth token
    MCP_Client->>APIM: send query
    APIM->>Init-Agent: invoke agent
    Init-Agent->>Sub_Agents: delegate query
    Sub_Agents-->>Init-Agent: return results
    Init-Agent-->>MCP_Client: return results 

```



### Internal Agent interaction flow

![data and control flow inside Poly](./architecture/agent-interaction.png)


### External info need/design choices

![external info and design choices](./architecture/external_info.png)


## Open Items

1. Cloud Infra design
2. Terraform or Bicep scripts for model deployments
3. Initial Agentic flow implementation
4. Terraform or Bicep scripts for APIM, ACA, VNet
5. Evaluation flow for models
6. Github workflow(s)