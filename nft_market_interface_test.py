import time

from src.blockchain_utils.transaction_repository import (
    ApplicationTransactionRepository,
    ASATransactionRepository,
    PaymentTransactionRepository,
)
from src.services import NetworkInteraction
from algosdk import logic as algo_logic
from algosdk.future import transaction as algo_txn
from algosdk.v2client import algod
from pyteal import compileTeal, Mode
from algosdk.encoding import decode_address
from src.smart_contracts import NFTMarketplaceASC1, nft_escrow
from flask import Flask, request,jsonify
app = Flask(__name__)
nft_marketplace_asc1 = NFTMarketplaceASC1()

#nova 코인 payment transaction 함수
def NovaPayment(client, sender_address, receiver_address, amount, sender_pk) :
    txn = PaymentTransactionRepository.payment(client=client,
                                                sender_address=sender_address,
                                                receiver_address=receiver_address,
                                                amount=amount,
                                                sender_private_key=sender_pk,
                                                sign_transaction=False)
    signed_txn = txn.sign(sender_pk)
    tx_id = NetworkInteraction.submit_transaction(client=client, transaction=signed_txn)
    return tx_id

#토큰 id에 해당하는 토큰을 amount만큼 전송하는 함수. 우리 어플은 개발사가 모든 토큰을 관리하고, sender의 토큰을 특정인에게 전달.
def TokenTransfer(client, dev_address, sender_address,receiver_address, amount, dev_pk, token_id) :
    txn = ASATransactionRepository.asa_transfer(client=client,
                                                sender_address=dev_address,
                                                receiver_address=receiver_address,
                                                amount=amount,
                                                asa_id=token_id,
                                                revocation_target=sender_address, #누구의 권한을 박탈할것인가
                                                sender_private_key=dev_pk,
                                                sign_transaction=False)
    signed_txn = txn.sign(dev_pk)
    tx_id = NetworkInteraction.submit_transaction(client=client, transaction=signed_txn)
    return tx_id


def CreateNFT(
        nft_creator_address: str, #nft 생성자. 일반적으로 개발사 계정 주소를 받는다.
        nft_creator_pk: str, #nft 생성자 개인키
        nft_reserve_address: str, #민팅되지 않은 자산이 귀속될 주소
        client, #클라이언트 노드 객체
        unit_name: str, #nft 단위명
        asset_name: str, #nft명
        nft_url: str): #nft정보를 저장한 json 저장경로 url
    signed_txn = ASATransactionRepository.create_non_fungible_asa(
        client=client,
        creator_private_key=nft_creator_pk,
        unit_name=unit_name,
        asset_name=asset_name,
        note=None,
        manager_address=nft_creator_address,
        reserve_address=nft_reserve_address,
        freeze_address=nft_creator_address,
        clawback_address=nft_creator_address,
        url=nft_url,
        default_frozen=True,
        sign_transaction=True,
    )

    nft_id, tx_id = NetworkInteraction.submit_asa_creation(
        client=client, transaction=signed_txn
    )

    return nft_id,tx_id

#nft 전송. 개발사가 개발 후 실제 소유자에게 전송한다.
def NFTTransfer(
        nft_creator_address: str,
        nft_creator_pk: str,
        nft_owner_address: str,
        client,
        nft_id: int):

    txn = ASATransactionRepository.asa_transfer(client=client,
                                                sender_address=nft_creator_address,
                                                receiver_address=nft_owner_address,
                                                amount=1,
                                                asa_id=nft_id,
                                                revocation_target=nft_creator_address,
                                                sender_private_key=None,
                                                sign_transaction=False)

    signed_txn = txn.sign(nft_creator_pk)

    tx_id = NetworkInteraction.submit_transaction(
        client=client, transaction=signed_txn
    )

    return tx_id

#nft 관련 configuration을 변경한다. 이 경우 escrow (임치 스마스컨트랙트 주소)를 clawback으로 설정한다.
# clawback은 자산을 이전할 권한이 있다.
def change_nft_credentials(
        nft_creator_address: str,
        nft_creator_pk: str,
        client,
        nft_id: int,
        app_id: int):
    txn = ASATransactionRepository.change_asa_management(
        client=client,
        current_manager_pk=nft_creator_pk,
        asa_id=nft_id,
        manager_address=nft_creator_address,
        reserve_address="",
        freeze_address="",
        strict_empty_address_check=False,
        clawback_address=escrow_address(app_id,nft_id,client),
        sign_transaction=True,
    )

    tx_id = NetworkInteraction.submit_transaction(client, transaction=txn)

    return tx_id

#nft를 configuration을 원래대로 돌려놓는다. stop_sell할 겨우 사용된다.
def back_nft_credentials(
        nft_creator_address: str,
        nft_creator_pk: str,
        nft_reserve_address: str,
        client,
        nft_id: int):
    txn = ASATransactionRepository.change_asa_management(
        client=client,
        current_manager_pk=nft_creator_pk,
        asa_id=nft_id,
        manager_address=nft_creator_address,
        reserve_address=nft_reserve_address,
        freeze_address=nft_creator_address,
        strict_empty_address_check=False,
        clawback_address=nft_creator_address,
        sign_transaction=True,
    )

    tx_id = NetworkInteraction.submit_transaction(client, transaction=txn)

    return tx_id


def escrow_bytes(app_id,nft_id,client):
    if app_id is None:
        raise ValueError("App not deployed")

    escrow_fund_program_compiled = compileTeal(
        nft_escrow(app_id=app_id, asa_id=nft_id),
        mode=Mode.Signature,
        version=3,
    )

    return NetworkInteraction.compile_program(
        client=client, source_code=escrow_fund_program_compiled
    )


def escrow_address(app_id,nft_id,client):
    print(algo_logic.address(escrow_bytes(app_id,nft_id,client)))
    return algo_logic.address(escrow_bytes(app_id,nft_id,client))


def app_initialization(
        nft_creator_address: str,
        nft_creator_pk: str,
        nft_reserve_address: str,
        nft_id: int,
        token_id: int,
        client,):

    approval_program_compiled = compileTeal(
        nft_marketplace_asc1.approval_program(),
        mode=Mode.Application,
        version=3,
    )

    clear_program_compiled = compileTeal(
        nft_marketplace_asc1.clear_program(),
        mode=Mode.Application,
        version=3
    )

    approval_program_bytes = NetworkInteraction.compile_program(
        client=client, source_code=approval_program_compiled
    )

    clear_program_bytes = NetworkInteraction.compile_program(
        client=client, source_code=clear_program_compiled
    )

    app_args = [
        decode_address(nft_reserve_address),
        decode_address(nft_creator_address),
    ]

    app_transaction = ApplicationTransactionRepository.create_application(
        client=client,
        creator_private_key=nft_creator_pk,
        approval_program=approval_program_bytes,
        clear_program=clear_program_bytes,
        global_schema=nft_marketplace_asc1.global_schema,
        local_schema=nft_marketplace_asc1.local_schema,
        app_args=app_args,
        foreign_assets=[nft_id,token_id],
    )

    tx_id = NetworkInteraction.submit_transaction(
        client, transaction=app_transaction
    )

    transaction_response = client.pending_transaction_info(tx_id)

    app_id = transaction_response["application-index"]

    return tx_id, app_id


def InitializeEscrow(
        app_id: int,
        nft_id: int,
        client,
        admin_pk: str,):
    app_args = [
        nft_marketplace_asc1.AppMethods.initialize_escrow,
        decode_address(escrow_address(app_id,nft_id,client)),
    ]

    initialize_escrow_txn = ApplicationTransactionRepository.call_application(
        client=client,
        caller_private_key=admin_pk,
        app_id=app_id,
        on_complete=algo_txn.OnComplete.NoOpOC,
        app_args=app_args,
        foreign_assets=[nft_id],
    )

    tx_id = NetworkInteraction.submit_transaction(
        client, transaction=initialize_escrow_txn
    )

    return tx_id


def FundEscrow(client,nft_creator_address: str,nft_creator_pk: str,nft_id: int,app_id: int):
    fund_escrow_txn = PaymentTransactionRepository.payment(
        client=client,
        sender_address=nft_creator_address,
        receiver_address=escrow_address(app_id,nft_id,client),
        amount=100000,
        sender_private_key=nft_creator_pk,
        sign_transaction=True,
    )

    tx_id = NetworkInteraction.submit_transaction(
        client, transaction=fund_escrow_txn
    )
    return tx_id


def sell_nft(client, app_id: int, sell_price: int, nft_owner_pk: str):
    app_args = [nft_marketplace_asc1.AppMethods.make_sell_offer, sell_price]

    app_call_txn = ApplicationTransactionRepository.call_application(
        client=client,
        caller_private_key=nft_owner_pk,
        app_id=app_id,
        on_complete=algo_txn.OnComplete.NoOpOC,
        app_args=app_args,
        sign_transaction=True,
    )

    tx_id = NetworkInteraction.submit_transaction(client, transaction=app_call_txn)
    return tx_id

#fungible token(토큰)에 옵트인한다. 토큰에 옵트인해야지 해당 토큰을 수신할 자격이 주어진다.
#따라서 토큰을 수신할 판매인은 우선 옵트인해야 한다.
def FToptIn(client, token_id: int,token_receiver_pk: str):
    opt_in_txn = ASATransactionRepository.asa_opt_in(
        client=client, sender_private_key=token_receiver_pk, asa_id=token_id
    )

    tx_id = NetworkInteraction.submit_transaction(client, transaction=opt_in_txn)
    return tx_id

#non-fungible token(NFT)에 옵트인한다. 토큰에 옵트인해야지 해당 토큰을 수신할 자격이 주어진다.
#따라서 NFT를 수신할 구매인은 우선 옵트인해야한다.
def NFToptIn(client, nft_id: int,nft_buyer_pk: str):
    opt_in_txn = ASATransactionRepository.asa_opt_in(
        client=client, sender_private_key=nft_buyer_pk, asa_id=nft_id
    )

    tx_id = NetworkInteraction.submit_transaction(client, transaction=opt_in_txn)
    return tx_id

def buy_nft(client,
            app_id: int,
            nft_id: int,
        nft_owner_address: str, dev_address: str, dev_pk: str, #dev_address와 dev_pk는 개발사 계정 주소와 개인키이다.
        buyer_address: str, buyer_pk: str, buy_price,token_id: int):
    # 1. Application call txn
    app_args = [
        nft_marketplace_asc1.AppMethods.buy
    ]

    app_call_txn = ApplicationTransactionRepository.call_application(client=client,
                                                                    caller_private_key=dev_pk,
                                                                    app_id=app_id,
                                                                    on_complete=algo_txn.OnComplete.NoOpOC,
                                                                    app_args=app_args,
                                                                    sign_transaction=False)


    asa_get_from_buyer_txn = ASATransactionRepository.asa_transfer(client=client,
                                                            sender_address=dev_address,
                                                            receiver_address=dev_address,
                                                            amount=buy_price,
                                                            asa_id=token_id,
                                                            revocation_target=buyer_address,
                                                            sender_private_key=None,
                                                            sign_transaction=False)

    asa_buy_payment_txn = ASATransactionRepository.asa_transfer(client=client,
                                                            sender_address=dev_address,
                                                            receiver_address=nft_owner_address,
                                                            amount=buy_price,
                                                            asa_id=token_id,
                                                            revocation_target=dev_address,
                                                            sender_private_key=None,
                                                            sign_transaction=False)


    # 3. Asset transfer transaction: escrow -> buyer
    asa_transfer_txn = ASATransactionRepository.asa_transfer(client=client,
                                                             sender_address=escrow_address(app_id, nft_id, client),
                                                             receiver_address=buyer_address,
                                                             amount=1,
                                                             asa_id=nft_id,
                                                             revocation_target=nft_owner_address,
                                                             sender_private_key=None,
                                                             sign_transaction=False)

    # Atomic transfer
    gid = algo_txn.calculate_group_id([app_call_txn,
                                       asa_get_from_buyer_txn,
                                        asa_buy_payment_txn,
                                        asa_transfer_txn])

    app_call_txn.group = gid
    asa_get_from_buyer_txn.group = gid
    asa_buy_payment_txn.group = gid
    asa_transfer_txn.group = gid

    app_call_txn_signed = app_call_txn.sign(dev_pk)
    asa_get_from_buyer_txn_signed = asa_get_from_buyer_txn.sign(dev_pk)
    asa_buy_txn_signed = asa_buy_payment_txn.sign(dev_pk)

    asa_transfer_txn_logic_signature = algo_txn.LogicSig(escrow_bytes(app_id,nft_id,client))
    asa_transfer_txn_signed = algo_txn.LogicSigTransaction(asa_transfer_txn, asa_transfer_txn_logic_signature)

    signed_group = [app_call_txn_signed,
                    asa_get_from_buyer_txn_signed,
                    asa_buy_txn_signed,
                    asa_transfer_txn_signed]

    tx_id = client.send_transactions(signed_group)
    return tx_id


def stop_sell(client, app_id: int, sell_price: int, nft_owner_pk: str):
    app_args = [nft_marketplace_asc1.AppMethods.stop_sell_offer, sell_price]

    app_call_txn = ApplicationTransactionRepository.call_application(
        client=client,
        caller_private_key=nft_owner_pk,
        app_id=app_id,
        on_complete=algo_txn.OnComplete.NoOpOC,
        app_args=app_args,
        sign_transaction=True,
    )

    tx_id = NetworkInteraction.submit_transaction(client, transaction=app_call_txn)
    return tx_id



# curl -d "dev_address=5QX5D4HPXQIQ3ODMGN6NTH6GO435N5GJSA72FBKSJI4WCAJ5VAXWTAF6UU&dev_pk=BFChzShBzM561pMUeZ3I7hTEurXr+ZoMzn27aQ8sV3jsL9Hw77wRDbhsM3zZn8Z3N9b0yZA/ooVSSjlhAT2oLw==&nft_owner_address=Q7LS5VUYTPV7NKMMKFT22Z3A2DWSHUQQA74ILF7OXRKMN3HRQ7VC57EELU&nft_owner_pk=/8qKTp3HAFjgGiStk2wjKBx2dZ2PDzxziDG6y0GIltiH1y7WmJvr9qmMUWetZ2DQ7SPSEAf4hZfuvFTG7PGH6g==&token=158a0082b552fe50d446f53329c972985de0c4ae43d5b2fd1bebc443b077cf59&ip_address=http://127.0.0.1:8080&unit_name=piece&asset_name=piece&nft_url=https://gateway.pinata.cloud/ipfs/QmZBiFNgb6hWj4JYwXc3PL5QqsoHYaGd4dNv2RWZZzSbjY" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://127.0.0.1:5000/create_nft
@app.route('/create_nft', methods=['POST'])
def create_nft():
   nft_creator_address = request.form['dev_address']
   nft_creator_pk = request.form['dev_pk']
   nft_reserve_address = request.form['nft_owner_address']
   nft_reserve_pk = request.form['nft_owner_pk']
   token = request.form['token']
   address = request.form['ip_address']
   purestake_token = {'X-Api-key': token}
   client = algod.AlgodClient(token, address, headers=purestake_token)
   unit_name = request.form['unit_name']
   asset_name = request.form['asset_name']
   nft_url = request.form['nft_url']
   nft_creator_pk=nft_creator_pk.replace(" ", "+")
   nft_reserve_pk=nft_reserve_pk.replace(" ", "+")
   #개발사는 NFT생성 후 해당 NFT id를 받아서, 실제 소유자를 해당 nft에 옵트인하고, 실제 NFT소유자에게 전송한다.
   # (NFT생성 시 비용 발생을 줄이려고 한 것이지만, 어차피 optin할 경우 tx fee가 발생하니 논의 후 수정할 예정.
   nft_id, txn_id_create =CreateNFT(nft_creator_address,nft_creator_pk,nft_reserve_address,client,unit_name,asset_name,nft_url)
   time.sleep(3)
   txn_id_nft_opt = NFToptIn(client, nft_id, nft_reserve_pk)
   time.sleep(3)
   txn_id = NFTTransfer(nft_creator_address,nft_creator_pk,nft_reserve_address,client,nft_id)
   return jsonify(result='success', nft_id=nft_id, txn_id=txn_id)

# curl -d "dev_address=5QX5D4HPXQIQ3ODMGN6NTH6GO435N5GJSA72FBKSJI4WCAJ5VAXWTAF6UU&dev_pk=BFChzShBzM561pMUeZ3I7hTEurXr+ZoMzn27aQ8sV3jsL9Hw77wRDbhsM3zZn8Z3N9b0yZA/ooVSSjlhAT2oLw==&nft_owner_address=Q7LS5VUYTPV7NKMMKFT22Z3A2DWSHUQQA74ILF7OXRKMN3HRQ7VC57EELU&nft_id=94445264&token_id=94434081&sell_price=100&token=158a0082b552fe50d446f53329c972985de0c4ae43d5b2fd1bebc443b077cf59&ip_address=http://127.0.0.1:8080" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://127.0.0.1:5000/sell_nft
@app.route('/sell_nft', methods=['POST'])
def make_sell_offer():
    nft_creator_address = request.form['dev_address']
    nft_creator_pk = request.form['dev_pk']
    nft_reserve_address = request.form['nft_owner_address']
    nft_id = request.form['nft_id']
    token_id = request.form['token_id']
    sell_price = request.form['sell_price']
    token = request.form['token']
    address = request.form['ip_address']
    purestake_token = {'X-Api-key': token}
    client = algod.AlgodClient(token, address, headers=purestake_token)
    nft_creator_pk=nft_creator_pk.replace(" ", "+")
    # 판매하기 위한 smart contract app을 초기화하고,
    # nft의 clawback을 app의 escrow로 변경한다. (credentials 변경)
    # escrow를 초기화하고, escrow가 해당 NFT관련 전송 권한을 가지고 있다가 구매시 구매자에게 NFT를 전송할 수 있도록, escrow에 자금 이체
    # sell_nft를 통해 app을 호출하고, smart contract에서 global변수를 판매중으로 놓고, 가격을 등록한다.
    txn_id_app, app_id = app_initialization(nft_creator_address, nft_creator_pk, nft_reserve_address,nft_id, token_id,client)
    time.sleep(3)
    txn_id_change_credentials = change_nft_credentials(nft_creator_address,nft_creator_pk, client, int(nft_id), int(app_id))
    time.sleep(3)
    txn_id_escrow = InitializeEscrow(int(app_id), int(nft_id), client, nft_creator_pk)
    time.sleep(3)
    txn_id_fundEscrow = FundEscrow(client, nft_creator_address, nft_creator_pk, int(nft_id), int(app_id))
    time.sleep(3)
    txn_id_sell = sell_nft(client, int(app_id), int(sell_price), nft_creator_pk)
    return jsonify(result='success', app_id=app_id, txn_id=txn_id_sell)


# curl -d "nft_owner_address=Q7LS5VUYTPV7NKMMKFT22Z3A2DWSHUQQA74ILF7OXRKMN3HRQ7VC57EELU&nft_owner_pk=/8qKTp3HAFjgGiStk2wjKBx2dZ2PDzxziDG6y0GIltiH1y7WmJvr9qmMUWetZ2DQ7SPSEAf4hZfuvFTG7PGH6g==&dev_address=5QX5D4HPXQIQ3ODMGN6NTH6GO435N5GJSA72FBKSJI4WCAJ5VAXWTAF6UU&dev_pk=BFChzShBzM561pMUeZ3I7hTEurXr+ZoMzn27aQ8sV3jsL9Hw77wRDbhsM3zZn8Z3N9b0yZA/ooVSSjlhAT2oLw==&buyer_address=CSWVHEEZDZQR452LEYCJGNBRDZU7SSKANOA32OPOKNBMYJSAV5BNZEXIXA&buyer_pk=zgoVj7FaDmVMwmJ/A8LvZvTMylApD3cXEyphl8Vi/wQUrVOQmR5hHndLJgSTNDEeaflJQGuBvTnuU0LMJkCvQg==&nft_id=94445264&app_id=94445368&buy_price=100&token_id=94434081&token=158a0082b552fe50d446f53329c972985de0c4ae43d5b2fd1bebc443b077cf59&ip_address=http://127.0.0.1:8080" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://127.0.0.1:5000/buy_nft
@app.route('/buy_nft', methods=['POST'])
def buy_nft_offer():
   nft_owner_address = request.form['nft_owner_address']
   nft_owner_pk = request.form['nft_owner_pk']
   dev_address = request.form['dev_address']
   dev_pk = request.form['dev_pk']
   buyer_address= request.form['buyer_address']
   buyer_pk = request.form['buyer_pk']
   buy_price = request.form['buy_price']
   app_id = request.form['app_id']
   nft_id = request.form['nft_id']
   token_id = request.form['token_id']
   token = request.form['token']
   address = request.form['ip_address']
   purestake_token = {'X-Api-key': token}
   client = algod.AlgodClient(token, address, headers=purestake_token)
   nft_owner_pk=nft_owner_pk.replace(" ", "+")
   dev_pk=dev_pk.replace(" ", "+")
   buyer_pk=buyer_pk.replace(" ", "+")
   # 판매자는 토큰을 보상으로 받으므로 토큰에 판매자를 optin한다.
   # 구매자는 nft를 수신하므로, NFT에 구매자를 optin한다.
   # buy_nft를 통해 app을 호출하고, smart contract에서 global변수를 판매종료로 놓고, asset transfer txn을 실행한다.
   txn_id_ft_opt = FToptIn(client, token_id, nft_owner_pk)
   time.sleep(3)
   txn_id_nft_opt = NFToptIn(client, nft_id, buyer_pk)
   time.sleep(3)
   txn_id =  buy_nft(client,int(app_id), int(nft_id),nft_owner_address,
                     dev_address,dev_pk,
                     buyer_address, buyer_pk, int(buy_price),int(token_id))
   return jsonify(result='success', txn_id=txn_id)


# curl -d "dev_address=5QX5D4HPXQIQ3ODMGN6NTH6GO435N5GJSA72FBKSJI4WCAJ5VAXWTAF6UU&dev_pk=BFChzShBzM561pMUeZ3I7hTEurXr+ZoMzn27aQ8sV3jsL9Hw77wRDbhsM3zZn8Z3N9b0yZA/ooVSSjlhAT2oLw==&nft_owner_address=Q7LS5VUYTPV7NKMMKFT22Z3A2DWSHUQQA74ILF7OXRKMN3HRQ7VC57EELU&nft_id=94440538&app_id=94440641&token_id=94434081&sell_price=100&token=158a0082b552fe50d446f53329c972985de0c4ae43d5b2fd1bebc443b077cf59&ip_address=http://127.0.0.1:8080" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://127.0.0.1:5000/stop_sell
@app.route('/stop_sell', methods=['POST'])
def stop_sell_nft():
    nft_creator_address = request.form['dev_address']
    nft_creator_pk = request.form['dev_pk']
    nft_reserve_address = request.form['nft_owner_address']
    nft_id = request.form['nft_id']
    app_id = request.form['app_id']
    sell_price = request.form['sell_price']
    token = request.form['token']
    address = request.form['ip_address']
    purestake_token = {'X-Api-key': token}
    client = algod.AlgodClient(token, address, headers=purestake_token)
    nft_creator_pk=nft_creator_pk.replace(" ", "+")
    txn_id_back = back_nft_credentials(nft_creator_address,nft_creator_pk, nft_reserve_address,client, int(nft_id))
    time.sleep(3)
    txn_id = stop_sell(client, int(app_id), int(sell_price), nft_creator_pk)
    return jsonify(result='success', txn_id=txn_id)



#curl -d "receiver_pk=zgoVj7FaDmVMwmJ/A8LvZvTMylApD3cXEyphl8Vi/wQUrVOQmR5hHndLJgSTNDEeaflJQGuBvTnuU0LMJkCvQg==&token_id=94434081&token=158a0082b552fe50d446f53329c972985de0c4ae43d5b2fd1bebc443b077cf59&ip_address=http://127.0.0.1:8080" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://127.0.0.1:5000/token_optin
@app.route('/token_optin', methods=['POST'])
def token_optin():
   receiver_pk = request.form['receiver_pk']
   token_id = request.form['token_id']
   token = request.form['token']
   address = request.form['ip_address']
   purestake_token = {'X-Api-key': token}
   client = algod.AlgodClient(token, address, headers=purestake_token)
   receiver_pk=receiver_pk.replace(" ", "+")
   txn_id = FToptIn(client, token_id, receiver_pk)
   return jsonify(result='success', txn_id=txn_id)


#curl -d "sender_address=FD3NQJQ4S6NDIGNTJ2C2LSCKZHC2PDPGSURBIUPTQWYBK64V7FQPUSUNXU&sender_pk=01Lo297AbcmD8zv0Nh%2BLV0YadUdRE59fZxATtdUI/JPkPwv3U7fmkEYGxi1dRHEy/rJRW%2BWvAglDEsMxLM0JBw==&receiver_address=6LB7WPUK3ZBX73F4YEM5TBUCHLLRCVBB5KGZQZE6CKKNVPR7A6S5RRD3FE&amount=100&token=212ba0a5ae0335a1443d52dd0af48b51305f621d02a58a267a9dd4985347b90d&ip_address=http://127.0.0.1:33755" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://127.0.0.1:5000/nova_payment
@app.route('/nova_payment', methods=['POST'])
def nova_payment():
   sender_address = request.form['sender_address']
   sender_pk = request.form['sender_pk']
   receiver_address = request.form['receiver_address']
   amount = request.form['amount']
   token = request.form['token']
   address = request.form['ip_address']
   purestake_token = {'X-Api-key': token}
   client = algod.AlgodClient(token, address, headers=purestake_token)
   sender_pk=sender_pk.replace(" ", "+")
   txn_id = NovaPayment(client, sender_address, receiver_address, amount, sender_pk)
   return jsonify(result='success', txn_id=txn_id)


#curl -d "dev_address=5QX5D4HPXQIQ3ODMGN6NTH6GO435N5GJSA72FBKSJI4WCAJ5VAXWTAF6UU&dev_pk=BFChzShBzM561pMUeZ3I7hTEurXr+ZoMzn27aQ8sV3jsL9Hw77wRDbhsM3zZn8Z3N9b0yZA/ooVSSjlhAT2oLw==&sender_address=CSWVHEEZDZQR452LEYCJGNBRDZU7SSKANOA32OPOKNBMYJSAV5BNZEXIXA&receiver_address=Q7LS5VUYTPV7NKMMKFT22Z3A2DWSHUQQA74ILF7OXRKMN3HRQ7VC57EELU&token_id=94434081&amount=1000&token=158a0082b552fe50d446f53329c972985de0c4ae43d5b2fd1bebc443b077cf59&ip_address=http://127.0.0.1:8080" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://127.0.0.1:5000/token_transfer
@app.route('/token_transfer', methods=['POST'])
def token_transfer():
   dev_address = request.form['dev_address']
   dev_pk = request.form['dev_pk']
   sender_address = request.form['sender_address']
   receiver_address = request.form['receiver_address']
   token_id = request.form['token_id']
   amount = request.form['amount']
   token = request.form['token']
   address = request.form['ip_address']
   purestake_token = {'X-Api-key': token}
   client = algod.AlgodClient(token, address, headers=purestake_token)
   dev_pk=dev_pk.replace(" ", "+")
   txn_id = TokenTransfer(client, dev_address, sender_address,receiver_address, int(amount), dev_pk, int(token_id))
   return jsonify(result='success', txn_id=txn_id)


if __name__ == '__main__':
   app.run('127.0.0.1',port=5000,debug=True)
