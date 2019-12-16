from pineapple_core.core.input_flags import (
    Hidden,
    Optional,
    create_input_flag,
)


def test_input_flags():
    FakeFlag = create_input_flag()

    assert not (Hidden in Optional)
    assert not (Optional in Hidden)
    assert not (FakeFlag in Hidden)
    assert not (FakeFlag in Optional)

    CombinedFlag = Hidden & Optional
    assert CombinedFlag in Hidden
    assert CombinedFlag in Optional
    assert not (FakeFlag in CombinedFlag)
    assert not (CombinedFlag in FakeFlag)
