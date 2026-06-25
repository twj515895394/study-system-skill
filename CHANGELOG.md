# CHANGELOG

## Unreleased

### Added

- Added `scripts/study_utils.py` shared helpers.
- Added `scripts/new_lesson.py` for creating lesson files from lesson type templates.
- Added `scripts/add_handoff.py` for generating standard handoff files.
- Added `scripts/add_learning_record.py` for creating learning records and updating review schedules.
- Added `scripts/close_lesson.py` for syncing lesson closeout state across `STATE.json`, `CURRENT.md`, `PROGRESS.md`, and `COURSE-LIST.md`.
- Added `docs/script-commands.md`.

## 0.4.0 - P3 Examples and Onboarding

### Added

- Added `examples/codebase-study-demo/` as a complete codebase learning workspace demo.
- Added `docs/quickstart.md`.
- Added `ROADMAP.md`.
- Added `CHANGELOG.md`.

## 0.3.0 - P2 Learning Effectiveness

### Added

- Added `references/comprehension-rubric.md`.
- Added `templates/review-quiz.md.template`.
- Added lesson type templates:
  - `concept-primer.md.template`
  - `code-trace.md.template`
  - `architecture-walkthrough.md.template`
  - `paper-reading.md.template`
  - `exercise-review.md.template`
  - `implementation-lab.md.template`
  - `phase-review.md.template`

### Changed

- Updated `lesson.md.template` with comprehension scoring fields.
- Updated `learning-record.md.template` with evidence and mastery level fields.
- Updated `lesson-flow.md` to require lesson type selection before writing a lesson.
- Updated `init_workspace.py` to copy lesson type templates into `study/_templates/`.
- Updated `validate_workspace.py` to check workspace templates.

## 0.2.0 - P1 Workspace Runtime

### Added

- Added `STATE.json` initialization.
- Added `scripts/validate_workspace.py`.
- Added `QUESTION-PARKING-LOT.md.template`.
- Added `REVIEW-SCHEDULE.md.template`.
- Added workspace template copying into `study/_templates/`.
- Added `references/status-model.md` fields for `STATE.json`.

### Changed

- Updated `SKILL.md`, README and handoff protocol to use `STATE.json` as machine-readable state.

## 0.1.0 - P0 Usability Baseline

### Added

- Added MIT License.
- Added Claude Code global/project install instructions.
- Added unified status model.

### Fixed

- Updated script invocation to use `${CLAUDE_SKILL_DIR}`.
- Removed unresolved placeholders from `TEACHING-PROTOCOL.md.template`.
