import time

from algosdk.v2client import algod

from src.blockchain_utils.transaction_repository import (
    ASATransactionRepository,
)
from src.services.network_interaction import NetworkInteraction


def FToptIn(client, token_id: int,token_receiver_pk: str):
    opt_in_txn = ASATransactionRepository.asa_opt_in(
        client=client, sender_private_key=token_receiver_pk, asa_id=token_id
    )

    tx_id = NetworkInteraction.submit_transaction(client, transaction=opt_in_txn)
    return tx_id

def TransferFT(
        sender_address: str,
        sender_pk: str,
        receiver_address: str,
        token_id: int,
        client,
        amount: int):

    asa_buy_payment_txn = ASATransactionRepository.asa_transfer(client=client,
                                                                sender_address=sender_address,
                                                                receiver_address=receiver_address,
                                                                amount=amount,
                                                                asa_id=token_id,
                                                                revocation_target="",
                                                                sender_private_key=None,
                                                                sign_transaction=False)

    asa_transfer_txn_signed = asa_buy_payment_txn.sign(sender_pk)
    tx_id = client.send_transaction(asa_transfer_txn_signed)
    return tx_id


def transfer_ft():
   ft_creator_address = "6LB7WPUK3ZBX73F4YEM5TBUCHLLRCVBB5KGZQZE6CKKNVPR7A6S5RRD3FE"
   ft_creator_pk = "6VO1Nync+r5k5TQXSX3Ncbcgcoxwob0XqLaF7Hi3fMjyw/s+it5Df+y8wRnZhoI61xFUIeqNmGSeEpTavj8HpQ=="
   receiver_address = "FD3NQJQ4S6NDIGNTJ2C2LSCKZHC2PDPGSURBIUPTQWYBK64V7FQPUSUNXU"
   receiver_pk = "IAexq8BPYQJAFmC0h6VsjX/XQEToCLes6H9SakQaTjoo9tgmHJeaNBmzToWlyErJxaeN5pUiFFHzhbAVe5X5YA=="
   token_id = 147
   amount = 100000
   token = "212ba0a5ae0335a1443d52dd0af48b51305f621d02a58a267a9dd4985347b90d"
   address = "http://127.0.0.1:33755"
   purestake_token = {'X-Api-key': token}
   client = algod.AlgodClient(token, address, headers=purestake_token)
   txn_id2 = FToptIn(client, token_id, receiver_pk)
   time.sleep(3)
   txn_id =TransferFT(ft_creator_address,ft_creator_pk,receiver_address,int(token_id),client,int(amount))
   return print(txn_id)


transfer_ft()


