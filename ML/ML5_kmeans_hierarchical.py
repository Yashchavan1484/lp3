"""ML5: K-Means (elbow method) and hierarchical clustering on sales_data_sample.csv.
Dataset: data/sales_data_sample.csv (https://www.kaggle.com/datasets/kyanyoga/sample-sales-data)
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # remove this line if you want plot windows
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("data/sales_data_sample.csv", encoding="latin1")
print(df.head(), "\n")

# numeric features used for segmentation
features = ["QUANTITYORDERED", "PRICEEACH", "SALES", "MSRP"]
X = df[features].dropna()
X_scaled = StandardScaler().fit_transform(X)

# ---------- Elbow method ----------
wcss = []
ks = range(1, 11)
for k in ks:
    wcss.append(KMeans(n_clusters=k, n_init=10, random_state=42).fit(X_scaled).inertia_)
plt.figure()
plt.plot(ks, wcss, "bo-")
plt.xlabel("Number of clusters (k)")
plt.ylabel("WCSS (inertia)")
plt.title("Elbow method")
plt.savefig("ml5_elbow.png")

K = 3  # choose from the elbow plot
km = KMeans(n_clusters=K, n_init=10, random_state=42).fit(X_scaled)
X = X.copy()
X["KMeans_Cluster"] = km.labels_
print(f"K-Means (k={K}) silhouette score:", round(silhouette_score(X_scaled, km.labels_), 4))
print(X.groupby("KMeans_Cluster").mean().round(2), "\n")

plt.figure()
plt.scatter(X_scaled[:, 0], X_scaled[:, 2], c=km.labels_, cmap="viridis", s=15)
plt.xlabel("QUANTITYORDERED (scaled)")
plt.ylabel("SALES (scaled)")
plt.title("K-Means clusters")
plt.savefig("ml5_kmeans_clusters.png")

# ---------- Hierarchical clustering ----------
sample = X_scaled[:300]  # dendrogram on a subset for readability
plt.figure(figsize=(10, 5))
dendrogram(linkage(sample, method="ward"))
plt.title("Dendrogram (first 300 rows)")
plt.savefig("ml5_dendrogram.png")

hc = AgglomerativeClustering(n_clusters=K, linkage="ward").fit(X_scaled)
print(f"Hierarchical (k={K}) silhouette score:", round(silhouette_score(X_scaled, hc.labels_), 4))
