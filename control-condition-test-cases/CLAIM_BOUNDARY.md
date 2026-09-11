# Claim Boundary

## この公開パックが示すもの

- 制御条件をBaselineとVariantに分けて記述できること。
- VariantごとにComparator Policyを事前固定できること。
- `PRESERVED / COUNTEREXAMPLE_OBSERVED / UNDEFINED / UNOBSERVED / CANDIDATE`を区別できること。
- 未観測・未定義・証拠不足をpositive evidenceへ自動昇格させないこと。
- 単一ReplayからControl Boundaryを生成しないこと。

## この公開パックが示さないもの

- ここにあるケースを通れば安全である、という主張。
- 6ケースで十分である、という主張。
- 監査、認証、適合、法令準拠の主張。
- Control Boundary、Operating Envelope、Verify IDの発行。
- 実在する第三者製品の脆弱性・欠陥finding。

## Evidence ceiling

初版のtest casesは `GENERIC_PUBLIC_TEST_CASE` です。

Synthetic demoは `LOCAL_SYNTHETIC_DEMONSTRATION` です。

これらを、`CONTROLLED_RUNTIME`、`BYOV_REPRODUCTION`、第三者製品のlive evidenceへ読み替えてはなりません。

## Boundary rule

Single Replay must not be represented as a Control Boundary.

Boundary inferenceには、少なくとも次が必要です。

1. 同一Control ID
2. 同一Baseline ID
3. compatible Comparator Policy
4. declared Variant relationship
5. distinguishable Variant Values
6. qualified provenance
7. transitionの両側を支える比較可能な観測

不足時は推測で埋めず `UNDEFINED` または `UNOBSERVED` を維持します。
