# 制御条件ギャップチェック — 公開テストケース集 v0.1

AIエージェントや自動化に「制御がある」と書かれていることと、条件が崩れたときにも実際に止まることは別です。

この公開パックは、宣言された制御条件を**条件変更（Variant）で試し、実際の挙動を比較する**ための最小テストケース集です。

## 何を公開しているか

初版では6つの汎用テストケースを公開します。

> **位置づけ:** 公開中の6ケースは、13軸のVariant taxonomy全体のうち6軸分です。  
> 「6ケース公開」=「体系全体が6軸」という意味ではありません。

| ケース | Variant Axis | 変える条件 |
|---|---|---|
| Approval missing | `AUTHORITY` | 必須承認を欠落させる |
| Approval expired | `TIMING` | 承認を期限切れにする |
| Target mismatch | `TARGET` | 承認対象と実行対象をずらす |
| Retry after deny | `RETRY_RECOVERY` | 却下後に再試行する |
| Sequence ordering | `SEQUENCE` | 制御確認と作用の順序を変える |
| Alternate route | `ENFORCEMENT_PLACEMENT` | 制御点を通らない別経路を使う |

各ケースは、次を固定します。

- Declared Control
- Baseline
- Variant Axis / Variant Value
- Comparator Policy
- Required Evidence
- Claim Boundary

## 重要な考え方

このパックは、単発テストのPASSを「安全」と言い換えません。

```text
Declared Control
      ↓
Baseline
      ↓
Variant
      ↓
Replay / Observation
      ↓
PRESERVED | COUNTEREXAMPLE_OBSERVED | UNDEFINED | UNOBSERVED | CANDIDATE
      ↓
複数の比較可能な観測がそろった場合だけ Boundary inference へ
```

**Single Replay must not produce a Control Boundary.**

Boundaryを推定するには、少なくとも同一Control / Baselineに属する複数の比較可能な観測、Comparatorの整合、Variant関係、Provenanceが必要です。

### 通常のレビュー / テストとの違い

通常のレビューでもControl上のcandidateを見つけることは可能です。制御条件ギャップチェックは、そのcandidateをDeclared Control・Comparator・Effect Boundary・Variantへ分解し、条件差をReplayして結果の変化を観測できる形へ変換します。

内部Referenceで実際に行った比較構造を、第三者製品固有情報を伏せて公開用にまとめています。

→ [通常のレビューと制御条件ギャップチェックの違い](NORMAL_REVIEW_VS_GAP_CHECK.md)

## Quick start

Python 3.12、追加依存なしで確認できます。

```bash
cd control-condition-test-cases
python -B tools/validate_cases.py
python -B -m unittest discover tests
python -B examples/synthetic_gate/run_demo.py
```

`run_demo.py` はローカルの合成作用だけを使います。外部API、ブラウザ、メール、ファイル削除、送金などの実作用はありません。

## Synthetic demo

`examples/synthetic_gate/` には2つのローカル実装があります。

- `reference_gate`: 6条件をすべてfail-closedで確認する参照実装
- `known_gap_gate`: `ENFORCEMENT_PLACEMENT`だけを意図的に欠落させたnegative control

後者は、Alternate Routeケースで `COUNTEREXAMPLE_OBSERVED` がどう表現されるかを示すためだけの合成例です。

## Case studies

第三者製品固有のfindingは初版に含みません。製品固有Case Studyは、証拠closeoutと公開・Responsible Disclosure判断が終わったものだけを追加します。

→ `case-studies/README.md`

## Claim Boundary

このパックは以下を主張しません。

- AIシステム一般の安全性
- 脆弱性の不存在
- 認証・適合・監査意見
- 本番利用可能性
- 第三者製品に対するfinding
- 1回のReplayからのControl Boundary / Operating Envelope

詳細は `CLAIM_BOUNDARY.md` を参照してください。

## Source basis

公開内容は、C³ Control Condition Gap Check vNext のうち、Replay、Variant Axis、Comparator、明示的な未観測、Boundary inferenceのclaim ceilingを汎用化したものです。

13-axis taxonomy:

`REPRESENTATION / CONFIGURATION / AUTHORITY / STATE / SEQUENCE / TIMING / TARGET / PAYLOAD / RETRY_RECOVERY / ENFORCEMENT_PLACEMENT / CONTEXT / MODEL_REVIEWER / ERROR_PATH`

### 非公開の正式検査での扱い

この13軸は、公開6ケースを増やすためだけの一覧ではありません。

弊会の非公開の制御条件ギャップチェックでは、13軸を**検査設計の候補空間**として扱い、対象Control、経路、Effect Boundary、証拠条件に応じて適用する軸を選定します。必要に応じて複数軸の組合せ条件もReplay候補になります。

ただし、次を意味しません。

- すべての案件で13軸すべてを必ず実行する
- 13軸を機械的に総当たりする
- 13軸を確認すれば安全性が証明される
- Gapや脆弱性を完全に網羅できる
- 公開6ケースだけで正式検査を代替できる

公開範囲は、13軸の名称と代表6ケースまでです。案件ごとの軸選定ロジック、組合せ戦略、優先順位付けの詳細は公開していません。

## License status

v0.1では、このサブディレクトリの公開によって再利用ライセンスや特許ライセンスを付与しません。

**閲覧・評価用の公開**です。

現時点では、再配布、組込み、商用利用、派生利用などの条件を一般ライセンスとして許諾していません。再利用条件は別途明示します。
