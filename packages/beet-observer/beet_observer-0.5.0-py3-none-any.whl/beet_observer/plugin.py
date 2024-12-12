from beet import Context, run_beet

from .data_pack import *
from .resource_pack import *


def beet_default(ctx: Context):
    if "observer" not in ctx.meta:
        return
    # get default directories
    if "default_dir" not in ctx.meta["observer"]:
        # default dir not defined
        ctx.meta["observer"]["default_dir_dp"] = "default_overlay"
        ctx.meta["observer"]["default_dir_rp"] = "default_overlay"
    elif isinstance(ctx.meta["observer"]["default_dir"], str):
        # default dir is the same for dp and rp
        ctx.meta["observer"]["default_dir_dp"] = ctx.meta["observer"]["default_dir"]
        ctx.meta["observer"]["default_dir_rp"] = ctx.meta["observer"]["default_dir"]
    else:
        # default dir is different for dp and rp
        ctx.meta["observer"]["default_dir_dp"] = ctx.meta["observer"]["default_dir"][
            "dp"
        ]
        ctx.meta["observer"]["default_dir_rp"] = ctx.meta["observer"]["default_dir"][
            "rp"
        ]
    # save current overlays
    save: list[str] = []
    for overlay in ctx.data.overlays:
        save.append(overlay)
    # loop through all overlays
    for overlay in ctx.meta["observer"]["overlays"]:
        # create relative path
        path = f"{ctx.directory}/{overlay['process']}"
        # generate context for overlay pack
        with run_beet(
            config={"data_pack": {"load": "."}, "resource_pack": {"load": "."}},
            directory=path,
        ) as ctx_overlay:
            if "directory" not in overlay:
                dp_dir = f"overlay_{ctx_overlay.data.pack_format}"
                rp_dir = f"overlay_{ctx_overlay.assets.pack_format}"
            else:
                dp_dir = overlay["directory"]
                rp_dir = overlay["directory"]
            # compare build pack and overlay pack
            gen_dp_overlays(ctx, ctx_overlay, dp_dir, save)
            gen_rp_overlays(ctx, ctx_overlay, rp_dir, save)
