import threading
from typing import Protocol

from . import network
from . import util
from . import logger

LOG = logger.LOG.get_logger(__name__)


class ControllerCommon(Protocol):
    """Protocol for the fundamental controller interface shared by sync/async implementations"""

    _action_sequence_last_sent: int
    _mcio_conn: network._Connection

    def send_action(self, action: network.ActionPacket) -> None:
        """Send action to minecraft. Automatically sets action.sequence."""
        self._action_sequence_last_sent += 1
        action.sequence = self._action_sequence_last_sent
        self._mcio_conn.send_action(action)

    def recv_observation(self) -> network.ObservationPacket: ...
    def close(self) -> None: ...


class ControllerSync(ControllerCommon):
    """
    Handles SYNC mode connections to Minecraft.
    Blocks in recv waiting for a new observation.
    """

    # XXX Implement context manager
    def __init__(self, host: str = "localhost"):
        self._action_sequence_last_sent = 0
        # This briefly sleeps for zmq initialization.
        self._mcio_conn = network._Connection()

    def recv_observation(
        self, block: bool = True, timeout: float | None = None
    ) -> network.ObservationPacket:
        """Receive observation. Blocks"""
        obs = self._mcio_conn.recv_observation()
        if obs is None:
            # This will only ever happen when zmq is shutting down
            return network.ObservationPacket()
        return obs

    def close(self) -> None:
        """Shut down the network connection"""
        self._mcio_conn.close()


class ControllerAsync(ControllerCommon):
    """
    Handles ASYNC mode connections to Minecraft
    """

    def __init__(self, host: str = "localhost"):
        self._action_sequence_last_sent = 0

        self.process_counter = util.TrackPerSecond("ProcessObservationPPS")
        self.queued_counter = util.TrackPerSecond("QueuedActionsPPS")

        # Flag to signal observation thread to stop.
        self._running = threading.Event()
        self._running.set()

        self._observation_queue = util.LatestItemQueue[network.ObservationPacket]()

        # This briefly sleeps for zmq initialization.
        self._mcio_conn = network._Connection()

        # Start observation thread
        self._observation_thread = threading.Thread(
            target=self._observation_thread_fn, name="ObservationThread"
        )
        self._observation_thread.daemon = True
        self._observation_thread.start()

        LOG.info("Controller init complete")

    def recv_observation(
        self, block: bool = True, timeout: float | None = None
    ) -> network.ObservationPacket:
        """
        Returns the most recently received observation pulling it from the processing queue.
        Block and timeout are like queue.Queue.get().
        Can raise Empty exception if non-blocking or timeout is used.
        """
        # RECV 3
        observation = self._observation_queue.get(block=block, timeout=timeout)
        return observation

    def _observation_thread_fn(self) -> None:
        """Loops. Receives observation packets from minecraft and places on observation_queue"""
        LOG.info("ObservationThread start")
        while self._running.is_set():
            # RECV 2
            # I don't think we'll ever drop here. this is a short loop to recv the packet
            # and put it on the queue to be processed.
            observation = self._mcio_conn.recv_observation()
            if observation is None:
                continue  # Exiting or packet decode error

            dropped = self._observation_queue.put(observation)
            if dropped:
                # This means the main (processing) thread isn't reading fast enough.
                # The first few are always dropped, presumably as we empty the initial zmq buffer
                # that built up during pause for "slow joiner syndrome".
                LOG.debug("Dropped observation packet from processing queue")
                pass

        LOG.info("ObservationThread shut down")

    def close(self) -> None:
        """Shut down the network connection"""
        self._running.clear()
        self._mcio_conn.close()

        self._observation_thread.join()
        # # Send empty action to unblock ActionThread
        # self._action_queue.put(None)
        # self._action_thread.join()
