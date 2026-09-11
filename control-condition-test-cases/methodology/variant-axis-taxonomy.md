# Variant Axis Taxonomy v0.1

この公開パックでは次の13軸を予約します。

1. `REPRESENTATION`
2. `CONFIGURATION`
3. `AUTHORITY`
4. `STATE`
5. `SEQUENCE`
6. `TIMING`
7. `TARGET`
8. `PAYLOAD`
9. `RETRY_RECOVERY`
10. `ENFORCEMENT_PLACEMENT`
11. `CONTEXT`
12. `MODEL_REVIEWER`
13. `ERROR_PATH`

## 初版で実例を置く6軸

- `AUTHORITY`: Approval missing
- `TIMING`: Approval expired
- `TARGET`: Target mismatch
- `RETRY_RECOVERY`: Retry after deny
- `SEQUENCE`: Security/effect ordering
- `ENFORCEMENT_PLACEMENT`: Alternate route

軸は互換語ではありません。例えばSEQUENCEのorderとTARGETのcategorical差分を同一の数値軸へ潰してはいけません。
