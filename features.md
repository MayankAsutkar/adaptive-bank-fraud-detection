| Feature                            | What it represents                                                            | Useful for                    |
| ---------------------------------- | ----------------------------------------------------------------------------- | ----------------------------- |
| `income`                           | Normalized customer income level                                              | Financial profile             |
| `name_email_similarity`            | Similarity between customer's name and email                                  | Identity fraud                |
| `prev_address_months_count`        | Number of months associated with the previous address                         | Customer history              |
| `current_address_months_count`     | Number of months at the current address                                       | Address stability             |
| `customer_age`                     | Customer age                                                                  | Demographics / risk profiling |
| `days_since_request`               | Time elapsed since the previous request                                       | Request frequency / velocity  |
| `intended_balcon_amount`           | Intended balance/amount associated with the request                           | Financial behavior            |
| `payment_type`                     | Type of payment mechanism used                                                | Transaction/request behavior  |
| `zip_count_4w`                     | Number of requests associated with the ZIP code during the last 4 weeks       | Geographic activity           |
| `velocity_6h`                      | Request/activity velocity over the last 6 hours                               | Short-term fraud behavior     |
| `velocity_24h`                     | Request/activity velocity over the last 24 hours                              | Short-term behavioral pattern |
| `velocity_4w`                      | Request/activity velocity over the last 4 weeks                               | Long-term behavioral pattern  |
| `bank_branch_count_8w`             | Number of bank branches associated with activity over 8 weeks                 | Banking behavior              |
| `date_of_birth_distinct_emails_4w` | Number of distinct emails associated with the same date of birth over 4 weeks | Identity/account linkage      |
| `employment_status`                | Customer employment category                                                  | Customer profile              |
| `credit_risk_score`                | Credit/risk score associated with the applicant                               | Financial risk                |
| `email_is_free`                    | Whether the email uses a free email provider                                  | Identity risk                 |
| `housing_status`                   | Customer housing category                                                     | Customer profile              |
| `phone_home_valid`                 | Whether the provided home phone number is valid                               | Identity verification         |
| `phone_mobile_valid`               | Whether the provided mobile phone number is valid                             | Identity verification         |
| `bank_months_count`                | Number of months associated with the bank account/history                     | Banking history               |
| `has_other_cards`                  | Whether the customer has other cards                                          | Customer profile              |
| `proposed_credit_limit`            | Credit limit proposed for the customer                                        | Financial risk                |
| `foreign_request`                  | Whether the request is classified as foreign                                  | Geographic risk               |
| `source`                           | Source/channel through which the request originated                           | Channel behavior              |
| `session_length_in_minutes`        | Duration of the user's session                                                | Behavioral anomaly            |
| `device_os`                        | Operating system of the device used                                           | Device behavior               |
| `keep_alive_session`               | Whether the session was maintained/kept alive                                 | Session behavior              |
| `device_distinct_emails_8w`        | Number of distinct emails associated with the device over 8 weeks             | Device/account relationship   |
| `device_fraud_count`               | Historical fraud count associated with the device                             | Historical fraud signal       |
| `month`                            | Time period/month index of the record                                         | Temporal evaluation / drift   |


| Column       | What it represents                                 |
| ------------ | -------------------------------------------------- |
| `fraud_bool` | **Target variable:** `0` = legitimate, `1` = fraud |



--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




** CATEGORIES

1. Customer & Demographic Profile

| Feature                 | What it represents                   |
| ----------------------- | ------------------------------------ |
| `income`                | Customer income level                |
| `customer_age`          | Customer age                         |
| `employment_status`     | Employment category                  |
| `housing_status`        | Housing category                     |
| `has_other_cards`       | Whether the customer has other cards |
| `credit_risk_score`     | Customer's credit/risk score         |
| `proposed_credit_limit` | Proposed credit limit                |


2. Identity & Contact Verification

| Feature                            | What it represents                                                  |
| ---------------------------------- | ------------------------------------------------------------------- |
| `name_email_similarity`            | Similarity between customer's name and email                        |
| `email_is_free`                    | Whether the email uses a free email provider                        |
| `phone_home_valid`                 | Whether the home phone is valid                                     |
| `phone_mobile_valid`               | Whether the mobile phone is valid                                   |
| `date_of_birth_distinct_emails_4w` | Number of distinct emails associated with the same DOB over 4 weeks |


3. Address & Banking History

| Feature                        | What it represents                                            |
| ------------------------------ | ------------------------------------------------------------- |
| `prev_address_months_count`    | Time associated with previous address                         |
| `current_address_months_count` | Time associated with current address                          |
| `bank_months_count`            | Length of banking history                                     |
| `bank_branch_count_8w`         | Number of bank branches associated with activity over 8 weeks |


4. Behavioral & Velocity Signals

| Feature                     | What it represents                                 |
| --------------------------- | -------------------------------------------------- |
| `days_since_request`        | Time since previous request                        |
| `zip_count_4w`              | Activity associated with the ZIP code over 4 weeks |
| `velocity_6h`               | Activity velocity over 6 hours                     |
| `velocity_24h`              | Activity velocity over 24 hours                    |
| `velocity_4w`               | Activity velocity over 4 weeks                     |
| `session_length_in_minutes` | Duration of the session                            |
| `keep_alive_session`        | Whether the session was kept alive                 |


5. Device & Account-Linkage Signals

| Feature                     | What it represents                                                |
| --------------------------- | ----------------------------------------------------------------- |
| `device_os`                 | Operating system of the device                                    |
| `device_distinct_emails_8w` | Number of distinct emails associated with the device over 8 weeks |
| `device_fraud_count`        | Historical fraud count associated with the device                 |


6. Request / Payment / Channel Information

| Feature                  | What it represents             |
| ------------------------ | ------------------------------ |
| `payment_type`           | Payment mechanism              |
| `intended_balcon_amount` | Intended balance/amount        |
| `foreign_request`        | Whether the request is foreign |
| `source`                 | Request source/channel         |


7. Temporal Information

| Feature | What it represents              |
| ------- | ------------------------------- |
| `month` | Month/time period of the record |



--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


| Category                        | Number of features |
| ------------------------------- | -----------------: |
| Customer & Demographic Profile  |                  7 |
| Identity & Contact Verification |                  5 |
| Address & Banking History       |                  4 |
| Behavioral & Velocity Signals   |                  7 |
| Device & Account-Linkage        |                  3 |
| Request / Payment / Channel     |                  4 |
| Temporal Information            |                  1 |
| **Total**                       |             **31** |



--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



