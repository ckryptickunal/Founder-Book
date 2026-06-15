---
type: source
title: Catch bugs locally faster with the last code linter you'll ever need (Trunk.io with Eli Schleifer)
created: 2026-05-27
updated: 2026-05-27
video_id: EdMJxU-0SPE
url: https://www.youtube.com/watch?v=EdMJxU-0SPE
channel: Garry Tan
published: 2021-11-30T15:30:03Z
tags:
  - software-engineering
  - devops
  - linting
  - static-analysis
  - trunk-io
  - developer-tools
  - coding-best-practices
---

# Catch bugs locally faster with the last code linter you'll ever need (Trunk.io with Eli Schleifer)

## Metadata

- Video ID: `EdMJxU-0SPE`
- Channel: Garry Tan
- Published: 2021-11-30T15:30:03Z
- URL: https://www.youtube.com/watch?v=EdMJxU-0SPE

## Summary

Garry Tan interviews Eli Schleifer regarding the launch of Trunk.io, a developer experience tool designed to centralize and automate the management of linters, static analyzers, and formatters across diverse codebases.

## Key Ideas

- Modern repositories contain a mix of technologies (Python, Rust, Docker, Terraform, etc.), each requiring its own set of linters and formatters.
- Manual maintenance of these tools leads to inconsistency and neglect within development teams.
- Trunk Check acts as a 'meta-linter' that manages, versions, and executes all necessary tools locally.
- Moving linting from CI/CD pipelines to local development environments provides immediate feedback, saving time and cloud compute costs.
- Configuration as code via a trunk.yaml file ensures all team members use identical tool versions.
- Automated version management helps prevent security vulnerabilities caused by outdated static analysis tools.

## Entities

- [[entities/eli-schleifer|Eli Schleifer]] (person): Co-founder of Trunk.io and former Microsoft engineer.
- [[entities/garry-tan|Garry Tan]] (person): Host of the channel and former colleague of Eli Schleifer.
- [[entities/trunk-io|Trunk.io]] (company): A developer experience platform focusing on code quality and automation.
- [[entities/trunk-check|Trunk Check]] (product): A meta-linter tool that manages and runs various static analysis tools.
- [[entities/yaml-cpp|yaml-cpp]] (project): An open-source C++ YAML parser library.

## Topics

- [[topics/developer-experience-devex|Developer Experience (DevEx)]]: The focus on improving the tools and workflows used by software engineers to increase productivity.
- [[topics/static-analysis|Static Analysis]]: The process of analyzing code without executing it to find bugs, security issues, and formatting inconsistencies.
- [[topics/ci-cd-optimization|CI/CD Optimization]]: Reducing the burden on continuous integration pipelines by shifting non-essential tasks to local development environments.

## Notable Claims

- Waiting for CI to report linting errors is inefficient and expensive. Evidence: Comparing it to waiting 10 minutes for a spell-check in a word processor; it wastes developer time and cloud compute resources.
- Trunk can identify high-severity security bugs in existing projects that have been missed by previous manual linting efforts. Evidence: Eli Schleifer cites a recent case where Trunk identified two high-severity security issues in a popular open-source Go project that had not been properly linted in two years.

## Quotes

> We are like devex in a box.
> You wouldn't tolerate that from Google Docs to wait 10 minutes to tell you you misspelled something; you shouldn't wait 10 minutes for your linter to tell you you have a linting problem.
> If it's someone maintaining it, that means they're forgetting to maintain it.
