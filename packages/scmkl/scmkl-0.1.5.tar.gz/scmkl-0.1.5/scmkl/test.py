import numpy as np
import sklearn


def predict(adata, metrics = None, return_probs = False):
    '''
    Function to return predicted labels and calculate any of AUROC, 
    Accuracy, F1 Score, Precision, Recall for a classification. 
    
    Parameters
    ----------  
    **adata** : *AnnData*
        > Has keys `'model'`, `'Z_train'`, and `'Z_test'` in 
        `adata.uns`.

    **metrics** : *list[str]* | *None*
        > Which metrics to calculate on the predicted values. Options
        are `'AUROC'`, `'Accuracy'`, `'F1-Score'`, `'Precision'`, and 
        `'Recall'`.

    **return_probs** : *bool*
        > If `True`, will return a dictionary with class probabilities.

    Returns
    -------
    **y_pred** : *np.ndarray*
        > Predicted cell classes.

    **metrics_dict** : *dict*
        > Contains `'AUROC'`, `'Accuracy'`, `'F1-Score'`, 
        `'Precision'`, and/or `'Recall'` keys depending on metrics 
        argument.

    **probs** : *dict*
        > If `return_probs` is `True`, will return a dictionary with 
        probabilities for each class in `y_test`.

    Examples
    --------
    >>> adata = scmkl.estimate_sigma(adata)
    >>> adata = scmkl.calculate_z(adata)
    >>> adata = scmkl.train_model(adata, metrics = ['AUROC', 'F1-Score', 
    ...                                             'Accuracy', 'Precision', 
    ...                                             'Recall'])
    >>>
    >>> metrics_dict = scmkl.predict(adata)
    >>> metrics_dict.keys()
    dict_keys(['AUROC', 'Accuracy', 'F1-Score', 'Precision', 'Recall'])
    '''
    y_test = adata.obs['labels'].iloc[adata.uns['test_indices']].to_numpy()
    X_test = adata.uns['Z_test']
    assert X_test.shape[0] == len(y_test), 'X and y must have the same number of samples'
    assert all([metric in ['AUROC', 'Accuracy', 'F1-Score', 'Precision', 'Recall'] for metric in metrics]), 'Unknown metric provided.  Must be one or more of AUROC, Accuracy, F1-Score, Precision, Recall'

    # Capturing class labels
    classes = np.unique(y_test)

    # Sigmoid function to force probabilities into [0,1]
    probabilities = 1 / (1 + np.exp(-adata.uns['model'].predict(X_test)))

    # Group Lasso requires 'continous' y values need to re-descritize it
    y = np.zeros((len(y_test)))
    y[y_test == classes[0]] = 1

    metric_dict = {}

    #Convert numerical probabilities into binary phenotype
    y_pred = np.array(np.repeat(classes[1], len(y_test)), dtype = 'object')
    y_pred[np.round(probabilities,0).astype(int) == 1] = classes[0]

    if (metrics == None) and (return_probs == False):
        return y_pred
    
    # Calculate and save metrics given in metrics
    if 'AUROC' in metrics:
        fpr, tpr, _ = sklearn.metrics.roc_curve(y, probabilities)
        metric_dict['AUROC'] = sklearn.metrics.auc(fpr, tpr)
    if 'Accuracy' in metrics:
        metric_dict['Accuracy'] = np.mean(y_test == y_pred)
    if 'F1-Score' in metrics:
        metric_dict['F1-Score'] = sklearn.metrics.f1_score(y_test, y_pred, pos_label = classes[0])
    if 'Precision' in metrics:
        metric_dict['Precision'] = sklearn.metrics.precision_score(y_test, y_pred, pos_label = classes[0])
    if 'Recall' in metrics:
        metric_dict['Recall'] = sklearn.metrics.recall_score(y_test, y_pred, pos_label = classes[0])

    if return_probs:
        probs = {classes[0] : probabilities,
                 classes[1] : 1 - probabilities}
        return y_pred, metric_dict, probs
    else:
        return y_pred, metric_dict


def find_selected_groups(adata) -> np.ndarray:
    '''
    Find feature groups selected by the model during training. If 
    feature weight assigned by the model is non-0, then the group 
    containing that feature is selected.

    Parameters
    ----------
    **adata** : *AnnData*
        > Has *celer.GroupLasso* object in `adata.uns['model']`.

    Returns
    -------
    **selected_groups** : *np.ndarray*
        > Array containing the names of the groups with nonzero kernel 
        weights.

    Examples
    --------
    >>> adata = scmkl.estimate_sigma(adata)
    >>> adata = scmkl.calculate_z(adata)
    >>> adata = scmkl.train_model(adata)
    >>>
    >>> selected_groups = scmkl.find_selected_groups(adata)
    >>> selected_groups
    np.ndarray(['HALLMARK_ESTROGEN_RESPONSE_EARLY', 'HALLMARK_HYPOXIA'])
    '''

    selected_groups = []
    coefficients = adata.uns['model'].coef_
    group_size = adata.uns['model'].get_params()['groups']
    group_names = np.array(list(adata.uns['group_dict'].keys()))

    # Loop over the model weights associated with each group and calculate the L2 norm.
    for i, group in enumerate(group_names):
        if not isinstance(group_size, (list, set, np.ndarray, tuple)):
            group_norm = np.linalg.norm(coefficients[np.arange(i * group_size, (i+1) * group_size - 1)])
        else: 
            group_norm = np.linalg.norm(coefficients[group_size[i]])

        # Only include the group if the model weights are > 0 
        if group_norm != 0:
            selected_groups.append(group)

    return np.array(selected_groups)
