import pytest
from pyautd3 import tracing_init
from pyautd3.utils import Duration

from pyautd3_link_soem import SOEM, ProcessPriority, RemoteSOEM, Status, SyncMode, ThreadPriority, TimerStrategy
from pyautd3_link_soem.native_methods.autd3capi_link_soem import NativeMethods as NativeSOEM
from pyautd3_link_soem.native_methods.autd3capi_link_soem import Status as _Status


def test_tracing_init():
    tracing_init()


def test_soem_adapers():
    adapters = SOEM.enumerate_adapters()
    for adapter in adapters:
        print(adapter)


def test_soem_thread_priority():
    _ = ThreadPriority.Max
    _ = ThreadPriority.Min
    _ = ThreadPriority.Crossplatform(0)
    _ = ThreadPriority.Crossplatform(99)
    with pytest.raises(ValueError):  # noqa: PT011
        _ = ThreadPriority.Crossplatform(-1)
    with pytest.raises(ValueError):  # noqa: PT011
        _ = ThreadPriority.Crossplatform(100)


def test_status():
    lost = Status.Lost()
    state_change = Status.StateChanged()
    err = Status.Error()

    assert lost == Status.Lost()
    assert state_change == Status.StateChanged()
    assert err == Status.Error()
    assert lost != state_change
    assert lost != err
    assert lost != _Status.Lost
    assert state_change != err
    assert state_change != lost
    assert state_change != _Status.StateChanged
    assert err != lost
    assert err != state_change
    assert err != _Status.Error

    status = Status.__private_new__(_Status.Lost, "lost")
    assert status == Status.Lost()
    assert str(status) == "lost"

    with pytest.raises(NotImplementedError):
        _ = Status()


def test_soem_is_default():
    builder = SOEM.builder()
    assert NativeSOEM().link_soem_is_default(
        builder.buf_size,
        builder.send_cycle._inner,
        builder.sync0_cycle._inner,
        builder.sync_mode,
        builder.process_priority,
        builder.thread_priority,
        builder.state_check_interval._inner,
        builder.timer_strategy,
        builder.sync_tolerance._inner,
        builder.sync_timeout._inner,
    )


def test_soem():
    def err_handler(slave: int, status: Status) -> None:
        print(f"slave: {slave}, status: {status}")

    builder = (
        SOEM.builder()
        .with_ifname("ifname")
        .with_buf_size(10)
        .with_send_cycle(Duration.from_millis(10))
        .with_sync0_cycle(Duration.from_millis(20))
        .with_err_handler(err_handler)  # type: ignore[arg-type]
        .with_timer_strategy(TimerStrategy.StdSleep)
        .with_sync_mode(SyncMode.FreeRun)
        .with_sync_tolerance(Duration.from_micros(10))
        .with_sync_timeout(Duration.from_secs(20))
        .with_state_check_interval(Duration.from_millis(200))
        .with_process_priority(ProcessPriority.Idle)
        .with_thread_priority(ThreadPriority.Min)
    )
    assert builder.ifname == "ifname"
    assert builder.buf_size == 10
    assert builder.send_cycle == Duration.from_millis(10)
    assert builder.sync0_cycle == Duration.from_millis(20)
    assert builder.err_handler == err_handler
    assert builder.timer_strategy == TimerStrategy.StdSleep
    assert builder.sync_mode == SyncMode.FreeRun
    assert builder.sync_tolerance == Duration.from_micros(10)
    assert builder.sync_timeout == Duration.from_secs(20)
    assert builder.state_check_interval == Duration.from_millis(200)
    assert builder.process_priority == ProcessPriority.Idle
    assert builder.thread_priority == ThreadPriority.Min


def test_remote_soem():
    _ = RemoteSOEM.builder("127.0.0.1:8080")
