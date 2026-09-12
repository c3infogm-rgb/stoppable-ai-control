# stoppable-ai-control

## 公開中: 制御条件ギャップチェック — テストケース集 v0.1

このリポジトリで現在いちばん見てほしい公開物は、**AIエージェントや自動化の制御条件を、条件変更（Variant）で揺さぶって確かめる6つの公開テストケース**です。

→ **[Control Condition Test Cases v0.1 を見る](control-condition-test-cases/README.md)**

公開中の6ケース:

| ケース | Variant Axis | 何を変えるか |
|---|---|---|
| Approval missing | `AUTHORITY` | 必須承認を欠落させる |
| Approval expired | `TIMING` | 承認を期限切れにする |
| Target mismatch | `TARGET` | 承認対象と実行対象をずらす |
| Retry after deny | `RETRY_RECOVERY` | 却下後に再試行する |
| Sequence ordering | `SEQUENCE` | 制御確認と作用の順序を変える |
| Alternate route | `ENFORCEMENT_PLACEMENT` | 制御点を通らない別経路を使う |

各ケースには、少なくとも以下を含みます。

- Declared Control
- Baseline
- Variant Axis / Variant Value
- Comparator Policy
- Required Evidence
- Claim Boundary

さらに `examples/synthetic_gate/` には、

- 6条件をすべてfail-closedで確認する参照実装
- `ENFORCEMENT_PLACEMENT` だけを意図的に欠落させた比較用negative control

の両方があります。

片方だけではなく、**参照実装と既知Gap実装を比較して、反例がどう出るか確認できる**構成です。

## 6ケースと13軸体系の関係

v0.1で公開しているのは、13軸のVariant taxonomyのうち6軸分です。

公開済み6軸:

`AUTHORITY / TIMING / TARGET / RETRY_RECOVERY / SEQUENCE / ENFORCEMENT_PLACEMENT`

全13軸:

`REPRESENTATION / CONFIGURATION / AUTHORITY / STATE / SEQUENCE / TIMING / TARGET / PAYLOAD / RETRY_RECOVERY / ENFORCEMENT_PLACEMENT / CONTEXT / MODEL_REVIEWER / ERROR_PATH`

したがって、**「6種類の公開テストケース」= 現在公開している6軸分**であり、体系全体が6軸という意味ではありません。

## この公開パックが主張しないこと

単発テストのPASSを「安全」とは扱いません。

この公開物は、以下を主張しません。

- AIシステム一般の安全性
- 脆弱性の不存在
- 認証・適合・監査意見
- 本番利用可能性
- 第三者製品に対するfinding
- 1回のReplayからのControl Boundary / Operating Envelope

詳細:

→ [Claim Boundary](control-condition-test-cases/CLAIM_BOUNDARY.md)

## Quick start

Python 3.12、追加依存なしで確認できます。

```bash
cd control-condition-test-cases
python -B tools/validate_cases.py
python -B -m unittest discover tests
python -B examples/synthetic_gate/run_demo.py
```

このデモはローカルの合成作用のみです。
ブラウザ、外部API、credential、メール送信、ファイル削除、送金などの実作用はありません。

---

## このリポジトリ名について

`stoppable-ai-control` は、初期の「止められる / fail-closedなAI制御ループ」デモから続くリポジトリ名です。

現在の公開テストケース集は「制御そのものを提供する」より、**宣言された制御が条件変更時にも維持されるかを確かめる**ことに重点があります。

既存リンクを維持するため、現時点ではリポジトリ名を変更していません。
将来、テストケース集が独立した主力公開物になった場合は、別リポジトリへの分離を検討します。

## Legacy: fail-closed control loop demo

このリポジトリには、初期のfail-closed / audit-firstデモも残しています。

Core idea:

- Uncertainty → `HOLD`
- Evidence verified → controlled recovery

旧デモ関連:

- `prompts/`
- `demo.txt`
- `covid_seed_audit_pack.zip`
- `AMS-SEED_Fail-Safe_Audit_(4).pdf`
- `特許技術についての解説.pdf`

### COVID audit artifactについて

`covid_seed_audit_pack.zip` は**模擬データを使ったfail-closed監査デモ**です。

医療判断・政策判断のためのデータや推奨ではありません。
現在の制御条件テストケース集とは別の、初期デモ由来のlegacy artifactです。

## License status

現時点では、このリポジトリまたは `control-condition-test-cases/` の公開によって、一般的な再利用ライセンスや特許ライセンスを付与していません。

**閲覧・評価用の公開**です。

- 公開された内容を読む
- テスト設計の考え方を評価・検討する

ことを想定しています。

再配布、組込み、商用利用、派生利用などの条件は、今後別途明示します。

---

### English summary

The primary public material in this repository is now **Control Condition Test Cases v0.1**: six generic test cases for perturbing declared control conditions and comparing observed behavior under an explicit Comparator Policy and Claim Boundary.

The six published cases cover 6 of a broader 13-axis Variant taxonomy. The repository name is retained for compatibility with existing links; older fail-closed audit materials are kept as legacy references.

Start here:

→ [control-condition-test-cases/README.md](control-condition-test-cases/README.md)
