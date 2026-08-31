# Results

| run | cases | raw | rows | gates | cost $ | wall s | git | ts |
|---|---|---|---|---|---|---|---|---|
| ablate-crosscheck | public | **0.804** | verdict_acc=0.75 confident_wrong=0.75 evidence_valid=1.0 score_error=0.777 | no_fabricated_evidence=1.00 valid_report=1.00 | 0 | 5554.0 | b8f4af6 | 2026-08-28T21:29:06Z |
| ablate-k1 | public | **0.82** | verdict_acc=0.729 confident_wrong=0.876 evidence_valid=1.0 score_error=0.777 | no_fabricated_evidence=1.00 valid_report=1.00 | 0 | 5554.0 | b8f4af6 | 2026-08-28T21:29:06Z |
| ablate-no-execution | public | **0.044** | verdict_acc=0.007 confident_wrong=1.0 evidence_valid=0.0 score_error=0.712 | no_fabricated_evidence=0.14 valid_report=1.00 | 0 | 232.9 | rewritten | 2026-08-28T21:35:39Z |
| ablate-no-execution-rescored | public | **0.044** | verdict_acc=0.007 confident_wrong=1.0 evidence_valid=0.0 score_error=0.712 | no_fabricated_evidence=0.14 valid_report=1.00 | 0 | 232.9 | rewritten | 2026-08-28T21:35:39Z |
| advanced-v1 | public | **0.441** | verdict_acc=0.408 confident_wrong=0.495 evidence_valid=0.621 coverage=0.621 score_error=0.506 | no_fabricated_evidence=1.00 valid_report=0.86 | 0 | 2874.0 | fa0e62b | 2026-08-28T19:50:12Z |
| advanced-v1-rescored | public | **0.454** | verdict_acc=0.493 confident_wrong=0.58 evidence_valid=0.58 score_error=0.506 | no_fabricated_evidence=1.00 valid_report=0.86 | 0 | 2874.0 | fa0e62b | 2026-08-28T19:50:12Z |
| advanced-v2 | public | **0.808** | verdict_acc=0.698 confident_wrong=0.887 evidence_valid=1.0 score_error=0.777 | no_fabricated_evidence=1.00 valid_report=1.00 | 0 | 5554.0 | b8f4af6 | 2026-08-28T21:29:06Z |
| advanced-v2-rescored | public | **0.836** | verdict_acc=0.75 confident_wrong=0.91 evidence_valid=1.0 score_error=0.777 | no_fabricated_evidence=1.00 valid_report=1.00 | 0 | 5554.0 | b8f4af6 | 2026-08-28T21:29:06Z |
| advanced-v3-ext | ext-cases | **0.846** | verdict_acc=0.774 confident_wrong=0.964 evidence_valid=1.0 score_error=0.701 | no_fabricated_evidence=1.00 valid_report=1.00 | 20.8464 | 2708.2 | cb34764 | 2026-08-29T17:48:27Z |
| advanced-v3-ext-rerun | ext-rerun | **0.781** | verdict_acc=0.67 confident_wrong=0.934 evidence_valid=1.0 score_error=0.617 | no_fabricated_evidence=1.00 valid_report=1.00 | 5.9736 | 736.7 | cb34764 | 2026-08-29T18:27:26Z |
| advanced-v3-ext-rescored | ext-cases | **0.859** | verdict_acc=0.802 confident_wrong=0.964 evidence_valid=1.0 score_error=0.701 | no_fabricated_evidence=1.00 valid_report=1.00 | 20.8464 | 2708.2 | cb34764 | 2026-08-29T17:48:27Z |
| advanced-v3-heldout | heldout | **0.66** | verdict_acc=0.551 confident_wrong=0.621 evidence_valid=0.969 score_error=0.624 | no_fabricated_evidence=1.00 valid_report=1.00 | 27.4806 | 1414.3 | adc5e50 | 2026-08-29T19:10:50Z |
| advanced-v3-heldout-drafttruth | heldout | **0.66** | verdict_acc=0.551 confident_wrong=0.621 evidence_valid=0.969 score_error=0.624 | no_fabricated_evidence=1.00 valid_report=1.00 | 27.4806 | 1414.3 | adc5e50 | 2026-08-29T19:10:50Z |
| advanced-v3-heldout-rerun | heldout-rerun | **0.687** | verdict_acc=0.531 confident_wrong=0.617 evidence_valid=1.0 score_error=0.829 | no_fabricated_evidence=1.00 valid_report=1.00 | 16.3868 | 2452.8 | 2b25f32 | 2026-08-30T02:39:35Z |
| advanced-v3-heldout-rescored | heldout | **0.806** | verdict_acc=0.774 confident_wrong=0.853 evidence_valid=0.969 score_error=0.624 | no_fabricated_evidence=1.00 valid_report=1.00 | 27.4806 | 1414.3 | adc5e50 | 2026-08-29T19:10:50Z |
| baseline-ext | ext-cases | **0.289** | verdict_acc=0.079 confident_wrong=0.608 evidence_valid=0.608 score_error=0.452 | no_fabricated_evidence=1.00 valid_report=0.83 | 2.9242 | 726.8 | d968bcb | 2026-08-29T17:03:18Z |
| baseline-ext2 | ext-cases | **0.35** | verdict_acc=0.087 confident_wrong=0.366 evidence_valid=1.0 score_error=0.739 | no_fabricated_evidence=1.00 valid_report=1.00 | 3.7073 | 280.8 | cb34764 | 2026-08-29T18:13:44Z |
| baseline-ext2-rescored | ext-cases | **0.35** | verdict_acc=0.094 confident_wrong=0.373 evidence_valid=1.0 score_error=0.739 | no_fabricated_evidence=1.00 valid_report=1.00 | 3.7073 | 280.8 | cb34764 | 2026-08-29T18:13:44Z |
| baseline-heldout | heldout | **0.35** | verdict_acc=0.16 confident_wrong=0.431 evidence_valid=1.0 score_error=0.829 | no_fabricated_evidence=1.00 valid_report=1.00 | 4.3795 | 342.8 | adc5e50 | 2026-08-29T18:47:16Z |
| baseline-heldout-drafttruth | heldout | **0.35** | verdict_acc=0.16 confident_wrong=0.431 evidence_valid=0.903 score_error=0.829 | no_fabricated_evidence=1.00 valid_report=1.00 | 4.3795 | 342.8 | adc5e50 | 2026-08-29T18:47:16Z |
| baseline-heldout-rescored | heldout | **0.35** | verdict_acc=0.087 confident_wrong=0.371 evidence_valid=1.0 score_error=0.829 | no_fabricated_evidence=1.00 valid_report=1.00 | 4.3795 | 342.8 | adc5e50 | 2026-08-29T18:47:16Z |
| baseline-v2-n1 | public | **0.529** | verdict_acc=0.095 confident_wrong=0.813 evidence_valid=0.332 coverage=1.0 score_error=0.811 | no_fabricated_evidence=1.00 valid_report=1.00 | 0 | 371.8 | 993589e | 2026-08-28T18:56:17Z |
| baseline-v2-n1-rescored | public | **0.284** | verdict_acc=0.074 confident_wrong=0.771 evidence_valid=0.111 score_error=0.811 | no_fabricated_evidence=0.86 valid_report=1.00 | 0 | 371.8 | 993589e | 2026-08-28T18:56:17Z |
| baseline-v2-n2 | public | **0.51** | verdict_acc=0.088 confident_wrong=0.783 evidence_valid=0.324 coverage=1.0 score_error=0.745 | no_fabricated_evidence=1.00 valid_report=1.00 | 0 | 360.4 | 993589e | 2026-08-28T19:02:18Z |
| baseline-v2-n2-rescored | public | **0.271** | verdict_acc=0.074 confident_wrong=0.783 evidence_valid=0.07 score_error=0.745 | no_fabricated_evidence=0.86 valid_report=1.00 | 0 | 360.4 | 993589e | 2026-08-28T19:02:18Z |
| single-shot-baseline | ss-cases | **0.443** | verdict_acc=0.25 confident_wrong=0.267 evidence_valid=0.942 score_error=0.593 | no_fabricated_evidence=1.00 valid_report=1.00 | 0 | 536.1 | 5eaa80c | 2026-08-31T09:09:34Z |

Per-case detail lives in proof/build_proof.json (find the run id above).
