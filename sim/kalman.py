"""High-throughput Kalman filter utilities for radar tracking simulations.

The module keeps the implementation lightweight and NumPy-based so it can be used in
batch simulations and fast iterated track updates without requiring a heavy scientific
stack.

It supports both the compact, matrix-driven API used in simulation code and the
convenience radar-tracking wrappers commonly used for position/velocity filtering.
"""

from __future__ import annotations

from typing import Iterable, List, Optional, Sequence, Tuple, Union

import numpy as np

ArrayLike = Union[Sequence[float], np.ndarray]


def _as_vector(values: ArrayLike, *, size: Optional[int] = None, name: str = "value") -> np.ndarray:
    arr = np.asarray(values, dtype=np.float64)
    if arr.ndim == 0:
        arr = arr.reshape(1)
    if arr.ndim != 1:
        raise ValueError(f"{name} must be a 1D array-like object.")
    if size is not None and arr.size != size:
        raise ValueError(f"{name} must have length {size}; got {arr.size}.")
    return arr


def _as_matrix(values: ArrayLike, *, shape: Optional[tuple[int, int]] = None, name: str = "value") -> np.ndarray:
    arr = np.asarray(values, dtype=np.float64)
    if arr.ndim == 0:
        if shape is None:
            arr = arr.reshape(1, 1)
        else:
            arr = np.full(shape, float(arr), dtype=np.float64)
    elif arr.ndim == 1:
        if shape is not None and shape[0] == shape[1] and arr.size == shape[0]:
            arr = np.diag(arr)
        elif shape is None:
            arr = np.diag(arr)
    if arr.ndim != 2:
        raise ValueError(f"{name} must be a 2D array-like object.")
    if shape is not None and arr.shape != shape:
        raise ValueError(f"{name} must have shape {shape}; got {arr.shape}.")
    return arr


def _default_measurement_matrix(state_dim: int, measurement_dim: int) -> np.ndarray:
    if measurement_dim > state_dim:
        raise ValueError("Measurement dimension cannot be larger than state dimension.")
    if measurement_dim == state_dim:
        return np.eye(state_dim, dtype=np.float64)
    return np.hstack(
        (
            np.eye(measurement_dim, dtype=np.float64),
            np.zeros((measurement_dim, state_dim - measurement_dim), dtype=np.float64),
        )
    )


class KalmanFilter:
    """Generic linear Kalman filter supporting both state-space and radar-specific usage."""

    def __init__(
        self,
        state_transition: Optional[ArrayLike] = None,
        process_noise: Optional[ArrayLike] = None,
        observation_matrix: Optional[ArrayLike] = None,
        observation_noise: Optional[ArrayLike] = None,
        initial_state: Optional[ArrayLike] = None,
        initial_covariance: Optional[ArrayLike] = None,
        *,
        state_dim: Optional[int] = None,
        measurement_dim: Optional[int] = None,
        process_matrix: Optional[ArrayLike] = None,
        measurement_matrix: Optional[ArrayLike] = None,
        process_noise_matrix: Optional[ArrayLike] = None,
        measurement_noise_matrix: Optional[ArrayLike] = None,
    ) -> None:
        if state_dim is not None:
            if state_dim <= 0:
                raise ValueError("state_dim must be positive.")
            if measurement_dim is None:
                measurement_dim = state_dim
            if measurement_dim <= 0:
                raise ValueError("measurement_dim must be positive.")
            self.state_dim = int(state_dim)
            self.measurement_dim = int(measurement_dim)
            self.x = _as_vector(initial_state if initial_state is not None else np.zeros(self.state_dim), size=self.state_dim, name="initial_state").reshape(-1, 1)
            self.P = _as_matrix(initial_covariance if initial_covariance is not None else np.eye(self.state_dim), shape=(self.state_dim, self.state_dim), name="initial_covariance")
            self.F = _as_matrix(process_matrix if process_matrix is not None else np.eye(self.state_dim), shape=(self.state_dim, self.state_dim), name="process_matrix")
            self.H = _as_matrix(measurement_matrix if measurement_matrix is not None else _default_measurement_matrix(self.state_dim, self.measurement_dim), shape=(self.measurement_dim, self.state_dim), name="measurement_matrix")
            self.Q = _as_matrix(process_noise if process_noise is not None else process_noise_matrix if process_noise_matrix is not None else np.eye(self.state_dim), shape=(self.state_dim, self.state_dim), name="process_noise")
            self.R = _as_matrix(observation_noise if observation_noise is not None else measurement_noise_matrix if measurement_noise_matrix is not None else np.eye(self.measurement_dim), shape=(self.measurement_dim, self.measurement_dim), name="measurement_noise")
        else:
            if state_transition is None:
                raise ValueError("state_transition is required when state_dim is not provided.")
            self.F = _as_matrix(state_transition, name="state_transition")
            self.Q = _as_matrix(process_noise if process_noise is not None else np.eye(self.F.shape[0]), shape=(self.F.shape[0], self.F.shape[0]), name="process_noise")
            self.H = _as_matrix(observation_matrix if observation_matrix is not None else np.eye(self.F.shape[0]), name="observation_matrix")
            self.R = _as_matrix(observation_noise if observation_noise is not None else np.eye(self.H.shape[0]), shape=(self.H.shape[0], self.H.shape[0]), name="measurement_noise")
            self.x = _as_vector(initial_state if initial_state is not None else np.zeros(self.F.shape[0]), size=self.F.shape[0], name="initial_state").reshape(-1, 1)
            if initial_covariance is None:
                self.P = np.eye(self.F.shape[0], dtype=np.float64)
            else:
                self.P = _as_matrix(initial_covariance, shape=(self.F.shape[0], self.F.shape[0]), name="initial_covariance")
            self.state_dim = self.F.shape[0]
            self.measurement_dim = self.H.shape[0]

        self.kalman_gain = np.zeros((self.state_dim, self.measurement_dim), dtype=np.float64)
        self.innovation = np.zeros(self.measurement_dim, dtype=np.float64)
        self.last_measurement: Optional[np.ndarray] = None
        self.last_prediction = self.x.copy()
        self.last_update = self.x.copy()

    @property
    def state_vector(self) -> np.ndarray:
        return self.x.copy()

    @property
    def covariance_matrix(self) -> np.ndarray:
        return self.P.copy()

    @property
    def state(self) -> np.ndarray:
        return self.x.copy().reshape(-1)

    @state.setter
    def state(self, values: ArrayLike) -> None:
        self.x = _as_vector(values, size=self.state_dim, name="state").reshape(-1, 1)

    @property
    def covariance(self) -> np.ndarray:
        return self.P.copy()

    @covariance.setter
    def covariance(self, values: ArrayLike) -> None:
        self.P = _as_matrix(values, shape=(self.state_dim, self.state_dim), name="covariance")

    def predict(
        self,
        control: Optional[ArrayLike] = None,
        dt: Optional[float] = None,
        *,
        process_matrix: Optional[ArrayLike] = None,
        process_noise: Optional[ArrayLike] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        F = self.F if process_matrix is None else _as_matrix(process_matrix, shape=(self.state_dim, self.state_dim), name="process_matrix")
        Q = self.Q if process_noise is None else _as_matrix(process_noise, shape=(self.state_dim, self.state_dim), name="process_noise")

        if dt is not None:
            if dt <= 0.0:
                raise ValueError("dt must be positive.")
            if F.shape == (2, 2):
                F = np.array([[1.0, dt], [0.0, 1.0]], dtype=np.float64)
            elif F.shape == (4, 4):
                F = np.array(
                    [
                        [1.0, 0.0, dt, 0.0],
                        [0.0, 1.0, 0.0, dt],
                        [0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 0.0, 1.0],
                    ],
                    dtype=np.float64,
                )

        u = np.zeros(self.state_dim, dtype=np.float64) if control is None else _as_vector(control, size=self.state_dim, name="control")
        self.x = F @ self.x + u.reshape(-1, 1)
        self.P = F @ self.P @ F.T + Q
        self.last_prediction = self.x.copy()
        self.F = F
        self.Q = Q
        return self.x.copy(), self.P.copy()

    def update(
        self,
        measurement: ArrayLike,
        *,
        measurement_matrix: Optional[ArrayLike] = None,
        measurement_noise: Optional[ArrayLike] = None,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        z = _as_vector(measurement, size=self.measurement_dim, name="measurement").reshape(-1, 1)
        H = self.H if measurement_matrix is None else _as_matrix(measurement_matrix, shape=(self.measurement_dim, self.state_dim), name="measurement_matrix")
        R = self.R if measurement_noise is None else _as_matrix(measurement_noise, shape=(self.measurement_dim, self.measurement_dim), name="measurement_noise")

        innovation = z - (H @ self.x)
        innovation_covariance = H @ self.P @ H.T + R
        self.kalman_gain = np.linalg.solve(innovation_covariance.T, (self.P @ H.T).T).T

        self.x = self.x + self.kalman_gain @ innovation
        identity = np.eye(self.state_dim, dtype=np.float64)
        self.P = (identity - self.kalman_gain @ H) @ self.P @ (identity - self.kalman_gain @ H).T + self.kalman_gain @ R @ self.kalman_gain.T
        self.last_measurement = z.copy()
        self.last_update = self.x.copy()
        self.innovation = innovation.reshape(-1)
        self.H = H
        self.R = R
        return self.x.copy(), self.P.copy(), innovation.copy()

    def filter_sequence(self, measurements: Iterable[ArrayLike]) -> List[np.ndarray]:
        tracked: List[np.ndarray] = []
        for measurement in measurements:
            self.predict()
            self.update(measurement)
            tracked.append(self.x.copy().reshape(-1))
        return tracked


LinearKalmanFilter = KalmanFilter


class ConstantVelocityKalmanFilter(KalmanFilter):
    """State-space constant-velocity tracker with state [x, y, vx, vy]."""

    def __init__(
        self,
        *,
        dt: float = 1.0,
        position_std: float = 1.0,
        velocity_std: float = 1.0,
        acceleration_std: float = 1.0,
        initial_state: Optional[ArrayLike] = None,
        initial_covariance: Optional[ArrayLike] = None,
    ) -> None:
        if dt <= 0.0:
            raise ValueError("dt must be positive.")

        process_matrix = np.array(
            [
                [1.0, 0.0, dt, 0.0],
                [0.0, 1.0, 0.0, dt],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ],
            dtype=np.float64,
        )
        measurement_matrix = np.array(
            [
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
            ],
            dtype=np.float64,
        )
        q11 = (dt**4 / 4.0) * (acceleration_std**2)
        q22 = (dt**4 / 4.0) * (acceleration_std**2)
        q13 = (dt**3 / 2.0) * (acceleration_std**2)
        q24 = (dt**3 / 2.0) * (acceleration_std**2)
        q33 = dt**2 * (acceleration_std**2)
        q44 = dt**2 * (acceleration_std**2)
        process_noise = np.array(
            [
                [q11, 0.0, q13, 0.0],
                [0.0, q22, 0.0, q24],
                [q13, 0.0, q33, 0.0],
                [0.0, q24, 0.0, q44],
            ],
            dtype=np.float64,
        )
        measurement_noise = np.eye(2, dtype=np.float64) * (position_std**2)
        initial = np.zeros(4, dtype=np.float64) if initial_state is None else np.asarray(initial_state, dtype=np.float64).reshape(-1)
        if initial.size != 4:
            raise ValueError("initial_state must be length 4 for a constant-velocity filter.")
        super().__init__(
            state_transition=process_matrix,
            process_noise=process_noise,
            observation_matrix=measurement_matrix,
            observation_noise=measurement_noise,
            initial_state=initial,
            initial_covariance=initial_covariance if initial_covariance is not None else np.diag([position_std**2, position_std**2, velocity_std**2, velocity_std**2]),
        )

    def predict(
        self,
        *,
        dt: Optional[float] = None,
        control: Optional[ArrayLike] = None,
        process_noise: Optional[ArrayLike] = None,
    ) -> np.ndarray:
        if dt is not None:
            if dt <= 0.0:
                raise ValueError("dt must be positive.")
            self.F = np.array(
                [
                    [1.0, 0.0, dt, 0.0],
                    [0.0, 1.0, 0.0, dt],
                    [0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0],
                ],
                dtype=np.float64,
            )
        return super().predict(control=control, process_matrix=self.F, process_noise=process_noise)[0]

    def update(self, measurement: ArrayLike, *, measurement_noise: Optional[ArrayLike] = None) -> np.ndarray:
        return super().update(measurement, measurement_matrix=self.H, measurement_noise=measurement_noise)[0]


class RadarTrackFilter(ConstantVelocityKalmanFilter):
    """A 2D position/velocity Kalman filter tuned for radar tracking."""

    def __init__(
        self,
        dt: float = 0.1,
        initial_position: Optional[Sequence[float]] = None,
        initial_velocity: Optional[Sequence[float]] = None,
        process_noise: float = 1.0,
        measurement_noise: float = 1.0,
        initial_covariance: float = 100.0,
    ) -> None:
        self.dt = float(dt)
        if self.dt <= 0.0:
            raise ValueError("dt must be positive.")

        pos = np.asarray(initial_position if initial_position is not None else (0.0, 0.0), dtype=np.float64)
        vel = np.asarray(initial_velocity if initial_velocity is not None else (0.0, 0.0), dtype=np.float64)
        if pos.shape != (2,):
            raise ValueError("initial_position must be a 2D coordinate (x, y).")
        if vel.shape != (2,):
            raise ValueError("initial_velocity must be a 2D velocity (vx, vy).")

        super().__init__(
            dt=self.dt,
            position_std=np.sqrt(initial_covariance),
            velocity_std=np.sqrt(initial_covariance),
            acceleration_std=np.sqrt(process_noise),
            initial_state=np.array([pos[0], pos[1], vel[0], vel[1]], dtype=np.float64),
            initial_covariance=np.eye(4, dtype=np.float64) * initial_covariance,
        )
        self.observation_noise_scale = float(measurement_noise)
        self.R = np.eye(2, dtype=np.float64) * self.observation_noise_scale
        self.H = np.array(
            [
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
            ],
            dtype=np.float64,
        )

    @property
    def state(self) -> np.ndarray:
        return self.x.copy().reshape(-1)

    @property
    def covariance(self) -> np.ndarray:
        return self.P.copy()

    def predict(self, dt: Optional[float] = None) -> np.ndarray:
        if dt is None:
            dt = self.dt
        if dt <= 0.0:
            raise ValueError("dt must be positive.")
        if abs(dt - self.dt) > 1e-12:
            self.dt = float(dt)
        return super().predict(dt=self.dt)

    def update(self, measurement: Sequence[float]) -> np.ndarray:
        z = np.asarray(measurement, dtype=np.float64).reshape(2)
        super().update(z, measurement_noise=np.eye(2, dtype=np.float64) * self.observation_noise_scale)
        return self.state.copy()

    def track(self, measurements: Iterable[Sequence[float]]) -> List[np.ndarray]:
        results: List[np.ndarray] = []
        for measurement in measurements:
            self.predict()
            self.update(measurement)
            results.append(self.state.copy())
        return results


RadarKalmanFilter = RadarTrackFilter
RadarTracker = RadarTrackFilter
KalmanFilter2D = ConstantVelocityKalmanFilter


def kalman_predict(filter_obj: KalmanFilter, control: Optional[ArrayLike] = None) -> Tuple[np.ndarray, np.ndarray]:
    """Convenience wrapper for a single prediction step."""
    return filter_obj.predict(control=control)


def kalman_update(filter_obj: KalmanFilter, measurement: ArrayLike) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Convenience wrapper for a single update step."""
    return filter_obj.update(measurement)


def filter_sequence(
    measurements: Sequence[ArrayLike],
    *,
    tracker: Optional[KalmanFilter] = None,
    dt: float = 1.0,
    process_noise: Optional[ArrayLike] = None,
    measurement_noise: Optional[ArrayLike] = None,
) -> np.ndarray:
    """Apply a Kalman filter to a sequence of observations and return the filtered states."""
    if tracker is None:
        tracker = ConstantVelocityKalmanFilter(dt=dt)
    states: List[np.ndarray] = []
    for measurement in measurements:
        tracker.predict(dt=dt, process_noise=process_noise)
        tracker.update(measurement, measurement_noise=measurement_noise)
        states.append(tracker.state.copy())
    return np.asarray(states, dtype=np.float64)


def track_radar(
    observations: Iterable[Sequence[float]],
    dt: float = 0.1,
    initial_position: Optional[Sequence[float]] = None,
    initial_velocity: Optional[Sequence[float]] = None,
    process_noise: float = 1.0,
    measurement_noise: float = 1.0,
) -> List[np.ndarray]:
    """Helper for tracking a radar target across a sequence of positions."""
    filter_obj = RadarTrackFilter(
        dt=dt,
        initial_position=initial_position,
        initial_velocity=initial_velocity,
        process_noise=process_noise,
        measurement_noise=measurement_noise,
    )
    return filter_obj.track(observations)


__all__ = [
    "KalmanFilter",
    "LinearKalmanFilter",
    "ConstantVelocityKalmanFilter",
    "KalmanFilter2D",
    "RadarTrackFilter",
    "RadarTracker",
    "RadarKalmanFilter",
    "filter_sequence",
    "kalman_predict",
    "kalman_update",
    "track_radar",
]
