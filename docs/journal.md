# Journal

One entry per milestone: what was built, problems, what was learned, numbers.

## Milestone 1 — Core (2026-11-06)

**Built:** the whole non-GUI pipeline.
- HDL lexer, parser and dataclass AST, with `file:line:col` errors.
- Elaboration that flattens any chip into a bit-level NAND netlist through a primitive table, then levelizes it.
- A three-valued engine (`value`/`known` bit-planes, Kleene NAND) that evaluates each level with one vectorized numpy operation.
- Our own `.tst` format and runner. The runner enforces each level's pins and allowed parts.
- `nandsim test`.
- The first six levels: Not, And, Or, Xor, Mux, DMux, each with a stub, brief, test and hidden reference.
- Level data ships inside the wheel. CI installs the wheel and runs every level from it.

**Problems and how they were solved:**
- *Parts in any order.* A part may read a wire that a later part drives. Every chip output and internal wire first gets a placeholder net, and when a part's output is bound, the placeholder is aliased to the real net. All aliases are resolved at the end in one vectorized pass (`mapping = mapping[mapping]` until stable).
- *Readable loop errors.* A loop shows up as gates left over after Kahn's algorithm. To name the wires, the levelizer walks back from a stuck gate through stuck drivers until a gate repeats. Each net is labelled with its shallowest wire path in the hierarchy, giving messages like `y -> x -> y`.
- *Levels in an installed game.* `chips/` and `reference/` live at the repo root for easy review. Hatch copies them into `nandsim/_data`, and `data_root()` prefers that directory when it exists.
- *Golden error tests.* My hand-counted columns were wrong three times, and the parser was right each time. Error tests are now written by running the parser once and checking the output by eye.

**Learned:**
- **Engine cost scales with depth, not gate count.** Each level costs about 3.4 µs of fixed numpy overhead, so a 4096-gate netlist 3 levels deep runs at about 148 M gate-evals/s, while a 257-gate chain 257 levels deep manages only about 0.3 M. Milestone 6's single-cycle CPU will be a few hundred levels deep, which points to roughly 1 kHz before builtins. The levers, in order: builtins for wide, deep blocks (adder, ALU, RAM, register file), then merging small levels or compiling level schedules.
- Kleene NAND matters already: `Mux` with `sel` defined and the unselected input undefined gives a defined output, as real hardware does.
- Stopping at the first error keeps every message precise; recovery can come later without changing the format.

**Numbers:**

| Measure | Value | How measured |
|---|---|---|
| Tests | 103 | `uv run pytest`: hdl 15, netlist 22, sim 15, testing 26, levels 19, cli 4, boundary 2 |
| Levels | 6/6 pass against their references | `uv run nandsim test` |
| Source LOC | 1358 | non-blank lines of `src/**/*.py`: hdl 302, netlist 564, sim 81, testing 333 |
| Test LOC | 513 | non-blank lines of `tests/**/*.py` |
| NAND count (depth) per reference | Not 1 (1), And 2 (2), Or 3 (2), Xor 4 (3), Mux 8 (5), DMux 5 (3) | `elaborate()` on each reference |
| Engine, wide | 4096 NAND, depth 3: 36k evals/s (148 M gate-evals/s); elaboration 0.12 s | 1024 parallel `Xor`s, `Simulator.eval()` in a loop for 2 s, Python 3.12.3, numpy 2.x, this laptop |
| Engine, deep | 257 NAND, depth 257: 1175 evals/s (0.3 M gate-evals/s) | chain of 257 `Not`s, same method |

**Next:** milestone 2, the base GUI. It starts with a pygame window that draws a chip from its netlist with a layered layout (inputs left, outputs right, parts in levels) and colours wires by 0, 1 or undefined. Then: clickable inputs, hierarchical navigation, the in-app editor with inline errors, saves, and the level select.
