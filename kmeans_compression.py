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
        # Check if the centroids have 4 channels (RGBA)
        if centroids.shape[1] == 4:  # If centroids have an alpha channel
            centroids = centroids * 255
            palette_image = np.zeros((6, 24 * len(centroids), 4), dtype=np.uint8)  # Create an RGBA image
        else:
            palette_image = np.zeros((6, 24 * len(centroids), 3), dtype=np.uint8)  # Create an RGB image

        # Fill the image with colors
        for i, color in enumerate(centroids):
            start_x = i * 24  # Width of each color block
            palette_image[:, start_x:start_x + 24] = color.astype(np.uint8)  # Assign color to the block

        # Convert the numpy array to an image
        color_palette_img = Image.fromarray(palette_image)

        # Save the image as a PNG (supports transparency)
        color_palette_img.save(os.path.join('static', 'compressed_images', 'colors.png'), format='PNG', dpi=(300, 300))

    show_centroid_colors(kmeans.cluster_centers_)


    return compressed_img
