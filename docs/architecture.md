# Architecture

## the layers are:
- Infrastructure layer
- Domain Layer
- Usecases Layer (similar to application layer)
- Interfaces Layer (equals to presentation layer from kaoruko)
- Native Layer (nim code) [not connect to other layers]

## Infrastructure Layer
the infrastructure layer is responsible for:
- config loading
- discord connection

## Domain Layer
the domain layer is responsible for:
- entities
- pure models (business models without any dependency with other layers)

## Usecases Layer (optional layer)
the usecases layer is responsible for:
- business rules implementation
- orchestrating the flow of data to and from the entities
note: ONLY commands how needs an complex logic will be used here. commands like get and random joke will be receive the service and the cog will orchestrate this

## Interfaces Layer
the interfaces layer is responsible for:
- commands implementation
- event listeners implementation
- interaction with discord api
- i18n abstraction for commands

all layers should use dependency inversion principle to depend on abstractions instead of concretions.
note: sometimes this principle is not followed strictly for simplification purposes.