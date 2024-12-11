import numpy as np
from tqdm import tqdm
from sklearn.ensemble import RandomForestRegressor


def are_all_features_non_eo(features):
    """
    Check if all the features non eo features

    Args:
        feature:

    Returns:

    """
    non_eo_features = ['Median Yield (tn per ha)',
                       'Analogous Year',
                       'Analogous Year Yield',
                       'lon',
                       'lat',
                       't -1 Yield (tn per ha)',
                       't -2 Yield (tn per ha)',
                       't -3 Yield (tn per ha)',
                       't -4 Yield (tn per ha)',
                       't -5 Yield (tn per ha)']

    # Check if all features are non-eo features, return True if they are
    return all(feature in non_eo_features for feature in features)


def select_features(X, y, method="RFE", min_features_to_select=3, threshold_nan=0.2, threshold_unique=0.6):
    """

    Args:
        X:
        y:
        method:
        min_features_to_select:
        threshold_unique:

    Returns:

    """

    # df = X.copy()
    #
    # # Initialize and apply StandardScaler
    # scaler = StandardScaler()
    # scaled_data = scaler.fit_transform(df)
    #
    # # Initialize and apply VarianceThreshold
    # # Note: Since data is standardized, all features now have variance of 1 before applying VarianceThreshold.
    # # You would adjust the threshold based on new criteria since variances have been normalized.
    # selector = VarianceThreshold(threshold=scaled_data.var().mean())
    # X = selector.fit_transform(scaled_data)
    selector = None
    X_original = X.copy()

    # Calculate the proportion of NaN values in each column
    nan_proportion = X.isna().mean()

    # Drop columns where more than 20% of the values are NaN
    X = X.loc[:, nan_proportion <= threshold_nan]

    # Fill in columns with median of that column
    X = X.fillna(X.median())

    # Calculate the proportion of unique values in each column
    unique_proportion = X.nunique() / len(X)

    # Filter columns that have at least 60% unique values
    columns_to_keep = unique_proportion[unique_proportion >= threshold_unique].index

    # Drop columns that do not meet the threshold
    X = X[columns_to_keep]

    # Define the RandomForestRegressor
    forest = RandomForestRegressor(
        n_estimators=500,
        n_jobs=8,
        max_depth=5,
        random_state=1,
    )

    # Adjusting numpy types due to deprecation warnings or errors
    np.int = np.int32
    np.float = np.float64
    np.bool = np.bool_

    if method == "SHAP":
        import pandas as pd
        from catboost import CatBoostRegressor
        from fasttreeshap import TreeExplainer as FastTreeExplainer
        from sklearn.model_selection import cross_val_score

        model = CatBoostRegressor(n_estimators=500, verbose=0, use_best_model=False)
        model.fit(X, y)

        explainer = FastTreeExplainer(model)
        shap_values = explainer.shap_values(X)

        # Step 5: Summarize the SHAP values for feature importance
        shap_importances = np.mean(np.abs(shap_values), axis=0)
        shap_importance_df = pd.DataFrame(
            {"feature": X.columns, "importance": shap_importances}
        ).sort_values(by="importance", ascending=False)

        def evaluate_model_with_n_features(N, X_train, y_train):
            top_features = shap_importance_df["feature"].head(N).values
            X_train_selected = X_train[top_features]
            selector = CatBoostRegressor(n_estimators=500, random_state=42, verbose=0)
            scores = cross_val_score(
                selector,
                X_train_selected,
                y_train,
                cv=5,
                scoring="neg_mean_squared_error",
                n_jobs=-1,
            )

            return np.mean(scores)

        # Evaluate model performance with different number of features
        nrange = [5, 10, 15, 20, 25, 30]
        cv_scores = []
        for N in tqdm(nrange):
            cv_scores.append(evaluate_model_with_n_features(N, X, y))

        # Select the number of features that gives the best cross-validation score (lowest MSE)
        optimal_N = nrange[np.argmax(cv_scores)]

        # Use optimal N to select features
        selected_features = (
            shap_importance_df["feature"].head(optimal_N).values.tolist()
        )
    elif method == "feature_engine":
        from feature_engine.selection import SmartCorrelatedSelection

        selector = SmartCorrelatedSelection(
            method="pearson",
            threshold=0.7,
            selection_method="model_performance",
            estimator=forest,
            scoring="neg_mean_squared_error",
        )

        X_filtered = selector.fit_transform(X, y)
        selected_features = X_filtered.columns.tolist()
    elif method == "mrmr":
        from mrmr import mrmr_regression

        try:
            selected_features = mrmr_regression(X=X, y=y, K=10)
        except:
            breakpoint()
        # combine X and y into a dataframe
        # df = pd.concat([X, y], axis=1)

    elif method == "RFECV":
        from sklearn.feature_selection import RFECV
        from sklearn.model_selection import KFold

        # Initialize a k-fold cross-validation strategy
        cv = KFold(n_splits=5)

        # Patch the scoring function to add a progress bar
        class RFECVWithProgress(RFECV):
            def _fit(self, X, y):
                from tqdm import tqdm

                n_features = X.shape[1]
                with tqdm(total=n_features) as pbar:

                    def patched_scorer(*args, **kwargs):
                        pbar.update(1)
                        return self.scorer_(*args, **kwargs)

                    self.scorer_ = patched_scorer
                    super()._fit(X, y)

        # Initialize RFECV with the estimator and cross-validation strategy
        selector = RFECVWithProgress(
            estimator=forest, step=1, n_jobs=-1, cv=cv, scoring="neg_mean_squared_error"
        )
        selector.fit(X, y)
        # Get the selected feature indices
        selected_features = selector.get_support(indices=True)

        # Get the selected feature names
        selected_features = X.columns[selected_features].tolist()
    elif method == "BorutaPy":
        from boruta import BorutaPy

        selector = BorutaPy(forest, n_estimators="auto", random_state=42)
        selector.fit(X.values, y.values)
        selected_features_mask = selector.support_
        selected_features = X.columns[selected_features_mask].tolist()
        tentative_features = X.columns[selector.support_weak_].tolist()

        selected_features = selected_features + tentative_features
    elif method == "Leshy":
        import arfs.feature_selection.allrelevant as arfsgroot
        from catboost import CatBoostRegressor

        model = CatBoostRegressor(n_estimators=350, verbose=0, use_best_model=False)
        selector = arfsgroot.Leshy(
            model,
            n_estimators="auto",
            verbose=1,
            max_iter=10,
            random_state=42,
            importance="fastshap",
        )
        selector.fit(X, y, sample_weight=None)

        selected_features = selector.get_feature_names_out()
        # feat_selector.plot_importance(n_feat_per_inch=5)
    elif method == "PowerShap":
        from powershap import PowerShap
        from catboost import CatBoostRegressor

        selector = PowerShap(
            model=CatBoostRegressor(n_estimators=500, verbose=0, use_best_model=True),
            power_alpha=0.05,
        )

        selector.fit(X, y)  # Fit the PowerShap feature selector
        selector.transform(X)  # Reduce the dataset to the selected features
    elif method == "BorutaShap":
        from BorutaShap import BorutaShap
        from catboost import CatBoostRegressor

        hyperparams = {
            "depth": 6,
            "learning_rate": 0.05,
            "iterations": 500,
            "subsample": 1.0,
            "random_strength": 0.5,
            "reg_lambda": 0.001,
            "loss_function": "RMSE",
            "early_stopping_rounds": 25,
            "random_seed": 42,
            "verbose": False,
        }
        model = CatBoostRegressor(**hyperparams)

        selector = BorutaShap(
            model=model, importance_measure="shap", classification=False
        )
        selector.fit(
            X=X,
            y=y,
            n_trials=100,
            sample=False,
            train_or_test="test",
            normalize=True,
            verbose=False,
        )
        selected_features_mask = selector.Subset().columns
        selected_features = X[selected_features_mask].columns.tolist()
    elif method == "Genetic":
        from sklearn_genetic import GAFeatureSelectionCV

        selector = GAFeatureSelectionCV(
            estimator=forest,
            cv=5,
            verbose=1,
            scoring="neg_mean_squared_error",
            max_features=max(len(X.columns) // 3, min_features_to_select),
            population_size=100,
            generations=40,
            crossover_probability=0.9,
            mutation_probability=0.1,
            keep_top_k=2,
            elitism=True,
            n_jobs=-1,
        )
        selector.fit(X, y)
        selected_features_mask = selector.support_
        selected_features = X.columns[selected_features_mask].tolist()
    elif method == "RFE":
        from sklearn.feature_selection import RFE

        selector = RFE(
            forest, n_features_to_select=min_features_to_select, step=1, verbose=1
        )
        selector = selector.fit(X, y)
        selected_features_mask = selector.support_
        selected_features = X.columns[selected_features_mask].tolist()
    else:
        raise ValueError("Method not recognized. Use BorutaPy, Genetic, or RFE")
    # tentative_features = X.columns[selector.support_weak_].tolist()

    non_eo = are_all_features_non_eo(selected_features)
    if non_eo or method == "SelectKBest":
        from sklearn.feature_selection import SelectKBest, f_regression

        k = 15  # Number of features to select
        selector = SelectKBest(score_func=f_regression, k=k)

        # Fit the selector to the data and transform the data to select the best features
        try:
            X_new = selector.fit_transform(X, y)
        except:
            breakpoint()

        # Get the selected feature indices
        selected_features = selector.get_support(indices=True)

        # Get the selected feature names
        selected_features = X.columns[selected_features].tolist()

    # print(selected_features)
    # Filter the dataset for selected features
    X_filtered = X.loc[:, selected_features]

    return selector, X_filtered, selected_features
