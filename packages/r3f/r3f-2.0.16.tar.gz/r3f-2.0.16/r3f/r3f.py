"""
Functions
=========
This library includes four sets of functions: general array checks, attitude-
representation conversions, reference-frame conversions, and rotation matrix
(direction cosine matrix) utilities.

All twenty possible conversions among the following five attitude
representations are provided: rotation vector, rotation axis and angle, roll and
pitch and yaw (RPY) Euler angles, direction cosine matrix (DCM), and quaternion.
However, some of the conversions are built using other conversions. In the
following table, the low-level conversions are marked with an `x` and the
conversions build using the other conversions are marked with an `o`:

    |         | vector  | ax, ang |   RPY   |   DCM   |  quat   |
    | ------- | ------- | ------- | ------- | ------- | ------- |
    | vector  |    -    |    x    |    o    |    o    |    o    |
    | ax, ang |    x    |    -    |    o    |    x    |    x    |
    |   RPY   |    o    |    x    |    -    |    x    |    x    |
    |   DCM   |    o    |    x    |    x    |    -    |    x    |
    |  quat   |    o    |    x    |    x    |    x    |    -    |

The roll, pitch, and yaw angles are applied in a zyx sequence of passive
rotations. The quaternions follow a Hamilton convention. Here is an example:

    roll = 20*np.pi/180
    pitch = 45*np.pi/180
    yaw = 10*np.pi/180
    C = r3f.rpy_to_dcm([roll, pitch, yaw])
    >> C = [[ 0.69636424  0.1227878  -0.70710678]
        [ 0.07499469  0.96741248  0.24184476]
        [ 0.71375951 -0.2214413   0.66446302]]

In addition to the conversion from the z, y, x sequence of Euler angles to a
DCM, the function `rot` is also provided for creating a DCM from a generic set
of Euler angles in any desired sequence of axes. Although this `rot` function
could be used, two additional functions are provided for generating rotation
matrices: `dcm_inertial_to_ecef` and `dcm_ecef_to_navigation`. By default, all
angles are treated as being in radians, but if the `degs` parameter is set to
True, then they are treated as being in degrees.

The defined functions for attitude-representation conversion are

-   axis_angle_to_vector
-   vector_to_axis_angle
-   rpy_to_vector
-   vector_to_rpy
-   dcm_to_vector
-   vector_to_dcm
-   quat_to_vector
-   vector_to_quat
-   rpy_to_axis_angle
-   axis_angle_to_rpy
-   dcm_to_axis_angle
-   axis_angle_to_dcm
-   quat_to_axis_angle
-   axis_angle_to_quat
-   dcm_to_rpy
-   rpy_to_dcm
-   rot
-   rotate
-   quat_to_rpy
-   rpy_to_quat
-   quat_to_dcm
-   dcm_to_quat
-   dcm_inertial_to_ecef
-   dcm_ecef_to_navigation

This library includes all twelve possible conversions among the following four
frames: ECEF (Earth-centered, Earth-fixed), geodetic (latitude, longitude, and
height above ellipsoid), local-level tangent, and local-level curvilinear. By
default, all local-level coordinates are interpreted as having a North, East,
Down (NED) orientation, but if the `ned` parameter is set to False, the
coordinates are interpreted as having an East, North, Up (ENU) orientation. Here
is an example:

    lat = 45*np.pi/180
    lon = 0.0
    hae = 1000.0
    [xe, ye, ze] = r3f.geodetic_to_ecef([lat, lon, hae])
    >> xe = 4518297.985630118
    >> ye = 0.0
    >> ze = 4488055.515647106

The functions for reference-frame conversions are

-   geodetic_to_ecef
-   ecef_to_geodetic
-   tangent_to_ecef
-   ecef_to_tangent
-   curvilinear_to_ecef
-   ecef_to_curvilinear
-   tangent_to_geodetic
-   geodetic_to_tangent
-   curvilinear_to_geodetic
-   geodetic_to_curvilinear
-   curvilinear_to_tangent
-   tangent_to_curvilinear

The rotation matrix utility functions are an `orthonormalize_dcm` function, a
`rodrigues_rotation` function, and an `inverse_rodrigues_rotation` function. The
`orthonormalize_dcm` function will work to make a rotation matrix normalized and
orthogonal, a proper rotation matrix. The two Rodrigues's rotation functions are
meant for converting a vector to the matrix exponential of the skew-symmetric
matrix of that vector and back again. The list of utility functions is

-   is_ortho
-   orthonormalize_dcm
-   rodrigues_rotation
-   inverse_rodrigues_rotation

Passive Rotations
=================
Unless specifically otherwise stated, all rotations are interpreted as passive.
This means they represent rotations of reference frames, not of vectors.

Vectorization
=============
When possible, the functions are vectorized in order to handle processing
batches of values. A set of scalars is a 1D array. A set of vectors is a 2D
array, with each vector in a column. So, a (3, 7) array is a set of seven
vectors, each with 3 elements. If the inputs do not have 3 rows, they will be
assumed to be transposed. A set of matrices is a 3D array with each matrix in a
stack. The first index is the stack number. So, a (5, 3, 3) array is a stack of
five 3x3 matrices. Roll, pitch, and yaw are not treated as a vector but as three
separate quantities. The same is true for latitude, longitude, and height above
ellipsoid. A quaternion is passed around as an array.

Robustness
==========
In general, the functions in this library check that the inputs are of the
correct type and shape. They do not generally handle converting inputs which do
not conform to the ideal type and shape. Generally, the allowed types are int,
float, list, and np.ndarray.
"""

import math
import numpy as np

# WGS84 constants (IS-GPS-200M and NIMA TR8350.2)
A_E = 6378137.0             # Earth's semi-major axis (m) (p. 109)
F_E = 298.257223563         # Earth's flattening constant (NIMA)
B_E = 6356752.314245        # Earth's semi-minor axis (m) A_E*(1 - 1/F_E)
E2 = 6.694379990141317e-3   # Earth's eccentricity squared (ND) (derived)
W_EI = 7.2921151467e-5      # sidereal Earth rate (rad/s) (p. 106)
TOL = 1e-7                  # Default tolerance

# -----------------------------------
# Attitude-representation Conversions
# -----------------------------------

def axis_angle_to_vector(ax, ang, degs=False):
    """
    Convert an axis vector, `ax`, and a rotation angle, `ang`, to a rotation
    vector.

    Parameters
    ----------
    ax : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Rotation axis vector or matrix of K rotation axis vectors.
    ang : float or (K,) list, tuple, or np.ndarray
        Rotation angle or array of K rotation angles. This is a positive value.
    degs : bool, default False
        Flag to interpret angles as degrees.

    Returns
    -------
    vec : (3,) or (3, K) or (K, 3) np.ndarray
        Rotation vector or matrix of K rotation vectors.

    See Also
    --------
    vector_to_axis_angle
    """

    # Check input.
    if isinstance(ax, (list, tuple)):
        ax = np.array(ax)
    if isinstance(ang, (list, tuple)):
        ang = np.array(ang)
    trs = (ax.ndim == 2 and ax.shape[0] != 3)
    s = np.pi/180 if degs else 1.0

    # Transpose input.
    if trs:
        ax = ax.T

    # Convert to a rotation vector.
    vec = s*ang*ax

    # Transpose output.
    if trs:
        vec = vec.T

    return vec


def vector_to_axis_angle(vec, degs=False):
    """
    Convert a rotation vector, `vec`, to an axis-angle representation.

    Parameters
    ----------
    vec : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Rotation vector or matrix of K rotation vectors.
    degs : bool, default False
        Flag to convert angles to degrees.

    Returns
    -------
    ax : (3,) or (3, K) or (K, 3) np.ndarray
        Rotation axis vector or matrix of K rotation axis vectors.
    ang : float or (K,) np.ndarray
        Rotation angle or array of K rotation angles.

    See Also
    --------
    axis_angle_to_vector

    Notes
    -----
    The ax vector will be normalized to a norm of 1. This can create a
    nonduality between this function and `axis_angle_to_vector`.
    """

    # Check the input.
    if isinstance(vec, (list, tuple)):
        vec = np.array(vec)
    trs = (vec.ndim == 2 and vec.shape[0] != 3)

    # Transpose input.
    if trs:
        vec = vec.T

    # Convert to axis vector and angle magnitude.
    ang = np.linalg.norm(vec, axis=0)
    ax = vec/ang

    # Transpose output.
    if trs:
        ax = ax.T

    # Scale the angle.
    if degs:
        ang *= 180/np.pi

    return ax, ang


def rpy_to_vector(rpy, degs=False):
    """
    Convert roll, pitch, and yaw Euler angles to rotation vector.

    Parameters
    ----------
    rpy : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Roll, pitch, and yaw Euler angle.
    degs : bool, default False
        Flag to interpret angles as degrees.

    Returns
    -------
    vec : (3,) or (3, K) or (K, 3) np.ndarray
        Rotation vector or matrix of K rotation vectors.

    See Also
    --------
    vector_to_rpy
    """

    # Check the input.
    if isinstance(rpy, (list, tuple)):
        rpy = np.array(rpy)

    ax, ang = rpy_to_axis_angle(rpy, degs)
    vec = axis_angle_to_vector(ax, ang, degs)
    return vec


def vector_to_rpy(vec, degs=False):
    """
    Convert rotation vector to roll, pitch, and yaw Euler angles.

    Parameters
    ----------
    vec : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Rotation vector or matrix of K rotation vectors.
    degs : bool, default False
        Flag to interpret angles as degrees.

    Returns
    -------
    rpy : (3,) or (3, K) or (K, 3) np.ndarray
        Roll, pitch, and yaw Euler angle in radians.

    See Also
    --------
    rpy_to_vector
    """

    # Check the input.
    if isinstance(vec, (list, tuple)):
        vec = np.array(vec)

    ax, ang = vector_to_axis_angle(vec, degs)
    rpy = axis_angle_to_rpy(ax, ang, degs)
    return rpy


def dcm_to_vector(C):
    """
    Convert from a DCM to a rotation vector.

    Parameters
    ----------
    C : (3, 3) or (K, 3, 3) list, tuple, or np.ndarray
        Rotation direction cosine matrix or stack of K such matrices.

    Returns
    -------
    vec : (3,) or (3, K) np.ndarray
        Rotation vector or matrix of K rotation vectors.

    See Also
    --------
    vector_to_dcm
    """

    # Check the input.
    if isinstance(C, (list, tuple)):
        C = np.array(C)

    ax, ang = dcm_to_axis_angle(C)
    vec = axis_angle_to_vector(ax, ang)
    return vec


def vector_to_dcm(vec):
    """
    Convert from a rotation vector to a DCM.

    Parameters
    ----------
    vec : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Rotation vector or matrix of K rotation vectors.

    Returns
    -------
    C : (3, 3) or (K, 3, 3) np.ndarray
        Rotation direction cosine matrix or stack of K such matrices.

    See Also
    --------
    dcm_to_vector
    """

    # Check the input.
    if isinstance(vec, (list, tuple)):
        vec = np.array(vec)

    ax, ang = vector_to_axis_angle(vec)
    C = axis_angle_to_dcm(ax, ang)
    return C


def quat_to_vector(q):
    """
    Convert a from a quaternion to a rotation vector. This follows the Hamilton
    convention.

    Parameters
    ----------
    q : (4,) or (4, K) or (K, 4) list, tuple, or np.ndarray
        Array of quaternion elements or matrix of K arrays of quaternion
        elements. The elements are a, b, c, and d where the quaterion `q` is
        a + b i + c j + d k.

    Returns
    -------
    vec : (3,) or (3, K) or (K, 3) np.ndarray
        Rotation vector or matrix of K rotation vectors.

    See Also
    --------
    vector_to_quat
    """

    # Check the input.
    if isinstance(q, (list, tuple)):
        q = np.array(q)

    ax, ang = quat_to_axis_angle(q)
    vec = axis_angle_to_vector(ax, ang)
    return vec


def vector_to_quat(vec):
    """
    Convert a from a rotation vector to a quaternion. This follows the Hamilton
    convention.

    Parameters
    ----------
    vec : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Rotation vector or matrix of K rotation vectors.

    Returns
    -------
    q : (4,) or (4, K) or (K, 4) np.ndarray
        Array of quaternion elements or matrix of K arrays of quaternion
        elements. The elements are a, b, c, and d where the quaterion `q` is
        a + b i + c j + d k.

    See Also
    --------
    quat_to_vector
    """

    # Check the input.
    if isinstance(vec, (list, tuple)):
        vec = np.array(vec)

    ax, ang = vector_to_axis_angle(vec)
    q = axis_angle_to_quat(ax, ang)
    return q


def rpy_to_axis_angle(rpy, degs=False):
    """
    Convert roll, pitch, and yaw Euler angles to rotation axis vector and
    rotation angle.

    Parameters
    ----------
    rpy : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Roll, pitch, and yaw Euler angle in radians.
    degs : bool, default False
        Flag to interpret angles as degrees.

    Returns
    -------
    ax : (3,) or (3, K) or (K, 3) np.ndarray
        Rotation axis vector or matrix of K rotation axis vectors.
    ang : float or (K,) np.ndarray
        Rotation angle or array of K rotation angles. This is a positive value.

    See Also
    --------
    axis_angle_to_rpy
    """

    # Check the input.
    if isinstance(rpy, (list, tuple)):
        rpy = np.array(rpy)

    q = rpy_to_quat(rpy, degs)
    ax, ang = quat_to_axis_angle(q, degs)
    return ax, ang


def axis_angle_to_rpy(ax, ang, degs=False):
    """
    Convert rotation axis vector, `ax`, and angle, `ang`, to roll, pitch, and
    yaw vectors.

    Parameters
    ----------
    ax : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Rotation axis vector or matrix of K rotation axis vectors.
    ang : float or (K,) list, tuple, or np.ndarray
        Rotation angle or array of K rotation angles.
    degs : bool, default False
        Flag to interpret angles as degrees.

    Returns
    -------
    rpy : (3,) or (3, K) or (K, 3) np.ndarray
        Roll, pitch, and yaw Euler angle in radians.

    See Also
    --------
    rpy_to_axis_angle

    Notes
    -----
    This function converts a vector rotation axis, `ax`, and a rotation angle,
    `ang`, to a vector of roll, pitch, and yaw Euler angles. The sense of the
    rotation is maintained. To make the conversion, some of the elements of the
    corresponding DCM are calculated as an intermediate step. The DCM is defined
    in terms of the elements of the corresponding quaternion, `q`, as

        q = a + b i + c j + d k

            .-                                                            -.
            |   2    2    2    2                                           |
            | (a  + b  - c  - d )    2 (b c + a d)       2 (b d - a c)     |
            |                                                              |
            |                       2    2    2    2                       |
        C = |    2 (b c - a d)    (a  - b  + c  - d )    2 (c d + a b)     |
            |                                                              |
            |                                           2    2    2    2   |
            |    2 (b d + a c)       2 (c d - a b)    (a  - b  - c  + d )  |
            '-                                                            -'

    where

        ax = [x  y  z]'
        a =   cos(ang/2)
        b = x sin(ang/2)
        c = y sin(ang/2)
        d = z sin(ang/2)

    Here `ax` is assumed to be a unit vector. We will overcome this limitation
    later. Using the half-angle identities

           2.- ang -.   1 - cos(ang)           2.- ang -.   1 + cos(ang)
        sin | ----- | = ------------        cos | ----- | = ------------
            '-  2  -'        2                  '-  2  -'        2

    we can simplify, as an example, the expression

          2    2    2    2
        (a  + b  - c  - d )

    to

                    2
        cos(ang) + x (1 - cos(ang)) .

    We can also use the fact that

              .- ang -.     .- ang -.
        2 cos | ----- | sin | ----- | = sin(ang)
              '-  2  -'     '-  2  -'

    to simplify

        2 (b c - a d)

    to

        x y (1 - cos(ang)) - z sin(ang)

    Through these simplifications the `C` can be redefined as

            .-         2                                     -.
            |    co + x cc     x y cc + z si   x z cc - y si  |
            |                                                 |
            |                          2                      |
        C = |  x y cc - z si     co + y cc     y z cc + x si  |
            |                                                 |
            |                                          2      |
            |  x z cc + y si   y z cc - x si     co + z cc    |
            '-                                               -'

    where `co` is the cosine of the angle, `si` is the sine of the angle, and
    `cc` is the compelement of the cosine: `(1 - co)`.

    Before the algorithm described above is applied, the `ax` input is first
    normalized. The norm is not thrown away. Rather it is multiplied into the
    `ang` value. This overcomes the limitation of assuming the axis vector is a
    unit vector.

    The `C` can also be defined in terms of the roll, pitch, and yaw as
            .-             -.
            |  c11 c12 c13  |
        C = |  c21 c22 c23  |
            |  c31 c32 c33  |
            '-             -'
            .-                                                 -.
            |       (cy cp)             (sy cp)          -sp    |
          = |  (cy sp sr - sy cr)  (sy sp sr + cy cr)  (cp sr)  |
            |  (sy sr + cy sp sr)  (sy sp cr - cy sr)  (cp cr)  |
            '-                                                 -'

    where `c` and `s` mean cosine and sine, respectively, and `r`, `p`, and `y`
    mean roll, pitch, and yaw, respectively, then we can see that

                                        .- cp sr -.
        r = arctan2(c23, c33) => arctan | ------- |
                                        '- cp cr -'

                                        .- sy cp -.
        y = arctan2(c12, c11) => arctan | ------- |
                                        '- cy cp -'

    where the `cp` values cancel in both cases. The value for pitch can be found
    from `c13` alone:

        p = -arcsin(c13)

    This function does not take advantage of the more advanced formula for pitch
    that we might use when the input is actually a DCM.

    Putting this together, the `ax` vector is normalized and its norm applied to
    the angle:

                .-----------------
               /   2      2      2
        nm = `/ ax1  + ax2  + ax3

             ax1             ax2
        x = -----       y = -----
             nm              nm

             ax3
        z = -----       ang = ang nm .
             nm

    Then the necessary elements of the DCM are calculated:

                    2
        c11 = co + x (1 - co)       c12 = x y (1 - co) + z si

                                    c13 = x z (1 - co) - y si
                    2
        c33 = co + z (1 - co)       c23 = y z (1 - co) + x si

    where `co` and `si` are the cosine and sine of `ang`. Now we can get roll,
    pitch, and yaw:

        r =  arctan2(c23, c33)
        p = -arcsin(c13)
        y =  arctan2(c12, c11)
    """

    # Check input.
    if isinstance(ax, (list, tuple)):
        ax = np.array(ax)
    if isinstance(ang, (list, tuple)):
        ang = np.array(ang)
    trs = (ax.ndim == 2 and ax.shape[0] != 3)
    s = np.pi/180 if degs else 1.0

    # Transpose input.
    if trs:
        ax = ax.T

    # Get the norm of the axis vector.
    nm = np.linalg.norm(ax, axis=0)

    # Normalize and parse the vector rotation axis.
    x = ax[0]/nm
    y = ax[1]/nm
    z = ax[2]/nm
    Ang = s*ang*nm

    # Get the cosine, sine, and complement of cosine of the angle.
    co = np.cos(Ang)
    si = np.sin(Ang)
    cc = 1 - co # complement of cosine

    # Calculate key elements of the DCM.
    c11 = co + (x**2)*cc
    c33 = co + (z**2)*cc
    c12 = x*y*cc + z*si
    c13 = x*z*cc - y*si
    c23 = y*z*cc + x*si

    # Build the output.
    r = np.arctan2(c23, c33)
    p = -np.arcsin(c13)
    y = np.arctan2(c12, c11)
    rpy = np.array([r, p, y])/s

    # Transpose output.
    if trs:
        rpy = rpy.T

    return rpy


def dcm_to_axis_angle(C, degs=False):
    """
    Convert from a DCM to a rotation axis vector, `ax`, and rotation angle,
    `ang`.

    Parameters
    ----------
    C : (3, 3) or (K, 3, 3) list, tuple, or np.ndarray
        Rotation direction cosine matrix or stack of K such matrices.
    degs : bool, default False
        Flag to convert angles to degrees.

    Returns
    -------
    ax : (3,) or (3, K) np.ndarray
        Rotation axis vector or matrix of K rotation axis vectors.
    ang : float or (K,) np.ndarray
        Rotation angle or array of K rotation angles.

    Notes
    -----
    This function converts a direction cosine matrix, `C`, to a rotation axis
    vector, `ax`, and rotation angle, `ang`. Here, the DCM is considered to
    represent a zyx sequence of right-handed rotations. This means it has the
    same sense as the axis vector and angle pair. The conversion is achieved by
    calculating a quaternion as an intermediate step.

    The implementation here is Cayley's method for obtaining the quaternion. It
    is used because of its superior numerical accuracy. This comes from the fact
    that it uses all nine of the elements of the DCM matrix. It also does not
    suffer from numerical instability due to division as some other methods do.

    Defining the rotation axis vector to be a unit vector, we will define the
    quaterion in terms of the axis and angle:

        ax = [x  y  z]'
        a =   cos(ang/2)
        b = x sin(ang/2)
        c = y sin(ang/2)
        d = z sin(ang/2)
        q = a + b i + c j + d k

    where `q` is the quaternion and `ax` is the rotation axis vector. Then, the
    norm of [b, c, d] will be

           .-----------       .---------------------------
          / 2    2    2      /  2    2    2     2.- ang -.       .- ang -.
        `/ b  + c  + d  =   / (x  + y  + z ) sin | ----- | = sin | ----- | .
                          `/                     '-  2  -'       '-  2  -'

    Since a = cos(ang/2), with the above value, we can calculate the angle by

                            .-   .-----------    -.
                            |   / 2    2    2     |
        ang = 2 sgn arctan2 | `/ b  + c  + d  , a | ,
                            '-                   -'

    where `sgn` is the sign of the angle based on whether the dot product of the
    vector [b, c, d] with [1, 1, 1] is positive:

        sgn = sign( b + c + d ) .

    Finally, the rotation axis vector is calculated by using the first set of
    equations above:

                b                    c                    d
        x = -------------    y = -------------    z = ------------- .
                .- ang -.            .- ang -.            .- ang -.
            sin | ----- |        sin | ----- |        sin | ----- |
                '-  2  -'            '-  2  -'            '-  2  -'

    It is true that `ang` and, therefore `sin(ang/2)`, could become 0, which
    would create a singularity. But, this will happen only if the norm of `[b,
    c, d]` is zero. In other words, if the quaternion is just a scalar value,
    then we will have a problem.

    References
    ----------
    .. [1]  Titterton & Weston, "Strapdown Inertial Navigation Technology"
    .. [2]  Soheil Sarabandi and Federico Thomas, "A Survey on the Computation
            of Quaternions from Rotation Matrices," Journal of Mechanisms and
            Robotics, 2018.
    """

    # Check input.
    if isinstance(C, (list, tuple)):
        C = np.array(C)

    # Parse and reshape the elements of Dcm.
    if C.ndim == 2:
        c11 = C[0, 0];      c12 = C[0, 1];      c13 = C[0, 2]
        c21 = C[1, 0];      c22 = C[1, 1];      c23 = C[1, 2]
        c31 = C[2, 0];      c32 = C[2, 1];      c33 = C[2, 2]
    else:
        c11 = C[:, 0, 0];   c12 = C[:, 0, 1];   c13 = C[:, 0, 2]
        c21 = C[:, 1, 0];   c22 = C[:, 1, 1];   c23 = C[:, 1, 2]
        c31 = C[:, 2, 0];   c32 = C[:, 2, 1];   c33 = C[:, 2, 2]

    # Get the squared sums and differences of off-diagonal pairs.
    p12 = (c12 + c21)**2
    p23 = (c23 + c32)**2
    p31 = (c31 + c13)**2
    m12 = (c12 - c21)**2
    m23 = (c23 - c32)**2
    m31 = (c31 - c13)**2

    # Get squared expressions of diagonal values.
    d1 = (c11 + c22 + c33 + 1)**2
    d2 = (c11 - c22 - c33 + 1)**2
    d3 = (c22 - c11 - c33 + 1)**2
    d4 = (c33 - c11 - c22 + 1)**2

    # Build the quaternion.
    a = 0.25*np.sqrt(d1 + m23 + m31 + m12)
    b = 0.25*np.sign(c23 - c32)*np.sqrt(m23 + d2 + p12 + p31)
    c = 0.25*np.sign(c31 - c13)*np.sqrt(m31 + p12 + d3 + p23)
    d = 0.25*np.sign(c12 - c21)*np.sqrt(m12 + p31 + p23 + d4)

    # Get the norm and sign of the last three elements of the quaternion.
    nm = np.sqrt(b**2 + c**2 + d**2)
    sgn = np.sign(b + c + d)

    # Get the angle of rotation.
    ang = 2*sgn*np.arctan2(nm, a)

    # Build the rotation axis vector.
    x = b/np.sin(ang/2)
    y = c/np.sin(ang/2)
    z = d/np.sin(ang/2)
    ax = np.array([x, y, z])

    # Scale the angle.
    if degs:
        ang *= 180/np.pi

    return ax, ang


def axis_angle_to_dcm(ax, ang, degs=False):
    """
    Create a direction cosine matrix (DCM) (also known as a rotation matrix) to
    rotate from one frame to another given a rotation `ax` vector and a
    right-handed `ang` of rotation.

    Parameters
    ----------
    ax : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Rotation axis vector or matrix of K rotation axis vectors.
    ang : float or (K,) list, tuple, or np.ndarray
        Rotation angle or array of K rotation angles.
    degs : bool, default False
        Flag to interpret angles as degrees.

    Returns
    -------
    C : (3, 3) or (K, 3, 3) np.ndarray
        Rotation direction cosine matrix or stack of K such matrices.

    See Also
    --------
    dcm_to_axis_anlge
    """

    # Check the inputs.
    if isinstance(ax, (list, tuple)):
        ax = np.array(ax)
    if isinstance(ang, (list, tuple)):
        ang = np.array(ang)
    trs = (ax.ndim == 2 and ax.shape[0] != 3)
    s = np.pi/180 if degs else 1.0

    # Transpose input.
    if trs:
        ax = ax.T

    # Normalize and parse the rotation axis vector.
    nm = np.linalg.norm(ax, axis=0)
    Ang = s*ang*nm
    x = ax[0]/nm
    y = ax[1]/nm
    z = ax[2]/nm

    # Get the cosine and sine of the ang.
    co = np.cos(Ang)
    si = np.sin(Ang)
    cc = 1 - co

    # Build the direction cosine matrix.
    if ax.ndim == 1:
        C = np.array([
            [co + (x**2)*cc,  x*y*cc + z*si,  x*z*cc - y*si],
            [x*y*cc - z*si,  co + (y**2)*cc,  y*z*cc + x*si],
            [x*z*cc + y*si,   y*z*cc - x*si, co + (z**2)*cc]])
    else:
        # Build the direction cosine matrix.
        C = np.zeros((len(x), 3, 3))
        C[:, 0, 0] = co + (x**2)*cc
        C[:, 0, 1] = x*y*cc + z*si
        C[:, 0, 2] = x*z*cc - y*si
        C[:, 1, 0] = x*y*cc - z*si
        C[:, 1, 1] = co + (y**2)*cc
        C[:, 1, 2] = y*z*cc + x*si
        C[:, 2, 0] = x*z*cc + y*si
        C[:, 2, 1] = y*z*cc - x*si
        C[:, 2, 2] = co + (z**2)*cc

    return C


def quat_to_axis_angle(q, degs=False):
    """
    Convert a from a quaternion to a rotation axis vector and angle. This
    follows the Hamilton convention.

    Parameters
    ----------
    q : (4,) or (4, K) or (K, 4) list, tuple, or np.ndarray
        Array of quaternion elements or matrix of K arrays of quaternion
        elements. The elements are a, b, c, and d where the quaterion `q` is
        a + b i + c j + d k.
    degs : bool, default False
        Flag to convert angles to degrees.

    Returns
    -------
    ax : (3,) or (3, K) or (K, 3) np.ndarray
        Rotation axis vector or matrix of K rotation axis vectors.
    ang : float or (K,) np.ndarray
        Rotation angle or array of K rotation angles. This is a positive value.

    See Also
    --------
    axis_angle_to_quat

    Notes
    -----
    The quaternion, `q`, is defined in terms of the unit axis vector, `ax`, and
    angle, `ang`:

        ax = [x, y, z]'                     a =   cos( ang/2 )
        q = a + b i + c j + d k             b = x sin( ang/2 )
                                            c = y sin( ang/2 )
                                            d = z sin( ang/2 ) .

    The norm of [b, c, d]' would be

           .-----------       .---------------------------
          / 2    2    2      /  2    2    2     2
        `/ b  + c  + d  =  `/ (x  + y  + z ) sin ( ang/2 ) = sin( ang/2 ) ,

    where [x, y, z]' is a unit vector by design. Since a = cos(ang/2), with the
    above value we can calculate the angle by

                            .-   .-----------   -.
                            |   / 2    2    2    |
        ang = 2 sgn arctan2 | `/ b  + c  + d , a | ,
                            '-                  -'

    where sgn is the sign of the angle based on whether the dot product of the
    vector [b, c, d]' with [1, 1, 1]' is positive:

        sgn = sign( b + c + d ) .

    Finally, the rotation axis vector is calculated by using the first set of
    equations above:

                 b                     c                     d
        x = -------------     y = -------------     z = ------------- .
                .- ang -.             .- ang -.             .- ang -.
            sin | ----- |         sin | ----- |         sin | ----- |
                '-  2  -'             '-  2  -'             '-  2  -'

    It is true that ang and, therefore sin(ang/2), could become 0, which would
    create a singularity. But, this would happen only if the norm of [b, c, d]'
    were zero. In other words, if the quaternion is just a scalar value, then we
    will have a problem.

    References
    ----------
    .. [1]  Titterton & Weston, "Strapdown Inertial Navigation Technology"
    """

    # Check input.
    if isinstance(q, (list, tuple)):
        q = np.array(q)
    trs = (q.ndim == 2 and q.shape[0] != 4)

    # Transpose input.
    if trs:
        q = q.T

    # Build the quaternion.
    sgn = np.sign(np.sum(q[1:], axis=0))
    nm = np.linalg.norm(q[1:], axis=0)
    ang = 2*sgn*np.arctan2(nm, q[0])
    ax = q[1:]/np.sin(ang/2)

    # Transpose output.
    if trs:
        ax = ax.T

    # Scale the angle.
    if degs:
        ang *= 180/np.pi

    return ax, ang


def axis_angle_to_quat(ax, ang, degs=False):
    """
    Convert rotation axis vector and angle to a quaternion. This follows the
    Hamilton convention.

    Parameters
    ----------
    ax : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Rotation axis vector or matrix of K rotation axis vectors.
    ang : float or (K,) list, tuple, or np.ndarray
        Rotation angle or array of K rotation angles.
    degs : bool, default False
        Flag to interpret angles as degrees.

    Returns
    -------
    q : (4,) or (4, K) or (K, 4) np.ndarray
        Array of quaternion elements or matrix of K arrays of quaternion
        elements. The elements are a, b, c, and d where the quaterion `q` is
        a + b i + c j + d k.

    See Also
    --------
    quat_to_axis_angle

    Notes
    -----
    The quaternion, `q`, is defined in terms of the unit axis vector, `ax`,
    and angle, `ang`:

        ax = [x, y, z]'                     a =   cos( ang/2 )
        q = a + b i + c j + d k             b = x sin( ang/2 )
                                            c = y sin( ang/2 )
                                            d = z sin( ang/2 ) .

    The `ax` input is first normalized. The norm is not thrown away, but rather
    multiplied into the `ang` value. This overcomes the limitation of assuming
    the axis vector is a unit vector.

    References
    ----------
    .. [1]  Titterton & Weston, "Strapdown Inertial Navigation Technology"
    """

    # Check input.
    if isinstance(ax, (list, tuple)):
        ax = np.array(ax)
    if isinstance(ang, (list, tuple)):
        ang = np.array(ang)
    trs = (ax.ndim == 2 and ax.shape[0] != 3)
    s = np.pi/180 if degs else 1.0

    # Transpose input.
    if trs:
        ax = ax.T

    # Normalize the vector rotation axis.
    nm = np.linalg.norm(ax, axis=0)
    Ax = ax/nm
    Ang = s*ang*nm

    # Build the quaternion.
    a = np.cos(Ang/2)
    si = np.sin(Ang/2)
    b = Ax[0]*si
    c = Ax[1]*si
    d = Ax[2]*si
    q = np.array([a, b, c, d])

    # Transpose output.
    if trs:
        q = q.T

    return q


def dcm_to_rpy(C, degs=False):
    """
    Convert the direction cosine matrix, `C`, to vectors of `roll`, `pitch`,
    and `yaw` (in that order) Euler angles.

    This `C` represents the z, y, x sequence of right-handed rotations. For
    example, if the DCM converted vectors from the navigation frame to the body
    frame, the roll, pitch, and yaw Euler angles would be the consecutive angles
    by which the vector would be rotated from the navigation frame to the body
    frame. This is as opposed to the Euler angles required to rotate the vector
    from the body frame back to the navigation frame.

    Parameters
    ----------
    C : (3, 3) or (K, 3, 3) list, tuple, or np.ndarray
        Rotation direction cosine matrix or stack of K such matrices.
    degs : bool, default False
        Flag to convert angles to degrees.

    Returns
    -------
    rpy : (3,) or (3, K) np.ndarray
        Roll, pitch, and yaw Euler angle.

    See Also
    --------
    rpy_to_dcm

    Notes
    -----
    If we define `C` as

            .-             -.
            |  c11 c12 c13  |
        C = |  c21 c22 c23  |
            |  c31 c32 c33  |
            '-             -'
            .-                                                 -.
            |       (cy cp)             (sy cp)          -sp    |
          = |  (cy sp sr - sy cr)  (sy sp sr + cy cr)  (cp sr)  |
            |  (sy sr + cy sp sr)  (sy sp cr - cy sr)  (cp cr)  |
            '-                                                 -'

    where `c` and `s` mean cosine and sine, respectively, and `r`, `p`, and `y`
    mean roll, pitch, and yaw, respectively, then we can see that

                                        .- cp sr -.
        r = arctan2(c23, c33) => arctan | ------- |
                                        '- cp cr -'

                                        .- sy cp -.
        y = arctan2(c12, c11) => arctan | ------- |
                                        '- cy cp -'

    where the cp values cancel in both cases. The value for pitch could be found
    from c13 alone:

        p = arcsin(-c13)

    However, this tends to suffer from numerical error around +- pi/2. So,
    instead, we will use the fact that

          2     2               2     2
        cy  + sy  = 1   and   cr  + sr  = 1 .

    Therefore, we can use the fact that

           .------------------------
          /   2      2      2      2     .--
        `/ c11  + c12  + c23  + c33  = `/ 2  cos( |p| )

    to solve for pitch. We can use the negative of the sign of c13 to give the
    proper sign to pitch. The advantage is that in using more values from the
    DCM matrix, we can can get a value which is more accurate. This works well
    until we get close to a pitch value of zero. Then, the simple formula for
    pitch is actually better. So, we will use both and do a weighted average of
    the two, based on pitch.

    References
    ----------
    .. [1]  Titterton & Weston, "Strapdown Inertial Navigation Technology"
    """

    # Check input.
    if isinstance(C, (list, tuple)):
        C = np.array(C)
    s = np.pi/180 if degs else 1.0

    if C.ndim == 2:
        # Parse out the elements of the DCM that are needed.
        c11 = C[0, 0]
        c33 = C[2, 2]
        c12 = C[0, 1]
        c13 = C[0, 2]
        c23 = C[1, 2]

        # Get roll.
        rpy = np.zeros(3)
        rpy[0] = math.atan2(c23, c33)

        # Get pitch.
        sp = -c13
        pa = math.asin(sp)
        nm = math.sqrt(c11**2 + c12**2 + c23**2 + c33**2)
        pb = math.acos(nm/math.sqrt(2))
        rpy[1] = (1.0 - abs(sp))*pa + sp*pb

        # Get yaw.
        rpy[2] = math.atan2(c12, c11)
    else:
        # Parse out the elements of the DCM that are needed.
        c11 = C[:, 0, 0]
        c33 = C[:, 2, 2]
        c12 = C[:, 0, 1]
        c13 = C[:, 0, 2]
        c23 = C[:, 1, 2]

        # Get roll.
        r = np.arctan2(c23, c33)

        # Get pitch.
        sp = -c13
        pa = np.arcsin(sp)
        nm = np.sqrt(c11**2 + c12**2 + c23**2 + c33**2)
        pb = np.arccos(nm/np.sqrt(2))
        p = (1.0 - np.abs(sp))*pa + sp*pb

        # Get yaw.
        y = np.arctan2(c12, c11)

        # Build the output.
        rpy = np.array([r, p ,y])/s

    return rpy


def rpy_to_dcm(rpy, degs=False):
    """
    Convert roll, pitch, and yaw Euler angles to a direction cosine matrix that
    represents a zyx sequence of right-handed rotations.

    Parameters
    ----------
    rpy : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Roll, pitch, and yaw Euler angle.
    degs : bool, default False
        Flag to interpret angles as degrees.

    Returns
    -------
    C : (3, 3) or (K, 3, 3) np.ndarray
        Rotation matrix or stack of K rotation matrices.

    See Also
    --------
    dcm_to_rpy
    rot

    Notes
    -----
    This is equivalent to generating a rotation matrix for the rotation from the
    navigation frame to the body frame. However, if you want to rotate from the
    body frame to the navigation frame (an xyz sequence of right-handed
    rotations), transpose the result of this function. This is a convenience
    function. You could instead use the `rot` function as follows:

        C = rot([yaw, pitch, roll], [2, 1, 0])

    However, the `rpy_to_dcm` function will compute faster than the `rot`
    function.
    """

    # Check input.
    if isinstance(rpy, (list, tuple)):
        rpy = np.array(rpy)
    trs = (rpy.ndim == 2 and rpy.shape[0] != 3)
    s = np.pi/180 if degs else 1.0

    # Transpose.
    if trs:
        rpy = rpy.T

    if rpy.ndim == 1:
        # Get the cosine and sine functions.
        r, p, y = rpy
        cr = math.cos(s*r)
        sr = math.sin(s*r)
        cp = math.cos(s*p)
        sp = math.sin(s*p)
        cy = math.cos(s*y)
        sy = math.sin(s*y)

        # Build the output matrix.
        C = np.array([
            [            cp*cy,             cp*sy,   -sp],
            [-cr*sy + sr*sp*cy,  cr*cy + sr*sp*sy, sr*cp],
            [ sr*sy + cr*sp*cy, -sr*cy + cr*sp*sy, cr*cp]])
    else:
        # Get the cosine and sine functions.
        cr = np.cos(s*rpy[0])
        sr = np.sin(s*rpy[0])
        cp = np.cos(s*rpy[1])
        sp = np.sin(s*rpy[1])
        cy = np.cos(s*rpy[2])
        sy = np.sin(s*rpy[2])

        # Build the output matrix.
        C = np.zeros((rpy.shape[1], 3, 3))
        C[:, 0, 0] = cp*cy
        C[:, 0, 1] = cp*sy
        C[:, 0, 2] = -sp
        C[:, 1, 0] = -cr*sy + sr*sp*cy
        C[:, 1, 1] = cr*cy + sr*sp*sy
        C[:, 1, 2] = sr*cp
        C[:, 2, 0] = sr*sy + cr*sp*cy
        C[:, 2, 1] = -sr*cy + cr*sp*sy
        C[:, 2, 2] = cr*cp

    return C


def rot(ang, ax=None, degs=False):
    """
    Build a three-dimensional rotation matrix from the rotation angles `ang`
    about the successive axes `ax`.

    Parameters
    ----------
    ang : float, int, list, tuple, or np.ndarray
        Angle of rotation in radians (or degrees if `degs` is True).
    ax : str, float, int, list, tuple, or np.ndarray, default None
        Axis name(s) ('x', 'y', or 'z') or index(es) (x:0, y:1, or z:2) about
        which to rotate.
    degs : bool, default False
        Flag to interpret angles as degrees.

    Returns
    -------
    C : (3, 3) np.ndarray
        Rotation matrix.

    See Also
    --------
    rpy_to_dcm
    """

    # Check the angle.
    if np.ndim(ang) == 0: # scalar
        ang = np.array([float(ang)])
    elif isinstance(ang, (list, tuple)):
        ang = np.array(ang, dtype=float)

    # Check the axis.
    if isinstance(ax, str): # string
        ax = ax.lower()
        ax_dict = {'x': 0, 'y': 1, 'z': 2}
        ax = np.array([ax_dict[k] for k in ax if k in ax_dict.keys()])
    elif np.ndim(ax) == 0: # scalar
        ax = np.array([int(ax)])
    elif isinstance(ax, (list, tuple)):
        ax = np.array(ax, dtype=int)
    elif isinstance(ax, np.ndarray) and ax.dtype is not int:
        ax = ax.astype(int)

    # Check the degrees flag.
    s = np.pi/180 if degs else 1.0

    # Build the rotation matrix.
    N = len(ang)
    C = np.eye(3)
    for n in range(N):
        # Skip trivial rotations.
        if ang[n] == 0:
            continue

        # Get the cosine and sine of ang.
        co = np.cos(s*ang[n])
        si = np.sin(s*ang[n])

        # Get new rotation matrix.
        if ax[n] == 0:
            C_n = np.array([[1, 0, 0], [0, co, si], [0, -si, co]])
        elif ax[n] == 1:
            C_n = np.array([[co, 0, -si], [0, 1, 0], [si, 0, co]])
        elif ax[n] == 2:
            C_n = np.array([[co, si, 0], [-si, co, 0], [0, 0, 1]])

        # Pre-multiply the old rotation matrix by the new.
        C = C_n @ C

    return C


def rotate(C, vec):
    """
    Rotate a vector over time. `C` should be a 3d array, a stack of rotation
    matrices, and `vec` should be a matrix of vectors. Each layer of the stack
    and each column of the vector correspond to a different moment in time.

    Parameters
    ----------
    vec : (3, K) or (K, 3) list, tuple, or np.ndarray
        Matrix of vectors in which each column (or row) is a vector.
    C : (K, 3, 3) np.ndarray
        Rotation matrix or stack of K rotation matrices.

    Returns
    -------
    out : (3, K) or (K, 3) np.ndarray
        Matrix of rotated vectors in which each column (or row) is a vector.
    """

    # Check input.
    if isinstance(vec, (list, tuple)):
        vec = np.array(vec)
    if np.ndim(vec) != 2:
        raise ValueError("vec must be a 2d array.")
    if np.ndim(C) != 3:
        raise ValueError("C must be a 3d array.")
    trs = (vec.shape[0] != 3)

    # Transpose input.
    if trs:
        vec = vec.T

    # Initialize the output.
    K = vec.shape[1]
    out = np.zeros((3, K))

    # Perform the matrix-vector multiplication.
    out[0] = C[:, 0, 0]*vec[0] + C[:, 0, 1]*vec[1] + C[:, 0, 2]*vec[2]
    out[1] = C[:, 1, 0]*vec[0] + C[:, 1, 1]*vec[1] + C[:, 1, 2]*vec[2]
    out[2] = C[:, 2, 0]*vec[0] + C[:, 2, 1]*vec[1] + C[:, 2, 2]*vec[2]

    # Transpose output.
    if trs:
        out = out.T

    return out


def quat_to_rpy(q, degs=False):
    """
    Convert from a quaternion right-handed frame rotation to a roll, pitch, and
    yaw, z, y, x sequence of right-handed frame rotations. If frame 1 is rotated
    in a z, y, x sequence to become frame 2, then the quaternion `q` would also
    rotate a vector in frame 1 into frame 2.

    Parameters
    ----------
    q : (4,) or (4, K) or (K, 4) list, tuple, or np.ndarray
        A quaternion vector or a matrix of such vectors.
    degs : bool, default False
        Flag to convert angles to degrees.

    Returns
    -------
    rpy : (3,) or (3, K) or (K, 3) np.ndarray
        Roll, pitch, and yaw Euler angle.

    See Also
    --------
    rpy_to_quat

    Notes
    -----
    An example use case is the calculation a yaw-roll-pitch (z, y, x) frame
    rotation when given the quaternion that rotates from the [nose, right wing,
    down] body frame to the [north, east, down] navigation frame.

    From the dcm_to_rpy function, we know that the roll, `r`, pitch, `p`, and
    yaw, `y`, can be calculated as follows:

        r = arctan2(c23, c33)
        p = -arcsin(c13)
        y = arctan2(c12, c11)

    where the `d` variables are elements of the DCM. We also know from the
    quat_to_dcm function that

              .-                                                            -.
              |   2    2    2    2                                           |
              | (a  + b  - c  - d )    2 (b c + a d)       2 (b d - a c)     |
              |                                                              |
              |                       2    2    2    2                       |
        Dcm = |    2 (b c - a d)    (a  - b  + c  - d )    2 (c d + a b)     |
              |                                                              |
              |                                           2    2    2    2   |
              |    2 (b d + a c)       2 (c d - a b)    (a  - b  - c  + d )  |
              '-                                                            -'

    This means that the `d` variables can be defined in terms of the quaternion
    elements:

               2    2    2    2
        c11 = a  + b  - c  - d           c12 = 2 (b c + a d)

                                         c13 = 2 (b d - a c)
               2    2    2    2
        c33 = a  - b  - c  + d           c23 = 2 (c d + a b)

    This function does not take advantage of the more advanced formula for pitch
    because testing showed it did not help in this case.

    References
    ----------
    .. [1]  Titterton & Weston, "Strapdown Inertial Navigation Technology"
    """

    # Check input.
    if isinstance(q, (list, tuple)):
        q = np.array(q)
    trs = (q.ndim == 2 and q.shape[0] != 4)
    s = np.pi/180 if degs else 1.0

    # Transpose input.
    if trs:
        q = q.T

    # Get the required elements of the DCM.
    c11 = q[0]**2 + q[1]**2 - q[2]**2 - q[3]**2
    c12 = 2*(q[1]*q[2] + q[0]*q[3])
    c13 = 2*(q[1]*q[3] - q[0]*q[2])
    c23 = 2*(q[2]*q[3] + q[0]*q[1])
    c33 = q[0]**2 - q[1]**2 - q[2]**2 + q[3]**2

    # Build the output.
    r = np.arctan2(c23, c33)
    p = -np.arcsin(c13)
    y = np.arctan2(c12, c11)
    rpy = np.array([r, p, y])/s

    # Transpose output.
    if trs:
        rpy = rpy.T

    return rpy


def rpy_to_quat(rpy, degs=False):
    """
    Convert roll, pitch, and yaw Euler angles to a quaternion, `q`.

    Parameters
    ----------
    rpy : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Roll, pitch, and yaw Euler angle.
    degs : bool, default False
        Flag to interpret angles as degrees.

    Returns
    -------
    q : (4,) or (4, K) or (K, 4) np.ndarray
        Array of quaternion elements or matrix of K arrays of quaternion
        elements. The elements are a, b, c, and d where the quaterion `q` is
        a + b i + c j + d k.

    See Also
    --------
    quat_to_rpy

    Notes
    -----
    The equations to calculate the quaternion are

        h = cr cp cy + sr sp sy
        a = abs(h)
        b = sgn(h) (sr cp cy - cr sp sy)
        c = sgn(h) (cr sp cy + sr cp sy)
        d = sgn(h) (cr cp sy - sr sp cy)
        q = a + b i + c j + d k

    where `q` is the quaternion, the `c` and `s` prefixes represent cosine and
    sine, respectively, the `r`, `p`, and `y` suffixes represent roll, pitch,
    and yaw, respectively, and `sgn` is the sign function. The sign of `h` is
    used to make sure that the first element of the quaternion is always
    positive. This is simply a matter of convention.

    References
    ----------
    .. [1]  Titterton & Weston, "Strapdown Inertial Navigation Technology"
    """

    # Check inputs.
    if isinstance(rpy, (list, tuple)):
        rpy = np.array(rpy)
    s = np.pi/180 if degs else 1.0
    trs = (rpy.ndim == 2 and rpy.shape[0] != 3)

    # Transpose input.
    if trs:
        rpy = rpy.T

    # Get the cosine and sine functions.
    cr = np.cos(s*rpy[0]/2)
    sr = np.sin(s*rpy[0]/2)
    cp = np.cos(s*rpy[1]/2)
    sp = np.sin(s*rpy[1]/2)
    cy = np.cos(s*rpy[2]/2)
    sy = np.sin(s*rpy[2]/2)

    # Build the matrix of quaternion vectors.
    h = cr*cp*cy + sr*sp*sy
    sgn = np.sign(h)
    a = sgn*h
    b = sgn*(sr*cp*cy - cr*sp*sy)
    c = sgn*(cr*sp*cy + sr*cp*sy)
    d = sgn*(cr*cp*sy - sr*sp*cy)
    q = np.array([a, b, c, d])

    # Transpose output.
    if trs:
        q = q.T

    return q


def quat_to_dcm(q):
    """
    Convert from a quaternion, `q`, that performs a right-handed frame rotation
    from frame 1 to frame 2 to a direction cosine matrix, `C`, that also
    performs a right-handed frame rotation from frame 1 to frame 2. The `C`
    represents a z, y, x sequence of right-handed rotations.

    Parameters
    ----------
    q : (4,) or (4, K) or (K, 4) list, tuple, or np.ndarray
        Array of quaternion elements or matrix of K arrays of quaternion
        elements. The elements are a, b, c, and d where the quaterion `q` is
        a + b i + c j + d k.

    Returns
    -------
    C : (3, 3) or (K, 3, 3) np.ndarray
        Rotation matrix or stack of K rotation matrices.

    See Also
    --------
    dcm_to_quat

    Notes
    -----
    An example use case is to calculate a direction cosine matrix that rotates
    from the [nose, right wing, down] body frame to the [north, east, down]
    navigation frame when given a quaternion frame rotation that rotates from
    the [nose, right wing, down] body frame to the [north, east, down]
    navigation frame.

    The DCM can be defined in terms of the elements of the quaternion
    [a, b, c, d] as

            .-                                                            -.
            |   2    2    2    2                                           |
            | (a  + b  - c  - d )    2 (b c + a d)       2 (b d - a c)     |
            |                                                              |
            |                       2    2    2    2                       |
        C = |    2 (b c - a d)    (a  - b  + c  - d )    2 (c d + a b)     |
            |                                                              |
            |                                           2    2    2    2   |
            |    2 (b d + a c)       2 (c d - a b)    (a  - b  - c  + d )  |
            '-                                                            -'

    References
    ----------
    .. [1]  Titterton & Weston, "Strapdown Inertial Navigation Technology"
    """

    # Check input.
    if isinstance(q, (list, tuple)):
        q = np.array(q)
    trs = (q.ndim == 2 and q.shape[0] != 4)

    # Transpose input.
    if trs:
        q = q.T

    # Parse quaternion array.
    a = q[0]
    b = q[1]
    c = q[2]
    d = q[3]

    # Square the elements of the quaternion.
    a2 = a**2
    b2 = b**2
    c2 = c**2
    d2 = d**2

    # Build the DCM.
    if q.ndim == 1:
        C = np.array([
            [a2 + b2 - c2 - d2, 2*(b*c + a*d), 2*(b*d - a*c)],
            [2*(b*c - a*d), a2 - b2 + c2 - d2, 2*(c*d + a*b)],
            [2*(b*d + a*c), 2*(c*d - a*b), a2 - b2 - c2 + d2]])
    else:
        C = np.zeros((len(a), 3, 3))
        C[:, 0, 0] = a2 + b2 - c2 - d2
        C[:, 0, 1] = 2*(b*c + a*d)
        C[:, 0, 2] = 2*(b*d - a*c)
        C[:, 1, 0] = 2*(b*c - a*d)
        C[:, 1, 1] = a2 - b2 + c2 - d2
        C[:, 1, 2] = 2*(c*d + a*b)
        C[:, 2, 0] = 2*(b*d + a*c)
        C[:, 2, 1] = 2*(c*d - a*b)
        C[:, 2, 2] = a2 - b2 - c2 + d2

    return C


def dcm_to_quat(C):
    """
    Convert a direction cosine matrix, `C`, to a quaternion vector, `q`. Here,
    the `C` is considered to represent a z, y, x sequence of right-handed
    rotations. This means it has the same sense as the quaternion.

    Parameters
    ----------
    C : (3, 3) or (K, 3, 3) list, tuple, or np.ndarray
        Rotation matrix or stack of K rotation matrices.

    Returns
    -------
    q : (4,) or (4, K) np.ndarray
        Array of quaternion elements or matrix of K arrays of quaternion
        elements. The elements are a, b, c, and d where the quaterion `q` is
        a + b i + c j + d k.

    See Also
    --------
    quat_to_dcm

    Notes
    -----
    The implementation here is Cayley's method for obtaining the quaternion. It
    is used because of its superior numerical accuracy. This comes from the fact
    that it uses all nine of the elements of the DCM matrix. It also does not
    suffer from numerical instability due to division as some other methods do.

    References
    ----------
    .. [1]  Titterton & Weston, "Strapdown Inertial Navigation Technology"
    .. [2]  Soheil Sarabandi and Federico Thomas, "A Survey on the Computation
            of Quaternions from Rotation Matrices," Journal of Mechanisms and
            Robotics, 2018.
    """

    # Check input.
    if isinstance(C, (list, tuple)):
        C = np.array(C)

    # Check for zero matrices.
    C_sums = np.sum(np.sum(np.abs(C), axis=-1), axis=-1)
    if np.any(C_sums == 0):
        raise ValueError("Input matrix C must not be zeros.")

    # Parse the elements of C.
    if C.ndim == 2:
        c11 = C[0, 0];      c12 = C[0, 1];      c13 = C[0, 2]
        c21 = C[1, 0];      c22 = C[1, 1];      c23 = C[1, 2]
        c31 = C[2, 0];      c32 = C[2, 1];      c33 = C[2, 2]
    else:
        c11 = C[:, 0, 0];   c12 = C[:, 0, 1];   c13 = C[:, 0, 2]
        c21 = C[:, 1, 0];   c22 = C[:, 1, 1];   c23 = C[:, 1, 2]
        c31 = C[:, 2, 0];   c32 = C[:, 2, 1];   c33 = C[:, 2, 2]

    # Get the squared sums and differences of off-diagonal pairs.
    p12 = (c12 + c21)**2
    p23 = (c23 + c32)**2
    p31 = (c31 + c13)**2
    m12 = (c12 - c21)**2
    m23 = (c23 - c32)**2
    m31 = (c31 - c13)**2

    # Get squared expressions of diagonal values.
    d1 = (c11 + c22 + c33 + 1)**2
    d2 = (c11 - c22 - c33 + 1)**2
    d3 = (c22 - c11 - c33 + 1)**2
    d4 = (c33 - c11 - c22 + 1)**2

    # Get the components.
    a = 0.25*np.sqrt(d1 + m23 + m31 + m12)
    b = 0.25*np.sign(c23 - c32)*np.sqrt(m23 + d2 + p12 + p31)
    c = 0.25*np.sign(c31 - c13)*np.sqrt(m31 + p12 + d3 + p23)
    d = 0.25*np.sign(c12 - c21)*np.sqrt(m12 + p31 + p23 + d4)

    # Build the quaternion.
    q = np.array([a, b, c, d])

    # Check the output.
    zero_q = (np.sum(np.abs(q), axis=0) < 1e-15)
    if np.any(zero_q):
        raise ValueError("The provided output is incorrectly all zeros, \n"
                + "probably due to the input being very close to a 180 "
                + "degree rotation.")

    return q


def dcm_inertial_to_ecef(t):
    """
    Create the passive rotation matrix from the Earth-centered Inertial (ECI)
    frame to the Earth-centered, Earth-fixed (ECEF) frame.

    Parameters
    ----------
    t : float or (K,) list, tuple, or np.ndarray
        Time of rotation where t = 0 means the ECI and ECEF frames are aligned.

    Returns
    -------
    C : (3, 3) or (K, 3, 3) np.ndarray
        Passive rotation matrix or stack of K such matrices.

    Notes
    -----
    The matrix this function calculates is simply

        .-                         -.
        | cos(theta)  sin(theta)  0 |
        |-sin(theta)  cos(theta)  0 |       : theta = W_EI * t
        |      0           0      1 |
        '-                         -'
    """

    # Check input.
    if isinstance(t, (list, tuple)):
        t = np.array(t)

    # Get cosine and sine of latitude and longitude.
    co = np.cos(W_EI*t)
    si = np.sin(W_EI*t)

    # Build the rotation matrix.
    if np.ndim(t) == 0: # scalar
        C = np.array([
            [co, si, 0],
            [-si, co, 0],
            [0, 0, 1]])
    else:
        print(type(t))
        C = np.zeros((len(t), 3, 3))
        C[:, 0, 0] = co
        C[:, 0, 1] = si
        C[:, 1, 0] = -si
        C[:, 1, 1] = co
        C[:, 2, 2] = 1.0

    return C


def dcm_ecef_to_navigation(lat, lon, ned=True, degs=False):
    """
    Create the passive rotation matrix from the Earth-centered, Earth-fixed
    (ECEF) frame to the local-level navigation frame.

    Parameters
    ----------
    lat : float or (K,) list, tuple, or np.ndarray
        Geodetic latitude in radians (or degrees if `degs` is True).
    lon : float or (K,) list, tuple, or np.ndarray
        Geodetic longitude in radians (or degrees if `degs` is True).
    ned : bool, default True
        Flag to use NED (True) or ENU (False) orientation.
    degs : bool, default False
        Flag to interpret angles as degrees.

    Returns
    -------
    C : (3, 3) or (K, 3, 3) np.ndarray
        Passive rotation matrix or stack of K such matrices.
    """

    # Check input.
    if isinstance(lat, (list, tuple)):
        lat = np.array(lat, dtype=float)
    if isinstance(lon, (list, tuple)):
        lon = np.array(lon, dtype=float)
    s = np.pi/180 if degs else 1.0

    # Get cosine and sine of latitude and longitude.
    clat = np.cos(s*lat)
    slat = np.sin(s*lat)
    clon = np.cos(s*lon)
    slon = np.sin(s*lon)

    # Get the rotation matrix elements.
    if ned:
        c11 = -slat*clon;   c12 = -slat*slon;   c13 = clat
        c21 = -slon;        c22 = clon;         c23 = 0*lat
        c31 = -clat*clon;   c32 = -clat*slon;   c33 = -slat
    else:
        c11 = -slon;        c12 = clon;         c13 = 0*lat
        c21 = -slat*clon;   c22 = -slat*slon;   c23 = clat
        c31 = clat*clon;    c32 = clat*slon;    c33 = slat

    # Assemble the rotation matrix.
    if np.ndim(lat) == 0: # scalar
        C = np.array([
            [c11, c12, c13],
            [c21, c22, c23],
            [c31, c32, c33]])
    else:
        C = np.zeros((len(lat), 3, 3))
        C[:, 0, 0] = c11;   C[:, 0, 1] = c12;   C[:, 0, 2] = c13
        C[:, 1, 0] = c21;   C[:, 1, 1] = c22;   C[:, 1, 2] = c23
        C[:, 2, 0] = c31;   C[:, 2, 1] = c32;   C[:, 2, 2] = c33

    return C

# ---------------------------
# Reference-frame Conversions
# ---------------------------

def geodetic_to_ecef(llh, degs=False):
    """
    Convert position in geodetic coordinates to ECEF (Earth-centered,
    Earth-fixed) coordinates. This method is direct and not an approximation.
    This follows the WGS-84 definitions (see WGS-84 Reference System (DMA report
    TR 8350.2)).

    Parameters
    ----------
    llh : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Vector of geodetic position in terms of latitude in radians (or degrees
        if `degs` is True), longitude in radians (or degrees if `degs` is True),
        and height above ellipsoid in meters, or matrix of such vectors.
    degs : bool, default False
        Flag to interpret angles as degrees.

    Returns
    -------
    pe : (3,) or (3, K) or (K, 3) np.ndarray
        Position vector in ECEF coordinates in meters or matrix of such vectors.

    See Also
    --------
    ecef_to_geodetic

    Notes
    -----
    The distance from the z axis is

             .-  aE       -.
        re = |  ---- + hae | cos(lat)
             '- klat      -'

    where `aE` is the semi-major radius of the earth and

                  .---------------
                 /      2   2
        klat = `/ 1 - eE sin (lat)

    The `eE` value is the eccentricity of the earth. Knowing the distance from
    the z axis, we can get the x and y coordinates:

        xe = re cos(lon)            ye = re sin(lon) .

    The z-axis coordinate is

             .-  aE         2       -.
        ze = |  ---- (1 - eE ) + hae | sin(lat) .
             '- klat                -'

    The output vector `pe` is made up of `xe`, `ye`, and `ze`: [xe, ye, ze].

    Several of these equations are admittedly not intuitively obvious. The
    interested reader should refer to external texts for insight.

    References
    ----------
    .. [1]  WGS-84 Reference System (DMA report TR 8350.2)
    .. [2]  Inertial Navigation: Theory and Implementation by David Woodburn
    """

    # Check inputs.
    if isinstance(llh, (list, tuple)):
        llh = np.array(llh)
    trs = (llh.ndim == 2 and llh.shape[0] != 3)
    s = np.pi/180 if degs else 1.0

    # Transpose input.
    if trs:
        llh = llh.T

    # Parse the input.
    lat = llh[0]
    lon = llh[1]
    hae = llh[2]

    # Get the intermediate values.
    slat = np.sin(s*lat)
    clat = np.cos(s*lat)
    klat = np.sqrt(1 - E2*slat**2)
    Rt = A_E/klat
    Rm = (Rt/klat**2)*(1 - E2)

    # Get the x, y, and z coordinates.
    re = (Rt + hae)*clat
    xe = re*np.cos(s*lon)
    ye = re*np.sin(s*lon)
    ze = (Rm*klat**2 + hae)*slat
    pe = np.array([xe, ye, ze])

    # Transpose output.
    if trs:
        pe = pe.T

    return pe


def ecef_to_geodetic(pe, degs=False):
    """
    Convert an ECEF (Earth-centered, Earth-fixed) position to geodetic
    coordinates. This follows the WGS-84 definitions (see WGS-84 Reference
    System (DMA report TR 8350.2)).

    Parameters
    ----------
    pe : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Position vector in ECEF coordinates in meters or matrix of such vectors.
    degs : bool, default False
        Flag to convert angles to degrees.

    Returns
    -------
    llh : (3,) or (3, K) or (K, 3) np.ndarray
        Vector of geodetic position in terms of latitude in radians (or degrees
        if `degs` is True), longitude in radians (or degrees if `degs` is True),
        and height above ellipsoid in meters, or matrix of such vectors.

    See Also
    --------
    geodetic_to_ecef

    Notes
    -----
    Note that inherent in solving the problem of getting the geodetic latitude
    and ellipsoidal height is finding the roots of a quartic polynomial because
    we are looking for the intersection of a line with an ellipse. While there
    are closed-form solutions to this problem (see Wikipedia), each point has
    potentially four solutions and the solutions are not numerically stable.
    Instead, this function uses the Newton-Raphson method to iteratively solve
    for the geodetic coordinates.

    First, we want to approximate the values for geodetic latitude, `lat`, and
    height above ellipsoid, `hae`, given the pe = [xe, ye, ze] position in the
    ECEF frame:

                                .--------
         ^                     /  2     2            ^
        hae = 0         re = `/ xe  + ye            lat = arctan2(ze, re),

    where `re` is the distance from the z axis of the ECEF frame. (While there
    are better approximations for `hae` than zero, the improvement in accuracy
    was not enough to reduce the number of iterations and the additional
    computational burden could not be justified.)  Then, we will iteratively use
    this approximation for `lat` and `hae` to calculate what `re` and `ze` would
    be, get the residuals given the correct `re` and `ze` values in the ECEF
    frame, use the inverse Jacobian to calculate the corresponding residuals of
    `lat` and `hae`, and update our approximations for `lat` and `hae` with
    those residuals. In testing millions of randomly generated points, three
    iterations was sufficient to reach the limit of numerical precision for
    64-bit floating-point numbers.

    So, first, let us define the transverse, `Rt`, and meridional, `Rm`, radii
    and the cosine and sine of the latitude:

                                                              .---------------
              aE               aE  .-      2 -.              /      2   2  ^
        Rt = ----       Rm = ----- | 1 - eE   |     klat = `/ 1 - eE sin (lat) ,
             klat                3 '-        -'
                             klat
                  ^                               ^
        co = cos(lat)                   si = sin(lat)

    where `eE` is the eccentricity of the Earth, and `aE` is the semi-major
    radius of the Earth. The ECEF-frame `re` and `ze` values given the
    approximations to geodetic latitude and height above ellipsoid are

         ^             ^                 ^              2   ^
        re = co (Rt + hae)              ze = si (Rm klat + hae) .

    We already know the correct values for `re` and `ze`, so we can get
    residuals:

         ~         ^                     ~         ^
        re = re - re                    ze = ze - ze .

    We can relate the `re` and `ze` residuals to the `lat` and `hae` residuals
    by using the inverse Jacobian matrix:

        .-  ~  -.       .-  ~ -.
        |  lat  |    -1 |  re  |
        |       | = J   |      | .
        |   ~   |       |   ~  |
        '- hae -'       '- ze -'

    With a bit of algebra, we can combine and simplify the calculation of the
    Jacobian with the calculation of the `lat` and `hae` residuals:

         ~         ~       ~             ~         ~       ~         ^
        hae = (si ze + co re)           lat = (co ze - si re)/(Rm + hae) .

    Conceptually, this is the backwards rotation of the (`re`, `ze`) residuals
    vector by the angle `lat`, where the resulting y component of the rotated
    vector is treated as an arc length and converted to an angle, `lat`, using
    the radius `Rm` + `hae`. With the residuals for `lat` and `hae`, we can
    update our approximations for `lat` and `hae`:

         ^     ^     ~                   ^     ^     ~
        hae = hae + hae                 lat = lat + lat

    and iterate again. Finally, the longitude, `lon`, is exactly the arctangent
    of the ECEF `xe` and `ye` values:

        lon = arctan2(ye, xe) .

    References
    ----------
    .. [1]  WGS-84 Reference System (DMA report TR 8350.2)
    .. [2]  Inertial Navigation: Theory and Implementation by David Woodburn
    """

    # Check inputs.
    if isinstance(pe, (list, tuple)):
        pe = np.array(pe)
    trs = (pe.ndim == 2 and pe.shape[0] != 3)
    s = np.pi/180 if degs else 1.0

    # Transpose input.
    if trs:
        pe = pe.T

    # Parse input.
    xe = pe[0]
    ye = pe[1]
    ze = pe[2]

    # Initialize the height above the ellipsoid.
    hhae = 0

    # Get the true radial distance from the z axis.
    re = np.sqrt(xe**2 + ye**2)

    # Initialize the estimated ground latitude.
    hlat = np.arctan2(ze, re) # bound to [-pi/2, pi/2]

    # Iterate to reduce residuals of the estimated closest point on the ellipse.
    for _ in range(3):
        # Using the estimated ground latitude, get the cosine and sine.
        co = np.cos(hlat)
        si = np.sin(hlat)
        klat2 = 1 - E2*si**2
        klat = np.sqrt(klat2)
        Rt = A_E/klat
        Rm = (Rt/klat2)*(1 - E2)

        # Get the estimated position in the meridional plane (the plane defined
        # by the longitude and the z axis).
        hre = co*(Rt + hhae)
        hze = si*(Rm*klat2 + hhae)

        # Get the residuals.
        tre = re - hre
        tze = ze - hze

        # Using the inverse Jacobian, get the residuals in lat and hae.
        tlat = (co*tze - si*tre)/(Rm + hhae)
        thae = si*tze + co*tre

        # Adjust the estimated ground latitude and ellipsoidal height.
        hlat = hlat + tlat
        hhae = hhae + thae

    # Get the longitude.
    lon = np.arctan2(ye, xe)

    # Assemble the matrix.
    llh = np.array([hlat/s, lon/s, hhae])

    # Transpose output.
    if trs:
        llh = llh.T

    return llh


def tangent_to_ecef(pt, pe0, ned=True):
    """
    Convert local, tangent Cartesian North, East, Down (NED) or East, North, Up
    (ENU) coordinates, with a defined local origin, to ECEF (Earth-centered,
    Earth-fixed) coordinates.

    Parameters
    ----------
    pt : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Position vector in local, tangent coordinates in meters or matrix of
        such vectors. This need not be the same shape as `pe0`.
    pe0 : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Position vector of the local, tangent frame's origin in ECEF coordinates
        in meters or matrix of such vectors. This need not be the same shape as
        `pt`. This input cannot be inferred from `pt`.
    ned : bool, default True
        Flag to use NED (True) or ENU (False) orientation.

    Returns
    -------
    pe : (3,) or (3, K) or (K, 3) np.ndarray
        Position vector in ECEF coordinates in meters or matrix of such vectors.

    See Also
    --------
    ecef_to_tangent

    Notes
    -----
    First, the ECEF origin is converted to geodetic coordinates. Then, those
    coordinates are used to calculate a rotation matrix from the local, tangent
    Cartesian frame to the ECEF frame:

              .-                     -.
              |  -sp cl  -sl  -cp cl  |
        Cet = |  -sp sl   cl  -cp sl  |      NED
              |    cp      0   -sp    |
              '-                     -'

              .-                     -.
              |   -sl  -sp cl  cp cl  |
        Cet = |    cl  -sp sl  cp sl  |      ENU
              |     0    cp     sp    |
              '-                     -'

    where `sp` and `cp` are the sine and cosine of the origin latitude,
    respectively, and `sl` and `cl` are the sine and cosine of the origin
    longitude, respectively. Then, the displacement vector of the ECEF position
    relative to the ECEF origin is rotated into the local, tangent frame:

        pe = Cet pt + pe0
    """

    # Check inputs.
    if isinstance(pt, (list, tuple)):
        pt = np.array(pt)
    if isinstance(pe0, (list, tuple)):
        pe0 = np.array(pe0)
    trs = (pt.ndim == 2 and pt.shape[0] != 3) \
            or (pe0.ndim == 2 and pe0.shape[0] != 3)

    # Transpose inputs.
    if trs:
        pt = pt.T
        pe0 = pe0.T

    # Get the local-level coordinates.
    llh0 = ecef_to_geodetic(pe0)

    # Get the cosines and sines of the latitude and longitude.
    cp = np.cos(llh0[0])
    sp = np.sin(llh0[0])
    cl = np.cos(llh0[1])
    sl = np.sin(llh0[1])

    # Get the local, tangent coordinates.
    if ned:
        xe = -sp*cl*pt[0] - sl*pt[1] - cp*cl*pt[2] + pe0[0]
        ye = -sp*sl*pt[0] + cl*pt[1] - cp*sl*pt[2] + pe0[1]
        ze =     cp*pt[0]            -    sp*pt[2] + pe0[2]
    else:
        xe = -sl*pt[0] - sp*cl*pt[1] + cp*cl*pt[2] + pe0[0]
        ye =  cl*pt[0] - sp*sl*pt[1] + cp*sl*pt[2] + pe0[1]
        ze =           +    cp*pt[1] +    sp*pt[2] + pe0[2]
    pe = np.array([xe, ye, ze])

    # Transpose output.
    if trs:
        pe = pe.T

    return pe


def ecef_to_tangent(pe, pe0=None, ned=True):
    """
    Convert ECEF (Earth-centered, Earth-fixed) coordinates, with a defined local
    origin, to local, tangent Cartesian North, East, Down (NED) or East, North,
    Up (ENU) coordinates.

    Parameters
    ----------
    pe : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Position vector in ECEF coordinates in meters or matrix of such vectors.
        This need not be the same shape as `pe0`.
    pe0 : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Position vector of the local, tangent frame's origin in ECEF coordinates
        in meters or matrix of such vectors. This need not be the same shape as
        `pe`. If not provided, the first values of `pe` will be used.
    ned : bool, default True
        Flag to use NED (True) or ENU (False) orientation.

    Returns
    -------
    pt : (3,) or (3, K) or (K, 3) np.ndarray
        Position vector in local, tangent coordinates in meters or matrix of
        such vectors.

    See Also
    --------
    tangent_to_ecef

    Notes
    -----
    First, the ECEF origin is converted to geodetic coordinates. Then, those
    coordinates are used to calculate a rotation matrix from the ECEF frame to
    the local, tangent Cartesian frame:

              .-                     -.
              |  -sp cl  -sp sl   cp  |
        Cte = |    -sl     cl      0  |      NED
              |  -cp cl  -cp sl  -sp  |
              '-                     -'

              .-                     -.
              |    -sl     cl      0  |
        Cte = |  -sp cl  -sp sl   cp  |      ENU
              |   cp cl   cp sl   sp  |
              '-                     -'

    where `sp` and `cp` are the sine and cosine of the origin latitude,
    respectively, and `sl` and `cl` are the sine and cosine of the origin
    longitude, respectively. Then, the displacement vector of the ECEF position
    relative to the ECEF origin is rotated into the local, tangent frame:

        pt = Cte (pe - pe0)
    """

    # Check the inputs.
    if isinstance(pe, (list, tuple)):
        pe = np.array(pe)
    if isinstance(pe0, (list, tuple)):
        pe0 = np.array(pe0)
    trs = (pe.ndim == 2 and pe.shape[0] != 3)

    # Transpose inputs.
    if trs:
        pe = pe.T
        if pe0 is not None:
            pe0 = pe0.T

    # Infer origin.
    if pe0 is None:
        if pe.ndim == 2:
            pe0 = pe[:, 0]
        else:
            pe0 = pe.copy()

    # Get the local-level coordinates.
    llh0 = ecef_to_geodetic(pe0)

    # Get the cosines and sines of the latitude and longitude.
    cp = np.cos(llh0[0])
    sp = np.sin(llh0[0])
    cl = np.cos(llh0[1])
    sl = np.sin(llh0[1])

    # Get the displacement ECEF vector from the origin.
    dxe = pe[0] - pe0[0]
    dye = pe[1] - pe0[1]
    dze = pe[2] - pe0[2]

    # Get the local, tangent coordinates.
    if ned:
        xt = -sp*cl*dxe - sp*sl*dye + cp*dze
        yt =    -sl*dxe +    cl*dye
        zt = -cp*cl*dxe - cp*sl*dye - sp*dze
    else:
        xt =    -sl*dxe +    cl*dye
        yt = -sp*cl*dxe - sp*sl*dye + cp*dze
        zt =  cp*cl*dxe + cp*sl*dye + sp*dze
    pt = np.array([xt, yt, zt])

    # Transpose output.
    if trs:
        pt = pt.T

    return pt


def curvilinear_to_ecef(pc, pe0, ned=True):
    """
    Convert position in curvilinear coordinates to ECEF (Earth-centered,
    Earth-fixed) coordinates. This function relies on other functions in this
    library to calculate the values.

    Parameters
    ----------
    pc : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Position vector in local, curvilinear coordinates in meters or matrix of
        such vectors. This need not be the same shape as `pe0`.
    pe0 : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Position vector of the local, curvilinear frame's origin in ECEF
        coordinates in meters or matrix of such vectors. This need not be the
        same shape as `pc`. This cannot be inferred from `pc`.
    ned : bool, default True
        Flag to use NED (True) or ENU (False) orientation.

    Returns
    -------
    pe : (3,) or (3, K) or (K, 3) np.ndarray
        Position vector in ECEF coordinates in meters or matrix of such vectors.

    See Also
    --------
    ecef_to_curvilinear
    """

    # Check the inputs.
    if isinstance(pc, (list, tuple)):
        pc = np.array(pc)
    if isinstance(pe0, (list, tuple)):
        pe0 = np.array(pe0)

    # Make conversions.
    llh0 = ecef_to_geodetic(pe0)
    llh = curvilinear_to_geodetic(pc, llh0, ned)
    pe = geodetic_to_ecef(llh)

    return pe


def ecef_to_curvilinear(pe, pe0=None, ned=True):
    """
    Convert position in ECEF (Earth-centered, Earth-fixed) coordinates to
    curvilinear coordinates. This function relies on other functions in this
    library to calculate the values.

    Parameters
    ----------
    pe : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Position vector in ECEF coordinates in meters or matrix of such vectors.
        This need not be the same shape as `pe0`.
    pe0 : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Position vector of the local, curvilinear frame's origin in ECEF
        coordinates in meters or matrix of such vectors. This need not be the
        same shape as `pe`. If not provided, the first values of `pe` will be
        used.
    ned : bool, default True
        Flag to use NED (True) or ENU (False) orientation.

    Returns
    -------
    pt : (3,) or (3, K) or (K, 3) np.ndarray
        Position vector in local, tangent coordinates in meters or matrix of
        such vectors.

    See Also
    --------
    ecef_to_curvilinear
    """

    # Check the inputs.
    if isinstance(pe, (list, tuple)):
        pe = np.array(pe)
    if isinstance(pe0, (list, tuple)):
        pe0 = np.array(pe0)
    trs = (pe.ndim == 2 and pe.shape[0] != 3)

    # Transpose inputs.
    if trs:
        pe = pe.T
        if pe0 is not None:
            pe0 = pe0.T

    # Infer origin.
    if pe0 is None:
        if pe.ndim == 2:
            pe0 = pe[:, 0]
        else:
            pe0 = pe.copy()

    # Convert coordinates.
    llh = ecef_to_geodetic(pe)
    llh0 = ecef_to_geodetic(pe0)
    pc = geodetic_to_curvilinear(llh, llh0, ned)

    # Transpose output.
    if trs:
        pc = pc.T

    return pc


def tangent_to_geodetic(pt, llh0, ned=True, degs=False):
    """
    Convert position in tangent coordinates to geodetic coordinates. This
    function relies on other functions in this library to calculate the values.

    Parameters
    ----------
    pt : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Position vector in local, tangent coordinates in meters or matrix of
        such vectors. This need not be the same shape as `llh0`.
    llh0 : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Vector of geodetic position of the local, tangent frame's origin in
        terms of latitude in radians (or degrees if `degs` is True), longitude
        in radians (or degrees if `degs` is True), and height above ellipsoid in
        meters, or matrix of such vectors. This need not be the same shape as
        `pt`. This cannot be inferred from `pt`.
    ned : bool, default True
        Flag to use NED (True) or ENU (False) orientation.
    degs : bool, default False
        Flag to interpret angles as degrees.

    Returns
    -------
    llh : (3,) or (3, K) or (K, 3) np.ndarray
        Vector of geodetic position in terms of latitude in radians (or degrees
        if `degs` is True), longitude in radians (or degrees if `degs` is True),
        and height above ellipsoid in meters, or matrix of such vectors.

    See Also
    --------
    geodetic_to_tangent
    """

    # Check the inputs.
    if isinstance(pt, (list, tuple)):
        pt = np.array(pt)
    if isinstance(llh0, (list, tuple)):
        llh0 = np.array(llh0)

    # Make conversions.
    pe0 = geodetic_to_ecef(llh0, degs)
    pe = tangent_to_ecef(pt, pe0, ned)
    llh = ecef_to_geodetic(pe, degs)

    return llh


def geodetic_to_tangent(llh, llh0=None, ned=True, degs=False):
    """
    Convert position in geodetic coordinates to tangent coordinates. This
    function relies on other functions in this library to calculate the values.

    Parameters
    ----------
    llh : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Vector of geodetic position in terms of latitude in radians (or degrees
        if `degs` is True), longitude in radians (or degrees if `degs` is True),
        and height above ellipsoid in meters, or matrix of such vectors. This
        need not be the same shape as `llh0`.
    llh0 : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Vector of geodetic position of the local, tangent frame's origin in
        terms of latitude in radians (or degrees if `degs` is True), longitude
        in radians (or degrees if `degs` is True), and height above ellipsoid in
        meters, or matrix of such vectors. This need not be the same shape as
        `llh`. If not provided, the first values of `llh` will be used.
    ned : bool, default True
        Flag to use NED (True) or ENU (False) orientation.
    degs : bool, default False
        Flag to interpret angles as degrees.

    Returns
    -------
    pt : (3,) or (3, K) or (K, 3) np.ndarray
        Position vector in local, tangent coordinates in meters or matrix of
        such vectors.

    See Also
    --------
    tangent_to_geodetic
    """

    # Check the inputs.
    if isinstance(llh, (list, tuple)):
        llh = np.array(llh)
    if isinstance(llh0, (list, tuple)):
        llh0 = np.array(llh0)
    trs = (llh.ndim == 2 and llh.shape[0] != 3)

    # Transpose inputs.
    if trs:
        llh = llh.T
        if llh0 is not None:
            llh0 = llh0.T

    # Infer origin.
    if llh0 is None:
        if llh.ndim == 2:
            llh0 = llh[:, 0]
        else:
            llh0 = llh.copy()

    # Make conversions.
    pe0 = geodetic_to_ecef(llh0, degs)
    pe = geodetic_to_ecef(llh, degs)
    pt = ecef_to_tangent(pe, pe0, ned)

    # Transpose output.
    if trs:
        pt = pt.T

    return pt


def curvilinear_to_geodetic(pc, llh0, ned=True, degs=False):
    """
    Convert local, curvilinear position in either North, East, Down (NED) or
    East, North, Up (ENU) coordinates to geodetic coordinates with a geodetic
    origin. The solution is iterative, using the Newton-Raphson method.

    Parameters
    ----------
    pc : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Position vector in local, curvilinear coordinates in meters or matrix of
        such vectors. This need not be the same shape as `llh0`.
    llh0 : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Vector of geodetic position of the local, curvilinear frame's origin in
        terms of latitude in radians (or degrees if `degs` is True), longitude
        in radians (or degrees if `degs` is True), and height above ellipsoid in
        meters, or matrix of such vectors. This need not be the same shape as
        `pc`. This cannot be inferred from `pc`.
    ned : bool, default True
        Flag to use NED (True) or ENU (False) orientation.
    degs : bool, default False
        Flag to interpret angles as degrees.

    Returns
    -------
    llh : (3,) or (3, K) or (K, 3) np.ndarray
        Vector of geodetic position in terms of latitude in radians (or degrees
        if `degs` is True), longitude in radians (or degrees if `degs` is True),
        and height above ellipsoid in meters, or matrix of such vectors.

    See Also
    --------
    geodetic_to_curvilinear

    Notes
    -----
    The equations to get curvilinear coordinates from geodetic are

        .-  -.   .-                                -.
        | xc |   |     (Rm + hae) (lat - lat0)      |
        | yc | = | (Rt + hae) cos(lat) (lon - lon0) |       NED
        | zc |   |           (hae0 - hae)           |
        '-  -'   '-                                -'

    or

        .-  -.   .-                                -.
        | xc |   | (Rt + hae) cos(lat) (lon - lon0) |
        | yc | = |     (Rm + hae) (lat - lat0)      |       ENU
        | zc |   |           (hae - hae0)           |
        '-  -'   '-                                -'

    where

                                       2                .---------------
              aE             aE (1 - eE )              /      2   2
        Rt = ----       Rm = ------------     klat = `/ 1 - eE sin (lat) .
             klat                    3
                                 klat

    Here, `aE` is the semi-major axis of the Earth, `eE` is the eccentricity of
    the Earth, `Rt` is the transverse radius of curvature of the Earth, and `Rm`
    is the meridional radius of curvature of the Earth. Unfortunately, the
    reverse process to get geodetic coordinates from curvilinear coordinates is
    not as straightforward. So the Newton-Raphson method is used. Using NED as
    an example, with the above equations, we can write the differential relation
    as follows:

        .-  ~ -.     .-  ~  -.              .-           -.
        |  xc  |     |  lat  |              |  J11   J12  |
        |      | = J |       |          J = |             | ,
        |   ~  |     |   ~   |              |  J21   J22  |
        '- yc -'     '- lon -'              '-           -'

    where the elements of the Jacobian J are

              .-     2         -.
              |  3 eE Rm si co  |   ^
        J11 = | --------------- | (lat - lat0) + Rm + h
              |          2      |
              '-     klat      -'

        J12 = 0

              .- .-   2  2    -.         -.
              |  |  eE co      |          |      ^
        J21 = |  | ------- - 1 | Rt - hae | si (lon - lon0)
              |  |      2      |          |
              '- '- klat      -'         -'

        J22 = (Rt + hae) co .

    where `si` and `co` are the sine and cosine of `lat`, respectively. Using
    the inverse Jacobian, we can get the residuals of `lat` and `lon` from the
    residuals of `xc` and `yc`:

                     ~        ~
         ~      J22 xc - J12 yc
        lat = -------------------
               J11 J22 - J21 J12

                     ~        ~
         ~      J11 yc - J21 xc
        lon = ------------------- .
               J11 J22 - J21 J12

    These residuals are added to the estimated `lat` and `lon` values and
    another iteration begins.

    References
    ----------
    .. [1]  Titterton & Weston, "Strapdown Inertial Navigation Technology"
    .. [2]  https://en.wikipedia.org/wiki/Earth_radius#Meridional
    .. [3]  https://en.wikipedia.org/wiki/Earth_radius#Prime_vertical
    """

    # Check the inputs.
    if isinstance(pc, (list, tuple)):
        pc = np.array(pc)
    if isinstance(llh0, (list, tuple)):
        llh0 = np.array(llh0)
    trs = (pc.ndim == 2 and pc.shape[0] != 3) \
            or (llh0.ndim == 2 and llh0.shape[0] != 3)
    s = np.pi/180 if degs else 1.0

    # Transpose inputs.
    if trs:
        pc = pc.T
        llh0 = llh0.T

    # Parse the inputs.
    xc = pc[0]
    yc = pc[1]
    zc = pc[2]
    lat0 = llh0[0]
    lon0 = llh0[1]
    hae0 = llh0[2]

    # Scale the angles.
    Lat0 = s*lat0
    Lon0 = s*lon0

    # Flip the orientation if it is ENU.
    if ned:
        Xc = xc
        Yc = yc
        Zc = zc
    else:
        Xc =  yc
        Yc =  xc
        Zc = -zc

    # Define height.
    hae = hae0 - Zc

    # Initialize the latitude and longitude.
    hlat = Lat0 + Xc/(A_E + hae)
    hlon = Lon0 + Yc/((A_E + hae)*np.cos(hlat))

    # Iterate.
    for _ in range(3):
        # Get the sine and cosine of latitude.
        si = np.sin(hlat)
        co = np.cos(hlat)

        # Get the parallel and meridional radii of curvature.
        kp2 = 1 - E2*si**2
        klat = np.sqrt(kp2)
        Rt = A_E/klat
        Rm = (Rt/klat**2)*(1 - E2)

        # Get the estimated xy position.
        hxc = (Rm + hae)*(hlat - Lat0)
        hyc = (Rt + hae)*co*(hlon - Lon0)

        # Get the residual.
        txc = Xc - hxc
        tyc = Yc - hyc

        # Get the inverse Jacobian.
        J11 = (3*E2*Rm*si*co/kp2)*(hlat - Lat0) + Rm + hae
        J12 = 0
        J21 = ((E2*co**2/kp2 - 1)*Rt - hae)*si*(hlon - Lon0)
        J22 = (Rt + hae)*co
        Jdet_inv = 1/(J11*J22 - J21*J12)

        # Using the inverse Jacobian, get the residuals in lat and lon.
        tlat = (J22*txc - J12*tyc)*Jdet_inv
        tlon = (J11*tyc - J21*txc)*Jdet_inv

        # Update the latitude and longitude.
        hlat = hlat + tlat
        hlon = hlon + tlon

    # Scale the angles.
    if degs:
        hlat *= 180/np.pi
        hlon *= 180/np.pi

    # Assemble the matrix.
    llh = np.array([hlat, hlon, hae])

    # Transpose output.
    if trs:
        llh = llh.T

    return llh


def geodetic_to_curvilinear(llh, llh0=None, ned=True, degs=False):
    """
    Convert geodetic coordinates with a geodetic origin to local, curvilinear
    position in either North, East, Down (NED) or East, North, Up (ENU)
    coordinates.

    Parameters
    ----------
    llh : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Vector of geodetic position in terms of latitude in radians (or degrees
        if `degs` is True), longitude in radians (or degrees if `degs` is True),
        and height above ellipsoid in meters, or matrix of such vectors. This
        need not be the same shape as `llh0`.
    llh0 : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Vector of geodetic position of the local, curvilinear frame's origin in
        terms of latitude in radians (or degrees if `degs` is True), longitude
        in radians (or degrees if `degs` is True), and height above ellipsoid in
        meters, or matrix of such vectors. This need not be the same shape as
        `llh`. This cannot be inferred from `llh`.
    ned : bool, default True
        Flag to use NED (True) or ENU (False) orientation.
    degs : bool, default False
        Flag to interpret angles as degrees.

    Returns
    -------
    pc : (3,) or (3, K) or (K, 3) np.ndarray
        Position vector in local, curvilinear coordinates in meters or matrix of
        such vectors.

    See Also
    --------
    curvilinear_to_geodetic

    Notes
    -----
    The equations are

        .-  -.   .-                                -.
        | xc |   |     (Rm + hae) (lat - lat0)      |
        | yc | = | (Rt + hae) cos(lat) (lon - lon0) |       NED
        | zc |   |           (hae0 - hae)           |
        '-  -'   '-                                -'

    or

        .-  -.   .-                                -.
        | xc |   | (Rt + hae) cos(lat) (lon - lon0) |
        | yc | = |     (Rm + hae) (lat - lat0)      |       ENU
        | zc |   |           (hae - hae0)           |
        '-  -'   '-                                -'

    where


                                       2                  .---------------
              aE             aE (1 - eE )                /      2   2
        Rt = ----       Rm = ------------       klat = `/ 1 - eE sin (lat) .
             klat                  3
                               klat

    Here, `aE` is the semi-major axis of the Earth, `eE` is the eccentricity of
    the Earth, `Rt` is the transverse radius of curvature of the Earth, and `Rm`
    is the meridional radius of curvature of the Earth.

    If `lat0`, `lon0`, and `hae0` are not provided (are left as `None`), the
    first values of `lat`, `lon`, and `hae` will be used as the origin.

    References
    ----------
    .. [1]  Titterton & Weston, "Strapdown Inertial Navigation Technology"
    .. [2]  https://en.wikipedia.org/wiki/Earth_radius#Meridional
    .. [3]  https://en.wikipedia.org/wiki/Earth_radius#Prime_vertical
    """

    # Check the inputs.
    if isinstance(llh, (list, tuple)):
        llh = np.array(llh)
    if isinstance(llh0, (list, tuple)):
        llh0 = np.array(llh0)
    trs = (llh.ndim == 2 and llh.shape[0] != 3)
    s = np.pi/180 if degs else 1.0

    # Transpose inputs.
    if trs:
        llh = llh.T
        if llh0 is not None:
            llh0 = llh0.T

    # Infer origin.
    if llh0 is None:
        if llh.ndim == 2:
            llh0 = llh[:, 0]
        else:
            llh0 = llh.copy()

    # Parse inputs.
    lat = llh[0]
    lon = llh[1]
    hae = llh[2]
    lat0 = llh0[0]
    lon0 = llh0[1]
    hae0 = llh0[2]

    # Scale the angles.
    Lat = s*lat
    Lon = s*lon
    Lat0 = s*lat0
    Lon0 = s*lon0

    # Get the parallel and meridional radii of curvature.
    klat = np.sqrt(1 - E2*np.sin(Lat)**2)
    Rt = A_E/klat
    Rm = (Rt/klat**2)*(1 - E2)

    # Get the curvilinear coordinates.
    if ned: # NED
        xc = (Rm + hae)*(Lat - Lat0)
        yc = (Rt + hae)*np.cos(Lat)*(Lon - Lon0)
        zc = hae0 - hae
    else:   # ENU
        xc = (Rt + hae)*np.cos(Lat)*(Lon - Lon0)
        yc = (Rm + hae)*(Lat - Lat0)
        zc = hae - hae0
    pc = np.array([xc, yc, zc])

    # Transpose output.
    if trs:
        pc = pc.T

    return pc


def curvilinear_to_tangent(pc, llh0, ned=True, degs=False):
    """
    Convert position in curvilinear coordinates to tangent coordinates. This
    function relies on other functions in this library to calculate the values.

    Parameters
    ----------
    pc : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Position vector in local, curvilinear coordinates in meters or matrix of
        such vectors. This need not be the same shape as `llh0`.
    llh0 : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Vector of geodetic position of the local, curvilinear frame's origin in
        terms of latitude in radians (or degrees if `degs` is True), longitude
        in radians (or degrees if `degs` is True), and height above ellipsoid in
        meters, or matrix of such vectors. This need not be the same shape as
        `pc`. This cannot be inferred from `pc`.
    ned : bool, default True
        Flag to use NED (True) or ENU (False) orientation.
    degs : bool, default False
        Flag to interpret angles as degrees.

    Returns
    -------
    pt : (3,) or (3, K) or (K, 3) np.ndarray
        Position vector in local, tangent coordinates in meters or matrix of
        such vectors.

    See Also
    --------
    tangent_to_curvilinear
    """

    # Check the inputs.
    if isinstance(pc, (list, tuple)):
        pc = np.array(pc)
    if isinstance(llh0, (list, tuple)):
        llh0 = np.array(llh0)

    llh = curvilinear_to_geodetic(pc, llh0, ned, degs)
    pe = geodetic_to_ecef(llh, degs)
    pe0 = geodetic_to_ecef(llh0, degs)
    pt = ecef_to_tangent(pe, pe0, ned)

    return pt


def tangent_to_curvilinear(pt, pe0, ned=True):
    """
    Convert position in tangent coordinates to curvilinear coordinates. This
    function relies on other functions in this library to calculate the values.

    Parameters
    ----------
    pt : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Position vector in local, tangent coordinates in meters or matrix of
        such vectors. This need not be the same shape as `pe0`.
    pe0 : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Position vector of the local, curvilinear frame's origin in ECEF
        coordinates in meters or matrix of such vectors. This need not be the
        same shape as `pt`. This cannot be inferred from `pt`.
    ned : bool, default True
        Flag to use NED (True) or ENU (False) orientation.

    Returns
    -------
    pc : (3,) or (3, K) or (K, 3) np.ndarray
        Position vector in local, curvilinear coordinates in meters or matrix of
        such vectors.

    See Also
    --------
    curvilinear_to_tangent
    """

    # Check the inputs.
    if isinstance(pt, (list, tuple)):
        pt = np.array(pt)
    if isinstance(pe0, (list, tuple)):
        pe0 = np.array(pe0)

    # Make conversions.
    pe = tangent_to_ecef(pt, pe0, ned)
    llh = ecef_to_geodetic(pe)
    llh0 = ecef_to_geodetic(pe0)
    pc = geodetic_to_curvilinear(llh, llh0, ned)

    return pc

# -------------------------
# Rotation Matrix Utilities
# -------------------------

def is_ortho(A):
    """
    Test if the matrix A is orthonormal to a tolerance of 2e-15.

    Parameters
    ----------
    A : (3, 3) or (K, 3, 3) list, tuple, or np.ndarray
        Square matrix or stack of K square matrices.

    Returns
    -------
    True or False

    Notes
    -----

    The value which is compared to the tolerance is

             3   3
            .-- .--
        e =  >   >  B           : B  = A' A - I,
            '-- '--  i,j
            i=1 j=1

    where `I` is a 3x3 identity matrix.
    """

    # Check the input.
    if isinstance(Cin, (list, tuple)):
        Cin = np.array(Cin)

    # Define the tolerance.
    tol = 2e-15

    # Check the matrix.
    if np.ndim(A) == 2:
        B = (A.T @ A) - np.eye(3)
        if np.sum(np.abs(B)) < tol:
            return True
    elif np.ndim(A) == 3:
        K = A.shape[0]
        B = (np.transpose(A, (0, 2, 1)) @ A) - np.eye(3)
        if np.sum(np.abs(B)) < tol*K:
            return True

    return False


def orthonormalize_dcm(Cin):
    """
    Orthonormalize the rotation matrix using the Modified Gram-Schmidt
    algorithm. This function does not modify the matrix in-place. Note that this
    algorithm only moves the matrix towards orthonormality; it does not
    guarantee that after one function call the returned matrix will be
    orthonormal. However, with a 2e-15 tolerance, orthonormality can be achieved
    typically within at most 2 function calls.

    Parameters
    ----------
    Cin : (3, 3) or (K, 3, 3) list, tuple, or np.ndarray
        Square matrix or stack of K square matrices.

    Returns
    -------
    C : (3, 3) or (K, 3, 3) np.ndarray
        Square matrix or stack of K square matrices, an orthonormalized version
        of the input.
    """

    # Check the input.
    if isinstance(Cin, (list, tuple)):
        Cin = np.array(Cin)

    # Make a copy.
    C = Cin.copy()

    if Cin.ndim == 2:
        # Orthonormalize a single matrix.
        C[:, 0] /= np.sqrt(C[0, 0]**2 + C[1, 0]**2 + C[2, 0]**2)
        C[:, 1] -= C[:, 0].dot(C[:, 1])*C[:, 0]
        C[:, 1] /= np.sqrt(C[0, 1]**2 + C[1, 1]**2 + C[2, 1]**2)
        C[:, 2] -= C[:, 0].dot(C[:, 2])*C[:, 0]
        C[:, 2] -= C[:, 1].dot(C[:, 2])*C[:, 1]
        C[:, 2] /= np.sqrt(C[0, 2]**2 + C[1, 2]**2 + C[2, 2]**2)
    else:
        # Orthonormalize a stack of matrices.
        Cnm = np.sqrt(C[:, 0, 0]**2 + C[:, 1, 0]**2 + C[:, 2, 0]**2)
        C[:, :, 0] /= Cnm[:, np.newaxis]
        Cdot = np.sum(C[:, :, 0]*C[:, :, 1], axis=1)
        C[:, :, 1] -= Cdot[:, np.newaxis]*C[:, :, 0]
        Cnm = np.sqrt(C[:, 0, 1]**2 + C[:, 1, 1]**2 + C[:, 2, 1]**2)
        C[:, :, 1] /= Cnm[:, np.newaxis]
        Cdot = np.sum(C[:, :, 0]*C[:, :, 2], axis=1)
        C[:, :, 2] -= Cdot[:, np.newaxis]*C[:, :, 0]
        Cdot = np.sum(C[:, :, 1]*C[:, :, 2], axis=1)
        C[:, :, 2] -= Cdot[:, np.newaxis]*C[:, :, 1]
        Cnm = np.sqrt(C[:, 0, 2]**2 + C[:, 1, 2]**2 + C[:, 2, 2]**2)
        C[:, :, 2] /= Cnm[:, np.newaxis]

    return C


def rodrigues_rotation(theta, degs=False):
    """
    Convert an active rotation vector to its passive equivalent rotation matrix.
    The rotation vector should not have a norm greater than pi. If it does,
    scale the vector by `-(2 pi - n)/n`, where `n` is the norm of the rotation
    vector.

    Parameters
    ----------
    theta : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Three-element vector of angles in radians (or degrees if `degs` is True)
        or matrix of such vectors.
    degs : bool, default False
        Flag to interpret angles as degrees.

    Returns
    -------
    Delta : (3, 3) or (K, 3, 3) np.ndarray
        Three-by-three matrix or stack of such matrices.

    See Also
    --------
    inverse_rodrigues_rotation

    Notes
    -----
    The Rodrigues Rotation formula is

                                    sin(l)            1 - cos(l)        2
        Delta = exp([theta] ) = I + ------ [theta]  + ---------- [theta] ,
                           x          l           x        2            x
                                                          l
    where
               .---------                  .-          -.           .-   -.
              / 2   2   2                  |  0  -z   y |           |  x  |
        l = `/ x + y + z ,      [theta]x = |  z   0  -x |   theta = |  y  |.
                                           | -y   x   0 |           |  z  |
                                           '-          -'           '-   -'

    The two trigonometric fractions become indeterminate when `l` is zero. While
    it is unlikely the vector magnitude `l` would ever become exactly zero, as
    the magnitude gets very small, there can be numerical problems. We need the
    limit of these terms as `l` approaches zero:

               sin(l)                  1 - cos(l)    1
         lim   ------ = 1,       lim   ---------- = --- .
        l -> 0   l              l -> 0      2        2
                                           l

    For finite-precision numbers, as we approach the limit of a term, the result
    becomes erratic. There is a point at which this numerical error exceeds the
    error of just setting the result equal to the limit. With double-precision,
    floating-point numbers, this point is `l` < 0.04 microradian for the sine
    term and `l` < 0.2 milliradian for the cosine term.

    Note that the relationship of the `theta` vector to the `Delta` matrix is
    the same as the negative of the rotation vector to the same matrix.
    """

    # Check the input.
    if isinstance(theta, (list, tuple)):
        theta = np.array(theta)
    trs = (theta.ndim == 2 and theta.shape[0] != 3)
    scale = np.pi/180 if degs else 1.0

    # Transpose input.
    if trs:
        theta = theta.T

    # Parse input.
    x = theta[0]*scale
    y = theta[1]*scale
    z = theta[2]*scale

    # Get the vector norm.
    x2 = x**2
    y2 = y**2
    z2 = z**2
    nm2 = x2 + y2 + z2
    nm = np.sqrt(nm2)

    if theta.ndim == 1:
        # Get the sine and cosine factors.
        s = 1.0 if nm < 0.04e-6 else math.sin(nm)/nm
        c = 0.5 if nm < 0.2e-3 else (1 - math.cos(nm))/nm2

        # Get the rotation matrix.
        Delta = np.array([
            [1.0 - c*(y2 + z2), c*x*y - s*z, c*x*z + s*y],
            [c*x*y + s*z, 1.0 - c*(x2 + z2), c*y*z - s*x],
            [c*x*z - s*y, c*y*z + s*x, 1.0 - c*(x2 + y2)]])
    elif theta.ndim == 2:
        # Get the sine and cosine factors.
        mask = nm >= 0.04e-6
        s = np.empty_like(nm)
        s[mask] = np.sin(nm[mask])/nm[mask]
        s[~mask] = 1.0
        mask = nm >= 0.2e-3
        c = np.empty_like(nm)
        c[mask] = (1 - np.cos(nm[mask]))/nm2[mask]
        c[~mask] = 0.5

        # Get the rotation matrix.
        Delta = np.zeros((len(x), 3, 3))
        Delta[:, 0, 0] = 1.0 - c*(y2 + z2)
        Delta[:, 0, 1] = c*x*y - s*z
        Delta[:, 0, 2] = c*x*z + s*y
        Delta[:, 1, 0] = c*x*y + s*z
        Delta[:, 1, 1] = 1.0 - c*(x2 + z2)
        Delta[:, 1, 2] = c*y*z - s*x
        Delta[:, 2, 0] = c*x*z - s*y
        Delta[:, 2, 1] = c*y*z + s*x
        Delta[:, 2, 2] = 1.0 - c*(x2 + y2)

    return Delta


def inverse_rodrigues_rotation(Delta, degs=False):
    """
    Convert a passive rotation matrix to its equivalent active rotation vector.
    The rotation vector will not have a norm greater than pi.

    Parameters
    ----------
    Delta : (3, 3) or (K, 3, 3) list, tuple, or np.ndarray
        Three-by-three matrix or stack of such matrices.
    degs : bool, default False
        Flag to interpret angles as degrees.

    Returns
    -------
    theta : (3,) or (3, K) np.ndarray
        Three-element vector of angles in radians (or degrees if `degs` is True)
        or matrix of such vectors.

    See Also
    --------
    rodrigues_rotation

    Notes
    -----
    In solving for the vector, the scaling factor `k` becomes indeterminate when
    `q` has a value of 3. So, a polynomial fit is used for `k`, instead, when
    `q` exceeds 2.9995.
    """

    # Check the input.
    if isinstance(Delta, (list, tuple)):
        Delta = np.array(Delta)
    s = np.pi/180 if degs else 1.0

    # Check for zero matrices.
    Delta_sums = np.sum(np.sum(np.abs(Delta), axis=-1), axis=-1)
    if np.any(Delta_sums == 0):
        raise ValueError("Input matrix Delta must not be zeros.")

    if Delta.ndim == 2:
        # Parse the input.
        d11 = Delta[0, 0];      d12 = Delta[0, 1];      d13 = Delta[0, 2]
        d21 = Delta[1, 0];      d22 = Delta[1, 1];      d23 = Delta[1, 2]
        d31 = Delta[2, 0];      d32 = Delta[2, 1];      d33 = Delta[2, 2]

        # Get the trace of the matrix and limit its value.
        q_min = 2*math.cos(3.1415926) + 1
        q = min(max(d11 + d22 + d33, q_min), 3.0)

        # Get the scaling factor of the vector.
        ang = math.acos((q-1)/2)
        k = (q**2 - 11*q + 54)/60 if q > 2.9995 \
                else ang/math.sqrt(3 + 2*q - q**2)
    elif Delta.ndim == 3:
        # Parse the input.
        d11 = Delta[:, 0, 0];   d12 = Delta[:, 0, 1];   d13 = Delta[:, 0, 2]
        d21 = Delta[:, 1, 0];   d22 = Delta[:, 1, 1];   d23 = Delta[:, 1, 2]
        d31 = Delta[:, 2, 0];   d32 = Delta[:, 2, 1];   d33 = Delta[:, 2, 2]

        # Get the trace of the matrix and limit its value.
        q_min = 2*np.cos(3.1415926) + 1
        q = np.minimum(np.maximum(d11 + d22 + d33, q_min), 3.0)

        # Get the scaling factor of the vector.
        ang = np.arccos((q-1)/2)
        k = np.empty_like(ang)
        mask = q <= 2.9995
        k[mask] = ang/np.sqrt(3 + 2*q[mask] - q[mask]**2)
        k[~mask] = (q[~mask]**2 - 11*q[~mask] + 54)/60

    # Build the vector.
    theta = s*k*np.array([d32 - d23, d13 - d31, d21 - d12])

    # Check the output.
    zero_vectors = (np.sum(np.abs(theta), axis=0) < 1e-15)
    minus_one_q = (q == q_min)
    if np.any(zero_vectors * minus_one_q):
        raise ValueError("The provided output is incorrectly all zeros, \n"
                + "probably due to the input being very close to a 180 "
                + "degree rotation.")

    return theta
