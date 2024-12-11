from numpy.linalg import LinAlgError
from scipy.sparse import csr_matrix, lil_matrix
import itertools
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.svm import SVR, SVC, LinearSVC
import numpy as np
from sklearn.linear_model import LinearRegression



class NBCS(BaseEstimator, TransformerMixin):  # (BaseEstimator,RegressorMixin):

    def __init__(self, C=1, k=1, type="barry", tolerance=0.1):
        self.C = C
        self.k = k
        if type == "barry":
            self.fit = self.fit_barry
            self.tolerance = 3
        elif type == "adapt_class":
            self.fit = self.fit_adapt_class
            self.tolerance = 10
        elif type == "adapt_reg":
            self.fit = self.fit_adapt_reg
            self.tolerance = 0.1

    def add_point(self, point):
        index, r = self.find_point(point)
        self.list = np.concatenate((self.list, [point]))
        new = np.zeros(point.shape[0] + 1, dtype=int)
        combinations = np.array(list(itertools.combinations(self.indicies[index], point.shape[0])))
        for simplex in combinations:
            simplex = np.concatenate((simplex, [self.list.shape[0] - 1]))
            new = np.vstack((new, simplex))

        self.indicies = np.vstack((self.indicies, new[1:, :]))
        self.indicies = np.delete(self.indicies, index, 0)

    def transform(self, X):
        d = lil_matrix((X.shape[0], self.list.shape[0]))
        self.category = np.zeros(X.shape[0])
        for i in range(X.shape[0]):
            try:
                j, r = self.find_point(X[i, :])
                d[i, self.indicies[j]] = r
                self.category[i] = j
            except TypeError:
                print("type error:", i, X[i, :])
            except IndexError:
                print("index error:", i, X[i, :])
        return d

    def find_point(self, pts):
        "returns which simplex you belong to and with  coefficients"
        for j in range(self.indicies.shape[0]):
            h = np.vstack([self.list[self.indicies[j]].T, np.ones(len(pts) + 1)])
            s = np.append(pts, 1)
            try:
                r = np.linalg.solve(h, s)
            except LinAlgError:
                print(h, s)
            flag = 1
            for alpha in r:
                if alpha < -1e-3:
                    flag = 0
                    break
            if (flag == 1):
                return j, r

    def fit_barry(self, X, y=None):
        self.list = np.eye(X.shape[1]) * X.shape[1]
        self.list = np.vstack([np.zeros(X.shape[1]), self.list])
        # self.list = np.array([[0, 0], [0, 2], [2, 0]])
        self.indicies = np.array([np.arange(X.shape[1] + 1)])

        for itr in range(self.k):
            indicies = self.indicies[:]
            d = self.transform(X)

            for simplex in range(indicies.shape[0]):
                q = (self.category == simplex)
                if not any(q) or X[q].shape[0] < self.tolerance:
                    continue
                self.add_point(np.mean(self.list[indicies[simplex]], axis=0))
        return self

    def fit_adapt_class(self, X, y=None):
        svc = LinearSVC()
        self.list = np.eye(X.shape[1]) * X.shape[1]
        self.list = np.vstack([np.zeros(X.shape[1]), self.list])
        # self.list = np.array([[0, 0], [0, 2], [2, 0]])
        self.indicies = np.array([np.arange(X.shape[1] + 1)])
        for iter in range(self.k):
            indicies = self.indicies[:]
            d = self.transform(X)
            svc.fit(d, y)
            for simplex in range(indicies.shape[0]):
                q = (self.category == simplex)
                if not any(q):
                    continue
                X1 = X[q]
                y1 = y[q]
                d1 = d[q]
                p = (svc.predict(d1) != y1)
                if not any(p) or X1[p].shape[0] < self.tolerance:
                    continue
                self.add_point(np.mean(X1[p], axis=0))
        return self

    def fit_adapt_reg(self, X, y):
        clf = LinearRegression()
        self.list = np.eye(X.shape[1]) * X.shape[1]
        self.list = np.vstack([np.zeros(X.shape[1]), self.list])
        # self.list = np.array([[0, 0], [0, 2], [2, 0]])
        self.indicies = np.array([np.arange(X.shape[1] + 1)])
        for iter in range(self.k):
            indicies = self.indicies[:]
            d = self.transform(X)
            clf.fit(d, y)
            for simplex in range(indicies.shape[0]):
                q = (self.category == simplex)
                if not any(q):
                    continue
                X1 = X[q]
                y1 = y[q]
                d1 = d[q]
                p = np.argmin(y1 - clf.predict(d1))
                elem = X1[p]
                if any(np.linalg.norm(q - elem) < self.tolerance for q in self.list):
                    continue
                if np.isin(elem, self.list) or X1.shape[0] < 3:
                    continue
                self.add_point(elem)
        return self
