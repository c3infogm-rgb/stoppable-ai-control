# Replay と Boundary の分離

## Replay Unit

Replay Unitは「1条件で1回何が観測されたか」を残す単位です。

最低限、次の概念を分離します。

- Control
- Baseline
- Variant Axis
- Variant Value
- Comparator Policy
- Method / Reviewer
- Run Index
- Evidence Class
- Observation
- Classification
- Provenance

Replay observation stateは次の5状態を区別します。

- `PRESERVED`
- `COUNTEREXAMPLE_OBSERVED`
- `UNDEFINED`
- `UNOBSERVED`
- `CANDIDATE`

## Repeated run

同じVariantを複数回試しても、各Runは別記録です。

`PRESERVED`と`COUNTEREXAMPLE_OBSERVED`が同じVariantで混在した場合、単純多数決で潰しません。解決規則がなければBoundary inferenceは `UNDEFINED` とします。

## Boundary

Boundaryは「状態変化が観測された関係」を表します。

例:

```text
Variant A -> PRESERVED
Variant B -> COUNTEREXAMPLE_OBSERVED
```

ただし、2回あれば自動的にBoundaryになるわけではありません。Control / Baseline / Comparator / Variant relation / provenanceが比較可能である必要があります。

## Relation modes

- `ORDERED`
- `UNORDERED`
- `DECLARED_ADJACENCY`

文字列順、enum順、JSON順、hash順から勝手にorderingを発明してはいけません。
