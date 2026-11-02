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

# This program does customer/order segmentation (unsupervised learning). It uses K-Means with the elbow method, and Hierarchical (Agglomerative) clustering with a dendrogram. I can’t see your output, so the results table is blank for you to fill in.

# Viva points:

# K = 3 is fixed by hand (“choose from the elbow plot”). Be ready to point at the bend in your ml5_elbow.png.
# The dendrogram uses only the first 300 rows, so it shows a sample, not the whole data.
# matplotlib.use("Agg") means plots are saved as PNG files and not shown in a window.
    
# Aim
# To group sales records into clusters using K-Means (with the elbow method to choose k) and Hierarchical clustering, and compare them using the silhouette score.

# Theory
# This is unsupervised learning: there is no target column, and the algorithm finds groups on its own.
# Features used: QUANTITYORDERED, PRICEEACH, SALES and MSRP (4 numeric columns).
# K-Means: pick k centroids, assign each point to its nearest centroid, move each centroid to the mean of its points, and repeat until nothing changes.
# WCSS (inertia): the sum of squared distances from each point to its own centroid. It always decreases as k increases.
# Elbow method: plot WCSS against k and pick the k where the curve bends, after which adding clusters gives little gain.
# Hierarchical (agglomerative) clustering: start with every point as its own cluster and repeatedly merge the two closest clusters, building a tree.
# Dendrogram: the tree diagram of the merges. Cutting it at a chosen height gives the clusters.
# Ward linkage: merges the pair of clusters that increases the total within-cluster variance the least.
# Silhouette score: measures how well each point fits its own cluster compared with the nearest other cluster. It ranges from −1 to +1, and closer to 1 is better.
# Scaling is essential: SALES (thousands) would dominate PRICEEACH (tens), so StandardScaler is applied first.

# Steps (matches your code)
# Load the CSV (encoding="latin1" because of special characters).
# Select the 4 numeric features and drop missing rows.
# Standardize the features.
# Run K-Means for k = 1 to 10 and store the WCSS for each.
# Plot the elbow curve and choose K = 3.
# Fit the final K-Means, print the silhouette score and the mean of each feature per cluster, and plot the clusters.
# Draw the dendrogram on 300 rows with Ward linkage.
# Fit Agglomerative clustering with 3 clusters and print its silhouette score.

# 1. Pipeline summary

# markdown
# | Step | Operation                                   | Purpose                                         |
# |------|---------------------------------------------|-------------------------------------------------|
# | 1    | Load CSV with latin1 encoding               | Read the sales records                          |
# | 2    | Select 4 numeric features, drop NaN         | Choose the inputs for clustering                |
# | 3    | StandardScaler                              | Put all features on the same scale              |
# | 4    | K-Means for k = 1 to 10, store WCSS         | Data for the elbow plot                         |
# | 5    | Choose K = 3 from the elbow                 | Pick the number of clusters                     |
# | 6    | Fit K-Means, silhouette, cluster means      | Evaluate and describe the clusters              |
# | 7    | Scatter plot (quantity vs sales)            | Visualize the clusters                          |
# | 8    | Dendrogram on first 300 rows (Ward)         | Show the hierarchical merge structure           |
# | 9    | Agglomerative clustering with 3 clusters    | Compare with K-Means using silhouette           |

# 2. K-Means algorithm steps

# markdown
# | Step | Action                                            |
# |------|---------------------------------------------------|
# | 1    | Choose k and place k initial centroids            |
# | 2    | Assign every point to its nearest centroid        |
# | 3    | Recompute each centroid as the mean of its points |
# | 4    | Repeat steps 2 and 3 until centroids stop moving  |

# 3. Mini K-Means example (1D points 1, 2, 3, 10, 11, 12 with k = 2, starting centroids 1 and 10)

# markdown
# | Iteration | Centroid 1 | Centroid 2 | Cluster 1 points | Cluster 2 points | New centroids |
# |-----------|------------|------------|------------------|------------------|---------------|
# | 1         | 1          | 10         | 1, 2, 3          | 10, 11, 12       | 2 and 11      |
# | 2         | 2          | 11         | 1, 2, 3          | 10, 11, 12       | 2 and 11 (no change, stop) |

# WCSS = (1² + 0² + 1²) + (1² + 0² + 1²) = 4

# 4. Mini hierarchical example (points A=1, B=2, C=6, D=7, E=20)

# markdown
# | Merge | Clusters joined | Reason                            | Clusters left        |
# |-------|-----------------|-----------------------------------|----------------------|
# | 1     | A + B           | Closest pair (distance 1)         | {A,B}, C, D, E       |
# | 2     | C + D           | Next closest pair (distance 1)    | {A,B}, {C,D}, E      |
# | 3     | {A,B} + {C,D}   | Closer to each other than to E    | {A,B,C,D}, E         |
# | 4     | {A,B,C,D} + E   | Last merge, very large distance   | One cluster          |

# Cutting the tree before merge 3 gives 3 clusters: {A,B}, {C,D}, {E}.

# 5. Metrics

# markdown
# | Metric           | Meaning                                                      | Better value                 |
# |------------------|--------------------------------------------------------------|------------------------------|
# | WCSS (inertia)   | Sum of squared distances of points to their centroid         | Lower (but it always falls as k grows) |
# | Silhouette score | (b − a) / max(a, b), where a = distance to own cluster, b = distance to nearest other cluster | Closer to +1 |

# 6. Your results (fill from your output)

# markdown
# | Method                  | k | Silhouette score |
# |-------------------------|---|------------------|
# | K-Means                 | 3 |                  |
# | Hierarchical (Ward)     | 3 |                  |
# markdown
# | Cluster | QUANTITYORDERED (mean) | PRICEEACH (mean) | SALES (mean) | MSRP (mean) | Description (your words) |
# |---------|------------------------|------------------|--------------|-------------|--------------------------|
# | 0       |                        |                  |              |             |                          |
# | 1       |                        |                  |              |             |                          |
# | 2       |                        |                  |              |             |                          |

# 7. Complexity (n = rows ≈ 2800, d = 4 features, k = clusters, I = iterations)

# markdown
# | Part                          | Time Complexity          | Space Complexity | Reason                                                   |
# |-------------------------------|--------------------------|------------------|----------------------------------------------------------|
# | Scaling                       | O(n·d)                   | O(n·d)           | One pass over the data                                   |
# | K-Means (one run)             | O(n·k·d·I)               | O(n·d + k·d)     | Each iteration measures n distances to k centroids       |
# | Elbow loop (10 values of k, 10 starts each) | About 100 × K-Means cost | O(n·d) | Repeats K-Means for every k and every start              |
# | Hierarchical (Ward)           | O(n²) to O(n² log n)     | O(n²)            | Needs pairwise distances between all points              |
# | Dendrogram (300 rows)         | O(300²)                  | O(300²)          | Small, which is why a sample is used                     |
# | Silhouette score              | O(n²·d)                  | O(n)             | Compares every point with every other point              |

# 8. K-Means vs Hierarchical

# markdown
# | Point                     | K-Means                                  | Hierarchical (Agglomerative)                  |
# |---------------------------|------------------------------------------|-----------------------------------------------|
# | Need k beforehand?        | Yes (use the elbow method)               | No, cut the dendrogram at any level           |
# | Approach                  | Centroid-based, iterative                | Tree-based, merges the closest clusters       |
# | Time                      | O(n·k·d·I), fast and scalable            | O(n²) or worse, slow for large n              |
# | Memory                    | Low                                      | High (distance matrix)                        |
# | Result each run           | Can vary with initial centroids          | Always the same (deterministic)               |
# | Cluster shape             | Round, similar-sized clusters            | Flexible, depends on linkage                  |
# | Visualization             | Scatter plot                             | Dendrogram shows the full hierarchy           |
# | Outliers                  | Sensitive (they pull centroids)          | Sensitive                                     |
# | Best for                  | Large datasets                           | Small datasets, when structure matters        |
# Why use both here (and an honest note)
# K-Means is fast and simple, so it suits about 2800 rows and is easy to explain with the elbow plot.
# Hierarchical clustering needs no k up front, and the dendrogram shows how clusters join, which is a useful check on the choice of k = 3.
# Comparing the silhouette scores gives a number to say which clustering separates the data better. Say honestly that the higher one fits better on this data, and avoid claiming a winner before you see your output.
# Honest points for the viva: SALES is roughly QUANTITYORDERED × PRICEEACH, and MSRP is related to price, so the features are correlated. That means the clusters are mostly driven by order size and product price. The elbow is often not sharp, so the choice of k = 3 is a judgment call.
# Easy example

# Imagine a shop owner sorting customers into groups without being told the groups.

# K-Means: place 3 flags on the map of customers, let each customer walk to the nearest flag, then move each flag to the middle of its crowd. Repeat until the flags stop moving.
# Hierarchical: start with every customer alone, and keep joining the two most similar customers or groups, like a family tree built from the bottom up. Cut the tree where you want 3 groups.
