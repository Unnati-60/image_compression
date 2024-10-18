import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.use('Agg')

from sklearn.cluster import KMeans
import numpy as np
import os



def compress_image(img_file,k):

    original_img = plt.imread(img_file)


    # Reshaping the image into an m x 3 matrix where m = number of pixels(if img is png then to m x 4)
    if original_img.shape[-1] == 4:
        X_img = original_img.reshape(-1,4)
    else:
        X_img = original_img.reshape(-1,3)

    #instance of kmean from sklearn
    kmeans = KMeans(n_clusters = k, n_init=10, max_iter=10)
    kmeans.fit(X_img)

    # Replace each pixel with the color of the closest centroid
    X_recovered = kmeans.cluster_centers_[kmeans.labels_, : ]

    if original_img.shape[-1] == 4:
        X_recovered = X_recovered*255

    # Reshape image into proper dimensions
    compressed_img = X_recovered.reshape(original_img.shape).astype(np.uint8)

    def show_centroid_colors(centroids):
        '''
        Displays colors used for in compressed image
        Args: 
        centroids (ndarray): (K, n) centroids
        '''
        if original_img.shape[-1] == 3:
            centroids = centroids/255
        
        palette = np.expand_dims(centroids, axis=0)
        num = np.arange(0,len(centroids))
        plt.figure(figsize=(24, 6))
        plt.xticks(num,fontsize=20)
        plt.yticks([])
        plt.imshow(palette)
        plt.savefig(os.path.join('static', 'compressed_images', 'colors.png'), bbox_inches='tight', pad_inches=0, dpi=300)
        plt.close()

    show_centroid_colors(kmeans.cluster_centers_)


    return compressed_img
