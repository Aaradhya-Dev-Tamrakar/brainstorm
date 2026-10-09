"""High-throughput Kalman filter utilities for radar tracking simulations.

This module intentionally keeps the implementation lightweight and NumPy-based so it can
be used in batch simulations and fast iterated track updates without requiring a heavy
scientific stack.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

import numpy as np


__all__ = [
    "KalmanFilter",
    "LinearKalmanFilter",
    "RadarTrackFilter",
    "RadarKalmanFilter",
    "kalman_predict",
    "kalman_update",
    "track_radar",
]


@dataclass
class KalmanFilter:
    """Generic linear Kalman filter implementation.

    This class supports the standard predict/update cycle used for radar target
    tracking, position estimation, and other time-series filtering tasks.
    """

    state_transition: np.ndarray
    process_noise: np.ndarray
    observation_matrix: np.ndarray
    observation_noise: np.ndarray
    initial_state: np.ndarray
    initial_covariance: np.ndarray | None = None
    state: np.ndarray | None = None
    covariance: np.ndarray | None = None

    def __post_init__(self) -> None:
        self.F = np.asarray(self.state_transition, dtype=np.float64)
        self.Q = np.asarray(self.process_noise, dtype=np.float64)
        self.H = np.asarray(self.observation_matrix, dtype=np.float64)
        self.R = np.asarray(self.observation_noise, dtype=np.float64)
        self.x = np.asarray(self.initial_state, dtype=np.float64).reshape(-1, 1)

        if self.initial_covariance is None:
            self.P = np.eye(self.F.shape[0], dtype=np.float64)
        else:
            self.P = np.asarray(self.initial_covariance, dtype=np.float64)
            if self.P.shape != (self.F.shape[0], self.F.shape[0]):
                raise ValueError("Initial covariance shape must match the state dimension.")

        if self.state is not None:
            self.x = np.asarray(self.state, dtype=np.float64).reshape(-1, 1)
        if self.covariance is not None:
            self.P = np.asarray(self.covariance, dtype=np.float64)

        self.last_measurement = None
        self.last_prediction = self.x.copy()
        self.last_update = self.x.copy()

    @property
    def state_vector(self) -> np.ndarray:
        return self.x.copy()

    @property
    def covariance_matrix(self) -> np.ndarray:
        return self.P.copy()

    def predict(self, control: np.ndarray | Sequence[float] | None = None, dt: float | None = None) -> Tuple[np.ndarray, np.ndarray]:
        """Project the state estimate one timestep forward."""
        if dt is not None and self.F.shape[0] == 2 and self.F.shape[1] == 2:
            # Kept for compatibility with very small 1D cases; generic F matrix is authoritative.
            pass

        x_pred = self.x.copy()
        if control is not None:
            u = np.asarray(control, dtype=np.float64).reshape(-1, 1)
            if self.F.shape[1] != self.x.shape[0]:
                raise ValueError("Control dimension does not match the state dimension.")
            if u.shape[0] != self.F.shape[1]:
                raise ValueError("Control vector length must match the state dimension.")
            x_pred = self.x + u

        x_pred = self.F @ self.x if control is None else self.F @ self.x + u
        P_pred = self.F @ self.P @ self.F.T + self.Q
        self.x = x_pred
        self.P = P_pred
        self.last_prediction = self.x.copy()
        return self.x.copy(), self.P.copy()

    def update(self, measurement: np.ndarray | Sequence[float]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Assimilate a measurement and update the estimate.

        Returns a triple of (state, covariance, innovation). Each result is a NumPy array.
        """
        z = np.asarray(measurement, dtype=np.float64).reshape(-1, 1)
        if self.H.shape[0] != z.shape[0]:
            raise ValueError("Measurement dimension does not match observation matrix rows.")

        innovation = z - (self.H @ self.x)
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)

        self.x = self.x + K @ innovation
        I = np.eye(self.x.shape[0], dtype=np.float64)
        self.P = (I - K @ self.H) @ self.P

        self.last_measurement = z.copy()
        self.last_update = self.x.copy()
        return self.x.copy(), self.P.copy(), innovation.copy()

    def filter_sequence(self, measurements: Iterable[Sequence[float]]) -> List[np.ndarray]:
        """Apply a predict/update cycle across a sequence of measurements."""
        tracked = []
        for measurement in measurements:
            self.predict()
            self.update(measurement)
            tracked.append(self.x.copy())
        return tracked


LinearKalmanFilter = KalmanFilter


class RadarTrackFilter:
    """A 2D position/velocity Kalman filter tuned for radar tracking."""

    def __init__(
        self,
        dt: float = 0.1,
        initial_position: Sequence[float] | None = None,
        initial_velocity: Sequence[float] | None = None,
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

        self.kf = KalmanFilter(
            state_transition=np.array(
                [
                    [1.0, 0.0, self.dt, 0.0],
                    [0.0, 1.0, 0.0, self.dt],
                    [0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0],
                ],
                dtype=np.float64,
            ),
            process_noise=np.eye(4, dtype=np.float64) * process_noise,
            observation_matrix=np.array(
                [
                    [1.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 0.0],
                ],
                dtype=np.float64,
            ),
            observation_noise=np.eye(2, dtype=np.float64) * measurement_noise,
            initial_state=np.array([pos[0], pos[1], vel[0], vel[1]], dtype=np.float64),
            initial_covariance=np.eye(4, dtype=np.float64) * initial_covariance,
        )

    @property
    def state(self) -> np.ndarray:
        return self.kf.x.copy().reshape(-1)

    @property
    def covariance(self) -> np.ndarray:
        return self.kf.P.copy()

    def predict(self, dt: float | None = None) -> np.ndarray:
        """Advance the target state one radar update interval."""
        if dt is None:
            dt = self.dt
        if dt <= 0.0:
            raise ValueError("dt must be positive.")
        if abs(dt - self.dt) > 1e-12:
            # Rebuild the transition matrix when a custom dt is supplied.
            self.kf.F = np.array(
                [
                    [1.0, 0.0, dt, 0.0],
                    [0.0, 1.0, 0.0, dt],
                    [0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0],
                ],
                dtype=np.float64,
            )
        return self.kf.predict()[0]

    def update(self, measurement: Sequence[float]) -> np.ndarray:
        """Correct the state with an observed radar position (x, y)."""
        z = np.asarray(measurement, dtype=np.float64).reshape(2)
        self.kf.update(z)
        return self.state.copy()

    def track(self, measurements: Iterable[Sequence[float]]) -> List[np.ndarray]:
        """Filter a sequence of radar observations."""
        results: List[np.ndarray] = []
        for measurement in measurements:
            self.predict()
            self.update(measurement)
            results.append(self.state.copy())
        return results


RadarKalmanFilter = RadarTrackFilter


def kalman_predict(filter_obj: KalmanFilter, control: np.ndarray | Sequence[float] | None = None) -> Tuple[np.ndarray, np.ndarray]:
    """Convenience wrapper for a single prediction step."""
    return filter_obj.predict(control=control)


def kalman_update(filter_obj: KalmanFilter, measurement: np.ndarray | Sequence[float]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Convenience wrapper for a single update step."""
    return filter_obj.update(measurement)


def track_radar(
    observations: Iterable[Sequence[float]],
    dt: float = 0.1,
    initial_position: Sequence[float] | None = None,
    initial_velocity: Sequence[float] | None = None,
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


if __name__ == "__main__":
    observations = [
        (0.0, 0.0),
        (1.0, 0.1),
        (2.0, 0.2),
        (3.0, 0.4),
        (4.0, 0.6),
    ]
    tracked = track_radar(observations, dt=0.25)
    print("Radar track estimate:")
    for idx, state in enumerate(tracked):
        print(idx, state)
