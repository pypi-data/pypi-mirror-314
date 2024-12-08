"""Utils for jax."""

import jax
import jax.numpy as jnp
from jax._src.typing import Array  # TODO: Check why Array is not in jax.typing like in the docs
from jax.typing import ArrayLike


# %% Tree utils
def tree_stack(trees, axis=0):
    """Stack pytrees along a given axis."""
    return jax.tree_map(lambda *v: jnp.stack(v, axis), *trees)


def tree_unstack(tree):
    leaves, treedef = jax.tree_flatten(tree)
    return [treedef.unflatten(leaf) for leaf in zip(*leaves, strict=True)]


def tree_pad(traj, pad_width, pad_mode="constant", pad_constant_values=0):
    return jax.tree_map(
        lambda x: jnp.pad(
            x, pad_width[: x.ndim], mode=pad_mode, constant_values=pad_constant_values
        ),
        traj,
    )


def compute_smart_bins(
    dataset: list[dict[str, ArrayLike]],
    nb_bins: int,
) -> list[list[dict[str, Array]]]:
    """
    Group trajectories in bins of similar length to limit the padding required.

    Thanks to Mathis Hardion for finding this elegant solution.
    """
    if nb_bins == 1:
        return [dataset]
    nb_sequences = len(dataset)
    sorted_dataset = sorted(dataset, key=lambda x: len(x["observations"]), reverse=True)
    len_deltas = [
        len(sorted_dataset[i]["observations"]) - len(sorted_dataset[i + 1]["observations"])
        for i in range(nb_sequences - 1)
    ]
    len_deltas = jnp.array(len_deltas)
    top_k_delta_indices = jnp.argpartition(len_deltas, -nb_bins + 1)[-nb_bins + 1 :]
    top_k_delta_indices = jnp.sort(top_k_delta_indices)

    bins = []
    start_index = 0
    for end_index in top_k_delta_indices:
        bins.append(sorted_dataset[start_index : end_index + 1])
        start_index = end_index + 1
    bins.append(sorted_dataset[start_index:])

    return bins


def smart_pad_dataset(
    dataset: list[dict[str, Array]],
    nb_bins: int,
    pad_mode: str = "constant",
    pad_constant_values: int = 0,
) -> list[dict[str, Array]]:
    """
    Pad dataset with smart bins.

    Output is a dataset whose trajectories are padded with nb_bins different lengths
    such that the total padding is minimized.
    """
    bins = compute_smart_bins(dataset, nb_bins)
    padded_dataset = []
    for traj_bin in bins:
        max_traj_len = max(len(traj["observations"]) for traj in traj_bin)
        for traj in traj_bin:
            traj_len = len(traj["observations"])
            pad_width = ((0, max_traj_len - traj_len), (0, 0), (0, 0), (0, 0))
            traj = tree_pad(traj, pad_width, pad_mode, pad_constant_values)
            traj["mask"] = jnp.concatenate([jnp.ones(traj_len), jnp.zeros(max_traj_len - traj_len)])
            padded_dataset.append(traj)

    return padded_dataset
