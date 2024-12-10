import numpy as np
import numpy.typing as npt
import trimesh

from .util import get_nearby_indices, round_zeros


def toldi_lrf(
    mesh: trimesh.Trimesh,
    vertex_index: int,
    radius: float,
    *,
    use_vertex_normal: bool = False,
) -> npt.NDArray[np.float64]:
    """Computes the Local Reference Frame (LRF) for a vertex using the TOLDI method.

    This function implements the LRF computation from the TOLDI (Triangular-based Overlapping
    Local Depth Images) descriptor. It creates a robust local coordinate system at a given
    vertex using a combination of PCA and projection-based weighting.

    Args:
        mesh: The input 3D mesh.
        vertex_index: Index of the vertex for which to compute the LRF.
        radius: Support radius for the LRF computation.
        use_vertex_normal: If True, uses the vertex normal directly as the
            z-axis of the LRF. If False, computes the z-axis from PCA.

    Returns:
        Axes of the LRF stored in columns [x-axis, y-axis, z-axis] forming a right-handed
        coordinate system.
        Shape: (3, 3)

    Note:
        The implementation follows these steps:
        1. Computes z-axis using PCA on a smaller neighborhood (radius/3)
        2. Ensures consistent z-axis orientation by aligning along the concave direction
        3. Computes x-axis using weighted projections in full neighborhood
        4. Derives y-axis to complete right-handed coordinate system

    Reference:
        Yang, J., Zhang, Q., Xiao, Y., & Cao, Z. (2017).
        "TOLDI: An effective and robust approach for 3D local shape description."
        Pattern Recognition, 65, 175-187.
    """
    vertex = mesh.vertices[vertex_index]
    neighbor_indices = get_nearby_indices(mesh, vertex_index, radius, exclude_self=True)
    differences = mesh.vertices[neighbor_indices] - vertex
    distances = trimesh.util.row_norm(differences)

    if use_vertex_normal:
        z_axis = round_zeros(mesh.vertex_normals[vertex_index])
    else:
        z_radius = radius / 3.0
        z_neighbors = get_nearby_indices(mesh, vertex_index, z_radius)
        z_vertices = mesh.vertices[z_neighbors]
        z_centroid = np.mean(z_vertices, axis=0)
        centroid_differences = z_vertices - z_centroid
        covariance = round_zeros(np.dot(centroid_differences.T, centroid_differences))
        _, eigenvectors = np.linalg.eigh(covariance)
        z_axis = round_zeros(eigenvectors[:, 0])
        if np.dot(np.sum(differences, axis=0), z_axis) > 0.0:
            z_axis *= -1
    projection_distances = np.dot(differences, z_axis)
    scale_factors = np.square((radius - distances) * projection_distances)
    x_axis = round_zeros(np.dot(differences.T, scale_factors))
    y_axis = trimesh.transformations.unit_vector(np.cross(z_axis, x_axis))
    x_axis = np.cross(y_axis, z_axis)
    axes = np.column_stack((x_axis, y_axis, z_axis))
    return axes


def toldi_frames(
    mesh: trimesh.Trimesh,
    vertex_indices: npt.NDArray[np.int_],
    radius: float,
    *,
    use_vertex_normal: bool = False,
) -> npt.NDArray[np.float64]:
    """Computes Local Reference Frames (LRFs) for multiple vertices using the TOLDI method.

    Vectorized version of toldi_lrf that computes LRFs for multiple vertices simultaneously.

    Args:
        mesh: The input 3D mesh.
        vertex_indices: Array of vertex indices for which to compute LRFs.
            Shape: (L,) where L is the number of vertices with LRFs.
        radius: Support radius for the LRF computation.
        use_vertex_normal: If True, uses vertex normals directly as the
            z-axes of the LRFs. If False, computes z-axes from PCA.

    Returns:
        Batch of axes of the LRFs stored in columns [x-axis, y-axis, z-axis] forming
        right-handed coordinate systems.
        Shape: (L, 3, 3)
    """
    vertex_indices = np.atleast_1d(vertex_indices)
    frame_vertices = mesh.vertices[vertex_indices]
    n_vertices = len(vertex_indices)

    neighbors = get_nearby_indices(mesh, vertex_indices, radius, exclude_self=True)
    neighbors_counts = np.array([len(n) for n in neighbors])
    flat_neighbors = np.concatenate(neighbors)
    frame_indices = np.repeat(np.arange(n_vertices), neighbors_counts)
    differences = mesh.vertices[flat_neighbors] - frame_vertices[frame_indices]  # (M, 3)
    distances = trimesh.util.row_norm(differences)
    reduce_indices = np.insert(np.cumsum(neighbors_counts)[:-1], 0, 0)

    # Compute z-axis
    if use_vertex_normal:
        z_axes = round_zeros(mesh.vertex_normals[vertex_indices])
    else:
        z_radius = radius / 3.0
        z_neighbors = get_nearby_indices(mesh, vertex_indices, z_radius)
        z_neighbors_counts = np.array([len(n) for n in z_neighbors])
        flat_z_neighbors = np.concatenate(z_neighbors)
        z_frame_indices = np.repeat(np.arange(n_vertices), z_neighbors_counts)
        z_vertices = mesh.vertices[flat_z_neighbors]
        z_reduce_indices = np.insert(np.cumsum(z_neighbors_counts)[:-1], 0, 0)
        z_centroids = np.add.reduceat(z_vertices, z_reduce_indices) / np.expand_dims(
            z_neighbors_counts, axis=1
        )
        z_differences = z_vertices - z_centroids[z_frame_indices]
        covariances = np.einsum("mi,mj->mij", z_differences, z_differences)
        weighted_covariance = round_zeros(np.add.reduceat(covariances, z_reduce_indices))
        _, eigenvectors = np.linalg.eigh(weighted_covariance)
        z_axes = round_zeros(eigenvectors[..., 0])
        differences_sum = np.add.reduceat(differences, reduce_indices)
        z_dots = np.sum(differences_sum * z_axes, axis=-1)
        z_axes[z_dots > 0] *= -1

    # Compute x-axis
    projection_distances = np.sum(differences * z_axes[frame_indices], axis=1)
    scale_factors = np.square((radius - distances) * projection_distances)
    x_axes = round_zeros(
        np.add.reduceat(np.expand_dims(scale_factors, axis=-1) * differences, reduce_indices)
    )

    # Compute y-axis
    y_axes = trimesh.transformations.unit_vector(np.cross(z_axes, x_axes), axis=-1)
    x_axes = np.cross(y_axes, z_axes)

    axes: npt.NDArray[np.float64] = np.stack((x_axes, y_axes, z_axes), axis=-1)
    return axes
