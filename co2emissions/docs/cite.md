### 1. **Nguyen, Q., Diaz-Rainey, I., and Kuruppuarachchi, D.** (2021) *Predicting corporate carbon footprints for climate finance risk analyses: A machine learning approach.* Energy Economics, 95:105129, 2021. ISSN 0140-9883. https://www.sciencedirect.com/science/article/pii/S0140988321000347.
- **Notes:**
    - 13,435 observations from 2,289 global companies are used to train six base models: ordinary least square regression, elastic network, neural network, K-nearest neighbour, random forest, and extreme gradient boosting. Then the estimates of the six base models are ensembled to generate the final estimate.
    - Best models (based off $R^2$ metric): gradient boosting and an elastic net meta-learner
- **Limitations:**
    - Only predicts aggregated scope 1/2 emissions
    - Only predicts 1 point; no future forecasting

### 2. **Han, Y., Gopal, A., Ouyang, L., & Key, A.** (2021, September 9). *Estimation of corporate greenhouse gas emissions via machine learning*. arXiv.org. https://arxiv.org/abs/2109.04318
- **Notes:** 
    - "Our machine learning model uses Gradient Boosting Decision Trees for Amortized Inference, Recalibration using Normalizing Flows, and Patterned Dropout for regularization. More specifically, we employ a two-phase model: first, a decision tree is used to map from features to Gamma distributions, and then a normalizing flow is used to transform the Gamma distributions to a more flexible class of distributions."
    - Need a model that can handle: non-linearity in the marginals, correlations, stability, interpretability, missing values, and categorical features
    - Gradient boosting trees are chosen over linear models and NNs since they are not only able to capture complex non-linear relationships, but also more stable and explainable than NNs
- **Limitations:**