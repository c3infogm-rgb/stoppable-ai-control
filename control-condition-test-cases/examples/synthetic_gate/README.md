# Synthetic Gate Demo

この例は完全ローカルです。

- network = 0
- browser = 0
- credential = 0
- external API = 0
- real external effect = 0

`reference_gate` は6ケースすべてをfail-closedで扱います。

`known_gap_gate` は `ENFORCEMENT_PLACEMENT` のroute checkだけを意図的に省いたnegative controlです。

`classify_no_effect_variant` は、「このVariantではpermit/effectが発生してはならない」という今回6ケース共通のComparatorにだけ使う補助関数です。一般-purposeのReplay classifierではありません。

目的は、「実装が良い／悪い」を採点することではなく、同じComparatorで `PRESERVED` と `COUNTEREXAMPLE_OBSERVED` をどう区別するかを小さく再現することです。
