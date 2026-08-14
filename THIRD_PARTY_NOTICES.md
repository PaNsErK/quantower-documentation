# Third-party notices

The local documentation build uses the following tooling:

- **MkDocs**, BSD-2-Clause license.
- **Material for MkDocs**, MIT license.
- **Python dependencies** listed with exact versions and hashes in `requirements.lock.txt`.
- **GitHub-owned Actions** pinned to immutable commit SHAs in `.github/workflows/pages.yml`.

No third-party JavaScript, font, analytics, CDN, or runtime asset is loaded by the generated documentation.

Material for MkDocs 9.7.7 is intentionally pinned. The project is in maintenance mode with critical/security support announced through November 2026. Content, CSS, and JavaScript therefore avoid deep theme overrides and deprecated projects/typeset features so a later renderer migration remains bounded.
