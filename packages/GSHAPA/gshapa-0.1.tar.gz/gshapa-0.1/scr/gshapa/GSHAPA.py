from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import pandas as pd
from tqdm.autonotebook import tqdm
from statsmodels.distributions.empirical_distribution import ECDF
from statsmodels.stats.multitest import multipletests
from sklearn.model_selection import GridSearchCV,StratifiedKFold,train_test_split
import fasttreeshap
from tqdm.autonotebook import tqdm

RANDOM_STATE = 0
MODEL = RandomForestClassifier(random_state=RANDOM_STATE,
                               max_features=1./2,
                               ccp_alpha=0.01,n_estimators=1000,n_jobs=-1)

TEST_SET_SIZE = 0.2



class GSHAPA3:
    """
    Class representing the GSHAPA method

    Attributes:
        model (sklearn.base.BaseEstimator): Scikit-learn ML tree-based model used to learn to predict an phenotype (e.g., disease) from gene expression
        test_set_size (float): Relative size for test set
    """
    def __init__(self,
                 model=MODEL,
                 test_set_size=TEST_SET_SIZE,
                 random_state = RANDOM_STATE
                ):
        """
        Constructor for GSHAPA object.

        Args:
            model (sklearn.base.BaseEstimator): Scikit-learn ML model used to learn to predict an phenotype (e.g., disease) from gene expression
            test_set_size (float): Relative size for test set
            random_state (int): Random seed
        """
        self.model = model
        self.test_set_size = test_set_size
        self.random_state = random_state

    def fit(self, X, y):
        """
        Splits dataset into train and test and fits the ML model

        Args:
            X (array-like) : The training input samples matrix of shape (n_samples, n_features) 
            y (pd.Series or np.array) : The target values (e.g., class labels) as integers/strings (classification) or floats (regression)
        """
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X,
                                                                                y,
                                                                                shuffle=True,
                                                                                stratify=y,
                                                                                test_size=self.test_set_size,
                                                                                random_state = self.random_state,
                                                                               )
        self.model.fit(self.X_train,self.y_train)
        
    def shap(self,X_explain=None,**fasttreeshap_TreeExplainer_params):
        """
        Compute SHAP values

        Args:
            X_explain (array-like) : The explanation target samples matrix of shape (n_samples_to_explain, n_features).
            fasttreeshap_TreeExplainer_params (dict) : Parameters for fasttreeshap.TreeExplainer
        """
        self.X_explain = X_explain
        self.explainer = fasttreeshap.TreeExplainer(self.model,
                                                    **fasttreeshap_TreeExplainer_params,
                                                   )
        self.SHAP_values = self.explainer(self.X_explain,check_additivity=False)
        self.SHAP_values = self.SHAP_values

    def compute_target_global_gene_enrichment_score(self, target_class):
        """
        Compute the average (global) gene-level enrichment scores for X_explain objects and the class of interest (in the case of regression the target_class param is ignored)

        Args:
            target_class (int or str) : label for the class for which the gene global enrichment scores should be computed

        Returns:
            pd.Series: gene-level global enrichment scores (i.e. average of absolute SHAP values)
        """
        if len(self.SHAP_values.shape) == 3:# i.e., rows , columns , classes
            # It is a classification task
            index_target_class = list(self.model.classes_).index(target_class)
            shap_values_interest = pd.DataFrame(self.SHAP_values.values[:,:,index_target_class],
                                                index=self.X_explain.index,
                                                columns=self.X_explain.columns)
        else:# i.e., just rows and columns
            # otherwise it is a regression task
            shap_values_interest = pd.DataFrame(self.SHAP_values.values,
                                                index=self.X_explain.index,
                                                columns=self.X_explain.columns)
        global_gene_enrichment_score = np.abs(shap_values_interest).mean()
        
        return global_gene_enrichment_score
 
    def pval_gene_set_enrichment(self, global_gene_enrichment_score, set_of_genes, n_tests=10000):
        """
        By permutation generates an empirical distribution of global enrichment scores for gene sets with the same gene set size, and assess p-value of enrichment 

        Args:
            global_gene_enrichment_score (pd.Series): global gene enrichment scores produced by function compute_target_global_gene_enrichment_score
            set_of_genes (list): list of gene ids in the gene set
            n_tests (int): number of permutations to run

        Returns:
            gene set level enrichment score (i.e. sum of enrichment scores of its genes)
            float: corresponding enrichment pvalue 
        """
        def sampling(x, size, n_tests):
            return np.random.choice(x.values,[size,n_tests]).sum(axis=0)

        gene_set_global_enrichment_score = global_gene_enrichment_score[set_of_genes].sum()
        nb_genes = len(set_of_genes)
        if len(set_of_genes) > 0:
            sample = sampling(global_gene_enrichment_score, nb_genes, n_tests)
            ecdf = ECDF(sample)
            p = ecdf(gene_set_global_enrichment_score)
            pvalue = 1-p#one sided since only high shap values are considered as interesting
        else:
            pvalue = 1
        return gene_set_global_enrichment_score, pvalue

    def explain_gene_sets(self, 
                          gene_sets, 
                          target_class, 
                          n_tests=1000, 
                          alpha=0.01, 
                          multiple_test_method="bonferroni",
                          ):
        """
        Computes multiple gene set enrichment scores, estimates their statistical significance and apply a multiple test correction

        Params:
            gene_sets (dict): the name of the gene sets are keys and the values are the lists with the genes'ids in each gene set 
            target_class (int or str) : label for the class for which the gene global enrichment scores should be computed (if regression this is ignored)
            n_tests (int): number of permutations to run
            alpha (float): threshold of significance
            method (str): multiple test correction method from statsmodels.stats.multitest.multipletests

        Returns:
            pd.DataFrame: Each row is a gene set and columnns represent 1) the enrichment scores, 2) P-values, 3 Corrected P-values
        """
        global_gene_enrichment_score = self.compute_target_global_gene_enrichment_score(target_class)
        genesets_shap = {}
        genesets_shap_pvals = {}

        for g_s in tqdm(gene_sets):
            genes = list(set(gene_sets[g_s]).intersection(self.X_explain.columns))
            shapvalues,pval = self.pval_gene_set_enrichment(global_gene_enrichment_score,
                                           genes, 
                                           n_tests)
            genesets_shap_pvals[g_s] = pval
            genesets_shap[g_s] = shapvalues
        genesets_shap_pvals = pd.Series(genesets_shap_pvals)
        reject,pvals_corrected,alpha_sidak,alpha_bonf = multipletests(genesets_shap_pvals.values.flatten(),
                                                                      alpha=alpha, 
                                                                      method=multiple_test_method,
                                                                      is_sorted=False, 
                                                                      returnsorted=False)
        genesets_shap_pvals_corrected = pvals_corrected.reshape(genesets_shap_pvals.shape)
        genesets_shap_pvals_corrected = pd.Series(genesets_shap_pvals_corrected,
                                                  index=genesets_shap_pvals.index)
        genesets_shap = pd.Series(genesets_shap)
        res = pd.DataFrame({"SHAP values":genesets_shap,
                            "P-values":genesets_shap_pvals,
                            "corrected P-values":genesets_shap_pvals_corrected})
        return res.sort_values("SHAP values",ascending=False)
