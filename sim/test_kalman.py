import numpy as np

from sim import ConstantVelocityKalmanFilter, filter_sequence
from sim.kalman import KalmanFilter, RadarTrackFilter


def test_kalman_filter_state_updates() -> None:
    kf = KalmanFilter(
        state_transition=np.array([[1.0, 1.0], [0.0, 1.0]], dtype=np.float64),
        process_noise=np.diag([0.01, 0.01]).astype(np.float64),
        observation_matrix=np.array([[1.0, 0.0]], dtype=np.float64),
        observation_noise=np.array([[0.5]], dtype=np.float64),
        initial_state=np.array([0.0, 1.0], dtype=np.float64),
        initial_covariance=np.eye(2, dtype=np.float64),
    )

    kf.predict()
    state, covariance, innovation = kf.update(np.array([1.0], dtype=np.float64))

    assert state.shape == (2, 1)
    assert covariance.shape == (2, 2)
    assert innovation.shape == (1, 1)
    assert np.all(np.isfinite(state))
    assert np.all(np.isfinite(covariance))
    assert np.all(np.isfinite(innovation))


def test_radar_track_filter_tracks_linear_motion() -> None:
    observations = np.array(
        [
            [0.0, 0.0],
            [1.0, 0.2],
            [2.0, 0.4],
            [3.0, 0.5],
        ],
        dtype=np.float64,
    )

    tracker = RadarTrackFilter(
        dt=0.5,
        initial_position=(0.0, 0.0),
        initial_velocity=(0.0, 0.0),
        process_noise=1e-2,
        measurement_noise=1e-2,
        initial_covariance=10.0,
    )

    track = tracker.track(observations)

    assert len(track) == len(observations)
    assert all(array.shape == (4,) for array in track)
    assert all(np.all(np.isfinite(array)) for array in track)
    assert track[-1][0] > track[0][0]


def test_package_exports_and_scalar_noise_inputs() -> None:
    kf = KalmanFilter(
        state_transition=np.array([[1.0, 1.0], [0.0, 1.0]], dtype=np.float64),
        process_noise=0.01,
        observation_matrix=np.array([[1.0, 0.0]], dtype=np.float64),
        observation_noise=0.5,
        initial_state=np.array([0.0, 1.0], dtype=np.float64),
        initial_covariance=np.eye(2, dtype=np.float64),
    )

    assert isinstance(ConstantVelocityKalmanFilter(dt=0.1), ConstantVelocityKalmanFilter)
    state, covariance, innovation = kf.update(np.array([1.0], dtype=np.float64))
    assert state.shape == (2, 1)
    assert covariance.shape == (2, 2)
    assert innovation.shape == (1, 1)

    filtered = filter_sequence(
        np.array([[0.0, 0.0], [1.0, 0.2], [2.0, 0.4]], dtype=np.float64),
        tracker=ConstantVelocityKalmanFilter(dt=0.5),
        dt=0.5,
    )
    assert filtered.shape == (3, 4)
    assert np.all(np.isfinite(filtered))
