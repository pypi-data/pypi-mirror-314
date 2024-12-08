# Run `pytest` in the terminal.
import math
import numpy as np
import matplotlib.pyplot as plt
import r3f

# -----------------------------------
# Attitude-representation Conversions
# -----------------------------------

def test_axis_angle_vector():
    a = 1.0/math.sqrt(3.0)
    ang = 2

    # single conversion with list
    ax = [a, a, a]
    vec = r3f.axis_angle_to_vector(ax, ang)
    assert np.allclose(vec, [2*a, 2*a, 2*a])
    AX, ANG = r3f.vector_to_axis_angle(vec)
    assert np.allclose(ax, AX)
    assert np.allclose(ang, ANG)

    # single conversion with tuple
    ax = (a, a, a)
    vec = r3f.axis_angle_to_vector(ax, ang)
    assert np.allclose(vec, [2*a, 2*a, 2*a])
    AX, ANG = r3f.vector_to_axis_angle(vec)
    assert np.allclose(ax, AX)
    assert np.allclose(ang, ANG)

    # single conversion with degrees
    ax = (a, a, a)
    ang = 2*180/math.pi
    vec = r3f.axis_angle_to_vector(ax, ang, degs=True)
    assert np.allclose(vec, [2*a, 2*a, 2*a])
    AX, ANG = r3f.vector_to_axis_angle(vec, degs=True)
    assert np.allclose(ax, AX)
    assert np.allclose(ang, ANG)

    # multiple conversions
    ax = np.array([
        [1, 0, 0, a],
        [0, 1, 0, a],
        [0, 0, 1, a]])
    ang = np.array([2, 2, 2, 2])
    vec = np.array([
            [2, 0, 0, 2*a],
            [0, 2, 0, 2*a],
            [0, 0, 2, 2*a]])
    VEC = r3f.axis_angle_to_vector(ax, ang)
    assert np.allclose(VEC, vec)
    AX, ANG = r3f.vector_to_axis_angle(VEC)
    assert np.allclose(ax, AX)
    assert np.allclose(ang, ANG)


def test_rpy_vector():
    # single conversion with list
    vec = [1.0, 1.0, 1.0]
    rpy = r3f.vector_to_rpy(vec)
    VEC = r3f.rpy_to_vector(rpy)
    assert np.allclose(vec, VEC)

    # single conversion with tuple
    vec = (1.0, 1.0, 1.0)
    rpy = r3f.vector_to_rpy(vec)
    VEC = r3f.rpy_to_vector(rpy)
    assert np.allclose(vec, VEC)

    # single conversion with degrees
    vec = (1.0, 1.0, 1.0)
    rpy = r3f.vector_to_rpy(vec, degs=True)
    VEC = r3f.rpy_to_vector(rpy, degs=True)
    assert np.allclose(vec, VEC)

    # mutiple conversions
    a = 1.0/math.sqrt(3.0)
    vec = np.array([
            [2, 0, 0, 2*a],
            [0, 2, 0, 2*a],
            [0, 0, 2, 2*a]])
    rpy = r3f.vector_to_rpy(vec)
    VEC = r3f.rpy_to_vector(rpy)
    assert np.allclose(vec, VEC)


def test_dcm_vector():
    ang = math.pi/4

    # single conversion with list
    vec = [0.0, 0.0, ang]
    dcm = np.array([
        [math.cos(ang), math.sin(ang), 0],
        [-math.sin(ang), math.cos(ang), 0],
        [0, 0, 1]])
    DCM = r3f.vector_to_dcm(vec)
    assert np.allclose(dcm, DCM)
    VEC = r3f.dcm_to_vector(DCM)
    assert np.allclose(vec, VEC)

    # single conversion with tuple
    vec = (0.0, ang, 0.0)
    dcm = np.array([
        [math.cos(ang), 0, -math.sin(ang)],
        [0, 1, 0],
        [math.sin(ang), 0, math.cos(ang)]])
    DCM = r3f.vector_to_dcm(vec)
    assert np.allclose(dcm, DCM)
    VEC = r3f.dcm_to_vector(DCM)
    assert np.allclose(vec, VEC)

    # multiple conversions
    a = 1.0/math.sqrt(3.0)
    vec = np.array([
            [2, 0, 0, 2*a],
            [0, 2, 0, 2*a],
            [0, 0, 2, 2*a]])
    DCM = r3f.vector_to_dcm(vec)
    VEC = r3f.dcm_to_vector(DCM)
    assert np.allclose(vec, VEC)


def test_quat_vector():
    ang = math.pi/4

    # single conversion with list
    vec = [0.0, 0.0, ang]
    quat = r3f.vector_to_quat(vec)
    VEC = r3f.quat_to_vector(quat)
    assert np.allclose(vec, VEC)

    # single conversion with tuple
    vec = (0.0, 0.0, ang)
    quat = r3f.vector_to_quat(vec)
    VEC = r3f.quat_to_vector(quat)
    assert np.allclose(vec, VEC)

    # multiple conversions
    a = 1.0/math.sqrt(3.0)
    vec = np.array([
            [2, 0, 0, 2*a],
            [0, 2, 0, 2*a],
            [0, 0, 2, 2*a]])
    quat = r3f.vector_to_quat(vec)
    VEC = r3f.quat_to_vector(quat)
    assert np.allclose(vec, VEC)


def test_rpy_axis_angle():
    # single conversions with list and tuple and ndarray and degrees
    ax, ang = r3f.rpy_to_axis_angle([0, 0, np.pi/4])
    assert np.allclose(ax, np.array([0, 0, 1]))
    assert np.allclose(ang, np.pi/4)
    ax, ang = r3f.rpy_to_axis_angle((0, np.pi/4, 0))
    assert np.allclose(ax, np.array([0, 1, 0]))
    assert np.allclose(ang, np.pi/4)
    ax, ang = r3f.rpy_to_axis_angle(np.array([45.0, 0, 0]), degs=True)
    assert np.allclose(ax, np.array([1, 0, 0]))
    assert np.allclose(ang, 45.0)
    RPY = r3f.axis_angle_to_rpy(ax, ang, degs=True)
    assert np.allclose(RPY, np.array([45.0, 0, 0]))

    # multiple conversions
    N = 10
    r = np.random.uniform(-np.pi, np.pi, N)
    p = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL, N)
    y = np.random.uniform(-np.pi, np.pi, N)
    ax, ang = r3f.rpy_to_axis_angle([r, p, y])
    [R, P, Y] = r3f.axis_angle_to_rpy(ax, ang)
    assert np.allclose(r, R)
    assert np.allclose(p, P)
    assert np.allclose(y, Y)


def test_dcm_axis_angle():
    # Define common angle and cosine and sine.
    ang = np.pi/4
    co = np.cos(ang)
    si = np.sin(ang)

    # Test individual axes.
    C = np.array([[co, si, 0], [-si, co, 0], [0, 0, 1]])
    C_p = r3f.axis_angle_to_dcm(np.array([0, 0, 1]), ang)
    assert np.allclose(C, C_p)
    ax1, ang1 = r3f.dcm_to_axis_angle(C_p)
    assert np.allclose(np.array([0, 0, 1]), ax1)
    assert np.allclose(ang, ang1)
    C = np.array([[co, 0, -si], [0, 1, 0], [si, 0, co]])
    C_p = r3f.axis_angle_to_dcm(np.array([0, 1, 0]), ang)
    assert np.allclose(C, C_p)
    ax1, ang1 = r3f.dcm_to_axis_angle(C_p)
    assert np.allclose(np.array([0, 1, 0]), ax1)
    assert np.allclose(ang, ang1)
    C = np.array([[1, 0, 0], [0, co, si], [0, -si, co]])
    C_p = r3f.axis_angle_to_dcm(np.array([1, 0, 0]), ang)
    assert np.allclose(C, C_p)
    ax1, ang1 = r3f.dcm_to_axis_angle(C_p)
    assert np.allclose(np.array([1, 0, 0]), ax1)
    assert np.allclose(ang, ang1)

    # Test vectorized reciprocity (requires positive axes).
    N = 5
    ax = np.abs(np.random.randn(3, N))
    nm = np.linalg.norm(ax, axis=0)
    ax /= nm
    ang = np.random.randn(N)
    C = r3f.axis_angle_to_dcm(ax, ang)
    ax1, ang1 = r3f.dcm_to_axis_angle(C)
    assert np.allclose(ax, ax1)
    assert np.allclose(ang, ang1)

    # preserve units
    ang = np.array([1.0, 0.5])
    ax = np.array([
        [1, 2],
        [1, 2],
        [1, 2]])
    C = r3f.axis_angle_to_dcm(ax, ang)
    assert np.allclose(ang, np.array([1.0, 0.5]))


def test_quat_axis_angle():
    # axis angle to quat
    a = np.array([1, 1, 1])/np.sqrt(3) # normalized
    q1 = r3f.axis_angle_to_quat(a, np.pi)
    assert np.allclose(q1, np.array([0, 1, 1, 1])/np.sqrt(3))
    b = np.array([2, 2, 2])/np.sqrt(12) # normalized
    q2 = r3f.axis_angle_to_quat(b, np.pi)
    assert np.allclose(q2, np.array([0, 2, 2, 2])/np.sqrt(12))

    # backwards (requires normalized start)
    ax, ang = r3f.quat_to_axis_angle(q1)
    assert np.allclose(a, ax)
    assert np.allclose(np.pi, ang)

    # Test vectorized reciprocity.
    A = np.column_stack((a, b))
    Q = np.column_stack((q1, q2))
    PI = np.array([np.pi, np.pi])
    assert np.allclose(r3f.axis_angle_to_quat(A, PI), Q)


def test_dcm_rpy():
    # Build a random DCM.
    R = np.random.uniform(-np.pi, np.pi)
    P = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL)
    Y = np.random.uniform(-np.pi, np.pi)

    # Get rotation matrix.
    C_1g = np.array([
        [np.cos(Y), np.sin(Y), 0],
        [-np.sin(Y), np.cos(Y), 0],
        [0, 0, 1]])
    C_21 = np.array([
        [np.cos(P), 0, -np.sin(P)],
        [0, 1, 0],
        [np.sin(P), 0, np.cos(P)]])
    C_b2 = np.array([
        [1, 0, 0],
        [0, np.cos(R), np.sin(R)],
        [0, -np.sin(R), np.cos(R)]])
    C_bg = C_b2 @ C_21 @ C_1g

    # Check DCM to RPY.
    [r, p, y] = r3f.dcm_to_rpy(C_bg)
    assert np.allclose(r, R)
    assert np.allclose(p, P)
    assert np.allclose(y, Y)

    # Test vectorized reciprocity.
    N = 5
    R = np.random.uniform(-np.pi, np.pi, N)
    P = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL, N)
    Y = np.random.uniform(-np.pi, np.pi, N)
    C = r3f.rpy_to_dcm([R, P, Y])
    [r, p, y] = r3f.dcm_to_rpy(C)
    assert np.allclose(r, R)
    assert np.allclose(p, P)
    assert np.allclose(y, Y)

    # preserve units
    R = np.random.uniform(-180.0, 180.0, N)
    P = np.random.uniform(-90.0 + r3f.TOL, 90.0 - r3f.TOL, N)
    Y = np.random.uniform(-180.0, 180.0, N)
    R0 = R.copy()
    P0 = P.copy()
    Y0 = Y.copy()
    C = r3f.rpy_to_dcm([R, P, Y], degs=True)
    assert np.allclose(R, R0)
    assert np.allclose(P, P0)
    assert np.allclose(Y, Y0)


def test_quat_rpy():
    # This set of tests relies on previous tests.

    # Test forward path.
    N = 5
    R = np.random.uniform(-np.pi, np.pi, N)
    P = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL, N)
    Y = np.random.uniform(-np.pi, np.pi, N)
    ax, ang = r3f.rpy_to_axis_angle([R, P, Y])
    q1 = r3f.axis_angle_to_quat(ax, ang)
    q2 = r3f.rpy_to_quat([R, P, Y])
    assert np.allclose(q1, q2)

    # Test backward path.
    [r, p, y] = r3f.quat_to_rpy(q2)
    assert np.allclose(r, R)
    assert np.allclose(p, P)
    assert np.allclose(y, Y)

    # preserve units
    R = np.random.uniform(-180.0, 180.0, N)
    P = np.random.uniform(-90.0 + r3f.TOL, 90.0 - r3f.TOL, N)
    Y = np.random.uniform(-180.0, 180.0, N)
    R0 = R.copy()
    P0 = P.copy()
    Y0 = Y.copy()
    q = r3f.rpy_to_quat([R, P, Y], degs=True)
    assert np.allclose(R, R0)
    assert np.allclose(P, P0)
    assert np.allclose(Y, Y0)



def test_quat_dcm():
    # This set of tests relies on previous tests.
    N = 5
    R = np.random.uniform(-np.pi, np.pi, N)
    P = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL, N)
    Y = np.random.uniform(-np.pi, np.pi, N)
    q1 = r3f.rpy_to_quat([R, P, Y])
    C1 = r3f.rpy_to_dcm([R, P, Y])
    C2 = r3f.quat_to_dcm(q1)
    assert np.allclose(C1, C2)

    # Test reciprocity.
    q2 = r3f.dcm_to_quat(C2)
    assert np.allclose(q1, q2)


def test_rot():
    irt2 = 1/np.sqrt(2)

    C = np.array([
        [irt2, irt2, 0],
        [-irt2, irt2, 0],
        [0, 0, 1]])
    assert np.allclose(r3f.rot(45, 2, True), C)

    B = np.array([
        [irt2, 0, -irt2],
        [0, 1, 0],
        [irt2, 0, irt2]])
    assert np.allclose(r3f.rot(45, 1, True), B)

    A = np.array([
        [1, 0, 0],
        [0, irt2, irt2],
        [0, -irt2, irt2]])
    assert np.allclose(r3f.rot(45, 0, True), A)

    # Multiple rotations
    R = r3f.rot([45, 45, 45], [2, 1, 0], True)
    assert np.allclose(R, A @ B @ C)

    # String axes
    R = r3f.rot([45, 45, 45], "zyx", True)
    assert np.allclose(R, A @ B @ C)

    # preserve units
    ang = np.array([45, 45, 45])
    ax = np.array([2, 1, 0])
    R = r3f.rot(ang, ax, True)
    assert np.allclose(ang, np.array([45, 45, 45]))


def test_rotate():
    # Generate the random inputs.
    N = 10
    R = np.random.uniform(-np.pi, np.pi, N)
    P = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL, N)
    Y = np.random.uniform(-np.pi, np.pi, N)
    C = r3f.rpy_to_dcm([R, P, Y])
    a = np.random.randn(3, N)

    # Rotate with the single function.
    b1 = r3f.rotate(C, a)

    # Rotate with a for loop.
    b2 = np.zeros((3, N))
    for n in range(N):
        b2[:, n] = C[n, :, :] @ a[:, n]

    # Check the results.
    assert np.allclose(b1, b2)


# -------------------------
# Reference-frame Rotations
# -------------------------

def test_dcm_inertial_to_ecef():
    # Test single time.
    t = np.pi/r3f.W_EI
    C = r3f.dcm_inertial_to_ecef(t)
    assert np.allclose(C, np.diag([-1, -1, 1]))

    # Test multiple times.
    N = 11
    t = np.linspace(0.0, (2*np.pi)/r3f.W_EI, N)
    C = r3f.dcm_inertial_to_ecef(t)
    assert np.allclose(C[0, :, :], np.eye(3))
    assert np.allclose(C[int((N - 1)/2), :, :], np.diag([-1, -1, 1]))
    assert np.allclose(C[-1, :, :], np.eye(3))

def test_dcm_ecef_to_navigation():
    # Test single.
    lat = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL)
    lon = np.random.uniform(-np.pi, np.pi)
    A = r3f.rot([lon, -(lat + np.pi/2)], [2, 1])
    B = r3f.dcm_ecef_to_navigation(lat, lon)
    assert np.allclose(A, B)

    # Test multiple.
    N = 10
    lat = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL, size=N)
    lon = np.random.uniform(-np.pi, np.pi, size=N)
    C = r3f.dcm_ecef_to_navigation(lat, lon)
    for n in range(N):
        A = r3f.dcm_ecef_to_navigation(lat[n], lon[n])
        assert np.allclose(A, C[n, :, :])

# ---------------------------
# Reference-frame Conversions
# ---------------------------

def test_ecef_geodetic():
    # Test single point.
    [xe, ye, ze] = r3f.geodetic_to_ecef([0.0, 0.0, 0.0])
    assert np.allclose([xe, ye, ze], [r3f.A_E, 0, 0])
    [lat, lon, hae] = r3f.ecef_to_geodetic([xe, ye, ze])
    assert np.allclose([lat, lon, hae], [0.0, 0.0, 0.0])

    # Build original data.
    N = 10
    lat = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL, size=N)
    lon = np.random.uniform(-np.pi, np.pi, size=N)
    hae = np.random.uniform(-10e3, 100e3, size=N)

    # Test vectorized reciprocity.
    [xe, ye, ze] = r3f.geodetic_to_ecef([lat, lon, hae])
    [Lat, Lon, Hae] = r3f.ecef_to_geodetic([xe, ye, ze])
    assert np.allclose([lat, lon, hae], [Lat, Lon, Hae])

    # preserve units
    lat = np.random.uniform(-90.0 + r3f.TOL, 90.0 - r3f.TOL, size=N)
    lon = np.random.uniform(-180.0, 180.0, size=N)
    hae = np.random.uniform(-10e3, 100e3, size=N)
    lat0 = lat.copy()
    lon0 = lon.copy()
    hae0 = hae.copy()
    [xe, ye, ze] = r3f.geodetic_to_ecef([lat, lon, hae], degs=True)
    assert np.allclose(lat, lat0)
    assert np.allclose(lon, lon0)


def test_ecef_tangent():
    # Test single point.
    xe = r3f.A_E
    ye = 0.0
    ze = r3f.B_E
    xe0 = r3f.A_E
    ye0 = 0.0
    ze0 = 0.0
    [xt, yt, zt] = r3f.ecef_to_tangent([xe, ye, ze], [xe0, ye0, ze0])
    XT = r3f.B_E
    YT = 0.0
    ZT = 0.0
    assert np.allclose([xt, yt, zt], [XT, YT, ZT])
    [XE, YE, ZE] = r3f.tangent_to_ecef([XT, YT, ZT], [xe0, ye0, ze0])
    assert np.allclose([xe, ye, ze], [XE, YE, ZE])

    # Build original data.
    N = 10
    lat = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL, size=N)
    lon = np.random.uniform(-np.pi, np.pi, size=N)
    hae = np.random.uniform(-10e3, 100e3, size=N)
    [xe, ye, ze] = r3f.geodetic_to_ecef([lat, lon, hae])

    # Test vectorized reciprocity.
    [xt, yt, zt] = r3f.ecef_to_tangent([xe, ye, ze])
    [XE, YE, ZE] = r3f.tangent_to_ecef([xt, yt, zt], [xe[0], ye[0], ze[0]])
    assert np.allclose([xe, ye, ze], [XE, YE, ZE])


def test_geodetic_curvilinear():
    # Test single point.
    [xc, yc, zc] = r3f.geodetic_to_curvilinear([np.pi/4, 0, 1000], [0, 0, 0])
    assert xc > 0
    assert yc == 0
    assert zc == -1000
    [lat, lon, hae] = r3f.curvilinear_to_geodetic([xc, yc, zc], [0, 0, 0])
    assert np.allclose([np.pi/4, 0.0, 1e3], [lat, lon, hae])

    # Build original data.
    N = 10
    lat = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL, size=N)
    lon = np.random.uniform(-np.pi, np.pi, size=N)
    hae = np.random.uniform(-10e3, 100e3, size=N)
    [xc, yc, zc] = r3f.geodetic_to_curvilinear([lat, lon, hae])

    # Test vectorized reciprocity.
    [Lat, Lon, Hae] = r3f.curvilinear_to_geodetic([xc, yc, zc],
        [lat[0], lon[0], hae[0]])
    assert np.allclose([lat, lon, hae], [Lat, Lon, Hae])


def test_curvilinear_ecef():
    N = 10
    lat = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL, size=N)
    lon = np.random.uniform(-np.pi, np.pi, size=N)
    hae = np.random.uniform(-10e3, 100e3, size=N)
    lat0 = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL)
    lon0 = np.random.uniform(-np.pi, np.pi)
    hae0 = np.random.uniform(-10e3, 100e3)
    [XE, YE, ZE] = r3f.geodetic_to_ecef([lat, lon, hae])
    [xc, yc, zc] = r3f.geodetic_to_curvilinear([lat, lon, hae],
            [lat0, lon0, hae0])
    [xe0, ye0, ze0] = r3f.geodetic_to_ecef([lat0, lon0, hae0])
    [xe, ye, ze] = r3f.curvilinear_to_ecef([xc, yc, zc], [xe0, ye0, ze0])
    assert np.allclose(xe, XE)
    assert np.allclose(ye, YE)
    assert np.allclose(ze, ZE)
    [XC, YC, ZC] = r3f.ecef_to_curvilinear([xe, ye, ze], [xe0, ye0, ze0])
    assert np.allclose(xc, XC)
    assert np.allclose(yc, YC)
    assert np.allclose(zc, ZC)


def test_geodetic_tangent():
    N = 10
    lat = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL, size=N)
    lon = np.random.uniform(-np.pi, np.pi, size=N)
    hae = np.random.uniform(-10e3, 100e3, size=N)
    lat0 = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL)
    lon0 = np.random.uniform(-np.pi, np.pi)
    hae0 = np.random.uniform(-10e3, 100e3)
    [xt, yt, zt] = r3f.geodetic_to_tangent([lat, lon, hae], [lat0, lon0, hae0])
    [xe, ye, ze] = r3f.geodetic_to_ecef([lat, lon, hae])
    [xe0, ye0, ze0] = r3f.geodetic_to_ecef([lat0, lon0, hae0])
    [XT, YT, ZT] = r3f.ecef_to_tangent([xe, ye, ze], [xe0, ye0, ze0])
    assert np.allclose(xt, XT)
    assert np.allclose(yt, YT)
    assert np.allclose(zt, ZT)
    [LAT, LON, HAE] = r3f.tangent_to_geodetic([xt, yt, zt], [lat0, lon0, hae0])
    assert np.allclose(lat, LAT)
    assert np.allclose(lon, LON)
    assert np.allclose(hae, HAE)


def test_curvilinear_tangent():
    N = 10
    lat = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL, size=N)
    lon = np.random.uniform(-np.pi, np.pi, size=N)
    hae = np.random.uniform(-10e3, 100e3, size=N)
    lat0 = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL)
    lon0 = np.random.uniform(-np.pi, np.pi)
    hae0 = np.random.uniform(-10e3, 100e3)
    [xc, yc, zc] = r3f.geodetic_to_curvilinear([lat, lon, hae], [lat0, lon0, hae0])
    [xt, yt, zt] = r3f.curvilinear_to_tangent([xc, yc, zc], [lat0, lon0, hae0])
    [xe, ye, ze] = r3f.geodetic_to_ecef([lat, lon, hae])
    [xe0, ye0, ze0] = r3f.geodetic_to_ecef([lat0, lon0, hae0])
    [XT, YT, ZT] = r3f.ecef_to_tangent([xe, ye, ze], [xe0, ye0, ze0])
    assert np.allclose(xt, XT)
    assert np.allclose(yt, YT)
    assert np.allclose(zt, ZT)
    [XC, YC, ZC] = r3f.tangent_to_curvilinear([xt, yt, zt], [xe0, ye0, ze0])
    assert np.allclose(xc, XC)
    assert np.allclose(yc, YC)
    assert np.allclose(zc, ZC)

# -------------------------
# Rotation Matrix Utilities
# -------------------------

# FIXME This check fails on some matrices.
def test_orthonormalize_dcm():
    # Build valid rotation matrices.
    J = 100000
    C = np.zeros((J, 3, 3))
    for j in range(J):
        for m in range(J):
            c = np.random.randn(3, 3)
            if np.dot(np.cross(c[0], c[1]), c[2]) > 0:
                break
        C[j] = c

    # Test single matrix.
    D = C[0] + 0
    D = r3f.orthonormalize_dcm(D)
    B = (D.T @ D) - np.eye(3)
    assert np.sum(np.abs(B)) < 2e-15

    # Run many single matrix tests.
    N = 10
    eo = np.zeros((N, J))
    for n in range(0, N):
        D = C + 0
        for m in range(0, n + 1):
            D = r3f.orthonormalize_dcm(D)
        B = (np.transpose(D, (0, 2, 1)) @ D) - np.eye(3)
        eo[n] = np.sum(np.sum(np.abs(B), axis=1), axis=1)

    nn = np.arange(N) + 1
    e_mean = np.mean(eo, axis=1)
    e_max = np.max(eo, axis=1)
    e_min = np.min(eo, axis=1)
    #plt.figure()
    #plt.semilogy(nn, e_min)
    #plt.semilogy(nn, e_mean)
    #plt.semilogy(nn, e_max)
    #plt.show()
    assert np.all(e_max[1:] < 2e-15)


def test_rodrigues():
    # Test single.
    theta = np.random.randn(3)
    Delta = r3f.rodrigues_rotation(theta)
    Theta = r3f.inverse_rodrigues_rotation(Delta)
    assert np.allclose(theta, Theta)

    # Test multiple.
    K = 1000
    theta = np.random.randn(3, K)
    delta = np.zeros((K, 3, 3))
    for k in range(K):
        delta[k, :, :] = r3f.rodrigues_rotation(theta[:, k])
    for k in range(K):
        theta[:, k] = r3f.inverse_rodrigues_rotation(delta[k, :, :])
    Delta = r3f.rodrigues_rotation(theta)
    assert np.allclose(delta, Delta)
    Theta = r3f.inverse_rodrigues_rotation(Delta)
    assert np.allclose(theta, Theta)

    # Test 180 degree rotation.
    theta = np.array([1, 1, 0])
    theta = theta/np.linalg.norm(theta)*np.pi
    delta = r3f.rodrigues_rotation(theta)
    Delta = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1.0]])
    assert np.allclose(delta, Delta)
    try:
        theta = r3f.inverse_rodrigues_rotation(Delta)
        assert False
    except:
        assert True

