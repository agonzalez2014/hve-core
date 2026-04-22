---
description: "Opt-in canonical deck and customer-card workflow for DT coaching"
applyTo: "**/.copilot-tracking/dt/**"
---

# DT Canonical Deck Instructions

Use this workflow only when the team explicitly opts in to canonical deck support.

## Scope

Canonical deck workflow covers two related outputs:

1. Canonical markdown artifacts under `.copilot-tracking/dt/{project-slug}/canonical/`.
2. Optional customer-card PowerPoint output under `.copilot-tracking/dt/{project-slug}/render/`.

Treat canonical deck and PowerPoint generation as optional and skippable at each offer point.

## Single Source of Truth

Keep canonical-deck rules in this file only.

Do not duplicate transition gates or non-waivable checks in:

- Method instructions (for example Method 1 or sequencing)
- DT Coach agent behavior text
- Other prompt files

## Activation Rule

The coach must explicitly ask the user once per DT project whether to enable canonical deck and customer-card workflow.

Use a direct yes-or-no checkpoint prompt during Session Initialization, before any method-specific coaching begins:

> Would you like to enable the canonical deck and customer-card workflow for this DT project?

This checkpoint is required once per DT project and is not skippable by the coach. The user can still decline the workflow.

After that prompt, the canonical-deck workflow is active only when either condition is true:

1. The user asks for canonical deck or customer cards.
2. The user accepts a canonical deck offer in the active DT session.

If neither condition is true, continue normal DT coaching with no canonical-deck enforcement.

## Offer Points (Optional)

When workflow is active, offer canonical deck snapshot creation or refresh at these method exits:

1. End of Method 1
2. End of Method 2
3. End of Method 3
4. End of Method 5

Checkpoint phrasing expectation:

- Between Method 1 and Method 2, ask whether to create or update the canonical deck and customer card artifacts.
- Between Method 2 and Method 3, ask whether to create or update the canonical deck and customer card artifacts.
- At the end of Method 5, ask whether to create or update the canonical deck and customer card artifacts.

Each offer must be optional and skippable. Declining an offer must not block method transition.

## Mandatory Post-Snapshot Customer-Card Checkpoint

After any canonical deck create or refresh, the coach must ask this yes-or-no question in the same turn:

> Would you like to generate the customer-card PowerPoint now?

This checkpoint is required whenever canonical artifacts were created or updated at Method 1, Method 2, Method 3, or Method 5 offer points.

Do not end canonical snapshot workflow without asking this question.

Record the offer timestamp and user response in coaching state.

## Offer Language

Use concise coaching language. Example:

> We can snapshot the canonical deck now so your current artifacts are easier to track and share. Want to do that now or skip for later?

If the team declines, continue without additional commentary.

## Validation Checklist (When Workflow Is Active)

Before generating or refreshing canonical deck content, run this checklist:

1. Confirm project scope path exists: `.copilot-tracking/dt/{project-slug}/`.
2. Resolve canonical directory as `.copilot-tracking/dt/{project-slug}/canonical/`.
3. Confirm canonical source artifacts available from DT method outputs.
4. Detect create vs refresh mode:
   - `create`: no canonical entries exist yet
   - `refresh`: canonical entries already exist
5. If refreshing, compute artifact fingerprints and update only changed or new entries.
6. Record snapshot metadata in coaching state for the current method checkpoint when generated.
7. Ask the mandatory post-snapshot customer-card checkpoint question.
8. Record the offer timestamp and user response in coaching state.
9. If requested, proceed to customer-card PowerPoint build branch.

## Canonical Artifact Model

Canonical deck entries are maintained in place under:

```text
.copilot-tracking/dt/{project-slug}/canonical/
├── vision-statement.md
├── problem-statement.md
├── scenarios/
├── use-cases/
└── personas/
```

Use existing Design Thinking evidence and avoid speculative content.

### Required Vision Statement Sections

Every vision-statement entry must include:

1. Title from frontmatter `title`, or first heading if no frontmatter title exists
2. `## Vision Statement`
3. `### Why This Matters`

If information is missing, use `<insufficient knowledge>` and add `#### Questions to Ask` with 2-5 targeted questions.

### Required Problem Statement Sections

Every problem-statement entry must include:

1. Title from frontmatter `title`, or first heading if no frontmatter title exists
2. `## Problem Statement`

If information is missing, use `<insufficient knowledge>` and add `#### Questions to Ask` with 2-5 targeted questions.

### Required Scenario Sections

Every scenario entry must include:

1. `### Description`
2. `### Scenario Narrative`
3. `### How Might We`

### Required Use Case Sections

Every use case entry must include all required subsections in this exact order:

1. `### Use Case Description`
2. `### Use Case Overview`
3. `### Business Value`
4. `### Primary User`
5. `### Secondary User`
6. `### Preconditions`
7. `### Steps`
8. `### Data Requirements`
9. `### Equipment Requirements`
10. `### Operating Environment`
11. `### Success Criteria`
12. `### Pain Points`
13. `### Extensions`
14. `### Evidence`

If information is missing, use `<insufficient knowledge>` and add `#### Questions to Ask` with 2-5 targeted questions.

### Required Persona Sections

Every persona entry must include:

1. `### Description`
2. `### User Goal`
3. `### User Needs`
4. `### User Mindset`

If information is missing, use `<insufficient knowledge>` and add targeted questions.

## Customer Card PowerPoint Branch

When the team requests PowerPoint output, accepts a build offer, or accepts the mandatory post-snapshot checkpoint:

1. Generate `content.yaml` slide artifacts from canonical markdown using the customer-card-render skill.
2. Detect the available shell environment before invoking the build pipeline:
   - Check whether `pwsh` is available by running `pwsh --version` or equivalent detection.
   - If `pwsh` is available, invoke `Invoke-PptxPipeline.ps1` from the PowerPoint skill.
   - If `pwsh` is not available but a POSIX shell (`bash`, `sh`) is available, invoke `invoke-pptx-pipeline.sh` instead.
   - If neither `pwsh` nor a shell environment is available, stop and inform the user: "I can't generate the PowerPoint without either PowerShell 7 (pwsh) or a shell environment to run the build script. Please install PowerShell 7 or run this in a bash-compatible environment."
3. Do not attempt the build step and do not silently fail if the required runtime is absent.

Do not restate pipeline internals here. Use these sources:

- `.github/skills/experimental/customer-card-render/README.md`
- `.github/skills/experimental/powerpoint/SKILL.md`

## Method 5 Auto-Generate

If the team completes Method 5 and canonical workflow is active, ask whether to create or update canonical deck and customer card artifacts. If accepted, generate a final canonical deck refresh and then offer customer-card build.

## Coaching State Expectations

When canonical workflow is active, maintain canonical state fields in coaching state for:

- Snapshot status and timestamp for offered checkpoints
- Entry counts and candidate counts when generated
- Fingerprints for staleness detection
- Last offered and last generated customer-card snapshot keys

If the team does not opt in, these fields are optional and should not gate progress.
