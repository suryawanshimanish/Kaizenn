# Kaizen Connect
## From Skills to Opportunities
SIH26044 · Academia–Industry Skill Mapping, Internships & Placement

A runnable, responsive hackathon demo with Student, Industry, Institution, and lightweight Academician portals. All records and organizations are synthetic. No original source project was supplied, so this is a new implementation of the supplied concept, not a verified reuse of an existing codebase.

## Open directly
Double-click the repository's `index.html` to open the demo in your browser. No server, Node.js, npm, or build step is required. In this mode, changes are saved in the browser's local storage on that device.

## Run with shared SQLite persistence
```sh
cd kaizen
python server.py
```
Open port 3000. Python 3 standard library only; no runtime package installation is needed. The server listens on `0.0.0.0`. Browser API calls use relative URLs. This mode stores state in SQLite and shares it across browser sessions.

## Implemented
- Profile editing and saved target role
- Ten-question practice assessment, with five technical skill scores
- Skill Profile with source and verification labels
- Three target-role benchmarks and deterministic Skill Gap Engine
- Gap-based curated learning paths, prerequisites, completion tracking
- Weighted matching, education eligibility, search and work-mode filters
- Internship and job details with transparent score breakdowns
- Applications requiring consent and saving a profile/evidence snapshot
- Recruiter opportunity creation, candidate review, and sequential status transitions
- Student application tracking and withdrawal
- Self-reported project evidence and text portfolio export
- Institution cohort analytics, skill gaps, demand counts, and CSV export
- Lightweight mentorship requests and faculty visibility
- SQLite persistence shared across portals

## Demo sequence
1. Start on the Student Dashboard with Aarav's seeded Skill Profile.
2. Open Skill Gaps: SQL and Power BI are the largest Data Analyst gaps.
3. Explore the Learning Path and complete a lesson. Completion does not increase proficiency.
4. Open Internships, view a Lumina Labs opportunity, and inspect its match breakdown.
5. Apply with consent and see the submitted application.
6. Switch to Industry using the sidebar selector.
7. Review Applications; advance Submitted → Under Review → Shortlisted → Interview → Selected/Rejected.
8. Switch back to Student to see the status history.
9. Switch to Institution to see aggregate application and skill analytics.
10. Optional: take the practice assessment to replace the five technical seed scores; inspect updated gaps and recommendations.

## Calculations
- Per-skill gap: `max(0, required - student)`.
- Gap classification: 0 = no gap; 1–10 = low; 11–20 = medium; 21+ = high.
- Coverage: `min(student / required, 1) * 100`.
- Role readiness: equal-weight average of required skill coverage, rounded.
- Opportunity skill score: coverage calculated against its own requirements.
- Eligibility: exact degree membership in the opportunity's allowed degrees; ineligible opportunities are excluded from student recommendations.
- Match = 50% skills + 20% interest + 15% education + 10% projects + 5% location.
- Interest: 100 for matching category, otherwise 40.
- Education: 100 for eligible, otherwise 0. It is also a hard filter.
- Projects: 50 for each project with at least one required skill, capped at 100. Evidence is self-reported, not verified.
- Location: 100 for remote or the preferred city, otherwise 0.
- Practice assessment: two equally weighted questions per technical skill, 50 points per correct answer. This is not a validated proficiency instrument.
- Seeded Data Analyst readiness is 79% under these formulas, not the illustrative 68% in the original brief.

## Architecture
- `static/index.html`: application shell.
- `index.html`: double-click entry point for opening the project without a server.
- `static/style.css`: responsive design system and layouts.
- `static/app.js`: portal views, demo rules, assessment, calculations, actions.
- `server.py`: Python HTTP server and JSON persistence API.
- `kaizen.sqlite3`: one JSON state document in SQLite. Created from the seed on first run.
- `GET /api/state`: retrieve shared demo state.
- `POST /api/state`: update allowed state keys.

This intentionally small architecture is **not** the proposed production React/Next.js + PostgreSQL architecture. Business logic runs in the browser for this prototype, not in an authoritative protected backend. The SQLite store is not a normalized production schema.

## Important limitations
- Portal switching is a demo control, **not authentication or authorization**.
- All users of this server share one state. Do not enter personal or sensitive information.
- No server-enforced role permissions, tenant isolation, rate limits, or production session handling.
- Only basic API shape/size checks; not a comprehensive schema-validation layer.
- Audit entries and consent flags demonstrate the workflow but are client-controlled and are not a security boundary.
- No actual certificate verification, real recruiter accounts, university integrations, email delivery, or external application submission.
- No AI or LLM is connected. Explanations are deterministic templates.
- No external course platform or full LMS. Lessons are short curated practice briefs.
- Academician programmes, research, consultancy, FDPs, live mentorship, and real placement verification are future scope.
- Five cohort members are static synthetic fixtures; the sixth uses the interactive profile. Outcomes reflect the interactive student's actions only.
- Google Fonts are optional external styling; system sans-serif is the fallback.

Before any real deployment: replace the mutable state endpoint with validated domain APIs; implement secure identity, server-side RBAC and tenant scoping; move all scoring and lifecycle checks server-side; normalize the database; secure consent and documents; add privacy retention controls, rate limits, audit integrity, backups, and tests.

## Tests
`test.cjs` is a Playwright smoke/end-to-end test. It visits every portal page, applies as a student, shortlists as a recruiter, checks status propagation, submits an assessment, and checks mobile horizontal overflow and browser errors.

Optional test dependencies:
```sh
npm install --no-save playwright
npx playwright install --with-deps chromium
node test.cjs
```
Run against a freshly seeded database; the test changes demo state. To reset, stop the server, delete `kaizen.sqlite3`, and restart. Do not delete a database containing changes you want to retain.
