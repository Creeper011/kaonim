# kaonim (discord bot)

kaonim is a alternative version of kaoruko bot but with some nim codes and a simplifiqued architecture. (the choice for a simplified architecture is to make it easier to maintain for me who is the only developer)

kaonim have some different features from kaoruko just be cause its an small bot and i have more possibility to add experimental features.
## the features are:
- music player
- jokes command
- image generation command (not ai)
- termo
- i18n

## Installation
wip

## Architecture
kaonim follows a simplified version of clean architecture and kaoruko architecture.
you can check the architecture on the docs folder. docs/architecture.md

## some differences with kaoruko:
- kaonim haves fun commands like jokes and termo and music player
- kaonim doesn't have a separated layer for composition root
- kaonim doesn't follow strictly the clean architecture
- kaonim doesn't follow strictly single responsibility principle (because adding more classes for each responsibility will make the project more complex to maintain for me)
- kaonim uses nim for some parts of the code (native layer) to improve performance and for me learn nim language
- kaonim doesn't have a elaborated config system like kaoruko with parsers, mappers, loaders, factories, etc.. (it's an simplified version of it)