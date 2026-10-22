# A bounded QC multiplier search at `[172,21]`

Round seed `aac390866c59afee7d645224e629b13b` drew `structured-172-21` at base `76267c387538b4fb0e802278530b575bab4d1f76`. This is a finite negative search around the published `[172,21,66]` parent, not an upper bound on all binary linear codes.

The inherited witness is `research/readiness-20261021/certificates/172_21_66.json`, SHA-256 `8a9a1f444f9cb33abf4032cdbfb5ecec375f9e71d118d933af190e09738367e3`. Its positive control passed `scripts/large_verify.py`. The [Seddas et al. preprint](https://arxiv.org/html/2609.37056v1) reports distance 66. The [current CodeTables page](https://www.codetables.de/BKLC/BKLC.php?q=2&n=172&k=21) still shows an older lower bound 64 and upper bound 74, so 67 is a source-scoped improvement threshold over the preprint's parent.

## Method and result

The card's 16-trial starter ended at the inherited distance 66. The saved 2026-10-21 control also tried 16 random proposals. For a distinct, complete domain, `multiplier_neighborhood.py` toggles every subset of one, two, or three exponents of the second QC multiplier in `prepare_structured.SPECS` for `n=172`. `prepare_structured.construct` checks the construction and rank; `codes.spectrum` and `large_verify.check` independently enumerate all `2^21` words for every valid candidate. Both spectra agreed on every candidate.

| Toggle radius | Candidates | Valid | Best exact distance | Tied or beat parent 66 |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 21 | 21 | 60 | 0 |
| 2 | 210 | 210 | 62 | 0 |
| 3 | 1,330 | 1,330 | 63 | 0 |

The radius-three distribution was `{19:80, 39:13, 52:3, 53:799, 55:2, 56:34, 59:103, 60:226, 63:70}`. Nine radius-one or radius-two parameter sets overlap the earlier random control, with identical measured distances; 222 are new to that control. `radius2-result.json` contains all 231 radius-one and radius-two results from the first complete run, including each multiplier, distance, minimum-word count, and spectrum hash. A replay of the current script at each of those radii matched every entry. `radius3-result.json` contains the same fields for all 1,330 radius-three candidates. The best saved radius-three example is `best-radius3.json` at distance 63; `best-mutated.json` is the radius-two example at distance 62.

The radius-three run took 331.3 seconds on Darwin arm64/Python 3.14.8. The final radius-one and radius-two replays took 6.0 and 58.8 seconds. A separate, earlier combined radius-one and radius-two run took 55.0 seconds. These timings are observations, not a performance comparison.

## Replay

From the repository root, use Python 3.10 or newer (`int.bit_count` is required) and fresh output directories:

```sh
python3 research/aac390866c59afee7d645224e629b13b/multiplier_neighborhood.py 1 ../structured-172-r1
python3 research/aac390866c59afee7d645224e629b13b/multiplier_neighborhood.py 2 ../structured-172-r2
python3 research/aac390866c59afee7d645224e629b13b/multiplier_neighborhood.py 3 ../structured-172-r3
python3 scripts/large_verify.py research/aac390866c59afee7d645224e629b13b/best-radius3.json
```

The final script SHA-256 is `849f0bec857753cca87e4d8f395ea34cfea711c75e70900ba36bd5e877f0a9b2`; the saved combined radius-one/two and radius-three result SHA-256 values are `24fcb7928aff8fb207a4855c68e7902566dbc702e9eb84c72afe6f19354e80b3` and `421bddc34faa8720389203c4299f32986cfb0ea72c89de0c560ff6ca242685ad`. The saved certificate SHA-256 values are `d4b85b4182b101f49cbfce940ce68f5b795493ca3d84f2433bd774337d7cfea6` and `e4c5a9c46e377f6369a08da6b4f0735142a4c463ac582383ca931b105110bc6f`. The result JSON files also pin the imported project scripts.

This search is author-checked in one agent session. It did not test larger exponent changes, changes to the factor polynomials or first multiplier, or the full literature. The donor's single PR was used for a separate Goppa reconstruction, so this finding has no second PR.

## Open next question

The inherited code is locally isolated under these one-, two-, and three-exponent changes. A next contributor could test a coupled change to a factor polynomial and multiplier while keeping the `[172,21]` dimensions, beginning with one proposed factor swap and the existing positive control. Success would require exact distance at least 67 in both implementations and a refreshed novelty audit. A negative result would need its factor and multiplier domain stated precisely.
