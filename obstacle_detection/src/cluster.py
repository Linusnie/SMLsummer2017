# Perform detection on point cloud
def detect(cloud):
    # Initialize detection parameters
    depth_max = 1.8  # only consider points within 4 meters from the camera, depth_max = velocity_max * processing_time
    height_min = 0.05  # only consider points higher than 0.05 meters
    width_min = -0.62
    width_max = 0.5
    point_real_list = []  # to store cloud point within desired range as list
    interval = 100  # sampling interval for visualizing a subset of clustered cloud points in 3D
    k = 4  # number of clusters for KMeans, maximum 8 for visualization convenience
    point_num_min = 6000  # minimum number of points to be regarded as a valid obstacle
    # bandwidth = 0.2  # bandwidth for meanshift
    # Initialize default output commands
    flag = "True"
    distance = 10.0
    angle = 0.0

    print ("Subscribing to /zed/point_cloud/cloud_registered.\n"
           "Received frame No.%d." % cloud.header.seq)
    print "Current time: ", time.time()

    # Read the cloud points into list
    point_list = np.zeros([cloud.height * cloud.width, 4])
    count = 0
    for p in pc2.read_points(cloud, field_names=("x", "y", "z", "rgb"), skip_nans=True):
        # "x: %f\ny: %f\nz: %f\nrgb: %f" % (p[0], p[1], p[2], p[3])
        # coordinates system relative to /zed_current_frame, basing on the left camera
        # x: depth, y: horizontal distance to the opposite of right camera, z: height
        if p[0] < depth_max and p[2] > height_min and width_min < p[1] < width_max:
            point_list[count, :] = np.asarray(p)
            count += 1

    print "For loop over cloud point time: ", time.time()
    print point_list.shape
    print count

    # point_num = len(point_list)
    # print "****************************************************"
    # if point_num < point_num_min:
    #     flag = "False"
    #     print "No obstacle detected!"
    # else:
    #     print "Obstacle detected!"

        # # Transform points into ndarray
        # point_ndarray = np.asarray(point_list)
        # # Normalize the last column, i.e. rgb, of the point cloud data ndarray
        # point_ndarray_norm = np.concatenate((point_ndarray[:, :3],
        #                                      (normalized(point_ndarray[:, 3], 0)).reshape([point_num, 1])), axis=1)
        # print "shape of normalized points: ", point_ndarray_norm.shape
        #
        # # Clustering
        # centers, labels = cluster_3d(point_ndarray_norm, k)
        # # Concatenate coordinates with labels
        # point_clustered_ndarray = np.concatenate((point_ndarray[:, :3], labels.reshape([point_num, 1])),
        #                                          axis=1)
        # np.random.shuffle(point_clustered_ndarray)  # shuffle point_ndarray along the first dimension
        #
        # print "Centroids: [x:depth, y:width, z:height, rgb:rgb]\n", centers
        # # print "shape of label: ", labels.shape
        #
        # # # Plot the clusters in 3D
        # # visual_3d(point_clustered_ndarray[0::interval, ...])
        # # # plt.show(block=True)
        #
        # # Save the clusters locally
        # # cwd = os.getcwd()
        # cwd = "/home/xiao/ros/catkin_ws/src/obstacle_detection/src"
        # np.savetxt(cwd + '/clustered_cloud_points.txt', point_clustered_ndarray[0::interval, ...])  # saved under ~/
        # print "Successively saved point_clustered_ndarray"

        # flag = "True"
        # distance = 1.0
        # angle = 30.0

    print "****************************************************"
    # Path planning

    # Publish the detection results
    # detect_result = Cmd()
    # detect_result.flag = flag
    # detect_result.distance = distance
    # detect_result.turn_angle = angle
    # result_pub.publish(detect_result)