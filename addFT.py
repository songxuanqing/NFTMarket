from algosdk.v2client import algod

from src.blockchain_utils.transaction_repository import (
    ASATransactionRepository,
)
from src.services import NetworkInteraction

def CreateFT(
        ft_creator_address: str,
        ft_creator_pk: str,
        client,
        unit_name: str,
        asset_name: str,
        ft_url: str):
    signed_txn = ASATransactionRepository.create_asa(
        client=client,
        creator_private_key=ft_creator_pk,
        unit_name=unit_name,
        asset_name=asset_name,
        total=10000000000000000,
        note=None,
        decimals=0,
        manager_address=ft_creator_address,
        reserve_address=ft_creator_address,
        freeze_address=ft_creator_address,
        clawback_address=ft_creator_address,
        url=ft_url,
        default_frozen=False,
        sign_transaction=True,
    )

    nft_id, tx_id = NetworkInteraction.submit_asa_creation(
        client=client, transaction=signed_txn
    )

    return nft_id,tx_id


def create_ft():
   ft_creator_address = "5QX5D4HPXQIQ3ODMGN6NTH6GO435N5GJSA72FBKSJI4WCAJ5VAXWTAF6UU"
   ft_creator_pk = "BFChzShBzM561pMUeZ3I7hTEurXr+ZoMzn27aQ8sV3jsL9Hw77wRDbhsM3zZn8Z3N9b0yZA/ooVSSjlhAT2oLw=="
   token = "158a0082b552fe50d446f53329c972985de0c4ae43d5b2fd1bebc443b077cf59"
   address = "http://127.0.0.1:8080"
   purestake_token = {'X-Api-key': token}
   client = algod.AlgodClient(token, address, headers=purestake_token)
   unit_name = "seed"
   asset_name = "seed"
   ft_url = ""
   ft_id, txn_id =CreateFT(ft_creator_address,ft_creator_pk,client,unit_name,asset_name,ft_url)
   return print(ft_id)


create_ft()


