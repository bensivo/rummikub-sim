from rummikub_sim.core.find_runs import find_runs
from rummikub_sim.core.serialization import set_from_str, set_to_str


def test__find_runs__basic():
    # Given: A list of tiles forming a basic run
    tiles = set_from_str("[r2,r3,r4]")

    # When: We call find_runs
    runs = find_runs(tiles)
    runs_str = [set_to_str(run) for run in runs]

    # Then: The run is returned
    assert "[r2,r3,r4]" in runs_str
    

def test__find_runs__multiple_runs():
    # Given: 2 runs in the same set of tiles
    tiles = set_from_str("[r2,r3,r4,b1,b2,b3]")

    # When: We call find_runs
    runs = find_runs(tiles)
    runs_str = [set_to_str(run) for run in runs]

    # Then: both runs are identified
    assert len(runs) == 2
    assert "[r2,r3,r4]" in runs_str
    assert "[b1,b2,b3]" in runs_str


def test__find_runs__with_overlapping():
    # Given: 2 overlapping runs in the same hand
    tiles = set_from_str("[r2,r3,r4,r5]")

    # When: We call find_runs
    runs = find_runs(tiles)
    runs_str = [set_to_str(run) for run in runs]

    # Then: All options are identified
    assert len(runs) == 3
    assert "[r2,r3,r4]" in runs_str
    assert "[r3,r4,r5]" in runs_str
    assert "[r2,r3,r4,r5]" in runs_str


def test__find_runs__with_overlapping_multi():
    # Given: 2 overlapping runs in the same hand
    tiles = set_from_str("[r2,r3,r4,r5,r6]")

    # When: We call find_runs
    runs = find_runs(tiles)
    runs_str = [set_to_str(run) for run in runs]

    # Then: All options are identified
    assert len(runs) == 6
    assert "[r2,r3,r4]" in runs_str
    assert "[r3,r4,r5]" in runs_str
    assert "[r4,r5,r6]" in runs_str
    assert "[r2,r3,r4,r5]" in runs_str
    assert "[r3,r4,r5,r6]" in runs_str
    assert "[r2,r3,r4,r5,r6]" in runs_str


def test__find_runs__handles_jokers():
    # Given: 2 tiles in a run with 1 joker
    tiles = set_from_str("[r2,r3,rJ]")

    # When: We call find_runs
    runs = find_runs(tiles)
    runs_str = [set_to_str(run) for run in runs]

    # Then: The run is returned with the joker
    assert len(runs) == 2
    assert "[r2,r3,rJ]" in runs_str
    assert "[rJ,r2,r3]" in runs_str
    
def test__find_runs__jokers_in_all_spots():
    # Given: 3 tiles in a run with 1 joker
    tiles = set_from_str("[r2,r3,r4,rJ]")

    # When: We call find_runs
    runs = find_runs(tiles)
    runs_str = [set_to_str(run) for run in runs]

    # Then: The run is returned with the jokers considered
    # at each spot, plus at the begining and end of the run
    assert len(runs) == 8
    assert "[rJ,r2,r3]" in runs_str  # j23
    assert "[r2,r3,r4]" in runs_str  # 234
    assert "[rJ,r3,r4]" in runs_str  # j34
    assert "[r2,rJ,r4]" in runs_str  # 2j4
    assert "[r2,r3,rJ]" in runs_str  # 23j
    assert "[r3,r4,rJ]" in runs_str  # 34j
    assert "[r2,r3,r4,rJ]" in runs_str  # 234j
    assert "[rJ,r2,r3,r4]" in runs_str  # j234  
    

def test__find_runs__doest_put_jokers_over_13():
    # Given: a hand 12,13,J
    tiles = set_from_str("[r12,r13,rJ]")

    # When: We call find_runs
    runs = find_runs(tiles)
    runs_str = [set_to_str(run) for run in runs]

    # Then: J,12,13 is found, but 12,13,J is not considered
    # becasue the J would be in slot "14"
    assert "[rJ,r12,r13]" in runs_str
    assert "[r12,r13,rJ]" not in runs_str

def test__find_runs__extends_run_ending_in_joker():
    # note: there was an obscure bug related to the fact that jokers internally have a '-1' as their number
    # When we used a joker as the final tile in a sequence, it would show up as -1, and the extension logic would try
    # to find a '0' as the next tile, not the proper next tile in the sequence.

    # Given: a hand which triggers extension logic using a joker
    tiles = set_from_str("[r2,r3,r4,rJ,r6]")

    # When: we call find_runs
    runs = find_runs(tiles)
    runs_str = [set_to_str(run) for run in runs]

    # Then: the run is successfully returned
    assert "[r2,r3,r4,rJ,r6]" in runs_str
