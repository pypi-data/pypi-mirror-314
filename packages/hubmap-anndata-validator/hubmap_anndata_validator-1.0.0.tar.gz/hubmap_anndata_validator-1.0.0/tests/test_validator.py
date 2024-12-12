import pytest
import anndata
import numpy as np
import pandas as pd
import scipy.sparse as sp
from anndata_validator import validate_anndata


def test_validate_anndata_valid():
    obs = pd.DataFrame({"original_obs_id": ["A", "B", "C"], "object_type": ["cell", "nucleus", "cell"]}, index=["A", "B", "C"])
    var = pd.DataFrame(index=["gene1", "gene2", "gene3"])
    X = sp.random(3, 3, density=0.1, format="csr")
    adata = anndata.AnnData(X=X, obs=obs, var=var)
    adata.uns['protocol'] = "DOI:whatever/protocol"

    try:
        validate_anndata(adata)
    except ValueError as e:
        pytest.fail(f"Unexpected ValueError: {e}")


def test_validate_anndata_missing_columns():
    obs = pd.DataFrame({"extra_column": ["A", "B", "C"]}, index=["A", "B", "C"])
    var = pd.DataFrame(index=["gene1", "gene2", "gene3"])
    X = sp.random(3, 3, density=0.1, format="csr")
    adata = anndata.AnnData(X=X, obs=obs, var=var)
    adata.uns['protocol'] = "DOI:whatever/protocol"

    with pytest.raises(ValueError, match="must contain a column named 'original_obs_id'"):
        validate_anndata(adata)


def test_validate_anndata_duplicate_indices():
    obs = pd.DataFrame({"original_obs_id": ["A", "B", "B"], "object_type": ["cell", "nucleus", "cell"]}, index=["A", "B", "B"])
    var = pd.DataFrame(index=["gene1", "gene2", "gene3"])
    X = sp.random(3, 3, density=0.1, format="csr")
    adata = anndata.AnnData(X=X, obs=obs, var=var)
    adata.uns['protocol'] = "DOI:whatever/protocol"

    with pytest.raises(ValueError, match="Found duplicate object IDs"):
        validate_anndata(adata)


def test_validate_anndata_dense_matrix_warns():
    obs = pd.DataFrame({"original_obs_id": ["A", "B", "C"], "object_type": ["cell", "nucleus", "cell"]}, index=["A", "B", "C"])
    var = pd.DataFrame(index=["gene1", "gene2", "gene3"])
    X = np.ones((3, 3))  # Dense matrix
    adata = anndata.AnnData(X=X, obs=obs, var=var)
    adata.uns['protocol'] = "DOI:whatever/protocol"

    with pytest.warns(UserWarning, match="is a dense matrix with sparsity"):
        validate_anndata(adata)


def test_validate_anndata_unused_columns_and_keys():
    obs = pd.DataFrame({
        "original_obs_id": ["A", "B", "C"],
        "object_type": ["cell", "nucleus", "cell"],
        "unused_column": [1, 2, 3],
    }, index=["A", "B", "C"])
    var = pd.DataFrame(index=["gene1", "gene2", "gene3"])
    X = sp.random(3, 3, density=0.1, format="csr")
    obsm = {"X_unused": np.zeros((3, 2))}
    adata = anndata.AnnData(X=X, obs=obs, var=var, obsm=obsm)
    adata.uns['protocol'] = "DOI:whatever/protocol"
    
    with pytest.warns(UserWarning, match="Unused .obs columns: unused_column"):
        validate_anndata(adata)



def test_validate_anndata_missing_protocol():
    obs = pd.DataFrame({"original_obs_id": ["A", "B", "C"], "object_type": ["cell", "nucleus", "cell"]}, index=["A", "B", "C"])
    var = pd.DataFrame(index=["gene1", "gene2", "gene3"])
    X = sp.random(3, 3, density=0.1, format="csr")
    adata = anndata.AnnData(X=X, obs=obs, var=var)

    with pytest.raises(ValueError, match="`.uns` must contain a key 'protocol'"):
        validate_anndata(adata)


def test_validate_anndata_missing_annotation_methods():
    obs = pd.DataFrame({"original_obs_id": ["A", "B", "C"], "object_type": ["cell", "nucleus", "cell"]}, index=["A", "B", "C"])
    var = pd.DataFrame(index=["gene1", "gene2", "gene3"])
    X = sp.random(3, 3, density=0.1, format="csr")
    obsm = {"annotation": np.array([[1, 2], [3, 4], [5, 6]])}
    adata = anndata.AnnData(X=X, obs=obs, var=var, obsm=obsm)
    adata.uns['protocol'] = "DOI:whatever/protocol"

    with pytest.raises(ValueError, match="`.obsm\\['annotation'\\]` exists, but `.uns\\['annotation_methods'\\]` is missing"):
        validate_anndata(adata)


def test_validate_anndata_valid_X_spatial():
    obs = pd.DataFrame({"original_obs_id": ["A", "B", "C"], "object_type": ["cell", "nucleus", "cell"]}, index=["A", "B", "C"])
    var = pd.DataFrame(index=["gene1", "gene2", "gene3"])
    X = sp.random(3, 3, density=0.1, format="csr")
    obsm = {"X_spatial": np.array([[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]])}
    adata = anndata.AnnData(X=X, obs=obs, var=var, obsm=obsm)
    adata.uns['protocol'] = "DOI:whatever/protocol"

    try:
        validate_anndata(adata)
    except ValueError as e:
        pytest.fail(f"Unexpected ValueError: {e}")


def test_validate_anndata_missing_X_embedding_warns():
    obs = pd.DataFrame({"original_obs_id": ["A", "B", "C"], "object_type": ["cell", "nucleus", "cell"]}, index=["A", "B", "C"])
    var = pd.DataFrame(index=["gene1", "gene2", "gene3"])
    X = sp.random(3, 3, density=0.1, format="csr")
    obsm = {"X_umap": np.array([[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]])}
    adata = anndata.AnnData(X=X, obs=obs, var=var, obsm=obsm)
    adata.uns['protocol'] = "DOI:whatever/protocol"

    with pytest.warns(UserWarning, match="Found the following embeddings but not 'X_embedding'"):
        validate_anndata(adata)
