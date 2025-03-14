import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def load_data():
    """Load dataset from a CSV file (Mall Customer Segmentation dataset)."""
    url = "customer_data.csv"
    df = pd.read_csv(url)
    return df

def preprocess_data(df):
    """Select relevant features and standardize the data."""
    X = df[['Annual Income (k$)', 'Spending Score (1-100)']]
    
    # Standardizing the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X, X_scaled, scaler

def find_optimal_clusters(X_scaled, max_clusters=5):  # Reduce max_clusters
    n_samples = X_scaled.shape[0]
    
    if max_clusters > n_samples:
        max_clusters = n_samples  # Ensure max_clusters does not exceed available data points
    
    distortions = []
    for i in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=i, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        distortions.append(kmeans.inertia_)

    return distortions

def apply_kmeans(X_scaled, k):
    """Apply K-Means clustering with a given number of clusters."""
    kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    return kmeans, clusters

def visualize_clusters(df, X, clusters, kmeans, scaler):
    """Visualize the clustered data."""
    df['Cluster'] = clusters
    
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=df['Annual Income (k$)'], y=df['Spending Score (1-100)'], 
                    hue=df['Cluster'], palette='viridis', s=100)
    
    # De-normalizing cluster centers
    cluster_centers = kmeans.cluster_centers_ * scaler.scale_ + scaler.mean_
    
    plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1], 
                s=300, c='red', label='Centroids', marker='X')

    plt.xlabel('Annual Income (k$)')
    plt.ylabel('Spending Score (1-100)')
    plt.title('Customer Segmentation using K-Means')
    plt.legend()
    plt.show()

def main():
    """Main function to run the customer segmentation pipeline."""
    # Step 1: Load data
    df = load_data()
    
    # Step 2: Preprocess data
    X, X_scaled, scaler = preprocess_data(df)
    
    print(f"Number of samples in dataset: {X_scaled.shape[0]}")


    # Step 3: Find optimal clusters (run this first, then manually choose k)
    find_optimal_clusters(X_scaled)
    
    # Step 4: Apply K-Means clustering (choose k based on the elbow method)
    k = 4  # Adjust this value based on the elbow method plot
    kmeans, clusters = apply_kmeans(X_scaled, k)
    
    # Step 5: Visualize clusters
    visualize_clusters(df, X, clusters, kmeans, scaler)

if __name__ == "__main__":
    main()
