# Asset generation pipeline — 3D assets and concept images

An optional tooling companion for workspaces where agents source, generate and prepare content: 3D assets for the engine, and 2D concept or reference images for design review. It sets the source priority, provenance rules, the generation and cleanup steps, and how generated images feed design review packs. Engine-side import and verification belong to the engine companions. Blender steps belong to `BLENDER_MCP_BRIDGE.md`.

## 1. Source priority (3D)

1. **Marketplace packs** (for example Fab, including Megascans), when the licence fits the project. They usually come with LODs, collision and consistent quality.
2. **AI 3D generation** (for example Tripo, Meshy; Rodin for higher-fidelity hero props) for props, debris, structures and set dressing. **Not for hero vehicles or anything that needs exact mechanical layout.** Generators rarely produce separate wheels, clean pivots or usable topology for rigs.
3. **Authored or kitbashed in Blender** for project-specific landmarks and vehicle rigs built on pack meshes.
4. **Engine modeling tools** for blockout only.

Pick the tool per asset class with a small bake-off (about 5 representative assets, judged in the engine at the minimum-spec preset) before committing to a subscription. Subscriptions and API spend need explicit user authorization (core section 2; the autonomous variant also records budgets, section 8).

## 2. Provenance and licences

- Every third-party or generated asset has a register row in the workspace's asset doc (or `ArtSource/_register.csv`): id, source (pack URL, or tool + model + prompt id + date), licence, status (`raw → cleaned → imported → approved`), budget class.
- Raw downloads and generations go in `ArtSource/<source>/<id>/` (Git LFS). Each folder holds a `source.json` sidecar with the same provenance fields.
- Reference images fetched from the web are **reference-only**. They live under `docs/refs/<topic>/web/` with a `_sources.md` (`UNREAL_MCP_BRIDGE.md`, Appendix F) and never ship.

## 3. AI 3D steps

1. **Brief:** the asset's design-doc entry, size in metres, budget class and reference images.
2. **Generate** via the tool's API or UI. Store the prompt, parameters and seed in `source.json`. Generate 2–4 candidates.
3. **Clean up** with batch Blender scripts: decimate or retopo to budget, fix UVs, check texel density, apply scale, set the pivot, add `UCX_` collision and LODs. Export to `ArtSource/Export/`.
4. **Import and validate** in the engine: naming, triangle counts, texture sizes, materials as instances of the project's master materials, collision present.
5. **Review:** an in-engine capture at the minimum-spec preset next to the brief's references. Mark the asset approved in the register.

## 4. Concept and reference images (2D)

Purpose: direction-setting images for design review packs (zone moods, vehicle concepts, key moments, illustrated maps). They show **intent, not measurements.** Exact layouts and dimensions come from deterministic diagrams generated from the project's spec files (`UNREAL_MCP_BRIDGE.md`, Appendix F).

- **API:** one key that reaches several models keeps bake-offs cheap (for example OpenRouter: gpt-image, Gemini image and Flux models behind one key). The key lives in an environment variable (for example `OPENROUTER_API_KEY`), never in the repository. Record the budget and the spend per plan.
- **Prompts are files:** `docs/refs/concept/prompts/<id>.md` holds the prompt, style anchors, model, size and seed. Reuse shared **style anchors** (palette, lens, time of day, materials vocabulary) across prompts for consistency.
- **Outputs:** `docs/refs/concept/<topic>/NN_<name>.jpg` (JPEG quality ~85, ≤ ~400 KB), plus `_sources.md` lines (file → prompt id, model, date).
- **Illustrated maps:** use image-to-image from the deterministic map diagram, so the painting follows the real layout. Annotations are **overlaid from the spec** afterwards, never painted by the model. Check that the result aligns with the diagram before using it.
- **Review:** contact sheets per topic (Appendix F recipe). The user's picks are recorded in the design doc. Rejected images stay out of the repository or move to `_rejected/` only when the user wants them kept.
- **Not shipped by default.** Generated images are reference-only unless the user decides to ship one and its terms allow it. Record that decision.

## 5. Workspace integration

- `MEMORY.md` conventions: source priority, register location, LFS paths, image API, budget.
- The design review pack (core section 6, design specs; autonomous variant section 5, design before build) links the diagrams, concept images and reference sets it presents.
