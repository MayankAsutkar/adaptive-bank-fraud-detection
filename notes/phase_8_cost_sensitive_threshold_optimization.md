PHASE 8 — COST-SENSITIVE THRESHOLD OPTIMIZATION

OBJECTIVE

The objective of Phase 8 is to determine how the fraud model's classification threshold affects:

- Precision
- Recall
- F1-score
- Number of fraud alerts
- Investigation workload
- False positives
- Missed fraud
- Relative business cost

The main idea is that there is no universally correct fraud threshold. The threshold should depend on the relative cost of:

- Missing a fraudulent case (False Negative)
- Investigating a legitimate case (False Positive)


1. CHRONOLOGICAL MODEL CALIBRATION

The chronological XGBoost model from Phase 7 was calibrated using isotonic calibration.

Calibration setup:

- Model: Chronological tuned XGBoost
- Method: Isotonic
- CV: 3-fold
- Calibration performed using chronological training data
- Month 5 used for threshold selection
- Months 6–7 remained untouched for final future evaluation

Calibrated probability ranges:

Validation:
- Minimum: 0.0
- Maximum: 0.7815

Test:
- Minimum: 0.0
- Maximum: 0.8974


2. CALIBRATED MODEL PERFORMANCE

Validation — Month 5:

- PR-AUC: 0.192239
- ROC-AUC: 0.896274
- Brier Score: 0.010578

Future Test — Months 6–7:

- PR-AUC: 0.188659
- ROC-AUC: 0.891654
- Brier Score: 0.012634

Comparison with raw chronological XGBoost:

                         Raw        Calibrated
Validation PR-AUC       0.191810    0.192239
Validation ROC-AUC      0.896511    0.896274
Test PR-AUC             0.194496    0.188659
Test ROC-AUC            0.893650    0.891654

Interpretation:

- Calibration had little effect on discrimination.
- Validation PR-AUC remained almost unchanged.
- Validation ROC-AUC remained almost unchanged.
- Brier score provides the probability-quality measurement.
- Future test calibration performance was somewhat weaker than validation.
- Threshold selection was performed only using Month 5 validation.


3. THRESHOLD ANALYSIS

Thresholds from 0.01 to 0.50 were evaluated on Month 5 validation.

Metrics evaluated:

- Precision
- Recall
- F1
- Number of alerts
- Alert rate
- False positives
- False negatives

Best F1 threshold:

- Threshold: 0.09
- Precision: 23.93%
- Recall: 30.90%
- F1: 26.97%
- Alerts: 1,822
- Alert rate: 1.527%
- False positives: 1,386
- False negatives: 975


4. VALIDATION THRESHOLD TRADE-OFF

Threshold    Precision    Recall    F1       Alerts    Alert Rate
0.07         19.55%       37.28%   25.65%   2,691     2.255%
0.08         21.81%       34.23%   26.64%   2,215     1.856%
0.09         23.93%       30.90%   26.97%   1,822     1.527%
0.10         25.42%       28.14%   26.71%   1,562     1.309%
0.11         27.51%       25.23%   26.32%   1,294     1.084%
0.12         29.78%       23.53%   26.29%   1,115     0.934%
0.13         31.94%       22.18%   26.18%     980     0.821%

General relationship:

Lower threshold
    ↓
More alerts
    ↓
Higher recall
    ↓
More false positives

Higher threshold
    ↓
Fewer alerts
    ↓
Higher precision
    ↓
More missed fraud


5. FUTURE TEST EVALUATION

Thresholds were selected using Month 5 validation and then evaluated on the untouched future test period (months 6–7).

Future Test:

Threshold    Precision    Recall    F1       Alerts    Alert Rate
0.07         21.18%       33.81%   26.04%   4,594     2.241%
0.08         22.90%       30.58%   26.19%   3,843     1.875%
0.09         24.34%       27.07%   25.63%   3,201     1.561%
0.10         25.58%       24.29%   24.92%   2,733     1.333%
0.11         27.15%       21.61%   24.07%   2,291     1.118%
0.12         29.16%       19.32%   23.24%   1,907     0.930%
0.13         30.66%       17.65%   22.40%   1,657     0.808%
0.14         32.88%       15.88%   21.42%   1,390     0.678%

Important:

The threshold 0.09 was selected using validation only.

It was NOT re-optimized using the future test set.

Therefore, the future test results represent an unseen temporal evaluation.


6. VALIDATION-SELECTED THRESHOLD GENERALIZATION

Threshold selected by F1:

- Threshold = 0.09

Validation:

- Precision = 23.93%
- Recall = 30.90%
- F1 = 26.97%
- Alert rate = 1.527%

Future test:

- Precision = 24.34%
- Recall = 27.07%
- F1 = 25.63%
- Alert rate = 1.561%

Comparison:

Precision:
23.93% → 24.34%

Recall:
30.90% → 27.07%

F1:
26.97% → 25.63%

Alert rate:
1.527% → 1.561%

Interpretation:

- Precision remained very similar.
- Recall decreased moderately.
- F1 decreased slightly.
- Alert rate remained close to the validation value.
- The threshold therefore transferred reasonably well to the future population.


7. COST-SENSITIVE THRESHOLD OPTIMIZATION

F1 does not directly represent business costs.

A fraud system may consider:

- Cost of missed fraud
- Cost of manual investigation
- Customer friction
- False declines
- Investigation team capacity

Therefore, a relative cost model was tested.

False Positive cost:

- 1 unit

False Negative cost:

- 1, 2, 5, 10, or 20 units


8. VALIDATION COST ANALYSIS

FN : FP Cost Ratio    Threshold    FP      FN      Alerts    Alert Rate    Relative Cost

1 : 1                  0.38         25     1360       76      0.064%          1385
2 : 1                  0.26         80     1320      171      0.143%          2720
5 : 1                  0.13        667     1098      980      0.821%          6157
10 : 1                 0.08       1732      928     2215      1.856%         11012
20 : 1                 0.04       4434      730     5115      4.287%         19034


9. COST INTERPRETATION

As the assumed cost of missing fraud increases:

Higher FN cost
      ↓
Lower threshold
      ↓
More alerts
      ↓
More false positives
      ↓
Fewer missed fraud cases

Examples:

5:1 cost ratio:
- Threshold = 0.13
- Alerts = 980
- Alert rate = 0.821%
- False negatives = 1,098

10:1 cost ratio:
- Threshold = 0.08
- Alerts = 2,215
- Alert rate = 1.856%
- False negatives = 928

20:1 cost ratio:
- Threshold = 0.04
- Alerts = 5,115
- Alert rate = 4.287%
- False negatives = 730


10. FUTURE TEST — COST-SELECTED THRESHOLDS

The cost-optimal thresholds were selected using Month 5 validation and then evaluated on months 6–7.

FN : FP    Threshold    TP      FP      FN      TN       Alerts    Alert Rate    Relative Cost

1 : 1       0.38         90      57     2788    202076      147      0.072%          2845
2 : 1       0.26        164     162     2714    201971      326      0.159%          5590
5 : 1       0.13        508    1149     2370    200984     1657      0.808%         12999
10 : 1       0.08        880    2963     1998    199170     3843      1.875%         22943
20 : 1       0.04       1358    7261     1520    194872     8619      4.204%         37661


11. IMPORTANT OBSERVATION

The validation-derived thresholds transfer to the future test, but their operating characteristics change.

Example — 10:1 cost assumption:

Validation:
- Threshold = 0.08
- Alerts = 2,215
- Alert rate = 1.856%
- False negatives = 928

Future test:
- Threshold = 0.08
- Alerts = 3,843
- Alert rate = 1.875%
- False negatives = 1,998

The alert rate remains remarkably similar despite the different population size and time period.

However, the absolute number of false negatives changes because the future test contains a different number of observations and fraud cases.


12. F1 THRESHOLD VS COST-SENSITIVE THRESHOLD

F1-based optimization:

- Validation-optimal threshold = 0.09

Cost-sensitive optimization:

- Depends on the assumed FN:FP cost ratio.

Examples:

1:1  → 0.38
2:1  → 0.26
5:1  → 0.13
10:1 → 0.08
20:1 → 0.04

Therefore:

There is no universally correct fraud threshold.

The threshold should ultimately depend on actual business costs and operational constraints.


13. PRODUCTION THRESHOLD CONSIDERATIONS

A real production system should consider:

- Financial cost of missed fraud
- Cost of manual investigation
- Customer friction
- False-decline cost
- Investigation team capacity
- Maximum acceptable alert volume
- Fraud capture requirement
- Regulatory/business constraints

The threshold should not be chosen solely because it produces the highest F1-score.


14. IMPORTANT METHODOLOGICAL RULE

The future test set was NOT used to select the threshold.

Correct workflow:

Months 0–4
    ↓
Train model
    ↓
Month 5
    ↓
Select threshold / business policy
    ↓
Months 6–7
    ↓
Final future evaluation

This prevents test-set threshold optimization and preserves the integrity of the temporal evaluation.


15. PHASE 8 FINAL CONCLUSION

Cost-sensitive threshold optimization demonstrates that fraud threshold selection is a business decision rather than purely a machine-learning optimization problem.

The F1-maximizing validation threshold was:

- 0.09
- Precision = 23.93%
- Recall = 30.90%
- F1 = 26.97%
- Alert rate = 1.527%

However, different relative costs produce different optimal thresholds:

- 1:1 → 0.38
- 2:1 → 0.26
- 5:1 → 0.13
- 10:1 → 0.08
- 20:1 → 0.04

As the cost of missing fraud increases, the optimal threshold decreases, increasing alert volume and fraud capture while also increasing false positives.

The validation-selected policies were then evaluated on the untouched future test period. This showed that the operating characteristics change somewhat across time, reinforcing the need for continuous monitoring.

FINAL TAKEAWAY:

The model should not have a threshold selected solely by F1.
The production threshold should be determined using actual business costs,
fraud-loss estimates, investigation capacity, and acceptable alert volume.

For this project:
- F1-selected threshold = 0.09
- Cost-sensitive thresholds depend on the assumed FN:FP cost ratio
- Future test evaluation confirms that validation-selected policies can be
  evaluated without test-set optimization
- Continuous threshold and alert-volume monitoring is required in production