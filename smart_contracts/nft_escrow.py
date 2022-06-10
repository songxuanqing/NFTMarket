from pyteal import *


def nft_escrow(app_id: int, asa_id: int):
    return Seq([
        Assert(Global.group_size() == Int(4)),
        Assert(Gtxn[0].application_id() == Int(app_id)),

        Assert(Gtxn[1].type_enum() == TxnType.AssetTransfer),
        Assert(Gtxn[2].type_enum() == TxnType.AssetTransfer),

        Assert(Gtxn[3].asset_amount() == Int(1)),
        Assert(Gtxn[3].xfer_asset() == Int(asa_id)),
        Assert(Gtxn[3].fee() <= Int(1000)),
        Assert(Gtxn[3].asset_close_to() == Global.zero_address()),
        Assert(Gtxn[3].rekey_to() == Global.zero_address()),

        Return(Int(1))
    ])
